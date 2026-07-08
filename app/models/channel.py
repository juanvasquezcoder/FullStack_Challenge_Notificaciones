from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)   # "email", "sms" — usado internamente por el strategy pattern
    name = Column(String, nullable=False)                 # "Correo electrónico" — para mostrar en UI
    is_active = Column(Boolean, default=True)              # el admin puede desactivar un canal sin borrarlo

    notifications = relationship("Notification", back_populates="channel")