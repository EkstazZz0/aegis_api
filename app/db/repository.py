from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine
from app.db.models import User, ResolverScope
from app.core.config import pwd_context
from app.core.exceptions import auth_ivalid_credentials_exception


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all())


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User:
    user = (await session.execute(select(User).where(User.username == username))).scalars().first()
    
    if not user or not pwd_context.verify(password, user.password):
        raise auth_ivalid_credentials_exception
    
    return user


async def get_user_scopes(session: AsyncSession, user_id: int):
    return (await session.execute(select(ResolverScope.service_id).where(ResolverScope.user_id == user_id))).scalars().all()
