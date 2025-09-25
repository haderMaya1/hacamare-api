def test_crud_sesion_chat(client, db_session, admin_token):
    # 1. Crear sesión de chat
    payload = {
        "nombre_tema": "Debate IA",
        "tipo": "público",
        "estado": "activa"
    }
    r = client.post(
        "/sesiones-chat/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201
    data = r.json()
    sesion_id = data["id_sesion"]
    assert data["nombre_tema"] == "Debate IA"
    assert data["estado"] == "activa"

    # 2. Obtener la sesión creada
    r = client.get(
        f"/sesiones-chat/{sesion_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert r.json()["id_sesion"] == sesion_id

    # 3. Listar sesiones
    r = client.get(
        "/sesiones-chat/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert any(s["id_sesion"] == sesion_id for s in r.json())

    # 4. Actualizar sesión
    update_payload = {"estado": "cerrada"}
    r = client.put(
        f"/sesiones-chat/{sesion_id}",
        json=update_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert r.json()["estado"] == "cerrada"

    # 5. Eliminar sesión
    r = client.delete(
        f"/sesiones-chat/{sesion_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    assert r.json()["message"] == "Sesión de chat eliminada correctamente"

    # 6. Confirmar que ya no existe
    r = client.get(
        f"/sesiones-chat/{sesion_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 404
