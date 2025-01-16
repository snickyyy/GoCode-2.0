import pytest
from tests.utils.db_operations import create_category, create_tests, create_tasks

@pytest.mark.asyncio
async def test_problem_details(client, session):
    url = "/problems/1"
    response = await client.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task does not exist"

    await create_category(5,session)
    await create_tests(60, session)
    await create_tasks(60, session)

    response = await client.get(url)
    assert response.status_code == 200
    assert list(response.json()["detail"].keys()) == ["id", "title", "description", "category", "difficulty", "image"]

@pytest.mark.asyncio
async def test_get_problems(client, session):
    url = "/problems/"
    response = await client.get(url)
    assert response.status_code == 200

    pagination_kit = ["current_page", "total_pages", "has_next", "has_previous", "next_page", "previous_page"]

    assert list(response.json()["detail"]["pagination"].keys()) == pagination_kit
    assert list(response.json()["detail"]["filters"].keys()) == ["categories", "difficulties"]
    assert list(response.json()["detail"]["tasks"].keys()) == ["data", "total"]
    assert len(response.json()["detail"]["tasks"].get("data")) == 25

@pytest.mark.asyncio
async def test_submit_solution_without_login(client, session):
    url = "/problems/1/solution"
    data = {"code": "print('Hello, World!')", "language": "python"}
    response = await client.post(url, json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "You need to be authenticated to solve problems"
