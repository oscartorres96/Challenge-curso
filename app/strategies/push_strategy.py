from datetime import datetime, timezone

from app.models.notification import Notification
from app.models.user import User
from app.schemas.delivery import DeliveryResult
from app.strategies.delivery_strategy import DeliveryStrategy


class PushStrategy(DeliveryStrategy):

    def send(
        self,
        notification: Notification,
        user: User
    ) -> DeliveryResult:
        if not user.device_token or not user.device_token.strip():
            raise ValueError("User does not have a valid device token")

        payload = {
            "title": notification.title,
            "body": notification.content
        }

        print(
            f"Enviando PUSH al token {user.device_token}: "
            f"{payload}"
        )

        return DeliveryResult(
            recipient=user.device_token,
            sent_at=datetime.now(timezone.utc),
            status="sent",
            payload=payload
        )
