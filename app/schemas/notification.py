from pydantic import BaseModel
from datetime import datetime
# from app.models.notification import NotificationChannel, NotificationStatus
from app.models.notification import NotificationStatus
from app.schemas.admin import ChannelOut


class NotificationCreate(BaseModel):
    title: str
    message: str
    channel_id: int


class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    channel: ChannelOut
    status: NotificationStatus
    is_read: bool
    created_at: datetime
    sent_at: datetime | None

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: bool