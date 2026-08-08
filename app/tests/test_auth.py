from fastapi import status
from fastapi.testclient import TestClient
from app.models.user import User


def test_login_success(
    client: TestClient,
    test_user: User,
    test_password: str
):
    response = client.post(
        "/auth/login",
        data = {
            "username": test_user.email,
            "password": test_password
        }
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["access_token"]
    assert response_data["token_type"] == "bearer"

def test_login_with_invalid_credentials(
        client: TestClient,
        test_user: User
):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "detail": "Credenciales incorrectas"
    }

def test_protected_enpoint_without_token(
        client: TestClient
):
    response = client.get("/users")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_register_user_success(
        client: TestClient,
):
    user_data = {
        "name": "Registered User",
        "email": "registered@example.com",
        "password": "password123",
        "phone_number": "5512345678",
        "device_token": "registered-device-token",
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
    assert response_data["phone_number"] == user_data["phone_number"]
    assert response_data["device_token"] == user_data["device_token"]
    assert "id" in response_data
    assert "password" not in response_data
    assert "hashed_password" not in response_data

def test_register_user_with_existing_email(
    client: TestClient,
    test_user: User,
):
    user_data = {
        "name": "Duplicate User",
        "email": test_user.email,
        "password": "password123",
    }

    response = client.post(
        "/auth/register",
        json=user_data,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "A user with this email already exists"
    }