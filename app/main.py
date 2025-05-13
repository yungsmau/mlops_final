from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from app.model_utils import load_metrics, load_model


app = FastAPI()


model = load_model()
metrics = load_metrics()


class PredictRequest(BaseModel):
    features: list[float]


@app.get("/metrics")
def get_metrics():
    """
    Возвращает метрики модели: MSE и R2
    """
    return {"mse": metrics.get("mse"), "r2": metrics.get("r2")}


@app.post("/predict")
def predict(request: PredictRequest):
    """
    Принимает список фичей и возвращает предсказание.
    """
    X = np.array(request.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": prediction.tolist()}
