import pytest

def test_register_and_login(client, db_session):
    # registro
    response = client.post("/auth/register", json={
        "nombre_usuario": "testauth",
        "contraseña": "1234",
        "nombres": "Auth",
        "apellidos": "User",
        "edad": 22,
        "email": "testauth@example.com",
        "id_rol": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_usuario"] == "testauth"

    # login con formato correcto
    response = client.post(
        "/auth/login",
        data={"username": "testauth", "password": "1234"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # acceso a /me
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["nombre_usuario"] == "testauth"


def test_me_invalid_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
