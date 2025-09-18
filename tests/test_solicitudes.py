import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def solicitud_data():
    return {
        "mensaje": "¿Quieres ser mi amigo?",
        "estado": "pendiente",
        "remitente_id": 1,
        "destinatario_id": 2
    }

def test_create_solicitud(client, solicitud_data):
    response = client.post("/solicitudes/", json=solicitud_data)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["mensaje"] == solicitud_data["mensaje"]
    assert data["data"]["remitente_id"] == solicitud_data["remitente_id"]
    assert data["data"]["destinatario_id"] == solicitud_data["destinatario_id"]

def test_get_solicitudes(client):
    response = client.get("/solicitudes/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_solicitud(client, solicitud_data):
    # Primero creamos una solicitud
    create_response = client.post("/solicitudes/", json=solicitud_data)
    solicitud_id = create_response.json()["data"]["id_solicitud"]

    response = client.get(f"/solicitudes/{solicitud_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id_solicitud"] == solicitud_id

def test_update_solicitud(client, solicitud_data):
    create_response = client.post("/solicitudes/", json=solicitud_data)
    solicitud_id = create_response.json()["data"]["id_solicitud"]

    update_data = {"estado": "aceptada"}
    response = client.put(f"/solicitudes/{solicitud_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["estado"] == "aceptada"

def test_delete_solicitud(client, solicitud_data):
    create_response = client.post("/solicitudes/", json=solicitud_data)
    solicitud_id = create_response.json()["data"]["id_solicitud"]

    response = client.delete(f"/solicitudes/{solicitud_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Solicitud eliminada correctamente"
