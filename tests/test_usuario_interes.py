from app.models.usuario import Usuario
from app.models.interes import Interes
from app.models.usuario_interes import UsuarioInteres
import pytest

def test_create_usuario_interes(client, db_session):
    db_session.query(UsuarioInteres).delete()
    db_session.query(Usuario).delete()
    db_session.query(Interes).delete()
    db_session.commit()
    
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "testuser",
        "contraseña": "1234",
        "nombres": "Test",
        "apellidos": "User",
        "edad": 20,
        "email": "testuser@example.com",
        "id_rol": 1
    })
    assert usuario.status_code == 200
    usuario_data = usuario.json()["data"]

    interes = client.post("/intereses/", json={
        "nombre": "Deportes",
        "categoria": "Salud"
    })
    assert interes.status_code == 200
    interes_data = interes.json()["data"]

    response = client.post("/usuario-interes/", json={
        "id_usuario": usuario_data["id_usuario"],
        "id_interes": interes_data["id_interes"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Relación usuario-interés creada exitosamente"
    assert data["data"]["id_usuario"] == usuario_data["id_usuario"]
    assert data["data"]["id_interes"] == interes_data["id_interes"]


def test_get_usuario_intereses(client):
    response = client.get("/usuario-interes/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_usuario_interes(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "testrel",
        "nombres": "Test",
        "contraseña": "1234",
        "apellidos": "Rel",
        "edad": 25,
        "email": "testrel@example.com",
        "id_rol": 1
    })
    assert usuario.status_code == 200
    usuario_data = usuario.json()["data"]

    interes = client.post("/intereses/", json={
        "nombre": "Música",
        "categoria": "Arte"
    })
    assert interes.status_code == 200
    interes_data = interes.json()["data"]

    client.post("/usuario-interes/", json={
        "id_usuario": usuario_data["id_usuario"],
        "id_interes": interes_data["id_interes"]
    })

    response = client.get(f"/usuario-interes/{usuario_data['id_usuario']}/{interes_data['id_interes']}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id_usuario"] == usuario_data["id_usuario"]
    assert data["data"]["id_interes"] == interes_data["id_interes"]


def test_delete_usuario_interes(client):
    usuario = client.post("/usuarios/", json={
        "nombre_usuario": "deleteuser",
        "contraseña": "1234",
        "nombres": "Delete",
        "apellidos": "User",
        "edad": 30,
        "email": "deleteuser@example.com",
        "id_rol": 1
    })
    assert usuario.status_code == 200
    usuario_data = usuario.json()["data"]

    interes = client.post("/intereses/", json={
        "nombre": "Lectura",
        "categoria": "Cultura"
    })
    assert interes.status_code == 200
    interes_data = interes.json()["data"]

    client.post("/usuario-interes/", json={
        "id_usuario": usuario_data["id_usuario"],
        "id_interes": interes_data["id_interes"]
    })

    response = client.delete(f"/usuario-interes/{usuario_data['id_usuario']}/{interes_data['id_interes']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Relación usuario-interés eliminada correctamente"

    response = client.get(f"/usuario-interes/{usuario_data['id_usuario']}/{interes_data['id_interes']}")
    assert response.status_code == 404
