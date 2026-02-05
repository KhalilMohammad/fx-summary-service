import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class FailingClient:
    async def get(self, *args, **kwargs):
        raise httpx.ConnectError("network down")


def test_fallback_used_on_network_failure(monkeypatch):
    import app.services.fx_service as fx

    original_client = httpx.AsyncClient

    httpx.AsyncClient = lambda *a, **k: FailingClient()

    try:
        res = client.get(
            "/summary",
            params={
                "start": "2025-07-01",
                "end": "2025-07-03",
                "breakdown": "day"
            }
        )

        assert res.status_code == 200
        body = res.json()
        assert body["daily"] is not None

    finally:
        httpx.AsyncClient = original_client
