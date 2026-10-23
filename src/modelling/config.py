from pathlib import Path

CATEGORICAL_COLS = ["sex"]
NUMERICAL_COLS = [
    "length",
    "diameter",
    "height",
    "whole_weight",
    "shucked_weight",
    "viscera_weight",
    "shell_weight",
]
TARGET = "rings"

LOCAL_OBJECTS_DIR = Path(__file__).resolve().parents[1] / "web_service" / "local_objects"
MODEL_PATH = LOCAL_OBJECTS_DIR / "model.pkl"
ENCODER_PATH = LOCAL_OBJECTS_DIR / "encoder.pkl"

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "abalone.csv"
