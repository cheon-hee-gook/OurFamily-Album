import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.dependencies import get_db
from app.models.base import Base
import uuid
from app.models.user import User
from app.config.settings import settings
from jose import jwt

# SQLite in-memory DB 생성
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 초기화
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


# 테스트용 DB 세션 주입
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user(test_client):
    from app.dependencies import get_db
    db = next(get_db())
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        name="테스트유저",
        password_hash="$2b$12$uYlP4DydYh0oZb8rY9OQQu0d8mOrE0Y6U05YKU34qqVMeYAw4zF3S"  # "testpassword" 암호화된 값
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def authorized_client(test_client, test_user):
    token = jwt.encode(
        {"sub": str(test_user.id)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    test_client.headers.update({"Authorization": f"Bearer {token}"})
    return test_client


@pytest.fixture
def new_user_token(test_client):
    payload = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "name": "신규유저"
    }
    test_client.post("/api/auth/signup", json=payload)
    res = test_client.post("/api/auth/login", json={
        "email": payload["email"],
        "password": payload["password"]
    })
    token = res.json()["access_token"]
    return token



@pytest.fixture
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clear_db(session):
    yield
    session.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()