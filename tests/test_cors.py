import asyncio

import httpx
import pytest

import database
from config import ConfigurationError
from main import create_app


@pytest.mark.parametrize("host", ["localhost", "127.0.0.1"])
@pytest.mark.parametrize("port", [5173, 4173])
def test_local_origin_preflight_and_errors(host, port, monkeypatch):
    origin = f"http://{host}:{port}"

    def unavailable(*args):
        raise ConfigurationError("synthetic-private-details")

    monkeypatch.setattr(database, "load_settings", unavailable)

    async def check():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app()),
                                     base_url="http://test") as client:
            response = await client.options("/applications", headers={
                "Origin": origin, "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"})
            assert response.status_code == 200
            assert response.headers["access-control-allow-origin"] == origin
            assert "access-control-allow-credentials" not in response.headers
            health = await client.get("/health", headers={"Origin": origin})
            assert health.json() == {"status": "healthy"}
            failed = await client.get("/applications", headers={"Origin": origin})
            assert failed.status_code == 500
            assert failed.headers["access-control-allow-origin"] == origin
            assert failed.json() == {"detail": "Internal server error"}
    asyncio.run(check())


@pytest.mark.parametrize("origin,method", [("https://unapproved.example", "POST"),
                                             ("http://localhost:5173", "DELETE")])
def test_disallowed_cors_preflight(origin, method):
    async def check():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=create_app()),
                                     base_url="http://test") as client:
            response = await client.options("/applications", headers={
                "Origin": origin, "Access-Control-Request-Method": method})
            assert response.status_code == 400
            if origin == "https://unapproved.example":
                assert "access-control-allow-origin" not in response.headers
    asyncio.run(check())
