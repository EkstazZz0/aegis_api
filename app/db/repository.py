from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from app.core.config import pwd_context
from app.core.exceptions import auth_ivalid_credentials
from app.db.models import Comment, ResolverScope, User
from app.db.session import engine
from app.schemas.comments import GetComments


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User:
    user = await get_user_by_login(session=session, username=username)

    if not user or not pwd_context.verify(password, user.password):
        raise auth_ivalid_credentials

    return user


async def get_user_by_login(session: AsyncSession, username: str) -> User | None:
    return (
        (await session.execute(select(User).where(User.username == username)))
        .scalars()
        .first()
    )


async def get_resolver_services_ids(session: AsyncSession, user_id: int) -> list[int]:
    return (
        (
            await session.execute(
                select(ResolverScope.service_id).where(ResolverScope.user_id == user_id)
            )
        )
        .scalars()
        .all()
    )


async def get_comments(
    session: AsyncSession, filter_data: GetComments
) -> list[Comment]:
    return (
        (
            await session.execute(
                select(Comment)
                .where(Comment.request_id == filter_data.request_id)
                .limit(limit=filter_data.limit)
                .offset(offset=filter_data.offset)
            )
        )
        .scalars()
        .all()
    )
