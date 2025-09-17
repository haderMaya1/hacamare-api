import uuid

def test_create_comentario(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "commenter" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Com",
        "apellidos": "Ment",
        "edad": 22,
        "email": f"comment_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicación
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Post para comentar",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear comentario
    resp = client.post("/comentarios/", json={
        "contenido": "Este es un comentario",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["contenido"] == "Este es un comentario"
    assert data["id_publicacion"] == publicacion_id
    assert data["id_usuario"] == usuario_id


def test_get_comentarios(client):
    resp = client.get("/comentarios/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_comentario(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "commenter2" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Com2",
        "apellidos": "Ment2",
        "edad": 23,
        "email": f"comment2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicación
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Otro post",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear comentario
    com_resp = client.post("/comentarios/", json={
        "contenido": "Respuesta a post",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = com_resp.json()["id_comentario"]

    resp = client.get(f"/comentarios/{comentario_id}")
    assert resp.status_code == 200
    assert resp.json()["id_comentario"] == comentario_id


def test_delete_comentario(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "commentdel" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Coment",
        "edad": 24,
        "email": f"commentdel_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicación
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Post a borrar comentario",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear comentario
    com_resp = client.post("/comentarios/", json={
        "contenido": "Comentario a eliminar",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = com_resp.json()["id_comentario"]

    # eliminar comentario
    delete_resp = client.delete(f"/comentarios/{comentario_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "Comentario eliminado correctamente"

    # intentar eliminar otra vez
    delete_resp2 = client.delete(f"/comentarios/{comentario_id}")
    assert delete_resp2.status_code == 404
