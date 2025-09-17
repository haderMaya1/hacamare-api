import uuid

def crear_usuario(client, prefix="user"):
    return client.post("/usuarios/", json={
        "nombre_usuario": prefix + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": prefix,
        "apellidos": "Test",
        "edad": 25,
        "email": f"{prefix}_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

def test_create_contacto(client):
    u1 = crear_usuario(client, "contacto1")
    u2 = crear_usuario(client, "contacto2")

    resp = client.post("/contactos/", json={"usuario_id_1": u1["id_usuario"], "usuario_id_2": u2["id_usuario"]})
    assert resp.status_code == 200
    data = resp.json()
    assert data["usuario_id_1"] == u1["id_usuario"]
    assert data["usuario_id_2"] == u2["id_usuario"]

def test_get_contactos(client):
    resp = client.get("/contactos/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_contactos_usuario(client):
    u1 = crear_usuario(client, "contactoU1")
    u2 = crear_usuario(client, "contactoU2")

    client.post("/contactos/", json={"usuario_id_1": u1["id_usuario"], "usuario_id_2": u2["id_usuario"]})

    resp = client.get(f"/contactos/usuario/{u1['id_usuario']}")
    assert resp.status_code == 200
    contactos = resp.json()
    assert any(c["usuario_id_1"] == u1["id_usuario"] or c["usuario_id_2"] == u1["id_usuario"] for c in contactos)

def test_delete_contacto(client):
    u1 = crear_usuario(client, "deleteC1")
    u2 = crear_usuario(client, "deleteC2")

    contacto = client.post("/contactos/", json={"usuario_id_1": u1["id_usuario"], "usuario_id_2": u2["id_usuario"]}).json()

    resp = client.delete(f"/contactos/{contacto['id_contacto']}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "Contacto eliminado correctamente"
