import pytest
from app.main import app
from app.database import get_db
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


DATABASE_URL = "sqlite:///./test_social_media.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def set_up_database():
    with engine.connect() as conn:
        conn.execute(text('''CREATE TABLE IF NOT EXISTS posts (
                            id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp
                            )'''))
        conn.execute(text('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            created_at TEXT DEFAULT current_timestamp
                            )'''))
        conn.commit()

def drop_database():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS posts"))
        conn.execute(text("DROP TABLE IF EXISTS users"))
        conn.commit()


@pytest.fixture
def client():
    # Run code before tests run
    app.dependency_overrides[get_db] = override_get_db
    drop_database()
    set_up_database()
    yield TestClient(app)
    # Run code after tests run


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "password123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user