import logging
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationStatus
from app.models.user import User
from app.services.channels.registry import get_channel_handler
from app.database import SessionLocal

logger = logging.getLogger(__name__)


def send_notification(notification_id: int, user_id: int):
    """
    Se ejecuta en background: abre su propia sesión de BD
    (no puede reusar la del request, que ya se cerró),
    envía por el canal correspondiente y actualiza el status.
    """
    db: Session = SessionLocal()
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        user = db.query(User).filter(User.id == user_id).first()

        if not notification or not user:
            logger.error(f"No se encontró notification={notification_id} o user={user_id}")
            return

        # handler = get_channel_handler(notification.channel)
        handler = get_channel_handler(notification.channel.code)
        success = handler.send(notification, user)

        notification.status = NotificationStatus.SENT if success else NotificationStatus.FAILED
        if success:
            from datetime import datetime
            notification.sent_at = datetime.utcnow()

        db.commit()

    except Exception as e:
        logger.error(f"Error enviando notification={notification_id}: {e}")
        db.rollback()
    finally:
        db.close()