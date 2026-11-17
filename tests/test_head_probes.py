import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.mark.parametrize("path", ["/healthz", "/readyz"])
def test_probes_support_head_without_cached_health(path):
    client = TestClient(app)
    result = client.head(path)
    assert result.status_code == 200
    assert result.content == b""
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["x-request-id"]
    assert client.get(path).headers["cache-control"] == "no-store"
