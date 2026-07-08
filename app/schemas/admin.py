from pydantic import BaseModel
from datetime import datetime


class ChannelCreate(BaseModel):
    code: str
    name: str


class ChannelUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class ChannelOut(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserAdminOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    is_active: bool
    role: RoleOut
    created_at: datetime

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role_name: str  # "admin" o "user"


class UserActiveUpdate(BaseModel):
    is_active: bool