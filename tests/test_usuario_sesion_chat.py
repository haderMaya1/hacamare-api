import uuid

def test_create_usuario_sesion_chat(client):
    # Crear usuario
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "userusc" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User",
        "apellidos": "Sesion",
        "edad": 26,
        "email": f"userusc_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    # Crear sesión
    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Charla Test",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    # Crear relación
    resp = client.post("/usuario-sesion-chat/", json={
        "id_usuario": usuario_id,
        "id_sesion": sesion_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Relación usuario-sesión creada exitosamente"
    assert data["data"]["id_usuario"] == usuario_id
    assert data["data"]["id_sesion"] == sesion_id

    # Intentar duplicado
    resp_dup = client.post("/usuario-sesion-chat/", json={
        "id_usuario": usuario_id,
        "id_sesion": sesion_id
    })
    assert resp_dup.status_code == 400
    assert resp_dup.json()["detail"] == "Relación ya existe"

def test_get_relaciones_usuario_sesion(client):
    resp = client.get("/usuario-sesion-chat/")
    assert resp.status_code == 200
    assert "data" in resp.json()

def test_get_relacion_usuario_sesion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "getusc" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "Rel",
        "edad": 27,
        "email": f"getusc_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Charla Get",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    client.post("/usuario-sesion-chat/", json={"id_usuario": usuario_id, "id_sesion": sesion_id})

    resp = client.get(f"/usuario-sesion-chat/{usuario_id}/{sesion_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"]["id_usuario"] == usuario_id
    assert data["data"]["id_sesion"] == sesion_id

def test_delete_usuario_sesion_chat(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "delusc" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Rel",
        "edad": 28,
        "email": f"delusc_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Charla Delete",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    client.post("/usuario-sesion-chat/", json={"id_usuario": usuario_id, "id_sesion": sesion_id})

    resp = client.delete(f"/usuario-sesion-chat/{usuario_id}/{sesion_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Relación usuario-sesión eliminada correctamente"

    # Intentar borrar de nuevo
    resp_not_found = client.delete(f"/usuario-sesion-chat/{usuario_id}/{sesion_id}")
    assert resp_not_found.status_code == 404
