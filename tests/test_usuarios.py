import pytest
from app.main import app
import uuid

def test_create_usuario(client):
    unique_email = f"usuario_{uuid.uuid4().hex[:6]}@test.com"
    response = client.post(
        "/usuarios/",
        json={
            "nombre_usuario": "testuser" + uuid.uuid4().hex[:4],
            "contraseña": "123456",
            "nombres": "Test",
            "apellidos": "User",
            "edad": 20,
            "email": unique_email,
            "id_rol": 1
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Usuario creado exitosamente"
    data = body["data"]
    assert "id_usuario" in data
    assert data["nombre_usuario"].startswith("testuser")

def test_get_usuarios(client):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Lista de usuarios"
    assert isinstance(body["data"], list)

def test_get_usuario(client):
    response = client.get("/usuarios/1")
    if response.status_code == 200:
        body = response.json()
        assert body["message"] == "Usuario encontrado"
        assert "id_usuario" in body["data"]
    else:
        assert response.status_code == 404

def test_update_usuario(client):
    response = client.put("/usuarios/1", json={"telefono": "123456789"})
    if response.status_code == 200:
        body = response.json()
        assert body["message"] == "Usuario actualizado correctamente"
        assert "telefono" in body["data"]
    else:
        assert response.status_code == 404

def test_delete_usuario(client):
    response = client.delete("/usuarios/1")
    if response.status_code == 200:
        body = response.json()
        assert body["message"] == "Usuario eliminado correctamente"
    else:
        assert response.status_code == 404
