from app.services.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User


class InAppChannel(NotificationChannel):
    def send(self, notification: Notification, user: User) -> bool:
        # Para in-app no hay "envío" real: ya está guardada en BD desde que se creó.
        # Simplemente confirmamos que existe.
        return True