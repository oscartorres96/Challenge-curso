from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryResult


class DeliveryRepository:

    @staticmethod
    def create(
        db: Session,
        notification_id: int,
        channel: str,
        result: DeliveryResult
    ) -> Delivery:
        delivery = Delivery(
            notification_id=notification_id,
            channel=channel,
            recipient=result.recipient,
            sent_at=result.sent_at,
            status=result.status,
            payload=result.payload
        )

        db.add(delivery)
        db.commit()
        db.refresh(delivery)

        return delivery

    @staticmethod
    def get_all_deliveries(
        db: Session
    ):
        return db.query(Delivery).all()
