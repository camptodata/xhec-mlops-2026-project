import pandas as pd

from src.modelling.predicting import predict
from src.modelling.preprocessing import preprocess
from src.modelling.training import train_model

NUMERICAL = {
    "length": 0.5,
    "diameter": 0.4,
    "height": 0.1,
    "whole_weight": 0.5,
    "shucked_weight": 0.2,
    "viscera_weight": 0.1,
    "shell_weight": 0.15,
}


def make_df(sexes: list[str]) -> pd.DataFrame:
    rows = [{"sex": sex, **NUMERICAL, "rings": 8 + i} for i, sex in enumerate(sexes)]
    return pd.DataFrame(rows)


def test_preprocess_one_hot_encodes_sex() -> None:
    features, target, _ = preprocess(make_df(["M", "F", "I", "M"]))
    assert list(features.columns[-3:]) == ["sex_F", "sex_I", "sex_M"]
    assert features.shape == (4, 10)
    assert target.tolist() == [8, 9, 10, 11]


def test_preprocess_reuses_encoder_and_ignores_unknown_sex() -> None:
    _, _, encoder = preprocess(make_df(["M", "F", "I"]))
    features, target, _ = preprocess(make_df(["X"]).drop(columns="rings"), encoder, False)
    assert target is None
    assert features[["sex_F", "sex_I", "sex_M"]].sum().sum() == 0


def test_train_and_predict_return_one_value_per_row() -> None:
    x, y, _ = preprocess(make_df(["M", "F", "I", "M", "F"]))
    model = train_model(x, y)
    assert predict(x, model).shape == (5,)
