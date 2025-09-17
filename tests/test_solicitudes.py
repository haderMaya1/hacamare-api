import uuid

def test_create_solicitud(client):
    # crear dos usuarios
    user1 = client.post("/usuarios/", json={
        "nombre_usuario": "sender" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Remitente",
        "apellidos": "Test",
        "edad": 25,
        "email": f"sender_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    user2 = client.post("/usuarios/", json={
        "nombre_usuario": "receiver" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Destinatario",
        "apellidos": "Test",
        "edad": 26,
        "email": f"receiver_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    resp = client.post("/solicitudes/", json={
        "mensaje": "¿Quieres ser mi amigo?",
        "remitente_id": user1["id_usuario"],
        "destinatario_id": user2["id_usuario"]
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["estado"] == "pendiente"
    assert data["remitente_id"] == user1["id_usuario"]
    assert data["destinatario_id"] == user2["id_usuario"]

def test_get_solicitudes(client):
    resp = client.get("/solicitudes/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_update_estado_solicitud(client):
    # crear usuarios
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "solicitador" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "U1",
        "apellidos": "Test",
        "edad": 20,
        "email": f"solicitador_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "solicitado" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "U2",
        "apellidos": "Test",
        "edad": 21,
        "email": f"solicitado_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    solicitud = client.post("/solicitudes/", json={
        "mensaje": "Conéctemos!",
        "remitente_id": u1["id_usuario"],
        "destinatario_id": u2["id_usuario"]
    }).json()

    resp = client.put(f"/solicitudes/{solicitud['id_solicitud']}?estado=aceptada")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "aceptada"

def test_delete_solicitud(client):
    # crear usuarios
    u1 = client.post("/usuarios/", json={
        "nombre_usuario": "deleter" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Udel",
        "apellidos": "Test",
        "edad": 22,
        "email": f"deleter_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    u2 = client.post("/usuarios/", json={
        "nombre_usuario": "deleted" + uuid.uuid4().hex[:5],
        "contraseña": "1234",
        "nombres": "Uded",
        "apellidos": "Test",
        "edad": 23,
        "email": f"deleted_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    }).json()

    solicitud = client.post("/solicitudes/", json={
        "mensaje": "Te envío solicitud",
        "remitente_id": u1["id_usuario"],
        "destinatario_id": u2["id_usuario"]
    }).json()

    delete_resp = client.delete(f"/solicitudes/{solicitud['id_solicitud']}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "Solicitud eliminada correctamente"
