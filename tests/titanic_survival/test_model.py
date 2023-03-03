# Description: Test the model.py file
from app.titanic_survival.model import predict

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


def test_predict():
    passengers = payload.copy()
    p1 = passengers[0]
    p2 = passengers[1]
    predictions = predict(passengers)

    assert predictions[0]["passenger_id"] == p1["PassengerId"]
    assert predictions[0]["survived"] == True
    assert predictions[0]["score"] >= 0.90

    assert predictions[1]["passenger_id"] == p2["PassengerId"]
    assert predictions[1]["survived"] == False
    assert predictions[1]["score"] <= 0.10
