def test_crud_usuario(client):
    # Crear usuario
    response = client.post("/usuarios/", json={
        "nombre_usuario": "newuser",
        "contraseña": "123456",
        "nombres": "Nuevo",
        "apellidos": "Usuario",
        "edad": 22,
        "email": "nuevo@example.com",
        "id_rol": 1
    }, headers={"Authorization": f"Bearer {get_token(client)}"})
    assert response.status_code == 201
    usuario = response.json()
    assert usuario["nombre_usuario"] == "newuser"

    usuario_id = usuario["id_usuario"]

    # Obtener usuario
    response = client.get(f"/usuarios/{usuario_id}", headers={"Authorization": f"Bearer {get_token(client)}"})
    assert response.status_code == 200
    assert response.json()["email"] == "nuevo@example.com"

    # Actualizar usuario
    response = client.put(f"/usuarios/{usuario_id}", json={"edad": 30}, headers={"Authorization": f"Bearer {get_token(client)}"})
    assert response.status_code == 200
    assert response.json()["edad"] == 30

    # Eliminar usuario
    response = client.delete(f"/usuarios/{usuario_id}", headers={"Authorization": f"Bearer {get_token(client)}"})
    assert response.status_code == 200
    assert "eliminado" in response.json()["message"].lower()


def get_token(client):
    """Helper para obtener token válido usando auth/login"""
    client.post("/auth/register", json={
        "nombre_usuario": "authuser",
        "contraseña": "123456",
        "nombres": "Auth",
        "apellidos": "User",
        "edad": 20,
        "email": "auth@example.com",
        "id_rol": 1
    })
    response = client.post("/auth/login", data={"username": "authuser", "password": "123456"})
    return response.json()["access_token"]
