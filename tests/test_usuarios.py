import pytest

def test_crud_usuarios(client, admin_token, db_session):
    headers = {"Authorization": f"Bearer {admin_token}"}

    # Crear usuario
    payload = {
        "nombre_usuario": "user_test",
        "contraseña": "Secret123",
        "nombres": "Test",
        "apellidos": "User",
        "edad": 25,
        "email": "user_test@example.com",
        "id_rol": 2
    }
    r = client.post("/usuarios/", json=payload, headers=headers)
    assert r.status_code == 201
    user = r.json()
    user_id = user["id_usuario"]

    # Listar usuarios
    r = client.get("/usuarios/", headers=headers)
    assert r.status_code == 200
    assert any(u["id_usuario"] == user_id for u in r.json())

    # Obtener usuario
    r = client.get(f"/usuarios/{user_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == payload["email"]

    # Actualizar usuario
    r = client.put(f"/usuarios/{user_id}",
                   json={"nombres": "Updated"},
                   headers=headers)
    assert r.status_code == 200
    assert r.json()["nombres"] == "Updated"

    # Eliminar usuario
    r = client.delete(f"/usuarios/{user_id}", headers=headers)
    assert r.status_code == 200
    assert "eliminado" in r.json()["message"].lower()
