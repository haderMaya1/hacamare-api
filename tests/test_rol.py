import pytest

def test_create_rol(client):
    rol_data = {"nombre": "editor", "permisos": {"posts": "edit"}}
    response = client.post("/roles/", json=rol_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "editor"
    assert "id_rol" in data

def test_get_roles(client):
    response = client.get("/roles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_rol(client):
    rol_data = {"nombre": "admin", "permisos": {"usuarios": "all"}}
    created = client.post("/roles/", json=rol_data).json()
    rol_id = created["id_rol"]

    response = client.get(f"/roles/{rol_id}")
    assert response.status_code == 200
    assert response.json()["id_rol"] == rol_id

def test_update_rol(client):
    rol_data = {"nombre": "mod", "permisos": {"usuarios": "read"}}
    created = client.post("/roles/", json=rol_data).json()
    rol_id = created["id_rol"]

    update_data = {"nombre": "mod_actualizado"}
    response = client.put(f"/roles/{rol_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == "mod_actualizado"

def test_delete_rol(client):
    rol_data = {"nombre": "temp", "permisos": {"usuarios": "read"}}
    created = client.post("/roles/", json=rol_data).json()
    rol_id = created["id_rol"]

    response = client.delete(f"/roles/{rol_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Rol eliminado correctamente"
