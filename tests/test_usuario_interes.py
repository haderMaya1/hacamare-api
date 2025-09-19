def test_usuario_interes(client):
    # Registrar usuario
    response = client.post("/auth/register", json={
        "nombre_usuario": "userinteres",
        "contraseña": "123456",
        "nombres": "User",
        "apellidos": "Interes",
        "edad": 25,
        "email": "userinteres@example.com",
        "id_rol": 1
    })
    assert response.status_code in (200, 201)
    usuario_id = response.json()["id_usuario"]

    # Login
    response = client.post("/auth/login", data={
        "username": "userinteres",
        "password": "123456"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear interés
    response = client.post("/intereses/", json={"nombre": "Deportes"}, headers=headers)
    assert response.status_code == 201
    interes_id = response.json()["id_interes"]

    # Asignar interés al usuario
    response = client.post(f"/usuarios/{usuario_id}/intereses/{interes_id}", headers=headers)
    assert response.status_code == 200
    assert any(i["id_interes"] == interes_id for i in response.json()["intereses"])

    # Quitar interés al usuario
    response = client.delete(f"/usuarios/{usuario_id}/intereses/{interes_id}", headers=headers)
    assert response.status_code == 200
    assert all(i["id_interes"] != interes_id for i in response.json()["intereses"])
