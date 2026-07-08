import logging
from app.services.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User

logger = logging.getLogger(__name__)


class EmailChannel(NotificationChannel):
    def send(self, notification: Notification, user: User) -> bool:
        try:
            # TODO: integrar proveedor real (SendGrid, SMTP, SES, etc.)
            logger.info(f"[EMAIL] Enviando a {user.email}: '{notification.title}'")
            return True
        except Exception as e:
            logger.error(f"[EMAIL] Falló el envío a {user.email}: {e}")
            return False