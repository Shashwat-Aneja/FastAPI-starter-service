"""Greeting route validation regression tests."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_greeting_trims_surrounding_whitespace():
    response = client.get("/hello/greet", params={"name": "  Ada  "})
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello, Ada!")


def test_greeting_rejects_whitespace_only_names():
    response = client.get("/hello/greet", params={"name": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] == "Name must not be blank."


def test_greeting_rejects_excessively_long_names():
    response = client.get("/hello/greet", params={"name": "a" * 81})
    assert response.status_code == 422


def test_greeting_retains_default_guest_name():
    response = client.get("/hello/greet")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello, Guest!")
