from fastapi import status
from fastapi.testclient import TestClient


def test_create_user(
    client: TestClient,
    auth_header: dict[str, str]
):
    new_user = {
        "name": "Yahir Torres",
        "email": "yahir@gmail.com",
        "password": "password123",
        "phone_number": "+52354123456",
        "device_token": "device-token-example"
    }

    response = client.post(
        "/users",
        json=new_user,
        headers=auth_header
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data['name'] == new_user['name']
    assert response_data['email'] == new_user['email']
    assert response_data['phone_number'] == new_user['phone_number']
    assert response_data['device_token'] == new_user['device_token']
    assert "id" in response_data
    assert "password" not in response_data
    assert "hashed_password" not in response_data

def test_create_user_with_existting_email(
    client: TestClient,
    auth_header: dict[str, str]
):
    user_data = {
        "name": "Usuario de prueba",
        "email": "test@example.com",
        "phone_number": "55512345678",
        "password": "password123",
        "device_token": "test-device-token"
    }

    response = client.post(
        "/users",
        json=user_data,
        headers=auth_header
    )

    assert response.status_code == 409  
    assert response.json()['detail'] == (
        "A user with this email already exists"
    )