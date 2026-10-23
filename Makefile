.PHONY: install data train prefect-server deploy api docker-build docker-run test lint

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

api:
	uv run uvicorn src.web_service.main:app --reload --port 8000

docker-build:
	docker build -t abalone-api -f Dockerfile.app .

docker-run:
	docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api

test:
	uv run pytest

lint:
	uv run pre-commit run --all-files
