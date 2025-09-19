def test_crud_sesion_chat(client):
    # Registrar usuario y loguear
    client.post("/auth/register", json={
        "nombre_usuario": "host",
        "contraseña": "123456",
        "nombres": "Host",
        "apellidos": "User",
        "edad": 30,
        "email": "host@example.com",
        "id_rol": 1
    })
    login = client.post("/auth/login", data={"username": "host", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear sesión
    response = client.post("/sesiones/", json={
        "nombre_tema": "Chat de prueba",
        "tipo": "público",
        "estado": "activa"  
    }, headers=headers)
    assert response.status_code == 201
    sesion_id = response.json()["id_sesion"]

    # Obtener sesión
    response = client.get(f"/sesiones/{sesion_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["nombre_tema"] == "Chat de prueba"

    # Listar sesiones
    response = client.get("/sesiones/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # Actualizar sesión
    response = client.put(f"/sesiones/{sesion_id}", json={
        "nombre_tema": "Prueba Actualizada",
        "tipo": "privado",
        "estado": "activa"
    }, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_tema"] == "Prueba Actualizada"
    assert data["tipo"] == "privado"

    # Eliminar sesión
    response = client.delete(f"/sesiones/{sesion_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión eliminada"
