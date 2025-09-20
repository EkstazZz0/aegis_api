from sqlmodel import Field, SQLModel

from app.core.enums import UserRole
from app.schemas.custom_fields import Password, PhoneNumber, Username


class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    phone_number: str
    medical_organisation_id: int
    active: bool
    role: UserRole


class GetUsersFilterData(SQLModel):
    limit: int | None = Field(default=50, gt=0, le=100)
    offset: int | None = Field(default=0, ge=0)
    username: Username | None = Field(default=None)
    phone_number: PhoneNumber | None = Field(default=None)
    full_name: str | None = Field(default=None, max_length=150)
    role: UserRole | None = Field(default=None)
    active: bool | None = Field(default=None)
    medical_organisation_id: int | None = Field(default=None)


class UserCreate(SQLModel):
    username: Username
    password: Password
    full_name: str = Field(max_length=150)
    phone_number: PhoneNumber
    medical_organisation_id: int


class UserUpdate(SQLModel):
    full_name: str | None = Field(default=None, max_length=150)
    phone_number: PhoneNumber | None = Field(default=None)
    medical_organisation_id: int | None = Field(default=None)


class UserUpdateAdmin(UserUpdate):
    role: UserRole | None = Field(default=None)


class AdminChangePassword(SQLModel):
    new_password: Password


class UserChangePasword(AdminChangePassword):
    current_password: str = Field(min_length=8, max_length=256)


class UserCreateResolverServices(SQLModel):
    services_id: list[int] = Field()
