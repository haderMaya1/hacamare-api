def test_crud_reaccion_publicacion(client):
    # Registrar usuario
    client.post("/auth/register", json={
        "nombre_usuario": "reactuser",
        "contraseña": "123456",
        "nombres": "React",
        "apellidos": "User",
        "edad": 25,
        "email": "reactuser@example.com",
        "id_rol": 1
    })
    login = client.post("/auth/login", data={"username": "reactuser", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear una publicación
    pub = client.post("/publicaciones/", json={"texto": "Publicación para reaccionar"}, headers=headers)
    assert pub.status_code == 201
    pub_id = pub.json()["id_publicacion"]

    # Crear reacción
    resp = client.post("/reacciones/", json={"tipo": "like", "id_publicacion": pub_id}, headers=headers)
    assert resp.status_code == 201
    reaccion_id = resp.json()["id_reaccion"]

    # Listar reacciones de la publicación
    resp = client.get(f"/reacciones/publicacion/{pub_id}", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Actualizar reacción
    resp = client.put(f"/reacciones/{reaccion_id}", json={"tipo": "me_encanta"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["tipo"] == "me_encanta"

    # Eliminar reacción
    resp = client.delete(f"/reacciones/{reaccion_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Reacción eliminada"
