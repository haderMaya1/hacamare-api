import uuid

def test_create_sesion_chat(client):
    # crear usuario anfitrión
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "host" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Host",
        "apellidos": "Chat",
        "edad": 28,
        "email": f"host_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    anfitrion_id = user_resp.json()["data"]["id_usuario"]

    sesion_data = {"nombre_tema": "Reunión semanal", "tipo": "público", "estado": "activa", "anfitrion_id": anfitrion_id}
    response = client.post("/sesiones_chat/", json=sesion_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sesión de chat creada exitosamente"
    assert data["data"]["nombre_tema"] == "Reunión semanal"

def test_get_sesiones_chat(client):
    response = client.get("/sesiones_chat/")
    assert response.status_code == 200
    assert "data" in response.json()

def test_get_sesion_chat(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "hostget" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "HostGet",
        "apellidos": "Chat",
        "edad": 29,
        "email": f"hostget_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    anfitrion_id = user_resp.json()["data"]["id_usuario"]

    sesion_resp = client.post("/sesiones_chat/", json={"nombre_tema": "Test Sesión", "anfitrion_id": anfitrion_id})
    sesion_id = sesion_resp.json()["data"]["id_sesion"]

    response = client.get(f"/sesiones_chat/{sesion_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id_sesion"] == sesion_id

def test_update_sesion_chat(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "hostupd" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "HostUpd",
        "apellidos": "Chat",
        "edad": 30,
        "email": f"hostupd_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    anfitrion_id = user_resp.json()["data"]["id_usuario"]

    sesion_resp = client.post("/sesiones_chat/", json={"nombre_tema": "Original", "anfitrion_id": anfitrion_id})
    sesion_id = sesion_resp.json()["data"]["id_sesion"]

    response = client.put(f"/sesiones_chat/{sesion_id}", json={"nombre_tema": "Editado"})
    assert response.status_code == 200
    assert response.json()["data"]["nombre_tema"] == "Editado"

def test_delete_sesion_chat(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "hostdel" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "HostDel",
        "apellidos": "Chat",
        "edad": 31,
        "email": f"hostdel_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    anfitrion_id = user_resp.json()["data"]["id_usuario"]

    sesion_resp = client.post("/sesiones_chat/", json={"nombre_tema": "Eliminar", "anfitrion_id": anfitrion_id})
    sesion_id = sesion_resp.json()["data"]["id_sesion"]

    response = client.delete(f"/sesiones_chat/{sesion_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Sesión de chat eliminada correctamente"
