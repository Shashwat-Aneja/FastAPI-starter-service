from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_process_time_header_is_numeric_and_non_negative():
    response = client.get("/healthz")

    assert response.status_code == 200
    elapsed_ms = float(response.headers["x-process-time-ms"])
    assert elapsed_ms >= 0


def test_process_time_header_coexists_with_request_id():
    response = client.get(
        "/healthz",
        headers={"X-Request-ID": "diagnostic-trace-42"},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "diagnostic-trace-42"
    assert float(response.headers["x-process-time-ms"]) >= 0
