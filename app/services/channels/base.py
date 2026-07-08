from abc import ABC, abstractmethod
from app.models.notification import Notification
from app.models.user import User


class NotificationChannel(ABC):
    """Interfaz que todo canal de notificación debe implementar."""

    @abstractmethod
    def send(self, notification: Notification, user: User) -> bool:
        """
        Envía la notificación por este canal.
        Devuelve True si el envío fue exitoso, False si falló.
        """
        raise NotImplementedError