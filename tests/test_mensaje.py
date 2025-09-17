import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_mensaje():
    # Crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "msguser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Msg",
        "apellidos": "User",
        "edad": 25,
        "email": f"msg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    # Crear sesión
    sesion_resp = client.post("/sesiones_chat/", json={
        "nombre_tema": "Sesión Mensajes",
        "tipo": "público",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion_resp.json()["id_sesion"]

    # Crear mensaje
    resp = client.post("/mensajes/", json={
        "contenido": "Hola mundo!",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["contenido"] == "Hola mundo!"
    assert data["id_remitente"] == usuario_id
    assert data["id_sesion"] == sesion_id

def test_get_mensajes():
    resp = client.get("/mensajes/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_mensajes_sesion():
    resp = client.get("/mensajes/sesion/1")
    assert resp.status_code in [200, 404]

def test_delete_mensaje():
    # Crear usuario + sesión + mensaje
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "delmsg" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Msg",
        "edad": 28,
        "email": f"delmsg_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["id_usuario"]

    sesion_resp = client.post("/sesiones_chat/", json={
        "nombre_tema": "Sesión Borrar Mensaje",
        "tipo": "privado",
        "anfitrion_id": usuario_id
    })
    sesion_id = sesion_resp.json()["id_sesion"]

    msg_resp = client.post("/mensajes/", json={
        "contenido": "Mensaje temporal",
        "id_remitente": usuario_id,
        "id_sesion": sesion_id
    })
    msg_id = msg_resp.json()["id_mensaje"]

    # Eliminar mensaje
    resp = client.delete(f"/mensajes/{msg_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Mensaje eliminado correctamente"
