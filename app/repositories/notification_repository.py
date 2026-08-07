from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notifications import NotificationCreate


class NotificationRepository:

    @staticmethod
    def create(
        db: Session,
        title: str,
        content: str,
        channel: str,
        user_id: int
    ) -> Notification:
        notification = Notification(
            title=title,
            content=content,
            channel=channel,
            user_id=user_id
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    @staticmethod
    def get_notifications_by_user(
        user_id: int,
        db: Session
    ) -> list[Notification]:
        notifications = db.query(Notification).filter(
            Notification.user_id == user_id
        ).all()

        return notifications

    @staticmethod
    def get_all_notifications(
        db: Session
    ) -> list[Notification]:
        return db.query(Notification).all()


    @staticmethod
    def update_notification(
        db: Session,
        notification_id: int,
        title: str,
        content: str,
        channel: str,
        user_id: int
    ):
        notification = db.get(Notification, notification_id)

        if notification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found."
            )

        notification.title = title
        notification.content = content
        notification.channel = channel
        notification.user_id = user_id

        db.commit()
        db.refresh(notification)

        return notification


    @staticmethod
    def delete_notification(
        notification_id: int,
        db: Session
    ):
        notification = db.get(Notification, notification_id)

        if notification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification has not found."
            )

        db.delete(notification)
        db.commit()