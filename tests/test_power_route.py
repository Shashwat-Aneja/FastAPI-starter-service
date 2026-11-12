import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("base", "exponent", "expected"),
    [(2, 3, 8), (9, 0.5, 3), (-2, 3, -8), (0, 0, 1)],
)
def test_power_returns_real_result(base, exponent, expected):
    response = client.get("/math/power", params={"x": base, "y": exponent})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(expected)


@pytest.mark.parametrize(
    ("base", "exponent"),
    [(-2, 0.5), (0, -1), (1e308, 2)],
)
def test_power_rejects_undefined_or_overflow_results(base, exponent):
    response = client.get("/math/power", params={"x": base, "y": exponent})
    assert response.status_code == 422


def test_power_rejects_nonfinite_operand():
    response = client.get("/math/power", params={"x": "inf", "y": 2})
    assert response.status_code == 422
