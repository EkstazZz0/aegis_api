from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app.core.config import secret_key
from app.db.models import User
from app.db.session import SessionDep


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="auth"
)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=User)
async def registration(session: SessionDep, user: User):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"provided login is busy")
    
    await session.refresh(user)
    return user


@router.post("")
async def authentication():
    pass
