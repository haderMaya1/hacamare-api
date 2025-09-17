def test_create_faq(client):
    resp = client.post("/faqs/", json={"pregunta": "¿Cómo registrarme?", "respuesta": "Haz clic en Registrarse."})
    assert resp.status_code == 200
    data = resp.json()
    assert data["pregunta"] == "¿Cómo registrarme?"

def test_get_faqs(client):
    resp = client.get("/faqs/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_faq(client):
    faq = client.post("/faqs/", json={"pregunta": "¿Cómo inicio sesión?", "respuesta": "Introduce tu correo y contraseña."}).json()
    resp = client.get(f"/faqs/{faq['id_faq']}")
    assert resp.status_code == 200
    assert resp.json()["pregunta"] == "¿Cómo inicio sesión?"

def test_update_faq(client):
    faq = client.post("/faqs/", json={"pregunta": "¿Cómo borrar cuenta?", "respuesta": "No se puede."}).json()
    resp = client.put(f"/faqs/{faq['id_faq']}", json={"pregunta": "¿Cómo borrar cuenta?", "respuesta": "En configuración -> Eliminar cuenta."})
    assert resp.status_code == 200
    assert resp.json()["respuesta"] == "En configuración -> Eliminar cuenta."

def test_delete_faq(client):
    faq = client.post("/faqs/", json={"pregunta": "¿Pregunta temporal?", "respuesta": "Respuesta temporal."}).json()
    resp = client.delete(f"/faqs/{faq['id_faq']}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "FAQ eliminada correctamente"
