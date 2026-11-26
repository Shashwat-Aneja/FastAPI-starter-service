import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.mark.parametrize('values,mean',[([1e308,1e308],1e308),([-1e308,1e308],0),([0,0],0)])
def test_statistics_mean_stays_finite_when_raw_sum_would_overflow(values,mean):
    response=TestClient(app).get('/math/statistics',params=[('values',str(x)) for x in values])
    assert response.status_code==200 and response.json()['mean']==mean
    assert response.json()['count']==len(values)

def test_statistics_rejects_nonfinite_and_oversized_batches():
    client=TestClient(app)
    assert client.get('/math/statistics',params={'values':'nan'}).status_code==422
    assert client.get('/math/statistics',params=[('values','1')]*1001).status_code==422

@pytest.mark.parametrize('values,expected',[([1e16,-9999999999999998.0],1.0),([1e308,1e-20,-1e308],1e-20/3),([1e308,1e308,-1e308,-1e308],0.0)])
def test_statistics_preserves_cancellation_residuals(values,expected):
    response=TestClient(app).get('/math/statistics',params=[('values',str(value)) for value in values])
    assert response.status_code==200 and response.json()['mean']==expected
