from fastapi.testclient import TestClient
from main import app
def test_duplicate_request_ids_generate_one_unambiguous_trace_id():
    with TestClient(app) as client:
        response=client.get('/healthz',headers=[('x-request-id','first'),('x-request-id','second')])
    assert response.status_code==200
    assert response.headers['x-request-id'] not in {'first','second','first, second'}
def test_single_valid_id_still_propagates():
    with TestClient(app) as client:
        assert client.get('/healthz',headers={'x-request-id':'known-id'}).headers['x-request-id']=='known-id'
