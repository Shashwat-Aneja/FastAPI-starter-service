import math
from fastapi.testclient import TestClient
from main import app
client=TestClient(app)

def test_stable_norm():
    assert client.get("/math/hypot",params=[("values",3),("values",4)]).json()["result"]==5
    value=client.get("/math/hypot",params=[("values",1e308),("values",1e308)]).json()["result"]
    assert math.isfinite(value) and value>1e308

def test_norm_rejects_invalid_and_overflow():
    for values in [["inf"], ["1"]*1001, ["1.7e308"]*2]:
        assert client.get("/math/hypot",params=[("values",v) for v in values]).status_code==422
