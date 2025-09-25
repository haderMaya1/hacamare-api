import pytest

# Este test cubre todo el CRUD de intereses
def test_crud_interes(client, admin_token):
    # ---------- Crear ----------
    payload = {
        "nombre": "Videojuegos",
        "categoria": "Ocio"
    }
    r = client.post(
        "/intereses/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 201, r.text
    data = r.json()
    interes_id = data["id_interes"]
    assert data["nombre"] == "Videojuegos"
    assert data["categoria"] == "Ocio"

    # ---------- Listar ----------
    r = client.get("/intereses/")
    assert r.status_code == 200
    lista = r.json()
    assert any(i["id_interes"] == interes_id for i in lista)

    # ---------- Obtener por ID ----------
    r = client.get(f"/intereses/{interes_id}")
    assert r.status_code == 200
    detalle = r.json()
    assert detalle["nombre"] == "Videojuegos"

    # ---------- Actualizar ----------
    update_payload = {"nombre": "Gaming"}
    r = client.put(
        f"/intereses/{interes_id}",
        json=update_payload,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    updated = r.json()
    assert updated["nombre"] == "Gaming"

    # ---------- Eliminar ----------
    r = client.delete(
        f"/intereses/{interes_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert r.status_code == 200
    msg = r.json()
    assert "eliminado" in msg["message"].lower()

    # Verificar que ya no exista
    r = client.get(f"/intereses/{interes_id}")
    assert r.status_code == 404
