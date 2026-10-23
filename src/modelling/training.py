"""Model training."""

import pandas as pd
from sklearn.linear_model import LinearRegression


def train_model(x_train: pd.DataFrame, y_train: pd.Series) -> LinearRegression:
    """Fit a linear regression, the best model of the modelling notebook.

    Args:
        x_train: Training features.
        y_train: Training target (number of rings).

    Returns:
        The fitted model.
    """
    return LinearRegression().fit(x_train, y_train)
