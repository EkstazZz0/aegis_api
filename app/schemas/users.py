import re

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from app.core.exceptions import invalid_phone_number
from app.core.enums import UserRole

class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    phone_number: str
    medical_organisation_id: int


class UserCreate(SQLModel):
    username: str = Field(max_length=15)
    password: str = Field(max_length=60)
    full_name: str = Field(max_length=150)
    phone_number: str
    medical_organisation_id: int

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        phone_regex = r"^\+79\d{9}$"

        if not re.match(phone_regex, v):
            raise invalid_phone_number

        return v


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=150)
    phone_number: str | None = Field(default=None)
    medical_organisation_id: int | None = Field(default=None)

    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        phone_regex = r"^\+79\d{9}$"

        if not re.match(phone_regex, v) and v:
            raise invalid_phone_number

        return v


class UserUpdateAdmin(UserUpdate):
    active: bool
    password: str = Field(max_length=60)


class UserPublicAdmin(UserPublic):
    active: bool
    role: UserRole
