from datetime import datetime, timezone
from fastapi.testclient import TestClient
from main import app
from routes import time_route


def test_timezone_conversion_uses_requested_offset(monkeypatch):
    monkeypatch.setattr(time_route, "utc_now", lambda: datetime(2026, 11, 17, 3, 30, tzinfo=timezone.utc))
    result = TestClient(app).get("/time/zone", params={"name": "Asia/Kolkata"})
    assert result.status_code == 200
    assert result.json() == {"timezone": "Asia/Kolkata", "current_time": "2026-11-17T09:00:00+05:30"}


def test_unknown_timezone_is_a_client_error():
    result = TestClient(app).get("/time/zone", params={"name": "Invalid/Nowhere"})
    assert result.status_code == 422
    assert result.json()["detail"] == "Unknown IANA timezone."
