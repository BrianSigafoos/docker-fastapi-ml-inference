import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.titanic_survival.model import TITANIC_MODEL_VERSION

client = TestClient(app)

payload = [
    {
        "PassengerId": 1248,
        "Pclass": 1,
        "Name": "Brown, Mrs. John Murray (Caroline Lane Lamson)",
        "Sex": "female",
        "Age": 59.0,
        "SibSp": 2,
        "Parch": 0,
        "Ticket": "11769",
        "Fare": 51.4792,
        "Cabin": "C101",
        "Embarked": "S",
    },
    {
        "PassengerId": 1128,
        "Pclass": 1,
        "Name": "Warren, Mr. Frank Manley",
        "Sex": "male",
        "Age": 64.0,
        "SibSp": 1,
        "Parch": 0,
        "Ticket": "110813",
        "Fare": 75.25,
        "Cabin": "D37",
        "Embarked": "C",
    },
]


def test_predict_survival_by_passengers():
    passengers = payload.copy()
    p1 = passengers[0]
    p2 = passengers[1]

    response = client.post("/predict_survival_by_passengers", json=payload)
    # Check that the response status code is 200 OK
    assert response.status_code == 200

    response = response.json()
    predictions = response["predictions"]
    assert predictions[0]["passenger_id"] == p1["PassengerId"]
    assert predictions[0]["survived"] == True
    assert predictions[0]["score"] >= 0.90

    assert predictions[1]["passenger_id"] == p2["PassengerId"]
    assert predictions[1]["survived"] == False
    assert predictions[1]["score"] <= 0.10

    metadata = response["metadata"]
    assert metadata["titanic_model_version"] == TITANIC_MODEL_VERSION


def test_health_check():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {
        "aws_region": None,
        "booted_at": None,
        "health": "OK",
        "k8s_env": None,
        "python_env": "test",
        "titanic_model_version": TITANIC_MODEL_VERSION,
        "version": "Missing $APP_REVISION env var, not set",
    }


def test_health_check_load_balancer():
    response = client.get("/health_check/load_balancer")
    assert response.status_code == 200
    assert response.json() == None
