from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DeliveryResult(BaseModel):
    recipient: str
    sent_at: datetime
    status: str | None = None
    payload: dict[str, Any] | None = None

class DeliveryResponse(BaseModel):
    channel: str
    recipient: str
    sent_at: datetime
    status: str | None = None
    payload: dict | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
