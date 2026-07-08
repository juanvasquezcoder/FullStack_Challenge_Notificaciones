from app.models.notification import NotificationStatus as ChannelEnum
from app.services.channels.base import NotificationChannel
from app.services.channels.email_channel import EmailChannel
from app.services.channels.sms_channel import SmsChannel
from app.services.channels.push_channel import PushChannel
from app.services.channels.inapp_channel import InAppChannel


_CHANNEL_MAP: dict[str, NotificationChannel] = {
    "email": EmailChannel(),
    "sms": SmsChannel(),
    "push": PushChannel(),
    "in_app": InAppChannel(),
}


def get_channel_handler(channel: ChannelEnum) -> NotificationChannel:
    handler = _CHANNEL_MAP.get(channel)
    if handler is None:
        raise ValueError(f"No hay handler registrado para el canal: {channel}")
    return handler


def get_channel_handler(code: str) -> NotificationChannel:
    handler = _CHANNEL_MAP.get(code)
    if handler is None:
        raise ValueError(f"No hay handler registrado para el canal: {code}")
    return handler