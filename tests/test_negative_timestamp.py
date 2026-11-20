from datetime import datetime,timezone
from fastapi.testclient import TestClient
from main import app
from routes import time_route
def test_pre_epoch_timestamps_use_floor_and_exact_milliseconds(monkeypatch):
    monkeypatch.setattr(time_route,'utc_now',lambda:datetime(1969,12,31,23,59,59,999000,tzinfo=timezone.utc))
    with TestClient(app) as client:
        assert client.get('/time/timestamp').json()=={'timestamp':-1}
        assert client.get('/time/timestamp-ms').json()==-1
