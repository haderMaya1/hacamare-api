import uuid
from app.models.usuario import Usuario
from app.models.interes import Interes
from app.models.usuario_interes import UsuarioInteres

def test_create_usuario_interes(client, db_session):
    db_session.query(UsuarioInteres).delete()
    db_session.query(Usuario).delete()
    db_session.query(Interes).delete()
    db_session.commit()
    
    nombre_usuario = "testuser"
    email = f"usuario_{uuid.uuid4().hex[:6]}@test.com"
    
    # Crear un usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": nombre_usuario,
        "contraseña": "1234",
        "nombres": "Usuario",
        "apellidos": "Prueba",
        "edad": 20,
        "email": email,
        "id_rol": 1
    })
    assert user_resp.status_code == 200
    user_data = user_resp.json()
    usuario_id = user_data["id_usuario"]

    # Crear un interés
    interes_resp = client.post("/intereses/", json={"nombre": "Música", "categoria": "Arte"})
    assert interes_resp.status_code == 200
    interes_data = interes_resp.json()
    interes_id = interes_data["id_interes"]

    # Crear la relación
    resp = client.post("/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id_usuario"] == usuario_id
    assert data["id_interes"] == interes_id

    # Intentar crear la misma relación -> debe dar 400
    resp_dup = client.post("/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})
    assert resp_dup.status_code == 400
    assert resp_dup.json()["detail"] == "Relación ya existe"


def test_get_relaciones(client):
    resp = client.get("/usuario_interes/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_intereses_usuario(client):
    # primero crear usuario + interés + relación
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "tempuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Temp",
        "apellidos": "User",
        "edad": 25,
        "email": f"temp_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    interes_resp = client.post("/intereses/", json={"nombre": "Deporte", "categoria": "Ocio"})
    interes_id = interes_resp.json()["id_interes"]

    client.post("/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})

    # ahora consultar intereses del usuario
    resp = client.get(f"/usuario_interes/usuario/{usuario_id}")
    assert resp.status_code == 200
    intereses = resp.json()
    assert isinstance(intereses, list)
    assert any(interes["id_interes"] == interes_id for interes in intereses)


def test_delete_usuario_interes(client):
    # crear usuario + interés + relación
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "deluser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "User",
        "edad": 30,
        "email": f"del_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    interes_resp = client.post("/intereses/", json={"nombre": "Cine", "categoria": "Entretenimiento"})
    interes_id = interes_resp.json()["id_interes"]

    client.post("/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})

    # borrar la relación
    resp = client.request("DELETE", "/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Relación eliminada correctamente"

    # intentar borrar de nuevo -> debe dar 404
    resp_not_found = client.request("DELETE", "/usuario_interes/", json={"id_usuario": usuario_id, "id_interes": interes_id})
    assert resp_not_found.status_code == 404