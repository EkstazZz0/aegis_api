from sqlmodel import Field, SQLModel


class GetServiceFilterData(SQLModel):
    limit: int | None = Field(default=50, gt=0, le=1000)
    offset: int | None = Field(default=0, ge=0)
    service_name: str | None = Field(default=None, max_length=200)


class ServiceBase(SQLModel):
    name: str = Field(max_length=200)


class EditService(ServiceBase):
    pass


class CreateService(ServiceBase):
    pass
