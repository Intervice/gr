# from collections.abc import Generator

# import pytest
# from fastapi import FastAPI
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from sqlalchemy.pool import StaticPool

# from src.database.db import get_db
# from src.database.models import Base
# from src.routes import skills, users


# @pytest.fixture()
# def client() -> Generator[TestClient, None, None]:
#     """Create a clean API client and an isolated database for every test."""
#     engine = create_engine(
#         "sqlite://",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     Base.metadata.create_all(bind=engine)

#     def override_get_db() -> Generator[Session, None, None]:
#         with Session(engine) as db:
#             yield db

#     test_app = FastAPI()
#     test_app.include_router(users.router)
#     test_app.include_router(skills.router)
#     test_app.dependency_overrides[get_db] = override_get_db

#     with TestClient(test_app) as test_client:
#         yield test_client

#     Base.metadata.drop_all(bind=engine)


# def test_get_users_returns_empty_list(client: TestClient) -> None:
#     response = client.get("/users/")

#     assert response.status_code == 200
#     assert response.json() == []


# def test_get_missing_user_returns_404(client: TestClient) -> None:
#     response = client.get("/users/999")

#     assert response.status_code == 404


# def test_create_and_get_skill(client: TestClient) -> None:
#     payload = {
#         "title": "Python",
#         "description": "Learn Python programming",
#         "category": "programming",
#         "level": "beginner",
#         "can_teach": True,
#         "want_learn": False,
#     }

#     create_response = client.post("/skills/", json=payload)

#     assert create_response.status_code == 200
#     skill_id = create_response.json()["id"]

#     get_response = client.get(f"/skills/{skill_id}")

#     assert get_response.status_code == 200
#     assert get_response.json()["title"] == "Python"


# def test_skill_matches_find_opposite_role(client: TestClient) -> None:
#     teacher = {
#         "title": "Python teacher",
#         "description": "Can teach Python programming",
#         "category": "programming",
#         "level": "expert",
#         "can_teach": True,
#         "want_learn": False,
#     }
#     learner = {
#         "title": "Python learner",
#         "description": "Wants to learn Python programming",
#         "category": "programming",
#         "level": "beginner",
#         "can_teach": False,
#         "want_learn": True,
#     }

#     teacher_id = client.post("/skills/", json=teacher).json()["id"]
#     client.post("/skills/", json=learner)

#     response = client.get(f"/skills/{teacher_id}/matches/")

#     assert response.status_code == 200
#     assert response.json()[0]["title"] == "Python learner"
