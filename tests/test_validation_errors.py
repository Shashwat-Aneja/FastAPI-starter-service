from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_validation_errors_include_request_trace_and_field_location():
    response = client.get(
        "/math/add",
        params={"x": "not-a-number", "y": "3"},
        headers={"X-Request-ID": "trace-validation-17"},
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"] == "Request validation failed"
    assert payload["request_id"] == "trace-validation-17"
    assert payload["errors"][0]["location"] == ["query", "x"]
    assert response.headers["x-request-id"] == "trace-validation-17"
    assert float(response.headers["x-process-time-ms"]) >= 0


def test_validation_errors_do_not_echo_submitted_values():
    submitted_secret = "private-value-that-must-not-be-reflected"
    response = client.get(
        "/math/add",
        params={"x": submitted_secret, "y": "1"},
        headers={"X-Request-ID": "trace-validation-redacted"},
    )

    assert response.status_code == 422
    assert submitted_secret not in response.text
    assert "input" not in response.json()["errors"][0]


def test_missing_query_parameter_reports_its_location():
    response = client.get(
        "/math/add",
        params={"x": "2"},
        headers={"X-Request-ID": "trace-validation-missing"},
    )

    assert response.status_code == 422
    assert response.json()["errors"][0]["location"] == ["query", "y"]
