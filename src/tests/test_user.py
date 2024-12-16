from starlette.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    url = "/accounts/auth/register"
    data = {"username": "testuser", "email": "testuser@example.com", "password": "test123"}

    response = client.post(url, json=data)
    assert response.status_code == 200
    assert response.json()["detail"] == "an email has been sent"

    data_without_password = data.copy()
    data_without_password.pop("password")
    response = client.post(url, json=data_without_password)
    assert response.status_code == 422

    response = client.post(url, json=data)
    assert response.status_code == 409
    assert response.json()["detail"] == "This username or email already exists"
