from fastapi import APIRouter, status, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from typing import Annotated
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import secret_key, pwd_context, jwt_algorithm
from app.core.exceptions import user_already_exists, auth_expired_token, auth_token_invalid
from app.core.utils import generate_new_token, generate_access_user_data, generate_refresh_user_data
from app.db.models import User
from app.db.session import SessionDep
from app.db.repository import authenticate_user, get_user_scopes, get_user_by_login
from app.schemas.users import UserPublic
from app.schemas.auth import NewToken


router = APIRouter(
    prefix="auth"
)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def registration(session: SessionDep, user: User):
    user.password = pwd_context.hash(user.password)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise user_already_exists
    
    await session.refresh(user)
    return user


@router.post("", status_code=status.HTTP_200_OK, response_model=NewToken)
async def authentication(session: SessionDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(session=session, username=form.username, password=form.password)

    return generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
        )


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=NewToken)
async def refresh_token(session: SessionDep, refresh_token: str = Body()):
    try:
        payload = jwt.decode(refresh_token, secret_key, jwt_algorithm)
    except ExpiredSignatureError:
        raise auth_expired_token
    except InvalidTokenError:
        raise auth_token_invalid
    
    user = await get_user_by_login(session=session, username=payload["sub"])
    
    return generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
    )
