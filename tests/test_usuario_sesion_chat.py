def test_usuario_sesion_chat(client):
    # Registrar usuario anfitrión
    client.post("/auth/register", json={
        "nombre_usuario": "host",
        "contraseña": "123456",
        "nombres": "Host",
        "apellidos": "User",
        "edad": 30,
        "email": "host@example.com",
        "id_rol": 1
    })
    login_host = client.post("/auth/login", data={"username": "host", "password": "123456"})
    token_host = login_host.json()["access_token"]
    headers_host = {"Authorization": f"Bearer {token_host}"}

    # Crear sesión de chat
    sesion = client.post("/sesiones/", json={"nombre_tema": "Chat Test", "tipo": "público"}, headers=headers_host)
    sesion_id = sesion.json()["id_sesion"]

    # Registrar otro usuario
    client.post("/auth/register", json={
        "nombre_usuario": "guest",
        "contraseña": "123456",
        "nombres": "Guest",
        "apellidos": "User",
        "edad": 25,
        "email": "guest@example.com",
        "id_rol": 1
    })
    login_guest = client.post("/auth/login", data={"username": "guest", "password": "123456"})
    token_guest = login_guest.json()["access_token"]
    headers_guest = {"Authorization": f"Bearer {token_guest}"}

    # Agregar guest a la sesión
    response = client.post("/usuario-sesion/", json={
        "id_usuario": 2,   # host = 1, guest = 2
        "id_sesion": sesion_id
    }, headers=headers_host)
    assert response.status_code == 201
    assert response.json()["id_usuario"] == 2
    assert response.json()["id_sesion"] == sesion_id

    # Eliminar guest de la sesión
    response = client.delete(f"/usuario-sesion/?id_usuario=2&id_sesion={sesion_id}", headers=headers_host)
    assert response.status_code == 200
    assert response.json()["message"] == "Usuario eliminado de la sesión"
