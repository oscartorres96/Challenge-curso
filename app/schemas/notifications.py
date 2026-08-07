from pydantic import BaseModel, ConfigDict, EmailStr


class NotificationCreate(BaseModel):
    title: str
    content: str
    channel: str
    user_id: int


class NotificationsResponse(BaseModel):
    id: int
    title: str
    content: str
    channel: str
    user_id: int

class NotificationsDelete(BaseModel):
    title: str
    content: str
    channel: str
    user_id: int