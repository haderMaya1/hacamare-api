import uuid

def test_create_notificacion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "notifuser" + uuid.uuid4().hex[:6],
        "contraseña": "1234",
        "nombres": "Notif",
        "apellidos": "User",
        "edad": 25,
        "email": f"notif_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    response = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Tu publicación fue marcada",
        "id_usuario": usuario_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "advertencia"
    assert data["estado"] == "activa"

def test_get_notificaciones(client):
    response = client.get("/notificaciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_notificacion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "notifget" + uuid.uuid4().hex[:6],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "Notif",
        "edad": 28,
        "email": f"notifget_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    resp = client.post("/notificaciones/", json={
        "tipo": "eliminacion",
        "contenido": "Tu comentario fue eliminado",
        "id_usuario": usuario_id
    })
    notif_id = resp.json()["id_notificacion"]

    response = client.get(f"/notificaciones/{notif_id}")
    assert response.status_code == 200
    assert response.json()["id_notificacion"] == notif_id

def test_update_notificacion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "notifupd" + uuid.uuid4().hex[:6],
        "contraseña": "1234",
        "nombres": "Upd",
        "apellidos": "Notif",
        "edad": 30,
        "email": f"notifupd_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    resp = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Revisa tus publicaciones",
        "id_usuario": usuario_id
    })
    notif_id = resp.json()["id_notificacion"]

    response = client.put(f"/notificaciones/{notif_id}", json={"estado": "resuelta"})
    assert response.status_code == 200
    assert response.json()["estado"] == "resuelta"

def test_delete_notificacion(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "notifdel" + uuid.uuid4().hex[:6],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Notif",
        "edad": 22,
        "email": f"notifdel_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = usuario.json()["data"]["id_usuario"]

    resp = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Tu sesión fue reportada",
        "id_usuario": usuario_id
    })
    notif_id = resp.json()["id_notificacion"]

    response = client.delete(f"/notificaciones/{notif_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Notificación eliminada correctamente"
