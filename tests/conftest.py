from fastapi.testclient import TestClient
import pytest
from database import get_db, Base
from models.rooms import Room
from models.user import User
from models.booking import Booking
from datetime import date
from services.security import hash_password
from uuid import uuid4
from main import app
client = TestClient(app)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import select
import os
load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db

    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def auth_headers(test_user):
    response = client.post(
        "login",
        json = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200

    data = response.json()
    token = data["access_token"]

    header = {
        "Authorization": f"Bearer {token}"
    }
    return header

@pytest.fixture
def test_room():
    db = TestSessionLocal()

    room = Room(
        number = uuid4().int % 1_000_000_000,
        room_type = "test",
        price = 1000,
        base_capacity = 2,
        max_capacity = 4
    )

    db.add(room)
    db.commit()
    db.refresh(room)

    yield room.id

    db.delete(room)
    db.commit()
    db.close()

@pytest.fixture
def other_user_booking(test_room):
    db = TestSessionLocal()

    user = User(
        email = f"test_{uuid4()}@test.com",
        name = "test",
        surname = "user",
        password_hash = hash_password("test12345")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    booking = Booking(
        user_id = user.id,
        room_id = test_room,
        check_in = date(2099, 10, 10),
        check_out = date(2099, 10, 12),
        guests = 1,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    yield booking.id

    db.delete(booking)
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def test_user():
    db = TestSessionLocal()

    user = User(
        email = f"test_{uuid4()}@test.com",
        name = "test",
        surname = "user",
        password_hash = hash_password("test12345")
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield {
        "email":user.email,
        "password": "test12345",
        "id": user.id
    }

    existing_user = db.execute(select(User).where(User.id == user.id)).scalars().first()

    if existing_user:
        db.delete(existing_user)
        db.commit()

    db.close()

@pytest.fixture
def test_admin():
    db = TestSessionLocal()

    admin = User(
        email = f"test_{uuid4()}@test.com",
        name = "test",
        surname = "user",
        password_hash = hash_password("test12345"),
        role = "admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    yield {
        "email":admin.email,
        "password": "test12345"
    }

    db.delete(admin)
    db.commit()
    db.close()

@pytest.fixture
def admin_headers(test_admin):

    response = client.post(
        "/login",
        json = {
            "email": test_admin["email"],
            "password": test_admin["password"]
        }
    )
    assert response.status_code == 200

    data = response.json()
    token = data["access_token"]

    header = {
        "Authorization": f"Bearer {token}"
        }
    yield header

