import pytest

def test_create_interes(client):
    interes_data = {"nombre": "Deportes", "categoria": "Salud"}
    response = client.post("/intereses/", json=interes_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Interés creado exitosamente"
    assert data["data"]["nombre"] == "Deportes"

def test_get_intereses(client):
    client.post("/intereses/", json={"nombre": "Música", "categoria": "Arte"})
    response = client.get("/intereses/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert any(i["nombre"] == "Música" for i in data["data"])

def test_get_interes(client):
    response = client.post("/intereses/", json={"nombre": "Viajes", "categoria": "Ocio"})
    interes_id = response.json()["data"]["id_interes"]

    response = client.get(f"/intereses/{interes_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["nombre"] == "Viajes"

def test_update_interes(client):
    response = client.post("/intereses/", json={"nombre": "Cine", "categoria": "Ocio"})
    interes_id = response.json()["data"]["id_interes"]

    response = client.put(f"/intereses/{interes_id}", json={"categoria": "Entretenimiento"})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["categoria"] == "Entretenimiento"

def test_delete_interes(client):
    response = client.post("/intereses/", json={"nombre": "Lectura", "categoria": "Cultura"})
    interes_id = response.json()["data"]["id_interes"]

    response = client.delete(f"/intereses/{interes_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Interés eliminado correctamente"

    # verificar que realmente fue eliminado
    response = client.get(f"/intereses/{interes_id}")
    assert response.status_code == 404
