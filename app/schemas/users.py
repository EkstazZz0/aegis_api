import re

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.core.exceptions import invalid_phone_number
from app.core.enums import UserRole
from app.schemas.custom_fields import PhoneNumber, Password

class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    phone_number: str
    medical_organisation_id: int
    active: bool
    role: UserRole


class UserCreate(SQLModel):
    username: str = Field(max_length=15)
    password: Password
    full_name: str = Field(max_length=150)
    phone_number: PhoneNumber
    medical_organisation_id: int


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=150)
    phone_number: PhoneNumber | None = Field(default=None)
    medical_organisation_id: int | None = Field(default=None)


class AdminChangePassword(SQLModel):
    new_password: Password


class UserChangePasword(AdminChangePassword):
    current_password: str = Field(min_length=8, max_length=256)
