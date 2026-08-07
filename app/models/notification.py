from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(String(600), nullable=False)
    channel = Column(String(100), nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )