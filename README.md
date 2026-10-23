# Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)

The age of an abalone (a sea snail) is normally found by counting the rings of its shell under a microscope, which is slow. This project predicts the number of rings, and so the age (rings + 1.5 years), from the sex and easy physical measurements of the animal. The model is trained by a Prefect workflow that is retrained every week, and served by a FastAPI application packaged in a Docker image.

## Team

- Nick Hartmann, GitHub [@camptodata](https://github.com/camptodata)

## Project structure

```
.
├── bin/run_services.sh        # starts the Prefect server and the API (used by Docker)
├── notebooks/                 # eda.ipynb, modelling.ipynb
├── src/
│   ├── modelling/             # preprocessing, training, prediction, Prefect flow and deployment
│   └── web_service/           # FastAPI app, Pydantic models, saved encoder and model
├── tests/                     # pytest tests (modelling and API)
├── Dockerfile.app
├── Makefile
└── pyproject.toml / uv.lock   # dependencies
```

## Setup

Prerequisites: [uv](https://docs.astral.sh/uv/) (it installs Python 3.11 for you) and [Docker](https://docs.docker.com/get-docker/) for the container.

```bash
uv sync
uv run pre-commit install
```

`make install` does the same. All other commands below are run from the repository root; most have a `make` target (see the `Makefile`).

## Data

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) into `data/` (no login needed), or run `make data`:

```bash
mkdir -p data
curl -L -o data/abalone.zip https://www.kaggle.com/api/v1/datasets/download/rodolfomendes/abalone-dataset
unzip -o data/abalone.zip -d data
```

## Notebooks

`notebooks/eda.ipynb` explores the data and `notebooks/modelling.ipynb` compares models and logs the runs in MLflow. To browse the runs:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Train the model

```bash
uv run python -m src.modelling.main data/abalone.csv
```

This runs the Prefect flow `train_model_workflow`, prints the test metrics (RMSE, MAE, R2) and saves `encoder.pkl` and `model.pkl` in `src/web_service/local_objects/`. The same command is available as `make train`.

## Prefect

1. Start the Prefect server in its own terminal:
   ```bash
   uv run prefect server start
   ```
2. In every other terminal, point Prefect to it:
   ```bash
   export PREFECT_API_URL=http://127.0.0.1:4200/api   # on Windows PowerShell: $env:PREFECT_API_URL = "http://127.0.0.1:4200/api"
   ```
3. Start the deployment, which retrains the model every Sunday at 00:00 (see `src/modelling/deployment.py`):
   ```bash
   uv run python -m src.modelling.deployment
   ```
4. Trigger a run without waiting for the schedule:
   ```bash
   uv run prefect deployment run "Train model/train-model-weekly"
   ```
5. Open the UI at http://127.0.0.1:4200 to see the runs and their tasks.

## API locally

```bash
uv run uvicorn src.web_service.main:app --port 8001
```

(or `make api`, which uses port 8000 with auto-reload). The interactive documentation, with a ready-to-try example, is at http://127.0.0.1:8001/docs. Example request:

```bash
curl -X POST http://127.0.0.1:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"sex": "M", "length": 0.455, "diameter": 0.365, "height": 0.095, "whole_weight": 0.514, "shucked_weight": 0.2245, "viscera_weight": 0.101, "shell_weight": 0.15}'
```

Response (status 201):

```json
{"rings": 9.204333139804264, "age": 10.704333139804264}
```

An invalid input (for example `"sex": "X"` or a negative length) returns status 422.

## Docker

The image runs the Prefect server and the API together (`bin/run_services.sh`).

```bash
docker build -t abalone-api -f Dockerfile.app .
docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api
```

(or `make docker-build` and `make docker-run`). Then open the API documentation at http://localhost:8000/docs and the Prefect UI at http://localhost:4200. The `curl` example above works with port 8000.

## Tests and code quality

```bash
uv run pytest
uv run pre-commit run --all-files
```

(`make test` and `make lint`). The GitHub Actions workflow in `.github/workflows/ci.yaml` runs the pre-commit hooks and the tests, then builds the Docker image and checks that the API and the Prefect UI answer.
