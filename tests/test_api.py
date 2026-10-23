from fastapi.testclient import TestClient

from src.web_service.main import app

client = TestClient(app)

SAMPLE = {
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15,
}


def test_health_check() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health_check": "App up and running!"}


def test_predict_returns_rings_and_age() -> None:
    response = client.post("/predict", json=SAMPLE)
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"rings", "age"}
    assert body["age"] == body["rings"] + 1.5


def test_predict_rejects_invalid_sex() -> None:
    response = client.post("/predict", json={**SAMPLE, "sex": "X"})
    assert response.status_code == 422
