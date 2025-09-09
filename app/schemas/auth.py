from sqlmodel import Field, SQLModel


class NewToken(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer", const=True)


class LoginForm(SQLModel):
    login: str = Field()
    password: str = Field()


class RefreshToken(SQLModel):
    refresh_token: str
