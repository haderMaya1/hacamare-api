def test_crud_interes(client):
    # Registrar usuario para autenticación
    response = client.post("/auth/register", json={
        "nombre_usuario": "interesuser",
        "contraseña": "123456",
        "nombres": "Interes",
        "apellidos": "Tester",
        "edad": 28,
        "email": "interes@example.com",
        "id_rol": 1
    })
    assert response.status_code in (200, 201)

    # Login
    response = client.post("/auth/login", data={
        "username": "interesuser",
        "password": "123456"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear interés
    response = client.post("/intereses/", json={
        "nombre": "Música",
        "categoria": "Arte"
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Música"
    interes_id = data["id_interes"]

    # Listar intereses
    response = client.get("/intereses/", headers=headers)
    assert response.status_code == 200
    assert any(i["id_interes"] == interes_id for i in response.json())

    # Obtener interés
    response = client.get(f"/intereses/{interes_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id_interes"] == interes_id

    # Actualizar interés
    response = client.put(f"/intereses/{interes_id}", json={"categoria": "Cultura"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["categoria"] == "Cultura"

    # Eliminar interés
    response = client.delete(f"/intereses/{interes_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Interés eliminado correctamente"
