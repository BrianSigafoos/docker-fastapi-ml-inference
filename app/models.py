from pydantic import BaseModel


class Passenger(BaseModel):
    """Passenger to predict survival for."""

    PassengerId: int
    Pclass: int
    Name: str
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Ticket: str
    Fare: float
    Cabin: str
    Embarked: str

    class Config:
        schema_extra = {
            "example": {
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
        }


class PassengerSurvivalPrediction(BaseModel):
    """Survival prediction for a single passenger."""

    passenger_id: int
    survived: bool
    score: float


class SurvivalPredictionByPassengerIds(BaseModel):
    """Survival prediction for a list of passengers."""

    predictions: list[PassengerSurvivalPrediction]
    metadata: dict
