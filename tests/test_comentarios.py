import uuid

def test_create_comentario(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "commentuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Comment",
        "apellidos": "User",
        "edad": 20,
        "email": f"comment_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Publicación con comentario",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    resp = client.post("/comentarios/", json={
        "contenido": "Este es un comentario",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"]["contenido"] == "Este es un comentario"

def test_get_comentarios(client):
    resp = client.get("/comentarios/")
    assert resp.status_code == 200
    assert "data" in resp.json()

def test_get_comentario(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "getcomment" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "Comment",
        "edad": 22,
        "email": f"getcomment_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Publicación con comentario único",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    comentario = client.post("/comentarios/", json={
        "contenido": "Comentario único",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = comentario.json()["data"]["id_comentario"]

    resp = client.get(f"/comentarios/{comentario_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id_comentario"] == comentario_id

def test_respuestas_comentario(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "respuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Resp",
        "apellidos": "User",
        "edad": 24,
        "email": f"resp_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Publicación con respuestas",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    comentario = client.post("/comentarios/", json={
        "contenido": "Comentario principal",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = comentario.json()["data"]["id_comentario"]

    respuesta = client.post("/comentarios/", json={
        "contenido": "Respuesta al comentario",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id,
        "id_comentario_padre": comentario_id
    })
    assert respuesta.status_code == 200

    resp = client.get(f"/comentarios/{comentario_id}/respuestas")
    assert resp.status_code == 200
    assert any(r["id_comentario_padre"] == comentario_id for r in resp.json()["data"])

def test_update_comentario(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "upcomment" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Up",
        "apellidos": "Comment",
        "edad": 23,
        "email": f"upcomment_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Post con comentario a editar",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    comentario = client.post("/comentarios/", json={
        "contenido": "Comentario editable",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = comentario.json()["data"]["id_comentario"]

    resp = client.put(f"/comentarios/{comentario_id}", json={"contenido": "Comentario editado"})
    assert resp.status_code == 200
    assert resp.json()["data"]["contenido"] == "Comentario editado"

def test_delete_comentario(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "delcomment" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Comment",
        "edad": 25,
        "email": f"delcomment_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Post para borrar comentario",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    comentario = client.post("/comentarios/", json={
        "contenido": "Comentario a borrar",
        "id_publicacion": publicacion_id,
        "id_usuario": usuario_id
    })
    comentario_id = comentario.json()["data"]["id_comentario"]

    resp = client.delete(f"/comentarios/{comentario_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Comentario eliminado correctamente"

    resp_not_found = client.delete(f"/comentarios/{comentario_id}")
    assert resp_not_found.status_code == 404
