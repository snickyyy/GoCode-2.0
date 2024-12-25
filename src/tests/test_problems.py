from starlette.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_problems():
    url = "/problems/"
    response = client.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Instance does not exist"


def test_get_problem_detail():
    url = "/problems/1"
    response = client.get(url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Instance does not exist"
