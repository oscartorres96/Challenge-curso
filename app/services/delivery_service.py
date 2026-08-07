from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.delivery import Delivery
from app.repositories.delivery_repository import DeliveryRepository
from app.strategies.delivery_strategy import DeliveryStrategy
from app.strategies.email_strategy import EmailStrategy
from app.strategies.sms_strategy import SMSStrategy
from app.strategies.push_strategy import PushStrategy
from app.repositories.user_repository import UserRepository


class DeliveryService:

    strategies: dict[str, DeliveryStrategy] = {
        "email": EmailStrategy(),
        "sms": SMSStrategy(),
        "push": PushStrategy(),
    }

    @classmethod
    def send_notification(
        cls,
        db: Session,
        notification_data: Notification
    ) -> Delivery:
        channel = notification_data.channel.strip().lower()

        strategy = cls.strategies.get(channel)

        if strategy is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported notification channel: {channel}"
            )

        user = UserRepository.get_by_id(
            db=db,
            user_id=notification_data.user_id
        )

        result = strategy.send(
            notification=notification_data,
            user=user
        )

        return DeliveryRepository.create(
            db=db,
            notification_id=notification_data.id,
            channel=channel,
            result=result
        )

    @staticmethod
    def get_all_deliveries(
        db: Session
    ):
        return DeliveryRepository.get_all_deliveries(
            db=db
        )
