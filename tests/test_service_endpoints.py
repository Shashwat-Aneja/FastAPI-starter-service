from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint_reports_healthy_status():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {"status": "healthy"}


def test_root_endpoint_points_to_api_docs():
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"]
    assert payload["docs"] == "/docs"


def test_readiness_endpoint_exposes_service_metadata():
    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "service": app.title,
        "version": app.version,
    }


def test_version_endpoint_exposes_service_metadata():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "service": "FastAPI Starter Service",
        "version": "1.0.0",
    }
