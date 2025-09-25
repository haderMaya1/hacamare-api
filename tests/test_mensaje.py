def test_mensaje_crud(client, db_session, user_token):
    # Crear sesión de chat
    sesion_payload = {"nombre_tema": "Sesión de prueba", "tipo": "público"}
    r = client.post("/sesiones-chat/", json=sesion_payload,
                    headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 201
    id_sesion = r.json()["id_sesion"]

    # Crear mensaje
    mensaje_payload = {"contenido": "Hola mundo!", "id_sesion": id_sesion}
    r = client.post("/mensajes/", json=mensaje_payload,
                    headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 201
    mensaje_id = r.json()["id_mensaje"]

    # Obtener mensaje  🔑
    r = client.get(f"/mensajes/{mensaje_id}",
                   headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert r.json()["contenido"] == "Hola mundo!"

    # Listar mensajes de la sesión 🔑
    r = client.get(f"/mensajes/sesion/{id_sesion}",
                   headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert any(m["id_mensaje"] == mensaje_id for m in r.json())

    # Actualizar mensaje 🔑
    update_payload = {"contenido": "Mensaje editado"}
    r = client.put(f"/mensajes/{mensaje_id}",
                   json=update_payload,
                   headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert r.json()["contenido"] == "Mensaje editado"

    # Eliminar mensaje 🔑
    r = client.delete(f"/mensajes/{mensaje_id}",
                      headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert "eliminado" in r.json()["message"]
