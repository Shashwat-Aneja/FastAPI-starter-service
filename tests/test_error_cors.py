from fastapi.testclient import TestClient
from main import create_app

def test_unhandled_error_preserves_allowed_origin_diagnostics():
    app=create_app(cors_origins=['https://example.com'])
    @app.get('/broken')
    def broken():raise RuntimeError('secret detail')
    client=TestClient(app,raise_server_exceptions=False)
    response=client.get('/broken',headers={'Origin':'https://example.com'})
    assert response.status_code==500
    assert response.headers['access-control-allow-origin']=='https://example.com'
    assert 'X-Request-ID' in response.headers['access-control-expose-headers']
    assert response.headers['vary']=='Origin'
    assert response.json()=={'detail':'Internal Server Error'}
    assert 'access-control-allow-origin' not in client.get('/broken',headers={'Origin':'https://other.com'}).headers
