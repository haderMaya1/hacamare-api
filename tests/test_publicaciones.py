import uuid

def test_create_publicacion(client):
    # crear usuario
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "pubuser" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Pub",
        "apellidos": "User",
        "edad": 22,
        "email": f"pub_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["data"]["id_usuario"]

    pub_data = {"texto": "Mi primera publicación", "imagen": "imagen.png", "estado": "visible", "id_usuario": usuario_id}
    response = client.post("/publicaciones/", json=pub_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Publicación creada exitosamente"
    assert data["data"]["texto"] == "Mi primera publicación"

def test_get_publicaciones(client):
    response = client.get("/publicaciones/")
    assert response.status_code == 200
    assert "data" in response.json()

def test_get_publicacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "getpub" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Get",
        "apellidos": "Pub",
        "edad": 23,
        "email": f"getpub_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["data"]["id_usuario"]

    pub_resp = client.post("/publicaciones/", json={"texto": "Prueba", "id_usuario": usuario_id})
    pub_id = pub_resp.json()["data"]["id_publicacion"]

    response = client.get(f"/publicaciones/{pub_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id_publicacion"] == pub_id

def test_update_publicacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "updpub" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Upd",
        "apellidos": "Pub",
        "edad": 24,
        "email": f"updpub_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["data"]["id_usuario"]

    pub_resp = client.post("/publicaciones/", json={"texto": "Original", "id_usuario": usuario_id})
    pub_id = pub_resp.json()["data"]["id_publicacion"]

    response = client.put(f"/publicaciones/{pub_id}", json={"texto": "Editado"})
    assert response.status_code == 200
    assert response.json()["data"]["texto"] == "Editado"

def test_delete_publicacion(client):
    user_resp = client.post("/usuarios/", json={
        "nombre_usuario": "delpub" + uuid.uuid4().hex[:4],
        "contraseña": "1234",
        "nombres": "Del",
        "apellidos": "Pub",
        "edad": 25,
        "email": f"delpub_{uuid.uuid4().hex[:6]}@test.com",
        "id_rol": 1
    })
    usuario_id = user_resp.json()["data"]["id_usuario"]

    pub_resp = client.post("/publicaciones/", json={"texto": "Eliminar", "id_usuario": usuario_id})
    pub_id = pub_resp.json()["data"]["id_publicacion"]

    response = client.delete(f"/publicaciones/{pub_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Publicación eliminada correctamente"
