def test_create_notificacion(client):
    # Crear un usuario primero
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "notifuser",
        "contraseña": "1234",
        "nombres": "Notif",
        "apellidos": "User",
        "edad": 25,
        "email": "notif@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    resp = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Has incumplido una norma",
        "id_usuario": usuario_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["tipo"] == "advertencia"
    assert data["estado"] == "activa"

def test_get_notificaciones(client):
    resp = client.get("/notificaciones/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_update_notificacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "updnotif",
        "contraseña": "1234",
        "nombres": "Update",
        "apellidos": "Notif",
        "edad": 26,
        "email": "updnotif@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    notif_resp = client.post("/notificaciones/", json={
        "tipo": "eliminacion",
        "contenido": "Publicación eliminada por infringir reglas",
        "id_usuario": usuario_id
    })
    notif_id = notif_resp.json()["id_notificacion"]

    resp = client.put(f"/notificaciones/{notif_id}", json={"estado": "resuelta"})
    assert resp.status_code == 200
    assert resp.json()["estado"] == "resuelta"

def test_delete_notificacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "delnotif",
        "contraseña": "1234",
        "nombres": "Delete",
        "apellidos": "Notif",
        "edad": 28,
        "email": "delnotif@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    notif_resp = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Comentario inapropiado",
        "id_usuario": usuario_id
    })
    notif_id = notif_resp.json()["id_notificacion"]

    resp = client.delete(f"/notificaciones/{notif_id}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Notificación eliminada correctamente"
