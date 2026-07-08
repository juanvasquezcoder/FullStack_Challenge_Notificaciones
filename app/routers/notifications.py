from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.notification import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationOut, NotificationUpdate
from app.services.notification_service import send_notification

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    data: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_notification = Notification(
        user_id=current_user.id,
        title=data.title,
        message=data.message,
        channel_id=data.channel_id,
        status=NotificationStatus.PENDING,
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    # Se ejecuta DESPUÉS de devolver la respuesta al cliente
    background_tasks.add_task(send_notification, new_notification.id, current_user.id)

    return new_notification

@router.get("/", response_model=list[NotificationOut])
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    unread_only: bool = False,
):
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    if unread_only:
        query = query.filter(Notification.is_read == False)
    return query.order_by(desc(Notification.created_at)).all()

@router.get("/{notification_id}", response_model=NotificationOut)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = _get_owned_notification(notification_id, db, current_user)
    return notification

@router.patch("/{notification_id}", response_model=NotificationOut)
def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = _get_owned_notification(notification_id, db, current_user)
    notification.is_read = data.is_read
    db.commit()
    db.refresh(notification)
    return notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notification = _get_owned_notification(notification_id, db, current_user)
    db.delete(notification)
    db.commit()

def _get_owned_notification(notification_id: int, db: Session, current_user: User) -> Notification:
    """Busca una notificación y verifica que pertenezca al usuario autenticado."""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id,
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    return notification
