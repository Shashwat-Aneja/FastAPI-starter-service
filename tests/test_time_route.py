from datetime import datetime, timezone
import re

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_now_returns_iso_8601_utc_timestamp():
    response = client.get("/time/now")

    assert response.status_code == 200
    value = response.json()["current_time"]
    assert value.endswith("Z")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert parsed.tzinfo == timezone.utc


def test_timestamp_returns_integer_epoch_seconds():
    before = int(datetime.now(timezone.utc).timestamp())
    response = client.get("/time/timestamp")
    after = int(datetime.now(timezone.utc).timestamp())

    assert response.status_code == 200
    value = response.json()["timestamp"]
    assert isinstance(value, int)
    assert before <= value <= after


def test_formatted_time_includes_utc_suffix():
    response = client.get("/time/formatted")

    assert response.status_code == 200
    assert re.fullmatch(r"\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2} UTC", response.json()["formatted_time"])
