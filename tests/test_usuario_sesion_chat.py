import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_usuario_sesion_chat(client):
    # Crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "chatuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Chat",
        "apellidos": "User",
        "edad": 25,
        "email": f"chat_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # Crear sesión
    sesion_resp = client.post("/sesiones_chat/", json={
        "nombre_tema": "Sesión Test",
        "tipo": "público",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion_resp.json()["id_sesion"]

    # Crear relación
    resp = client.post("/usuario_sesion_chat/", json={"id_usuario": usuario_id, "id_sesion": sesion_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id_usuario"] == usuario_id
    assert data["id_sesion"] == sesion_id

def test_get_relaciones(client):
    resp = client.get("/usuario_sesion_chat/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_delete_usuario_sesion_chat(client):
    # Crear nuevo usuario + sesión
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "tempuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Temp",
        "apellidos": "User",
        "edad": 22,
        "email": f"temp_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    sesion_resp = client.post("/sesiones_chat/", json={
        "nombre_tema": "Sesión Temporal",
        "tipo": "privado",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion_resp.json()["id_sesion"]

    # Crear relación
    client.post("/usuario_sesion_chat/", json={"id_usuario": usuario_id, "id_sesion": sesion_id})

    # Eliminar relación
    resp = client.request("DELETE", "/usuario_sesion_chat/", json={"id_usuario": usuario_id, "id_sesion": sesion_id})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Relación eliminada"
