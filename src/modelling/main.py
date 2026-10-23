"""Training flow: read the data, preprocess it, train a model and save it."""

import argparse
from pathlib import Path

from sklearn.model_selection import train_test_split

from src.modelling.config import ENCODER_PATH, MODEL_PATH
from src.modelling.predicting import evaluate_model, predict
from src.modelling.preprocessing import load_data, preprocess
from src.modelling.training import train_model
from src.modelling.utils import pickle_object


def main(trainset_path: Path) -> None:
    """Train a model using the data at the given path and save the model and encoder (pickle).

    Args:
        trainset_path: Path to the abalone CSV file.
    """
    df = load_data(trainset_path)
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    x_train, y_train, encoder = preprocess(df_train)
    x_test, y_test, _ = preprocess(df_test, encoder)

    model = train_model(x_train, y_train)
    metrics = evaluate_model(y_test, predict(x_test, model))
    print(f"Test metrics: {metrics}")

    pickle_object(encoder, ENCODER_PATH)
    pickle_object(model, MODEL_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a model using the data at the given path.")
    parser.add_argument("trainset_path", type=Path, help="Path to the training set")
    args = parser.parse_args()
    main(args.trainset_path)
