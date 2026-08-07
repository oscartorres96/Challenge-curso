from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, index=True)

    notification_id = Column(
        Integer,
        ForeignKey("notifications.id"),
        nullable=False,
        index=True,
    )

    channel = Column(String(50), nullable=False)
    recipient = Column(String(255), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=True)
    payload = Column(JSON, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
