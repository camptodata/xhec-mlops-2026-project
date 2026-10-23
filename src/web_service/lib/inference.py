"""Inference on new data."""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

from src.modelling.preprocessing import preprocess
from src.web_service.lib.models import InputData


def run_inference(input_data: InputData, encoder: OneHotEncoder, model: LinearRegression) -> float:
    """Predict the number of rings of one abalone.

    Args:
        input_data: Validated measurements of the abalone.
        encoder: Fitted encoder from the training.
        model: Fitted model from the training.

    Returns:
        The predicted number of rings.
    """
    df = pd.DataFrame([input_data.model_dump()])
    features, _, _ = preprocess.fn(df, encoder, with_target=False)
    return float(model.predict(features)[0])
