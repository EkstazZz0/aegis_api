from sqlmodel import Field, SQLModel


class GetComments(SQLModel):
    limit: int | None = Field(default=100, gt=0, le=500)
    offset: int | None = Field(default=0, ge=0)
    request_id: int = Field()


class CommentCreate(SQLModel):
    request_id: int
    content: str = Field(max_length=500)
