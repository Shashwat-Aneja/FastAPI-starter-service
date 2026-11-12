from datetime import datetime, timezone

from fastapi.testclient import TestClient

from main import app
from routes import time_route


def test_millisecond_timestamp_uses_integer_microseconds(monkeypatch):
    instant = datetime(2026, 11, 12, 3, 30, 0, 999999, tzinfo=timezone.utc)
    monkeypatch.setattr(time_route, "utc_now", lambda: instant)

    response = TestClient(app).get("/time/timestamp-ms")

    assert response.status_code == 200
    expected = int(instant.timestamp()) * 1000 + 999
    assert response.json() == expected


def test_millisecond_timestamp_truncates_not_rounds(monkeypatch):
    instant = datetime(2026, 11, 12, 3, 30, 0, 1001, tzinfo=timezone.utc)
    monkeypatch.setattr(time_route, "utc_now", lambda: instant)

    assert TestClient(app).get("/time/timestamp-ms").json() == int(instant.timestamp()) * 1000 + 1
