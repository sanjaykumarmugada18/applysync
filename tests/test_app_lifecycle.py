import asyncio
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock

import httpx
from starlette.requests import Request

import database
from config import ConfigurationError
from main import create_app


def test_lazy_engine_reuse_and_shutdown(monkeypatch):
    app = create_app("test")
    engine = Mock()
    build = Mock(return_value=engine)
    settings = Mock()
    monkeypatch.setattr(database, "load_settings", settings)
    monkeypatch.setattr(database, "build_engine", build)

    async def check():
        async with app.router.lifespan_context(app):
            build.assert_not_called()
            request = Request({"type": "http", "app": app})
            with ThreadPoolExecutor(max_workers=4) as executor:
                engines = list(executor.map(lambda _: database.get_engine(request), range(8)))
            assert all(value is engine for value in engines)
            settings.assert_called_once_with("test")
            build.assert_called_once()
        engine.dispose.assert_called_once()
        assert app.state.engine is None
    asyncio.run(check())


def test_missing_configuration_keeps_health_available(monkeypatch, caplog):
    def fail_settings(*args):
        raise ConfigurationError("synthetic-private-configuration")
    monkeypatch.setattr(database, "load_settings", fail_settings)
    app = create_app()

    async def check():
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
                assert (await client.get("/health")).json() == {"status": "healthy"}
                assert (await client.get("/unknown")).status_code == 404
                response = await client.get("/applications")
                assert response.status_code == 500
                assert response.json() == {"detail": "Internal server error"}
                assert "synthetic-private-configuration" not in caplog.text
    asyncio.run(check())
