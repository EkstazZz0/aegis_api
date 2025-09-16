from datetime import datetime

from sqlmodel import Field, SQLModel

from app.core.enums import RequestStatus


class RequestCreate(SQLModel):
    service_id: int = Field()
    title: str = Field(max_length=300)
    vipnet_node: str = Field(max_length=250)
    description: str = Field(max_length=3000)


class GetRequests(SQLModel):
    limit: int | None = Field(default=50, gt=0, le=100)
    offset: int | None = Field(default=0, ge=0)
    statuses: list[RequestStatus] | None = Field(default=[])
    services_id: list[int] | None = Field(default=[])
