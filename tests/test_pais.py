def test_crud_pais(client, admin_token, db_session):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Crear país
    payload = {
        "pais": "Colombia",
        "estado": "Antioquia",
        "ciudad": "Medellín"
    }
    r = client.post("/paises/", json=payload,
                    headers=headers)
    assert r.status_code == 201
    data = r.json()
    pais_id = data["id_pais"]
    assert data["pais"] == "Colombia"
    assert data["estado"] == "Antioquia"
    assert data["ciudad"] == "Medellín"

    # Listar
    r = client.get("/paises/")
    assert r.status_code == 200
    lista = r.json()
    assert any(p["pais"] == "Colombia" for p in lista)

    # Obtener por id
    r = client.get(f"/paises/{pais_id}")
    assert r.status_code == 200
    assert r.json()["estado"] == "Antioquia"

    # Actualizar
    r = client.put(
        f"/paises/{pais_id}",
        json={"estado": "Cundinamarca", "ciudad": "Bogotá"},
        headers=headers
    )
    assert r.status_code == 200
    upd = r.json()
    assert upd["estado"] == "Cundinamarca"
    assert upd["ciudad"] == "Bogotá"

    # Eliminar
    r = client.delete(f"/paises/{pais_id}",
                      headers=headers)
    assert r.status_code == 200
    assert "eliminado" in r.json()["message"].lower()
