import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {
        "aws_region": None,
        "booted_at": None,
        "health": "OK",
        "k8s_env": None,
        "python_env": "test",
        "version": "Missing $APP_REVISION env var, not set",
    }


def test_health_check_load_balancer():
    response = client.get("/health_check/load_balancer")
    assert response.status_code == 200
    assert response.json() == None
