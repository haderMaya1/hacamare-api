def test_crud_faq(client):
    # Registrar usuario para autenticación
    client.post("/auth/register", json={
        "nombre_usuario": "adminfaq",
        "contraseña": "123456",
        "nombres": "Admin",
        "apellidos": "Faq",
        "edad": 30,
        "email": "adminfaq@example.com",
        "id_rol": 1
    })

    login = client.post("/auth/login", data={"username": "adminfaq", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear FAQ
    r = client.post("/faq/", json={
        "pregunta": "¿Cómo crear una cuenta?",
        "respuesta": "Debes registrarte en la página de inicio."
    }, headers=headers)
    assert r.status_code == 201
    faq_id = r.json()["id_faq"]

    # Listar FAQs
    r = client.get("/faq/")
    assert r.status_code == 200
    assert any(f["id_faq"] == faq_id for f in r.json())

    # Obtener una FAQ
    r = client.get(f"/faq/{faq_id}")
    assert r.status_code == 200
    assert r.json()["pregunta"] == "¿Cómo crear una cuenta?"

    # Actualizar FAQ
    r = client.put(f"/faq/{faq_id}", json={"respuesta": "Solo haz clic en Registrarse."}, headers=headers)
    assert r.status_code == 200
    assert r.json()["respuesta"] == "Solo haz clic en Registrarse."

    # Eliminar FAQ
    r = client.delete(f"/faq/{faq_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "FAQ eliminada correctamente"
