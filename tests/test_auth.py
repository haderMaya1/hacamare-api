import pytest
from app.main import app

# ------------------------------------------------------------
# TEST COMPLETO DE AUTENTICACIÓN Y SEGURIDAD
# ------------------------------------------------------------
def test_auth_full_flow(client, db_session):
    """
    Cubre:
      - Registro usuario normal
      - Login (access + refresh token)
      - /auth/me con token válido
      - Refresh token -> nuevo access token
      - Change password -> login con nueva contraseña
      - Logout -> revocar token
      - Comprobar que token revocado no sirve
    """
    # ---------- Registro usuario ----------
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
    user_id = data["id_usuario"]

    # ---------- Login ----------
    login_data = {
        "username": payload["nombre_usuario"],
        "password": payload["contraseña"]
    }
    r = client.post("/auth/login", data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # ---------- /auth/me ----------
    r = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["id_usuario"] == user_id
    assert me["email"] == payload["email"]

    # ---------- Refresh token ----------
    r = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200
    refreshed = r.json()
    assert "access_token" in refreshed
    new_access = refreshed["access_token"]
    assert new_access != access_token  # debería ser diferente

    # ---------- Change password ----------
    change_body = {
        "old_password": payload["contraseña"],
        "new_password": "NewSecret123"
    }
    r = client.post(
        "/auth/change-password",
        json=change_body,
        headers={"Authorization": f"Bearer {new_access}"}
    )
    assert r.status_code == 200
    assert r.json()["message"].lower().startswith("contraseña actualizada")

    # Login con nueva contraseña debe funcionar
    r = client.post(
        "/auth/login",
        data={"username": payload["nombre_usuario"], "password": "NewSecret123"}
    )
    assert r.status_code == 200
    tokens2 = r.json()
    assert "access_token" in tokens2

    # ---------- Logout / revocar token ----------
    # Cerramos sesión usando el último access token
    r = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {tokens2['access_token']}"}
    )
    assert r.status_code == 200
    assert "sesión cerrada" in r.json()["message"].lower() or "Token ya revocado" in r.json()["message"]

    # Intentar usar el token revocado debe fallar
    r = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens2['access_token']}"}
    )
    assert r.status_code == 401
