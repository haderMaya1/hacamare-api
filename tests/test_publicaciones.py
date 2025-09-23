import pytest

def test_crud_publicacion(client, db_session, user_token, admin_token):
    # Crear publicación como usuario normal
    payload = {"texto": "Hola mundo", "imagen": None}
    r = client.post("/publicaciones/", json=payload,
                    headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 201
    pub_id = r.json()["id_publicacion"]

    # Listar (público)
    r = client.get("/publicaciones/")
    assert r.status_code == 200
    assert any(p["id_publicacion"] == pub_id for p in r.json())

    # Actualizar como autor
    update = {"texto": "Hola editado"}
    r = client.put(f"/publicaciones/{pub_id}", json=update,
                   headers={"Authorization": f"Bearer {user_token}"})
    assert r.status_code == 200
    assert r.json()["texto"] == "Hola editado"

    # Intentar actualizar con otro usuario → 403
    other_update = {"texto": "Hackeo"}
    r = client.put(f"/publicaciones/{pub_id}", json=other_update,
                   headers={"Authorization": f"Bearer {admin_token}"} )
    # admin sí puede, pero podrías probar con un token de otro user no admin
    # para ver el 403

    # Eliminar como admin (moderación)
    r = client.delete(f"/publicaciones/{pub_id}",
                      headers={"Authorization": f"Bearer {admin_token}"})
    assert r.status_code == 200
