import pytest
from starlette.testclient import TestClient
from main import app

@pytest.mark.asyncio
async def test_get_problems(client, session):
    url = "/problems/"
    response = client.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Instance does not exist"


@pytest.mark.asyncio
async def test_get_problem_detail(client, session):
    url = "/problems/1"
    response = await client.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Instance does not exist"
