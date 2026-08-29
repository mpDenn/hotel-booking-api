from fastapi.testclient import TestClient
import pytest
from database import SessionLocal
from models.rooms import Room
from models.user import User
from models.booking import Booking
from datetime import date
from services.security import hash_password
from uuid import uuid4
from main import app
client = TestClient(app)

@pytest.fixature
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
    db = SessionLocal()

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
    db = SessionLocal()

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
    db = SessionLocal()

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
        "password": "test12345"
    }

    db.delete(user)
    db.commit()
    db.close()
        