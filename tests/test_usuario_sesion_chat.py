# tests/test_usuario_sesion_chat.py
def test_usuario_sesion_chat_crud(client, db_session, user_token):
    # Crear sesión de chat como admin o user antes (suponiendo que ya hay una)
    sesion_payload = {
        "nombre_tema": "Prueba Chat",
        "tipo": "privado"
    }
    r = client.post("/sesiones-chat/", json=sesion_payload,
                    headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 201
    id_sesion = r.json()["id_sesion"]

    # Unirse a la sesión
    join_payload = {"id_usuario": 0, "id_sesion": id_sesion}  # id_usuario se ignora
    r = client.post("/usuario-sesion-chat/", json=join_payload,
                    headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 201
    data = r.json()
    assert data["id_sesion"] == id_sesion

    # Listar participantes
    r = client.get(f"/usuario-sesion-chat/participants/{id_sesion}",
                   headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    participantes = r.json()
    assert any(p["id_sesion"] == id_sesion for p in participantes)

    # Salir de la sesión
    r = client.request("DELETE", "/usuario-sesion-chat/",
                       json=join_payload,
                       headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert "Usuario removido" in r.json()["message"]
