import logging
from app.services.channels.base import NotificationChannel
from app.models.notification import Notification
from app.models.user import User

logger = logging.getLogger(__name__)


class PushChannel(NotificationChannel):
    def send(self, notification: Notification, user: User) -> bool:
        try:
            # TODO: integrar con el WebSocket manager (Paso 7) o un proveedor push real
            logger.info(f"[PUSH] Enviando a usuario {user.id}: '{notification.title}'")
            return True
        except Exception as e:
            logger.error(f"[PUSH] Falló el envío a usuario {user.id}: {e}")
            return False