# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid
from app.routers.auth import get_password_hash
from app.database import get_db
from app.models.usuario import Usuario

@pytest.fixture
def test_user(db_session):
    """Crea un usuario de prueba con contraseña hasheada"""
    nombre_usuario = "authuser_" + uuid.uuid4().hex[:6]
    user = Usuario(
        nombre_usuario=nombre_usuario,
        contraseña=get_password_hash("testpass"),
        nombres="Auth",
        apellidos="User",
        edad=25,
        email=f"{nombre_usuario}@test.com",
        id_rol=1
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_login_success(client, test_user):
    response = client.post(
        "/auth/token",
        data={"username": test_user.nombre_usuario, "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client, test_user):
    response = client.post(
        "/auth/token",
        data={"username": test_user.nombre_usuario, "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"
