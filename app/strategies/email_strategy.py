from datetime import datetime, timezone

from email_validator import EmailNotValidError, validate_email

from app.models.notification import Notification
from app.models.user import User
from app.schemas.delivery import DeliveryResult
from app.strategies.delivery_strategy import DeliveryStrategy


class EmailStrategy(DeliveryStrategy):

    def get_template(
        self,
        notification: Notification
    ):

        template = f"""
        Subject: {notification.title}

        Hello,

        You have received a new notification.

        Title: {notification.title}

        Message:
        {notification.content}

        Regards,
        Notification System
        """
        return template

    def send(
        self,
        notification: Notification,
        user: User
    ) -> DeliveryResult:
        try:
            email = validate_email(
                user.email,
                check_deliverability=False
            ).normalized
        except EmailNotValidError as error:
            raise ValueError("Invalid recipient email") from error

        template = self.get_template(notification)
        print(template)

        return DeliveryResult(
            recipient=email,
            sent_at=datetime.now(timezone.utc),
            payload={
                "subject": notification.title,
                "body": template
            }
        )

