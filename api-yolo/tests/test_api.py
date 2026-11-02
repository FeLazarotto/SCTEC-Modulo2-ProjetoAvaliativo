
from fastapi.testclient import TestClient

from app.main import app


cliente = TestClient(app)


def test_inicio():
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "API YOLO funcionando!"


def test_health():
    resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_detect_sem_arquivo():
    resposta = cliente.post("/detect")

    assert resposta.status_code == 422
