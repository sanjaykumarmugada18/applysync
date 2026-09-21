import asyncio

from httpx import ASGITransport, AsyncClient

from main import app


def test_health_and_unknown_route():
    async def check():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}
            response = await client.get("/does-not-exist")
            assert response.status_code == 404
            assert response.json() == {"detail": "Not Found"}
    asyncio.run(check())
