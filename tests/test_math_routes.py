from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_returns_operation_and_result():
    response = client.get("/math/add", params={"x": 2, "y": 3})

    assert response.status_code == 200
    assert response.json() == {"operation": "add", "x": 2.0, "y": 3.0, "result": 5.0}


def test_divide_rejects_zero_denominator():
    response = client.get("/math/divide", params={"x": 10, "y": 0})

    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero."


def test_math_rejects_non_finite_operands():
    response = client.get("/math/add", params={"x": "inf", "y": 1})

    assert response.status_code == 422
    assert response.json()["detail"] == "Operands must be finite numbers."


def test_multiplication_rejects_overflow_result():
    response = client.get("/math/multiply", params={"x": 1e308, "y": 1e308})

    assert response.status_code == 422
    assert response.json()["detail"] == "Result is outside the supported numeric range."


def test_subtract_returns_expected_result():
    response = client.get("/math/subtract", params={"x": 9, "y": 4})

    assert response.status_code == 200
    assert response.json()["result"] == 5.0


def test_divide_returns_expected_result():
    response = client.get("/math/divide", params={"x": 9, "y": 3})

    assert response.status_code == 200
    assert response.json()["result"] == 3.0

