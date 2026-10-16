import pytest

from app.main import app, bookings


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    bookings.clear()

    with app.test_client() as test_client:
        yield test_client

    bookings.clear()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_list_rooms(client):
    response = client.get("/rooms")

    assert response.status_code == 200
    assert len(response.json["rooms"]) == 3


def test_create_booking(client):
    response = client.post(
        "/bookings",
        json={"room_id": 1, "guest_name": "Demo Guest"},
    )

    assert response.status_code == 201
    assert response.json["booking"]["status"] == "confirmed"


def test_reject_invalid_booking(client):
    response = client.post(
        "/bookings",
        json={"room_id": 999, "guest_name": "Demo Guest"},
    )

    assert response.status_code == 404
    assert response.json["error"] == "Room not found"