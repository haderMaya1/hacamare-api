def test_crud_roles(client):
    # Registrar usuario para autenticación
    response = client.post("/auth/register", json={
        "nombre_usuario": "adminuser",
        "contraseña": "123456",
        "nombres": "Admin",
        "apellidos": "User",
        "edad": 30,
        "email": "admin@example.com",
        "id_rol": 1
    })
    assert response.status_code in (200, 201)
    
    # Login
    response = client.post("/auth/login", data={
        "username": "adminuser",
        "password": "123456"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear rol
    response = client.post("/roles/", json={
        "nombre": "Admin",
        "permisos": {"usuarios": ["crear", "editar", "eliminar"]}
    }, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Admin"

    rol_id = data["id_rol"]

    # Listar roles
    response = client.get("/roles/", headers=headers)
    assert response.status_code == 200
    assert any(r["id_rol"] == rol_id for r in response.json())

    # Obtener rol
    response = client.get(f"/roles/{rol_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id_rol"] == rol_id

    # Actualizar rol
    response = client.put(f"/roles/{rol_id}", json={
        "nombre": "SuperAdmin",
        "permisos": {"usuarios": ["leer"]}
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["nombre"] == "SuperAdmin"

    # Eliminar rol
    response = client.delete(f"/roles/{rol_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Rol eliminado correctamente"
