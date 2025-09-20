def test_crud_mensaje(client):
    # Registrar usuario
    client.post("/auth/register", json={
        "nombre_usuario": "msguser",
        "contraseña": "123456",
        "nombres": "Msg",
        "apellidos": "User",
        "edad": 25,
        "email": "msguser@example.com",
        "id_rol": 1
    })
    login = client.post("/auth/login", data={"username": "msguser", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear sesión de chat
    sesion = client.post("/sesiones/", json={"nombre_tema": "Chat Mensajes", "tipo": "público"}, headers=headers)
    sesion_id = sesion.json()["id_sesion"]

    # Crear mensaje
    response = client.post("/mensajes/", json={"contenido": "Hola mundo", "id_sesion": sesion_id}, headers=headers)
    assert response.status_code == 201
    mensaje_id = response.json()["id_mensaje"]

    # Obtener mensaje
    response = client.get(f"/mensajes/{mensaje_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["contenido"] == "Hola mundo"

    # Listar mensajes de la sesión
    response = client.get(f"/mensajes/sesion/{sesion_id}", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Actualizar mensaje
    response = client.put(f"/mensajes/{mensaje_id}", json={"contenido": "Mensaje editado"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["contenido"] == "Mensaje editado"

    # Eliminar mensaje
    response = client.delete(f"/mensajes/{mensaje_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Mensaje eliminado"
