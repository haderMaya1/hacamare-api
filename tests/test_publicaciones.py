import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_publicacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "pubuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Pub",
        "apellidos": "Tester",
        "edad": 22,
        "email": f"pub_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    response = client.post("/publicaciones/", json={
        "texto": "Mi primera publicación",
        "imagen": None,
        "id_usuario": usuario_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["texto"] == "Mi primera publicación"
    assert data["estado"] == "visible"
    assert "id_publicacion" in data

def test_get_publicaciones(client):
    response = client.get("/publicaciones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_publicacion(client):
    response = client.get("/publicaciones/1")
    assert response.status_code in [200, 404]

def test_update_publicacion(client):
    response = client.put("/publicaciones/1", json={"estado": "oculto"})
    assert response.status_code in [200, 404]

def test_delete_publicacion(client):
    response = client.delete("/publicaciones/1")
    assert response.status_code in [200, 404]
