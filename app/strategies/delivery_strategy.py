from abc import ABC, abstractmethod

from app.models.notification import Notification
from app.models.user import User
from app.schemas.delivery import DeliveryResult


class DeliveryStrategy(ABC):

    @abstractmethod
    def send(
        self,
        notification: Notification,
        user: User
    ) -> DeliveryResult:
        pass
