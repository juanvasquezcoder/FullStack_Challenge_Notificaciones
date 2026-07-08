import logging
from app.services.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User

logger = logging.getLogger(__name__)


class SmsChannel(NotificationChannel):
    def send(self, notification: Notification, user: User) -> bool:
        try:
            # TODO: integrar proveedor real (Twilio, etc.)
            # Nota: SMS requiere un campo phone_number en el modelo User
            logger.info(f"[SMS] Enviando a usuario {user.id}: '{notification.title}'")
            return True
        except Exception as e:
            logger.error(f"[SMS] Falló el envío a usuario {user.id}: {e}")
            return False