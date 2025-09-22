import pytest
from app.main import app

def test_register_and_login(client, db_session):
    # Registro
    payload = {
        "nombre_usuario": "testuser",
        "contraseña": "Secret123",
        "nombres": "Test",
        "apellidos": "User",
        "edad": 20,
        "email": "test@example.com",
        "id_rol": 1
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["nombre_usuario"] == payload["nombre_usuario"]

    # Login
    login_data = {
        "username": payload["nombre_usuario"],
        "password": payload["contraseña"]
    }
    r = client.post("/auth/login", data=login_data)
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # Obtener datos del usuario autenticado
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == payload["email"]
