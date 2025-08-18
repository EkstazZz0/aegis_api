from sqlmodel import SQLModel, Field
from pydantic import field_validator
import re

class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    phone_number: str
    # medical_organisation: str


class UserCreate(SQLModel):
    username: str = Field(max_length=15)
    password: str = Field(max_length=60)
    full_name: str = Field(max_length=150)
    phone_number: str
    # medical_organisation_id: int

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        phone_regex = r'^\+79\d{9}$'

        if not re.match(phone_regex, v):
            raise ValueError("Некорректный номер телефона")
        
        return v
    