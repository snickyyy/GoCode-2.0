import pytest


@pytest.mark.asyncio
async def test_register_user(client, session):
    url = "/accounts/auth/register"
    data = {"username": "testuser1", "email": "testuser@example.com", "password": "test1213"}

    response = await client.post(url, json=data)
    assert response.status_code == 200
    assert response.json()["detail"] == "an email has been sent"

    data_without_password = data.copy()
    data_without_password.pop("password")
    response = await client.post(url, json=data_without_password)
    assert response.status_code == 422

    response = await client.post(url, json=data)
    assert response.status_code == 409
    assert response.json()["detail"] == "User must be unique"


@pytest.mark.asyncio
async def test_bad_login_user(client, session):
    url = "/accounts/auth/login"
    data = {"username_or_email": "testuser", "password": "test123"}

    response = await client.post(url, json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
