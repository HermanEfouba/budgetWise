import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db, Base
import models

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data

def test_login_user():
    # First register a user
    client.post(
        "/auth/register",
        json={
            "name": "Login Test",
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    
    # Then try to login
    response = client.post(
        "/auth/login",
        data={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_category():
    response = client.post(
        "/categories/",
        json={"name": "Test Category"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"

def test_get_categories():
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_unauthorized_access():
    response = client.get("/budgets/dashboard")
    assert response.status_code == 401