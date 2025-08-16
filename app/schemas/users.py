from sqlmodel import SQLModel

class UserPublic(SQLModel):
    id: int
    login: str
    full_name: str
    phone_number: str
    medical_organisation: str
    