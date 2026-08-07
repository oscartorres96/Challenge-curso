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