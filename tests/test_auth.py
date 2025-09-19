import pytest

def test_register_and_login_and_me(client):
    # Registro
    response = client.post("/auth/register", json={
        "nombre_usuario": "testuser",
        "contraseña": "123456",
        "nombres": "Test",
        "apellidos": "User",
        "edad": 25,
        "email": "test@example.com",
        "id_rol": 1
    })
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_usuario"] == "testuser"

    # Login
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "123456"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_usuario"] == "testuser"
    assert data["email"] == "test@example.com"
