from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from app.core.config import pwd_context
from app.core.exceptions import auth_ivalid_credentials, user_not_found
from app.db.models import Comment, ResolverService, Service, User
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


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = await session.get(User, user_id)

    if not user:
        raise user_not_found

    return user


async def get_resolver_services_ids(session: AsyncSession, user_id: int) -> list[int]:
    return (
        (
            await session.execute(
                select(ResolverService.service_id).where(
                    ResolverService.user_id == user_id
                )
            )
        )
        .scalars()
        .all()
    )


async def update_resolver_services(
    session: AsyncSession, resolver: User, services_ids: list[int]
):
    db_services_ids = await get_resolver_services_ids(
        session=session, user_id=resolver.id
    )

    to_delete_services = set(db_services_ids) - set(services_ids)
    to_add_services = set(services_ids) - set(db_services_ids)

    for to_delete_service in to_delete_services:
        await session.delete(
            (
                await session.execute(
                    select(ResolverService)
                    .where(ResolverService.service_id == to_delete_service)
                    .where(ResolverService.user_id == resolver.id)
                )
            )
            .scalars()
            .first()
        )

    for to_add_service in to_add_services:
        service = await session.get(Service, to_add_service)

        if not service:
            continue

        session.add(ResolverService(user_id=resolver.id, service_id=to_add_service))

    await session.commit()


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
