from sqlmodel import SQLModel, Field


class RequestCreate(SQLModel):
    service_id: int = Field()
    tutle: str = Field(max_length=300)
    vipnet_node: str = Field(max_length=250)
    description: str = Field(max_length=3000)
