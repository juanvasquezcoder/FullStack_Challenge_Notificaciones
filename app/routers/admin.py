from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db, require_admin
from app.models.user import User
from app.models.role import Role
from app.models.channel import Channel
from app.schemas.admin import (
    ChannelCreate, ChannelUpdate, ChannelOut,
    UserAdminOut, UserRoleUpdate, UserActiveUpdate,
)

router = APIRouter(prefix="/admin", tags=["admin"])


# ---------- Canales ----------

@router.get("/channels", response_model=list[ChannelOut])
def list_all_channels(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(Channel).all()


@router.post("/channels", response_model=ChannelOut, status_code=status.HTTP_201_CREATED)
def create_channel(data: ChannelCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if db.query(Channel).filter(Channel.code == data.code).first():
        raise HTTPException(status_code=400, detail="Ya existe un canal con ese código")
    channel = Channel(code=data.code, name=data.name)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel


@router.patch("/channels/{channel_id}", response_model=ChannelOut)
def update_channel(channel_id: int, data: ChannelUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Canal no encontrado")
    if data.name is not None:
        channel.name = data.name
    if data.is_active is not None:
        channel.is_active = data.is_active
    db.commit()
    db.refresh(channel)
    return channel


@router.delete("/channels/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Canal no encontrado")
    db.delete(channel)
    db.commit()


# ---------- Usuarios ----------

@router.get("/users", response_model=list[UserAdminOut])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).all()


@router.patch("/users/{user_id}/active", response_model=UserAdminOut)
def toggle_user_active(user_id: int, data: UserActiveUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return user


@router.patch("/users/{user_id}/role", response_model=UserAdminOut)
def change_user_role(user_id: int, data: UserRoleUpdate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    role = db.query(Role).filter(Role.name == data.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Rol '{data.role_name}' no existe")

    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()