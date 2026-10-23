"""FastAPI application serving the abalone age model."""

from fastapi import FastAPI

from src.modelling.config import ENCODER_PATH, MODEL_PATH
from src.web_service.app_config import APP_DESCRIPTION, APP_TITLE, APP_VERSION
from src.web_service.lib.inference import run_inference
from src.web_service.lib.models import InputData, PredictionOut
from src.web_service.utils import load_object

# Loaded once when the app starts, not at every request.
encoder = load_object(ENCODER_PATH)
model = load_object(MODEL_PATH)

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)


@app.get("/")
def home() -> dict[str, str]:
    """Health check."""
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData) -> PredictionOut:
    """Predict the number of rings and the age of an abalone."""
    rings = run_inference(payload, encoder, model)
    return PredictionOut(rings=rings, age=rings + 1.5)
