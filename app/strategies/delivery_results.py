from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DeliveryResult:
    recipient: str
    sent_at: datetime
    status: str | None = None
    payload: dict[str, Any] | None = None 
