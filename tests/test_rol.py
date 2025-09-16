import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def test_rol():
    rol_data = {"nombre": "admin", "permisos": {"usuarios": "all"}}
    response = client.post("/roles/", json=rol_data)
    assert response.status_code == 200
    return response.json()

def test_create_rol():
    rol_data = {"nombre": "editor", "permisos": {"posts": "edit"}}
    response = client.post("/roles/", json=rol_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "editor"
    assert "id_rol" in data

def test_get_roles():
    response = client.get("/roles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_rol(test_rol):
    rol_id = test_rol["id_rol"]
    response = client.get(f"/roles/{rol_id}")
    assert response.status_code == 200
    assert response.json()["id_rol"] == rol_id

def test_update_rol(test_rol):
    rol_id = test_rol["id_rol"]
    update_data = {"nombre": "admin_modificado"}
    response = client.put(f"/roles/{rol_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == "admin_modificado"

def test_delete_rol(test_rol):
    rol_id = test_rol["id_rol"]
    response = client.delete(f"/roles/{rol_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Rol eliminado correctamente"
