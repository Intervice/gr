import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client_user(client: TestClient) -> TestClient:
    return TestClient(client.app, base_url="http://testserver/users")

@pytest.fixture
def create_multiple_users(client_user: TestClient) -> list[dict]:
    created_users = []
    for i in range(1, 21):
        user_data = {
            "username": f"user_{i}",
            "email": f"user_{i}@email.com",
            "bio": f"Bio for user {i}",
        }
        response = client_user.post("/", json=user_data)
        assert response.status_code == 201
        created_users.append(response.json())

    return created_users

@pytest.fixture
def create_user(client_user: TestClient):
    user_data = {
        "username": "username",
        "email": "email@email.com",
        "bio": "Ready to learn something new"
        }
    response = client_user.post("/", json=user_data)
    assert response.status_code == 201
    return response.json()

def test_health_check(client_user: TestClient):
    response = client_user.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "test works | prefix: /users"}

def test_get_users_empty(client_user: TestClient):
    response = client_user.get("/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_users_one(client_user: TestClient, create_user: dict):
    response = client_user.get("/")
    assert response.status_code == 200
    assert response.json() == [create_user]
    
def test_get_single_user_non_existent(client_user: TestClient):
    response = client_user.get("/999")
    assert response.status_code == 404
    
def test_get_single_user(client_user: TestClient, create_user: dict):
    response = client_user.get("/1")
    assert response.status_code == 200
    assert response.json() == create_user

def test_create_user_valid(client_user: TestClient):
    user_data = {
        "username": "username",
        "email": "email@email.com",
        "bio": "Ready to learn something new"
        }
    response = client_user.post("/", json=user_data)
    assert response.status_code == 201
    result = response.json()
    for k, v in user_data.items():
        assert result[k] == v
    assert result["is_active"] == True
    assert result["id"] == 1
    assert result["created_at"]
    assert result["skills"] == []
    
def test_create_user_invalid(client_user: TestClient):
    user_data = {
        "username": "username",
        "email": "email",
        "bio": "Ready to learn something new"
        }
    response = client_user.post("/", json=user_data)
    assert response.status_code == 422
    
def test_user_update(client_user: TestClient, create_user: dict):
    update_data = {"username": "new_username"}
    response = client_user.put("/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == update_data["username"]
    
def test_delete_user_non_existent(client_user: TestClient):
    response = client_user.delete("/1")
    assert response.status_code == 404
    
def test_delete_user_check_deleted_user(client_user: TestClient, create_user: dict):
    response = client_user.delete("/1")
    assert response.status_code == 204
    response = client_user.get("/1")
    assert response.status_code == 404
    
# def test_get_users_pagination(client_user):
#     pass


# {
#   "username": "username",
#   "email": "email@email.com",
#   "bio": "Ready to learn something new",
#   "id": 1,
#   "created_at": "2026-10-20T11:47:46",
#   "skills": []
# }