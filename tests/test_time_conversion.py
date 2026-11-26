from fastapi.testclient import TestClient
from main import app

def test_known_instant_is_converted_without_reading_wall_clock():
    response=TestClient(app).get('/time/convert',params={'instant':'2026-11-26T00:00:00Z','name':'Asia/Kolkata'})
    assert response.status_code==200 and response.json()['current_time']=='2026-11-26T05:30:00+05:30'

def test_naive_or_unsupported_instants_fail_explicitly():
    client=TestClient(app)
    for value in ['2026-11-26T00:00:00','not-a-date','9999-12-31T23:59:59-23:00']:
        assert client.get('/time/convert',params={'instant':value,'name':'Asia/Kolkata'}).status_code==422
