import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_usuario():
    response = client.post(
        "/usuarios/",
        json={
            "nombre_usuario": "testuser",
            "contraseña": "123456",
            "nombres": "Test",
            "apellidos": "User",
            "edad": 20,
            "email": "test@example.com",
            "id_rol": 1
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_usuario"] == "testuser"
    assert "id_usuario" in data

def test_get_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_usuario():
    response = client.get("/usuarios/1")
    assert response.status_code in [200, 404]

def test_update_usuario():
    response = client.put("/usuarios/1", json={"telefono": "123456789"})
    assert response.status_code in [200, 404]

def test_delete_usuario():
    response = client.delete("/usuarios/1")
    assert response.status_code in [200, 404]
