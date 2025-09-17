import uuid

def test_create_contacto(client):
    # Crear dos usuarios
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "cuser1_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User1",
        "apellidos": "Test",
        "edad": 20,
        "email": f"cuser1_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "cuser2_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User2",
        "apellidos": "Test",
        "edad": 21,
        "email": f"cuser2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    resp = client.post("/contactos/", json={"usuario_id_1": u1, "usuario_id_2": u2})
    assert resp.status_code == 200
    assert resp.json()["data"]["usuario_id_1"] == u1
    assert resp.json()["data"]["usuario_id_2"] == u2

def test_get_contactos(client):
    resp = client.get("/contactos/")
    assert resp.status_code == 200
    assert "data" in resp.json()

def test_get_contacto(client):
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "cget1_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User1",
        "apellidos": "Get",
        "edad": 22,
        "email": f"cget1_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "cget2_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User2",
        "apellidos": "Get",
        "edad": 23,
        "email": f"cget2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    contacto = client.post("/contactos/", json={"usuario_id_1": u1, "usuario_id_2": u2}).json()["data"]

    resp = client.get(f"/contactos/{contacto['id_contacto']}")
    assert resp.status_code == 200
    assert resp.json()["data"]["id_contacto"] == contacto["id_contacto"]

def test_get_contactos_usuario(client):
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "cusu1_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User1",
        "apellidos": "U",
        "edad": 24,
        "email": f"cusu1_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "cusu2_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User2",
        "apellidos": "U",
        "edad": 25,
        "email": f"cusu2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    client.post("/contactos/", json={"usuario_id_1": u1, "usuario_id_2": u2})

    resp = client.get(f"/contactos/usuario/{u1}")
    assert resp.status_code == 200
    assert any(c["usuario_id_1"] == u1 or c["usuario_id_2"] == u1 for c in resp.json()["data"])

def test_delete_contacto(client):
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "cdel1_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User1",
        "apellidos": "Del",
        "edad": 26,
        "email": f"cdel1_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "cdel2_" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "User2",
        "apellidos": "Del",
        "edad": 27,
        "email": f"cdel2_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()["data"]["id_usuario"]

    contacto = client.post("/contactos/", json={"usuario_id_1": u1, "usuario_id_2": u2}).json()["data"]["id_contacto"]

    resp = client.delete(f"/contactos/{contacto}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Contacto eliminado correctamente"

    resp_not_found = client.delete(f"/contactos/{contacto}")
    assert resp_not_found.status_code == 404
