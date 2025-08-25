from sqlmodel import SQLModel, Field


class GetMedicalOrganisations():
    limit: int | None = Field(default=50, le=100, gt=0)
    offset: int | None = Field(default=0, ge=0)
    mo_code: int | None = Field()
    mo_name: str | None = Field(max_length=200)
