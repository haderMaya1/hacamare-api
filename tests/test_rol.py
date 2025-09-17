import pytest

def test_create_rol(client):
    rol_data = {"nombre": "admin", "permisos": {"posts": "edit"}}
    response = client.post("/roles/", json=rol_data)
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Rol creado exitosamente"
    assert data["data"]["nombre"] == "admin"
    assert isinstance(data["data"]["permisos"], dict)
    assert data["data"]["permisos"]["posts"] == "edit"


def test_get_roles(client):
    # Crear uno para asegurar resultados
    client.post("/roles/", json={"nombre": "user", "permisos": {"read": "only"}})

    response = client.get("/roles/")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert any(r["nombre"] == "user" for r in data["data"])


def test_get_rol(client):
    # Crear rol
    response = client.post("/roles/", json={"nombre": "moderator", "permisos": {"usuarios": "all"}})
    rol_id = response.json()["data"]["id_rol"]

    # Obtener por id
    response = client.get(f"/roles/{rol_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["data"]["nombre"] == "moderator"
    assert isinstance(data["data"]["permisos"], dict)
    assert data["data"]["permisos"]["usuarios"] == "all"


def test_update_rol(client):
    # Crear rol
    response = client.post("/roles/", json={"nombre": "editor", "permisos": {"usuarios": "read"}})
    rol_id = response.json()["data"]["id_rol"]

    # Actualizar permisos
    response = client.put(f"/roles/{rol_id}", json={"permisos": {"usuarios": "write"}})
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Rol actualizado correctamente"
    assert isinstance(data["data"]["permisos"], dict)
    assert data["data"]["permisos"]["usuarios"] == "write"


def test_delete_rol(client):
    # Crear rol temporal
    response = client.post("/roles/", json={"nombre": "temp", "permisos": {"usuarios": "read"}})
    rol_id = response.json()["data"]["id_rol"]

    # Eliminar rol
    response = client.delete(f"/roles/{rol_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Rol eliminado correctamente"

    # Verificar que ya no existe
    response = client.get(f"/roles/{rol_id}")
    assert response.status_code == 404
