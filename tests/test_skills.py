import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client_skill(client: TestClient) -> TestClient:
    return TestClient(client.app, base_url="http://testserver/skills")

@pytest.fixture
def create_skill(client_skill: TestClient):
    skill_data = {
        "title": "title",
        "description": "description",
        "category": "languages",
        "level": "beginner",
        "can_teach": True,
        "want_learn": False
        }
    response = client_skill.post("/", json=skill_data)
    assert response.status_code == 201
    return response.json()

def test_health_check(client_skill: TestClient):
    response = client_skill.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "test works prefix: /skills "}
    
def test_get_skills_empty(client_skill: TestClient):
    response = client_skill.get("/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_skills_one(client_skill: TestClient, create_skill: dict):
    response = client_skill.get("/")
    assert response.status_code == 200
    assert response.json() == [create_skill]

def test_get_single_skill(client_skill: TestClient, create_skill: dict):
    response = client_skill.get("/1")
    assert response.status_code == 200
    assert response.json() == create_skill

def test_delete_skill_non_existent(client_skill: TestClient):
    response = client_skill.delete("/1")
    assert response.status_code == 404
    
def test_delete_skill_check_deleted_skill(client_skill: TestClient, create_skill: dict):
    response = client_skill.delete("/1")
    assert response.status_code == 204
    response = client_skill.get("/1")
    assert response.status_code == 404
    
def test_create_skill_both_true(client_skill: TestClient):
    skill_data = {
        "title": "title",
        "description": "description",
        "category": "languages",
        "level": "beginner",
        "can_teach": True,
        "want_learn": True
        }
    response = client_skill.post("/", json=skill_data)
    assert response.status_code == 422
    
def test_create_skill_both_false(client_skill: TestClient):
    skill_data = {
        "title": "title",
        "description": "description",
        "category": "languages",
        "level": "beginner",
        "can_teach": False,
        "want_learn": False
        }
    response = client_skill.post("/", json=skill_data)
    assert response.status_code == 422
    
def test_create_skill_wrong_level(client_skill: TestClient):
    skill_data = {
        "title": "title",
        "description": "description",
        "category": "languages",
        "level": "good",
        "can_teach": False,
        "want_learn": False
        }
    response = client_skill.post("/", json=skill_data)
    assert response.status_code == 422
    
def test_create_skill_wrong_category(client_skill: TestClient):
    skill_data = {
        "title": "title",
        "description": "description",
        "category": "description",
        "level": "beginner",
        "can_teach": False,
        "want_learn": False
        }
    response = client_skill.post("/", json=skill_data)
    assert response.status_code == 422
    
def test_skill_update(client_skill: TestClient, create_skill: dict):
    update_data = {"title": "new_title", "level": "expert"}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == update_data["title"]
    assert result["level"] == update_data["level"]

def test_skill_update_non_existent(client_skill: TestClient):
    update_data = {"title": "new_title", "level": "expert"}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 404

def test_skill_update_teach_learn_false(client_skill: TestClient, create_skill: dict):
    update_data = {"can_teach": False, "want_learn": False}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 200
    assert response.json()["can_teach"] == update_data["can_teach"]
    assert response.json()["want_learn"] == update_data["want_learn"]

def test_skill_update_teach_learn_true(client_skill: TestClient, create_skill: dict):
    update_data = {"can_teach": True, "want_learn": True}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 422

def test_skill_update_teach_learn_db_synch_want_learn(client_skill: TestClient, create_skill: dict):
    update_data = {"want_learn": True}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 422

def test_skill_update_teach_learn_db_synch_can_teach(client_skill: TestClient, create_skill: dict):
    update_data = {"can_teach": True}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 200  
    update_data = {"want_learn": True}
    response = client_skill.put("/1", json=update_data)
    assert response.status_code == 422  
