.PHONY: install data train prefect-server deploy test lint

install:
	uv sync && uv run pre-commit install

data:
	mkdir -p data && curl -L -o data/abalone.zip https://www.kaggle.com/api/v1/datasets/download/rodolfomendes/abalone-dataset && unzip -o data/abalone.zip -d data

train:
	uv run python -m src.modelling.main data/abalone.csv

prefect-server:
	uv run prefect server start

deploy:
	uv run python -m src.modelling.deployment

test:
	uv run pytest

lint:
	uv run pre-commit run --all-files
