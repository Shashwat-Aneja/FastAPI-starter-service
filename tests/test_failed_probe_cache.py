from fastapi.testclient import TestClient
from main import app
def test_unhandled_probe_failure_is_never_cacheable():
    route=next(r for r in app.routes if getattr(r,'path',None)=='/healthz' and 'GET' in r.methods)
    old=route.dependant.call
    def fail():raise RuntimeError('probe failed')
    route.dependant.call=fail
    try:
        with TestClient(app,raise_server_exceptions=False) as client:
            response=client.get('/healthz')
        assert response.status_code==500
        assert response.headers['cache-control']=='no-store'
        assert response.headers.get('x-request-id')
    finally:route.dependant.call=old
