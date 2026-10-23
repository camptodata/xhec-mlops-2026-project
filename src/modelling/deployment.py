"""Serve the training flow as a weekly deployment."""

from prefect import serve

from src.modelling.config import DATA_PATH
from src.modelling.main import train_model_workflow

if __name__ == "__main__":
    train_model_deployment = train_model_workflow.to_deployment(
        name="train-model-weekly",
        version="0.1.0",
        tags=["training"],
        cron="0 0 * * 0",
        parameters={"trainset_path": str(DATA_PATH)},
    )
    serve(train_model_deployment)
