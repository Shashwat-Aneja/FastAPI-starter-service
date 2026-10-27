from uuid import UUID

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_request_id_header_is_preserved_when_well_formed():
    response = client.get("/healthz", headers={"X-Request-ID": "trace-123.alpha"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "trace-123.alpha"


def test_missing_request_id_is_generated_as_uuid():
    response = client.get("/healthz")

    assert response.status_code == 200
    UUID(response.headers["x-request-id"])


def test_malformed_request_id_is_replaced():
    response = client.get("/healthz", headers={"X-Request-ID": "bad request id"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] != "bad request id"
    UUID(response.headers["x-request-id"])
