import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_sesion_chat(client):
    # crear usuario anfitrión
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "host" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Host",
        "apellidos": "User",
        "edad": 28,
        "email": f"host_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    anfitrion_id = user_resp.json()["id_usuario"]

    resp = client.post("/sesiones_chat/", json={
        "nombre_tema": "Chat de prueba",
        "tipo": "público",
        "anfitrion_id": anfitrion_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["nombre_tema"] == "Chat de prueba"
    assert "id_sesion" in data

def test_get_sesiones_chat(client):
    resp = client.get("/sesiones_chat/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_sesion_chat(client):
    resp = client.get("/sesiones_chat/1")
    assert resp.status_code in [200, 404]

def test_update_sesion_chat(client):
    resp = client.put("/sesiones_chat/1", json={"estado": "cerrada"})
    assert resp.status_code in [200, 404]

def test_delete_sesion_chat(client):
    resp = client.delete("/sesiones_chat/1")
    assert resp.status_code in [200, 404]
