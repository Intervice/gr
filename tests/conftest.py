from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from fastapi.testclient import TestClient

from main import app, Base
from src.database.db import get_db
import pytest

test_engine = create_engine("sqlite:///test_skillswap.db",
                            connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)    

@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


