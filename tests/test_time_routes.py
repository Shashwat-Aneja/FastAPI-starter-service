from datetime import datetime, timezone

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_now_returns_iso_utc_timestamp():
    response = client.get("/time/now")

    assert response.status_code == 200
    value = response.json()["current_time"]
    assert value.endswith("Z")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo == timezone.utc


def test_timestamp_returns_current_unix_seconds():
    before = int(datetime.now(timezone.utc).timestamp())

    response = client.get("/time/timestamp")

    after = int(datetime.now(timezone.utc).timestamp())
    assert response.status_code == 200
    assert before <= response.json()["timestamp"] <= after


def test_formatted_time_uses_explicit_utc_label():
    response = client.get("/time/formatted")

    assert response.status_code == 200
    value = response.json()["formatted_time"]
    assert value.endswith(" UTC")
    datetime.strptime(value, "%Y-%m-%d %H:%M:%S UTC")
