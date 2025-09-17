from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_interes(client):
    response = client.post("/intereses/", json={"nombre": "Deportes", "categoria": "Ocio"})
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Deportes"
    assert "id_interes" in data

def test_get_intereses(client):
    response = client.get("/intereses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_interes(client):
    response = client.get("/intereses/1")
    assert response.status_code in [200, 404]

def test_update_interes(client):
    response = client.put("/intereses/1", json={"categoria": "Entretenimiento"})
    assert response.status_code in [200, 404]

def test_delete_interes(client):
    response = client.delete("/intereses/1")
    assert response.status_code in [200, 404]
