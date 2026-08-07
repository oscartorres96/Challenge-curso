from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.notifications import NotificationCreate, NotificationsResponse
from app.services.delivery_service import DeliveryService


class NotificationService:

    @staticmethod
    def create_notification(
        db: Session,
        notification_data: NotificationCreate
    ):
        user = UserRepository.get_by_id(
            db=db,
            user_id=notification_data.user_id
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User has not found."
            )

        notification = NotificationRepository.create(
            db=db,
            title=notification_data.title,
            content=notification_data.content,
            channel=notification_data.channel,
            user_id=notification_data.user_id
        )

        # Send notification
        DeliveryService.send_notification(
            db=db,
            notification_data=notification
        )

        return notification

    @staticmethod
    def get_notifications_by_user(
        user_id: int,
        db: Session
    ):
        return NotificationRepository.get_notifications_by_user(
            user_id=user_id,
            db=db
        )

    @staticmethod
    def get_all_notifications(
        db: Session
    ):
        return NotificationRepository.get_all_notifications(
            db=db
        )

    @staticmethod
    def update_notification(
        db: Session,
        notification_id: int,
        notification_data: NotificationsResponse
    ):
        return NotificationRepository.update_notification(
            db=db,
            notification_id=notification_id,
            title=notification_data.title,
            content=notification_data.content,
            channel=notification_data.channel,
            user_id=notification_data.user_id
        )

    @staticmethod
    def delete_notification(
        notification_id: int,
        db: Session
    ):
        return NotificationRepository.delete_notification(
            notification_id=notification_id,
            db=db
        )

    