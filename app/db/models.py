from sqlmodel import SQLModel, Field
from pydantic import field_validator, IPvAnyAddress
from uuid import UUID, uuid4
from datetime import datetime
import re

from app.core.config import refresh_token_expire_time
from app.core.enums import UserRole, RequestStatus
from app.core.exceptions import invalid_phone_number
from app.core.utils import default_expired_at


class MedicalOrganisation(SQLModel, table=True):
    __tablename__ = "medical_organisations"

    id: int | None = Field(default=None, primary_key=True)
    mo_code: int = Field(nullable=False, unique=True, lt=100000000)
    mo_name: str = Field(nullable=False, unique=True, max_length=200)


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, max_length=200)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=15, nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, max_length=60)
    full_name: str = Field(nullable=False, max_length=150)
    phone_number: str = Field(unique=True)
    role: UserRole | None = Field(default=UserRole.customer, nullable=False)
    medical_organisation_id: int = Field(foreign_key="medical_organisations.id", ondelete="SET NULL", nullable=True)


    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        phone_regex = r'^\+79\d{9}$'

        if not re.match(phone_regex, v):
            raise invalid_phone_number
        
        return v


class Request(SQLModel, table=True):
    __tablename__ = "requests"

    id: int | None = Field(default=None, primary_key=True)
    service_id: int = Field(foreign_key="services.id", ondelete="SET NULL", nullable=True)
    customer_id: int = Field(foreign_key="users.id", ondelete="RESTRICT")
    title: str = Field(max_length=60, nullable=False)
    vipnet_node: str = Field(max_length=250, nullable=False)
    description: str = Field(max_length=3000)
    status: RequestStatus | None = Field(default=RequestStatus.pending, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __setattr__(self, name, value):
        if name != 'updated_at' and hasattr(self, name):
            super().__setattr__('updated_at', datetime.now())
        
        return super().__setattr__(name, value)
    
    
    def sqlmodel_update(self, obj, *, update = None):
        self.updated_at = datetime.now()
        return super().sqlmodel_update(obj, update=update)


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    request_id: int = Field(foreign_key="requests.id", ondelete="RESTRICT", nullable=False)
    author_id: int = Field(foreign_key="users.id", ondelete="RESTRICT", nullable=False)
    content: str = Field(max_length=500, nullable=False)


class ResolverScope(SQLModel, table=True):
    __tablename__ = "resolver_scopes"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    service_id: int = Field(foreign_key="services.id", ondelete="CASCADE")


class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    refresh_token: str = Field(unique=True)
    device_id: str = Field(max_length=128)
    fingerprint: str = Field(max_length=256)
    user_agent: str | None = Field(default=None, nullable=True)
    last_login: datetime | None = Field(default_factory=datetime.now)
    expired_at: datetime | None = Field(default_factory=default_expired_at)

    def __setattr__(self, name, value):
        if name != 'last_login' and hasattr(self, name):
            super().__setattr__('last_login', datetime.now())
            super().__setattr__('expired_at', default_expired_at())
        
        return super().__setattr__(name, value)
    
    
    def sqlmodel_update(self, obj, *, update = None):
        self.last_login = datetime.now()
        self.expired_at = default_expired_at()
        return super().sqlmodel_update(obj, update=update)
