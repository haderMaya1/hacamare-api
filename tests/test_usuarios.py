import pytest
import uuid

def test_create_usuario(client):
    unique_email = f"usuario_{uuid.uuid4().hex[:6]}@test.com"
    nombre_usuario = "testuser" + uuid.uuid4().hex[:4]
    response = client.post(
        "/usuarios/",
        json={
            "nombre_usuario": nombre_usuario,
            "contraseña": "123456",
            "nombres": "Test",
            "apellidos": "User",
            "edad": 20,
            "email": unique_email,
            "id_rol": 1
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_usuario"].startswith("testuser")
    assert "id_usuario" in data

def test_get_usuarios(client):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_usuario(client):
    response = client.get("/usuarios/1")
    assert response.status_code in [200, 404]

def test_update_usuario(client):
    response = client.put("/usuarios/1", json={"telefono": "123456789"})
    assert response.status_code in [200, 404]

def test_delete_usuario(client):
    response = client.delete("/usuarios/1")
    assert response.status_code in [200, 404]
