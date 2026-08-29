from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_my_bookings(auth_headers):

    response = client.get(
        "/booking/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data,list)

def test_get_my_bookings_without_token():
    response = client.get(
        "/booking/me"
    )

    assert response.status_code == 401

def test_get_my_bookings_response_structure(auth_headers):

    response = client.get(
        "/booking/me",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data,list)

    if data:
        assert "id" in data[0]
        assert "room_id" in data[0]
        assert "check_in" in data[0]
        assert "check_out" in data[0]

def test_create_booking_without_token():
    response = client.post(
        "/booking",
        json={
            "room_id": 1,
            "check_in": "2030-01-10",
            "check_out": "2030-01-12",
            "guests": 2
        }
    )

    assert response.status_code == 401

def test_create_booking(auth_headers, test_room):

    response = client.post(
        "/booking",
        headers = auth_headers,
        json={
            "room_id": test_room,
            "check_in": "2099-01-10",
            "check_out": "2099-01-12",
            "guests": 2
        }

    )

    assert response.status_code == 200

    data = response.json()
    booking_id = data["id"]


    assert data["room_id"] == test_room
    assert data["guests"] == 2
    assert data["check_in"] == "2099-01-10"
    assert data["check_out"] == "2099-01-12"

    delete_response = client.delete(
        f"/booking/{booking_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

def test_create_booking_wrong_dates(auth_headers,test_room):
    response = client.post(
        "/booking",
        headers=auth_headers,
        json = {
            "room_id": test_room,
            "check_in": "2099-05-15",
            "check_out": "2099-05-10",
            "guests": 1
        }
    )
    assert response.status_code == 400

def test_create_booking_invalid_guests_type(auth_headers,):

    response = client.post(
        "/booking",
        headers=auth_headers,
        json = {
                "room_id": 1,
                "check_in": "2099-05-10",
                "check_out": "2099-05-15",
                "guests": "hello"
        }
        )
    assert response.status_code == 422

def test_create_booking_too_many_guests(auth_headers, test_room):

    response = client.post(
        "/booking",
        headers=auth_headers,
        json = {
                "room_id": test_room,
                "check_in": "2099-05-10",
                "check_out": "2099-05-15",
                "guests": 999
        }
        )
    assert response.status_code == 400

def test_create_booking_conflict(auth_headers,test_room):

    response = client.post(
            "/booking",
            headers=auth_headers,
            json = {
                "room_id": test_room,
                "check_in": "2099-07-12",
                "check_out": "2099-07-14",
                "guests": 1
            }
        )
    assert response.status_code == 200
    data = response.json()
    booking_id = data["id"]

    response = client.post(
            "/booking",
            headers=auth_headers,
            json = {
                "room_id": test_room,
                "check_in": "2099-07-12",
                "check_out": "2099-07-14",
                "guests": 1
            }
        )

    assert response.status_code == 409

    delete_response = client.delete(
        f"/booking/{booking_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 200

def test_delete_booking_not_found(auth_headers):


    response = client.delete(
        "/booking/99999",
        headers = auth_headers
    )

    assert response.status_code == 404

def test_delete_other_user_booking(auth_headers, other_user_booking):

    response = client.delete(
            f"/booking/{other_user_booking}",
            headers = auth_headers
            )

    assert response.status_code == 403









