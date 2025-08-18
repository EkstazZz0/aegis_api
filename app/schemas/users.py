from sqlmodel import SQLModel

class UserPublic(SQLModel):
    id: int
    username: str
    full_name: str
    phone_number: str
    medical_organisation: str


class UserCreate(SQLModel):
    username: str
    full_name: str
    phone_number: str
    medical_organisation_id: int
    