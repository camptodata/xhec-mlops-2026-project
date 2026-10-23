"""Prediction and evaluation."""

import numpy as np
import pandas as pd
from prefect import task
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@task(name="Predict")
def predict(x: pd.DataFrame, model: LinearRegression) -> np.ndarray:
    """Predict the number of rings.

    Args:
        x: Preprocessed features.
        model: Fitted model.

    Returns:
        One prediction per row of `x`.
    """
    return model.predict(x)


@task(name="Evaluate model")
def evaluate_model(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    """Compute regression metrics.

    Args:
        y_true: Actual number of rings.
        y_pred: Predicted number of rings.

    Returns:
        RMSE, MAE and R2.
    """
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }
