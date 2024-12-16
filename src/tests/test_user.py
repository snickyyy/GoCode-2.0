import httpx


def test_register_user():
    timeout = httpx.Timeout(10.0)
    url = "http://127.0.0.1:8000/accounts/auth/register"
    data = {"username": "testuser2", "email": "testuser2@example.com", "password": "test123"}

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, json=data)
        assert response.status_code == 200
        assert response.json()["detail"] == "an email has been sent"

        data.pop("password")
        without_password = client.post(url, json=data)
        assert without_password.status_code == 422

    data = {"username": "testuser2", "email": "testuser2@example.com", "password": "test123"}
    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, json=data)
        assert response.status_code == 409
        assert response.json()["detail"] == "This username or email already exists"
