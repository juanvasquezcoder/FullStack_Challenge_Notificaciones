from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.channel import Channel
from app.schemas.admin import ChannelOut

router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("/", response_model=list[ChannelOut])
def list_active_channels(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(Channel).filter(Channel.is_active == True).all()