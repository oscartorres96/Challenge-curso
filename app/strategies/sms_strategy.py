from datetime import datetime, timezone

from app.models.notification import Notification
from app.models.user import User
from app.schemas.delivery import DeliveryResult
from app.strategies.delivery_strategy import DeliveryStrategy


class SMSStrategy(DeliveryStrategy):

    def send(
        self,
        notification: Notification,
        user: User
    ) -> DeliveryResult:
        if not user.phone_number:
            raise ValueError("User does not have a phone number")

        content = notification.content[:160]

        print(
            f"Enviando SMS al número {user.phone_number}: "
            f"{content}"
        )

        return DeliveryResult(
            recipient=user.phone_number,
            sent_at=datetime.now(timezone.utc),
            payload={"message": content}
        )
