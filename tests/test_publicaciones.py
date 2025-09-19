def test_crud_publicacion(client):
    token = get_token(client)

    # Crear publicación
    response = client.post("/publicaciones/", json={"texto": "Mi primera publicación"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    publicacion = response.json()
    assert publicacion["texto"] == "Mi primera publicación"

    publicacion_id = publicacion["id_publicacion"]

    # Obtener publicación
    response = client.get(f"/publicaciones/{publicacion_id}")
    assert response.status_code == 200
    assert response.json()["texto"] == "Mi primera publicación"

    # Actualizar publicación
    response = client.put(f"/publicaciones/{publicacion_id}", json={"texto": "Publicación editada"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["texto"] == "Publicación editada"

    # Eliminar publicación
    response = client.delete(f"/publicaciones/{publicacion_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "eliminada" in response.json()["message"].lower()


def get_token(client):
    """Helper para obtener un token válido"""
    client.post("/auth/register", json={
        "nombre_usuario": "pubuser",
        "contraseña": "123456",
        "nombres": "Pub",
        "apellidos": "User",
        "edad": 20,
        "email": "pubuser@example.com",
        "id_rol": 1
    })
    response = client.post("/auth/login", data={"username": "pubuser", "password": "123456"})
    return response.json()["access_token"]
