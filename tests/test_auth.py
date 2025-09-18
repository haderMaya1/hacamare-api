def test_register_and_login(client):
    # Registro de usuario
    response = client.post("/auth/register", data={"username": "authuser", "password": "1234"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    # Login con usuario registrado
    response = client.post("/auth/login", data={"username": "authuser", "password": "1234"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_invalid(client):
    response = client.post("/auth/login", data={"username": "nouser", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"
