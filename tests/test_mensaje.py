import uuid

def test_create_mensaje(client):
    # Crear usuario
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "msguser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Msg",
        "apellidos": "User",
        "edad": 22,
        "email": f"msg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    # Crear sesión
    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Chat Test",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    # Crear mensaje
    resp = client.post("/mensajes/", json={
        "contenido": "Hola mundo",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Mensaje enviado exitosamente"
    assert data["data"]["contenido"] == "Hola mundo"
    assert data["data"]["id_remitente"] == usuario_id

def test_get_mensajes(client):
    resp = client.get("/mensajes/")
    assert resp.status_code == 200
    assert "data" in resp.json()

def test_get_mensaje(client):
    # Crear usuario + sesión + mensaje
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "getmsg" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "Msg",
        "edad": 23,
        "email": f"getmsg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Chat Get",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    mensaje = client.post("/mensajes/", json={
        "contenido": "Mensaje único",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    mensaje_id = mensaje.json()["data"]["id_mensaje"]

    resp = client.get(f"/mensajes/{mensaje_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id_mensaje"] == mensaje_id

def test_update_mensaje(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "upmsg" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Up",
        "apellidos": "Msg",
        "edad": 24,
        "email": f"upmsg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Chat Update",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    mensaje = client.post("/mensajes/", json={
        "contenido": "Texto viejo",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    mensaje_id = mensaje.json()["data"]["id_mensaje"]

    resp = client.put(f"/mensajes/{mensaje_id}", json={"contenido": "Texto nuevo"})
    assert resp.status_code == 200
    assert resp.json()["data"]["contenido"] == "Texto nuevo"

def test_delete_mensaje(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "delmsg" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Msg",
        "edad": 25,
        "email": f"delmsg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    sesion = client.post("/sesiones_chat/", json={
        "nombre_tema": "Chat Delete",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion.json()["data"]["id_sesion"]

    mensaje = client.post("/mensajes/", json={
        "contenido": "Borrar este mensaje",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    mensaje_id = mensaje.json()["data"]["id_mensaje"]

    resp = client.delete(f"/mensajes/{mensaje_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Mensaje eliminado correctamente"

    resp_not_found = client.delete(f"/mensajes/{mensaje_id}")
    assert resp_not_found.status_code == 404
