import httpx


def test_register_user():
    url = "http://127.0.0.1:8000/accounts/auth/register"
    data = {"username": "testuser", "email": "testuser@example.com", "password": "test123"}

    with httpx.Client() as client:
        response = client.post(url, json=data)
        assert response.status_code == 200
        assert response.json()["success"] == "an email has been sent"

        data.pop("password")
        bad_response = client.post(url, json=data)
        assert bad_response.status_code == 400
