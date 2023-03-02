from pathlib import Path

import joblib
import pandas as pd

TITANIC_MODEL_VERSION = 20230228

BASE_DIR = Path(__file__).resolve(strict=True).parent


with open(f"{BASE_DIR}/model-{TITANIC_MODEL_VERSION}.joblib", "rb") as f:
    model = joblib.load(f)


def preprocess_data(df):
    # Add new features
    df["NameLength"] = df.Name.apply(len)
    df["HasCabin"] = df.Cabin.apply(lambda x: 0 if type(x) == float else 1)
    df["IsFemale"] = df.Sex == "female"

    # Drop columns
    drop_cols = ["Name", "Ticket", "Cabin", "Embarked", "PassengerId", "Sex"]
    df = df.drop(drop_cols, axis=1)

    # Fill missing values
    df["Fare"] = df.Fare.fillna(0)
    # TODO: actually handle NA values for inference correctly
    # df.fillna(modes, inplace=True)

    # Reorder columns alphabetically
    df = df.reindex(sorted(df.columns), axis=1)
    return df


# Payload is a dict, already converted from pydantic object
def predict(passengers):
    """Predict passengers' survival."""
    df = pd.DataFrame.from_records(passengers)
    passenger_ids = df.PassengerId
    df = preprocess_data(df)
    y_pred = model.predict(df)

    return [
        {
            "passenger_id": passenger_id,
            "survived": bool(score),
            "score": round(score, 3),
        }
        for passenger_id, score in zip(passenger_ids, y_pred)
    ]
