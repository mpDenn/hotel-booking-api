from fastapi.testclient import TestClient
from main import app
from tests.conftest import TestSessionLocal
from models.booking import Booking
from datetime import date
from sqlalchemy import select
from models.user import User

client = TestClient(app)

def test_delete_user_safe_response(admin_headers, test_user):

    response = client.delete(
        f"/user/{test_user["id"]}",
        headers=admin_headers
    )
    assert response.status_code == 200

    data = response.json()

    assert "password_hash" not in data
    assert "role" not in data

def test_delete_user_with_bookings(admin_headers, test_user, test_room):
    db = TestSessionLocal()

    booking = Booking(
        user_id = test_user["id"],
        room_id = test_room,
        check_in = date(2029, 5, 12),
        check_out = date(2029, 5, 13),
        guests = 1
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    response = client.delete(
            f"/user/{test_user["id"]}",
            headers=admin_headers
        )

    data = response.json()

    assert response.status_code == 409
    assert data["detail"] == "User has existing bookings"

    user_in_db = db.execute(select(User).where(User.id == test_user["id"])).scalars().first()

    assert user_in_db is not None

    db.delete(booking)
    db.commit()
    db.close()

def test_create_user_invalid_email():

    response = client.post(
        "/users",
        json = {
            "name": "Denis",
            "surname": "smith",
            "email": "123123123",
            "password": "123456789"
        }
    )

    assert response.status_code == 422

def test_create_user_invalid_password():

    response = client.post(
        "/users",
        json = {
            "name": "Denis",
            "surname": "smith",
            "email": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 422

def test_create_user_empty_name():

    response = client.post(
        "/users",
        json = {
            "name": "         ",
            "surname": "smith",
            "email": "test@example.com",
            "password": "123456789"
        }
    )

    assert response.status_code == 422

def test_update_user_empty_surname(admin_headers, test_user):

    response = client.patch(
        f"/user/{test_user["id"]}",
        json={
            "surname": "     "
        },
        headers = admin_headers
    )

    assert response.status_code == 422

def test_update_user_null_surname(admin_headers, test_user):

    response = client.patch(
        f"/user/{test_user["id"]}",
        json={
            "surname": None
        },
        headers = admin_headers
    )

    assert response.status_code == 422

def test_update_user_null_email(admin_headers, test_user):

    response = client.patch(
        f"/user/{test_user["id"]}",
        json={
            "email": None
        },
        headers = admin_headers
    )

    assert response.status_code == 422

def test_update_user_null_password(admin_headers, test_user):

    response = client.patch(
        f"/user/{test_user["id"]}",
        json={
            "password": None
        },
        headers = admin_headers
    )

    assert response.status_code == 422
