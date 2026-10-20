import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client_user(client: TestClient) -> TestClient:
    return TestClient(client.app, base_url="http://testserver/users")

@pytest.fixture
def create_user(client_user: TestClient):
    user_data = {}
    response = client_user.post("/", json=user_data)
    assert response.status_code == 201
    return response.json()

def test_health_check(client_user: TestClient):
    response = client_user.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "test words | prefix: /users"}

def test_get_users_empty(client_user: TestClient):
    response = client_user.get("/")
    assert response.status_code == 200
    assert response.json() == []
    
def test_get_users_pagination(client_user):
    pass
