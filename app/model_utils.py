import joblib
import json


def load_model(path="models/model.joblib"):
    return joblib.load(path)


def load_metrics(path="pipeline/metrics.json"):
    with open(path, "r") as f:
        return json.load(f)
