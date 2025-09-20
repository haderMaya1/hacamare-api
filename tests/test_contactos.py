def test_crud_contacto(client):
    # Registrar usuarios
    client.post("/auth/register", json={
        "nombre_usuario": "alice",
        "contraseña": "123456",
        "nombres": "Alice",
        "apellidos": "Smith",
        "edad": 28,
        "email": "alice@example.com",
        "id_rol": 1
    })
    client.post("/auth/register", json={
        "nombre_usuario": "bob",
        "contraseña": "123456",
        "nombres": "Bob",
        "apellidos": "Johnson",
        "edad": 29,
        "email": "bob@example.com",
        "id_rol": 1
    })

    # Login Alice
    login = client.post("/auth/login", data={"username": "alice", "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Crear contacto Alice → Bob
    r = client.post("/contactos/", json={"usuario_id_2": 2}, headers=headers)
    assert r.status_code == 201
    contacto_id = r.json()["id_contacto"]
    assert r.json()["usuario_id_1"] == 1
    assert r.json()["usuario_id_2"] == 2

    # Listar contactos de Alice
    r = client.get("/contactos/", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert any(c["id_contacto"] == contacto_id for c in data)

    # Eliminar contacto
    r = client.delete(f"/contactos/{contacto_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Contacto eliminado"
