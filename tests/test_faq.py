import pytest

def test_create_faq(client):
    faq_data = {"pregunta": "¿Cómo registrarse?", "respuesta": "Haz clic en el botón de registro."}
    response = client.post("/faqs/", json=faq_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "FAQ creada exitosamente"
    assert data["data"]["pregunta"] == "¿Cómo registrarse?"

def test_get_faqs(client):
    response = client.get("/faqs/")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

def test_get_faq(client):
    faq_data = {"pregunta": "¿Cómo iniciar sesión?", "respuesta": "Ingresa tus credenciales."}
    create = client.post("/faqs/", json=faq_data)
    faq_id = create.json()["data"]["id_faq"]

    response = client.get(f"/faqs/{faq_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["pregunta"] == "¿Cómo iniciar sesión?"

def test_update_faq(client):
    faq_data = {"pregunta": "¿Cómo actualizar perfil?", "respuesta": "En la sección de configuración."}
    create = client.post("/faqs/", json=faq_data)
    faq_id = create.json()["data"]["id_faq"]

    response = client.put(f"/faqs/{faq_id}", json={"respuesta": "Desde la configuración de usuario."})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["respuesta"] == "Desde la configuración de usuario."

def test_delete_faq(client):
    faq_data = {"pregunta": "¿Cómo eliminar cuenta?", "respuesta": "Contacta soporte."}
    create = client.post("/faqs/", json=faq_data)
    faq_id = create.json()["data"]["id_faq"]

    response = client.delete(f"/faqs/{faq_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "FAQ eliminada correctamente"
