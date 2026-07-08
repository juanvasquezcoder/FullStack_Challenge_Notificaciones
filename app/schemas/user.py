from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True   # permite construir el schema desde un objeto SQLAlchemy


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"