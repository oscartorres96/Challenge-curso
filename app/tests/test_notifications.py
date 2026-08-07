from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.models.notification import Notification
from app.models.user import User


def test_create_email_notification(
        client: TestClient,
        auth_header: dict[str, str],
        test_user: User,
        db_session: Session
):
    notification_data = {
        "title": "Bienvenido",
        "content": "Gracias por registrarte.",
        "channel": "email",
        "user_id": test_user.id,
    }

    response = client.post(
        "/notifications",
        json=notification_data,
        headers=auth_header,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["title"] == notification_data["title"]
    assert response_data["content"] == notification_data["content"]
    assert response_data["channel"] == notification_data["channel"]
    assert response_data["user_id"] == test_user.id
    assert "id" in response_data

    notification = db_session.scalar(
        select(Notification).where(
            Notification.id == response_data["id"]
        )
    )

    assert notification is not None

    delivery = db_session.scalar(
        select(Delivery).where(
            Delivery.notification_id == notification.id
        )
    )

    assert delivery is not None
    assert delivery.channel == "email"
    assert delivery.recipient == test_user.email
    assert delivery.payload["subject"] == notification_data["title"]


def test_create_sms_notification(
        client: TestClient,
        auth_header: dict[str, str],
        test_user: User,
        db_session: Session
):
    long_content = "A" * 200

    notification_data = {
        "title": "SMS Message",
        "content": long_content,
        "channel": "sms",
        "user_id": test_user.id,
    }

    response = client.post(
        "/notifications",
        json=notification_data,
        headers=auth_header
    )

    assert response.status_code == status.HTTP_201_CREATED

    notification_id = response.json()["id"]

    delivery = db_session.scalar(
        select(Delivery).where(
            Delivery.notification_id == notification_id
        )
    )

    assert delivery is not None
    assert delivery.channel == "sms"
    assert delivery.recipient == test_user.phone_number
    assert len(delivery.payload["message"]) == 160
    assert delivery.payload["message"] == long_content[:160]


def test_create_push_notification(
        client: TestClient,
        auth_header: dict[str, str],
        test_user: User,
        db_session: Session,
):
    notification_data = {
        "title": "New Promotion",
        "content": "You have a new promotion available",
        "channel": "push",
        "user_id": test_user.id,
    }

    response = client.post(
        "/notifications",
        json=notification_data,
        headers=auth_header
    )

    assert response.status_code  == status.HTTP_201_CREATED

    notification_id = response.json()["id"]

    delivery = db_session.scalar(
        select(Delivery).where(
            Delivery.notification_id == notification_id
        )
    )

    assert delivery is not None
    assert delivery.channel == "push"
    assert delivery.recipient == test_user.device_token
    assert delivery.status == "sent"
    assert delivery.payload == {
        "title": notification_data["title"],
        "body": notification_data["content"]
    }


def test_get_notifications(
    client: TestClient,
    auth_header: dict[str, str],
    test_notification: Notification,
):
    response = client.get(
        "/notifications",
        headers=auth_header,
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert len(response_data) == 1
    assert response_data[0]["id"] == test_notification.id
    assert response_data[0]["title"] == test_notification.title
    assert response_data[0]["content"] == test_notification.content


def test_update_notification(
    client: TestClient,
    auth_header: dict[str, str],
    test_notification: Notification,
    db_session: Session,
):
    update_data = {
        "title": "Título actualizado",
        "content": "Contenido actualizado",
        "channel": "sms",
        "user_id": test_notification.user_id,
    }

    response = client.put(
        f"/notifications/{test_notification.id}",
        json=update_data,
        headers=auth_header,
    )

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["title"] == update_data["title"]
    assert response_data["content"] == update_data["content"]
    assert response_data["channel"] == update_data["channel"]

    db_session.refresh(test_notification)

    assert test_notification.title == update_data["title"]
    assert test_notification.content == update_data["content"]


def test_delete_notification(
    client: TestClient,
    auth_header: dict[str, str],
    test_notification: Notification,
    db_session: Session,
):
    notification_id = test_notification.id

    response = client.delete(
        f"/notifications/{notification_id}",
        headers=auth_header,
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    deleted_notification = db_session.get(
        Notification,
        notification_id,
    )

    assert deleted_notification is None


def test_create_notification_with_invalid_channel(
    client: TestClient,
    auth_header: dict[str, str],
    test_user: User,
):
    notification_data = {
        "title": "Canal inválido",
        "content": "Este mensaje no debe enviarse.",
        "channel": "whatsapp",
        "user_id": test_user.id,
    }

    response = client.post(
        "/notifications",
        json=notification_data,
        headers=auth_header,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Unsupported notification channel: whatsapp"
    }

