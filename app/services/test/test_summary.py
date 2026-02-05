from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_summary_without_breakdown():
    res = client.get(
        "/summary",
        params={
            "start": "2025-07-01",
            "end": "2025-07-03"
        }
    )

    assert res.status_code == 200
    body = res.json()

    assert "start_rate" in body
    assert "end_rate" in body
    assert "mean_rate" in body
    assert "total_percent_change" in body
    assert "daily" not in body or body["daily"] is None

def test_summary_with_daily_breakdown():
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

    daily = body["daily"]
    assert isinstance(daily, list)
    assert len(daily) > 0

    day = daily[0]
    assert "date" in day
    assert "rate" in day
    assert "percent_change" in day
