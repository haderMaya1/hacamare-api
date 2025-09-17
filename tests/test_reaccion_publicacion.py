import uuid

def test_create_reaccion(client):
    # Crear usuario
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "reactuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "React",
        "apellidos": "User",
        "edad": 20,
        "email": f"react_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    # Crear publicación
    publicacion = client.post("/publicaciones/", json={
        "texto": "Publicación para reaccionar",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    # Crear reacción
    resp = client.post("/reacciones/", json={
        "tipo": "like",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Reacción creada exitosamente"
    assert data["data"]["tipo"] == "like"

def test_get_reacciones(client):
    resp = client.get("/reacciones/")
    assert resp.status_code == 200
    assert "data" in resp.json()

def test_get_reaccion(client):
    # Crear usuario + publicación + reacción
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "getreact" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "React",
        "edad": 22,
        "email": f"getreact_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Post con reacción única",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    reaccion = client.post("/reacciones/", json={
        "tipo": "me_encanta",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    reaccion_id = reaccion.json()["data"]["id_reaccion"]

    resp = client.get(f"/reacciones/{reaccion_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id_reaccion"] == reaccion_id

def test_update_reaccion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "upreact" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Up",
        "apellidos": "React",
        "edad": 23,
        "email": f"upreact_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Post para actualizar reacción",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    reaccion = client.post("/reacciones/", json={
        "tipo": "dislike",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    reaccion_id = reaccion.json()["data"]["id_reaccion"]

    resp = client.put(f"/reacciones/{reaccion_id}", json={"tipo": "me_asombra"})
    assert resp.status_code == 200
    assert resp.json()["data"]["tipo"] == "me_asombra"

def test_delete_reaccion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "delreact" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "React",
        "edad": 25,
        "email": f"delreact_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    publicacion = client.post("/publicaciones/", json={
        "texto": "Post para borrar reacción",
        "id_usuario": usuario_id
    })
    publicacion_id = publicacion.json()["data"]["id_publicacion"]

    reaccion = client.post("/reacciones/", json={
        "tipo": "me_enoja",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    reaccion_id = reaccion.json()["data"]["id_reaccion"]

    resp = client.delete(f"/reacciones/{reaccion_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Reacción eliminada correctamente"

    resp_not_found = client.delete(f"/reacciones/{reaccion_id}")
    assert resp_not_found.status_code == 404
