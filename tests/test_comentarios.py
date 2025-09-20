def test_crud_comentario(client):
    # Crear usuario y login
    client.post("/auth/register", json={
        "nombre_usuario": "comuser",
        "contraseña": "123456",
        "nombres": "Com",
        "apellidos": "User",
        "edad": 25,
        "email": "comuser@example.com",
        "id_rol": 1
    })
    login = client.post("/auth/login", data={"username": "comuser", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear publicación primero (necesaria para el comentario)
    pub = client.post("/publicaciones/", json={
        "texto": "Publicación para comentario"
    }, headers=headers)
    id_publicacion = pub.json()["id_publicacion"]

    # Crear comentario
    resp = client.post("/comentarios/", json={
        "contenido": "Primer comentario",
        "id_publicacion": id_publicacion
    }, headers=headers)
    assert resp.status_code == 201
    comentario_id = resp.json()["id_comentario"]

    # Obtener comentario
    resp = client.get(f"/comentarios/{comentario_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["contenido"] == "Primer comentario"

    # Listar comentarios de la publicación
    resp = client.get(f"/comentarios/publicacion/{id_publicacion}", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # Actualizar comentario
    resp = client.put(f"/comentarios/{comentario_id}", json={"contenido": "Editado"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["contenido"] == "Editado"

    # Eliminar comentario
    resp = client.delete(f"/comentarios/{comentario_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Comentario eliminado"
