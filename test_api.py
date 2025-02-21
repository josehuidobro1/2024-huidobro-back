import requests
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de que apunta correctamente a tu archivo FastAPI
# Supongo que tienes una función para crear tokens válidos
from app.config import create_token

client = TestClient(app)


def create_valid_token():
    return create_token("valid_user_id")

# Crear un token inválido para pruebas


def invalid_token():
    return "invalid_token"

# Ruta para obtener datos de un usuario


ENDPOINT = "https://two024-huidobro-back.onrender.com"


def test_can_call_enpoint():
    valid_token = create_valid_token()
    response = requests.get(
        ENDPOINT, headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
