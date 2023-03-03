import os
from datetime import datetime, timezone

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.env import load_env_vars
from app.titanic_survival.model import TITANIC_MODEL_VERSION
from app.titanic_survival.model import predict as titanic_survival_predict

from .models import Passenger, SurvivalPredictionByPassengerIds

app = FastAPI()

load_env_vars()

booted_at = {}


@app.on_event("startup")
def startup_event():
    booted_at["time"] = datetime.now(timezone.utc)


# Redirect base url to /docs
@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post(
    "/predict_survival_by_passengers", response_model=SurvivalPredictionByPassengerIds
)
def predict_survival_by_passengers(passengers: list[Passenger]):
    # Convert passengers to a list of dicts; this is what the model expects
    # There must be a better way to do this.
    passengers = [passenger.dict() for passenger in passengers]

    # Make predictions
    results = [] if not passengers else titanic_survival_predict(passengers)

    return {
        "predictions": results,
        "metadata": {
            "titanic_model_version": TITANIC_MODEL_VERSION,
        },
    }


@app.get("/health_check")
def health_check():
    return {
        "aws_region": os.environ.get("AWS_REGION"),
        "booted_at": booted_at.get("time"),
        "health": "OK",
        "k8s_env": os.environ.get("K8S_ENV"),
        "python_env": os.environ["PYTHON_ENV"],
        "titanic_model_version": TITANIC_MODEL_VERSION,
        "version": os.environ.get(
            "APP_REVISION", "Missing $APP_REVISION env var, not set"
        ),
    }


# Don't render JSON for load balancer health check, just return 200
@app.get("/health_check/load_balancer")
def health_check_load_balancer():
    return
