"""Data loading and preprocessing."""

from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from src.modelling.config import CATEGORICAL_COLS, NUMERICAL_COLS, TARGET


def load_data(path: Path) -> pd.DataFrame:
    """Read the abalone CSV and rename its columns to snake_case.

    Args:
        path: Path to the CSV file.

    Returns:
        The raw data with snake_case column names.
    """
    df = pd.read_csv(path)
    return df.rename(columns=lambda col: col.lower().replace(" ", "_"))


def preprocess(
    df: pd.DataFrame, encoder: OneHotEncoder | None = None, with_target: bool = True
) -> tuple[pd.DataFrame, pd.Series | None, OneHotEncoder]:
    """One-hot encode the categorical columns and keep the numerical ones.

    Args:
        df: Data with snake_case column names.
        encoder: Fitted encoder. If None, a new one is fitted on `df`.
        with_target: Whether `df` contains the target column.

    Returns:
        The features, the target (None if `with_target` is False) and the encoder.
    """
    if encoder is None:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        encoder.fit(df[CATEGORICAL_COLS])
    encoded = pd.DataFrame(
        encoder.transform(df[CATEGORICAL_COLS]),
        columns=encoder.get_feature_names_out(CATEGORICAL_COLS),
        index=df.index,
    )
    features = pd.concat([df[NUMERICAL_COLS], encoded], axis=1)
    target = df[TARGET] if with_target else None
    return features, target, encoder
