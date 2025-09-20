def test_crud_notificacion(client):
    # Registrar usuario normal y administrador para IDs válidos
    client.post("/auth/register", json={
        "nombre_usuario": "usernotif",
        "contraseña": "123456",
        "nombres": "User",
        "apellidos": "Notif",
        "edad": 25,
        "email": "usernotif@example.com",
        "id_rol": 1
    })
    login = client.post("/auth/login", data={"username": "usernotif", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear Notificación
    r = client.post("/notificaciones/", json={
        "tipo": "advertencia",
        "contenido": "Publicación inapropiada detectada",
        "estado": "activa",
        "id_usuario": 1,
        "id_publicacion": None,
        "id_sesion": None,
        "id_administrador": 1
    }, headers=headers)
    assert r.status_code == 201
    notif_id = r.json()["id_notificacion"]

    # Listar Notificaciones
    r = client.get("/notificaciones/", headers=headers)
    assert r.status_code == 200
    assert any(n["id_notificacion"] == notif_id for n in r.json())

    # Obtener Notificación
    r = client.get(f"/notificaciones/{notif_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["tipo"] == "advertencia"

    # Actualizar Notificación
    r = client.put(f"/notificaciones/{notif_id}", json={"estado": "resuelta"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["estado"] == "resuelta"

    # Eliminar Notificación
    r = client.delete(f"/notificaciones/{notif_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Notificación eliminada correctamente"
