import uuid

def test_create_reaccion(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "reactuser" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "React",
        "apellidos": "User",
        "edad": 25,
        "email": f"react_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicacion
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Mi primera publicación",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear reacción
    resp = client.post("/reacciones/", json={
        "tipo": "like",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })

    assert resp.status_code == 200
    data = resp.json()
    assert data["tipo"] == "like"
    assert data["id_usuario"] == usuario_id
    assert data["id_publicacion"] == publicacion_id


def test_get_reacciones(client):
    resp = client.get("/reacciones/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_reaccion(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "reactuser2" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "React2",
        "apellidos": "User2",
        "edad": 28,
        "email": f"react2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicacion
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Otra publicación",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear reacción
    reaccion_resp = client.post("/reacciones/", json={
        "tipo": "me_encanta",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    reaccion_id = reaccion_resp.json()["id_reaccion"]

    # obtener reacción por ID
    resp = client.get(f"/reacciones/{reaccion_id}")
    assert resp.status_code == 200
    assert resp.json()["id_reaccion"] == reaccion_id


def test_delete_reaccion(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "reactdel" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "ReactDel",
        "apellidos": "User",
        "edad": 26,
        "email": f"reactdel_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # crear publicacion
    pub_resp = client.post("/publicaciones/", json={
        "texto": "Publicación a reaccionar",
        "id_usuario": usuario_id
    })
    publicacion_id = pub_resp.json()["id_publicacion"]

    # crear reacción
    reaccion_resp = client.post("/reacciones/", json={
        "tipo": "me_divierte",
        "id_usuario": usuario_id,
        "id_publicacion": publicacion_id
    })
    reaccion_id = reaccion_resp.json()["id_reaccion"]

    # eliminar reacción
    delete_resp = client.delete(f"/reacciones/{reaccion_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "Reacción eliminada correctamente"

    # intentar eliminar otra vez → debe dar 404
    delete_resp2 = client.delete(f"/reacciones/{reaccion_id}")
    assert delete_resp2.status_code == 404
