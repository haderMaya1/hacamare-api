def test_crud_solicitud_amistad(client):
    # Registrar usuarios
    client.post("/auth/register", json={
        "nombre_usuario": "user1",
        "contraseña": "123456",
        "nombres": "User",
        "apellidos": "One",
        "edad": 25,
        "email": "user1@example.com",
        "id_rol": 1
    })
    client.post("/auth/register", json={
        "nombre_usuario": "user2",
        "contraseña": "123456",
        "nombres": "User",
        "apellidos": "Two",
        "edad": 26,
        "email": "user2@example.com",
        "id_rol": 1
    })

    # Login user1
    login1 = client.post("/auth/login", data={"username": "user1", "password": "123456"})
    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Login user2
    login2 = client.post("/auth/login", data={"username": "user2", "password": "123456"})
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Crear solicitud
    r = client.post("/solicitudes/", json={"destinatario_id": 2, "mensaje": "¡Hola!"}, headers=headers1)
    assert r.status_code == 201
    solicitud_id = r.json()["id_solicitud"]

    # Listar solicitudes
    r = client.get("/solicitudes/", headers=headers1)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # Aceptar solicitud (user2)
    r = client.put(f"/solicitudes/{solicitud_id}", json={"estado": "aceptada"}, headers=headers2)
    assert r.status_code == 200
    assert r.json()["estado"] == "aceptada"

    # Eliminar solicitud (user1)
    r = client.delete(f"/solicitudes/{solicitud_id}", headers=headers1)
    assert r.status_code == 200
    assert r.json()["message"] == "Solicitud eliminada"
