from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint_reports_healthy_status():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint_points_to_api_docs():
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"]
    assert payload["docs"] == "/docs"
