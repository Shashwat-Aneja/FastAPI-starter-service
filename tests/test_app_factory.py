import pytest
from fastapi.testclient import TestClient
from main import app, create_app

def test_isolated_opt_in_cors():
    client=TestClient(create_app(cors_origins=['https://example.com']))
    headers={'Origin':'https://example.com','Access-Control-Request-Method':'GET','Access-Control-Request-Headers':'X-Request-ID'}
    response=client.options('/healthz',headers=headers)
    assert response.status_code==200 and response.headers['access-control-allow-origin']=='https://example.com'
    assert client.get('/healthz',headers={'Origin':'https://example.com'}).headers['access-control-allow-origin']=='https://example.com'
    assert 'access-control-allow-origin' not in client.get('/healthz',headers={'Origin':'https://other.com'}).headers
    assert 'access-control-allow-origin' not in TestClient(app).get('/healthz',headers={'Origin':'https://example.com'}).headers

@pytest.mark.parametrize('origins',['https://example.com',[None],[' '],['x']*101])
def test_bad_origins(origins):
    with pytest.raises(ValueError):create_app(cors_origins=origins)
