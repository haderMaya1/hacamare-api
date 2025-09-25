def test_crud_notificacion(client, admin_token, db_session):
    # 1️⃣ Crear notificación
    payload = {
        "tipo": "advertencia",
        "contenido": "Nueva política de privacidad",
        "id_usuario": 1
    }
    r = client.post(
        "/notificaciones/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    data = r.json()
    assert data["tipo"] == "advertencia"
    notif_id = data["id_notificacion"]

    # 2️⃣ Listar notificaciones
    r = client.get("/notificaciones/", headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200
    assert any(n["id_notificacion"] == notif_id for n in r.json())

    # 3️⃣ Obtener notificación
    r = client.get(f"/notificaciones/{notif_id}", headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200
    assert r.json()["contenido"] == "Nueva política de privacidad"

    # 4️⃣ Actualizar notificación
    r = client.put(
        f"/notificaciones/{notif_id}",
        json={"contenido": "Actualización de términos"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert r.json()["contenido"] == "Actualización de términos"

    # 5️⃣ Eliminar notificación
    r = client.delete(
        f"/notificaciones/{notif_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert "eliminada" in r.json()["message"].lower()
