from fastapi import APIRouter, status, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from sqlmodel import SQLModel, Field, select

from app.core.config import secret_key, pwd_context, jwt_algorithm
from app.core.exceptions import user_already_exists, auth_expired_token, auth_token_invalid, medical_organisation_not_found, user_not_found, session_not_found
from app.core.utils import generate_new_token, generate_access_user_data, generate_refresh_user_data, get_payload
from app.db.models import User, MedicalOrganisation, UserSession
from app.db.session import SessionDep
from app.db.repository import authenticate_user, get_user_scopes, get_user_by_login
from app.schemas.users import UserCreate
from app.schemas.auth import NewToken, RefreshToken


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class DeviceHeader(SQLModel):
    device_id: str = Field(max_length=128)
    fingerprint: str = Field(max_length=256)
    user_agent: str | None = Field(default=None, max_length=512)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def registration(session: SessionDep, create_user_data: UserCreate):
    if not await session.get(MedicalOrganisation, create_user_data.medical_organisation_id):
        raise medical_organisation_not_found

    user = User.model_validate(create_user_data)
    user.password = pwd_context.hash(user.password)
    
    session.add(user)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise user_already_exists
    
    await session.refresh(user)

    return {"success": True}


@router.post("", status_code=status.HTTP_200_OK, response_model=NewToken)
async def authentication(session: SessionDep,
                         form: Annotated[OAuth2PasswordRequestForm, Depends()],
                         device_data: Annotated[DeviceHeader, Header()]):
    user = await authenticate_user(session=session, username=form.username, password=form.password)

    user_session = (await session.execute(select(UserSession)
                                         .where(UserSession.device_id == device_data.device_id)
                                         .where(UserSession.fingerprint == device_data.fingerprint)
                                         .where(UserSession.user_agent == device_data.user_agent))).scalars().first()
    
    token = generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
        )
    
    if user_session:
        user_session.refresh_token = token.refresh_token
    else:
        user_session = UserSession(**device_data.model_dump_json(), refresh_token=token.refresh_token, user_id=user.id)
    
    session.add(user_session)
    await session.commit()
    await session.refresh(user_session)

    return token


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=NewToken)
async def refresh_token(session: SessionDep, token_data: RefreshToken):
    try:
        payload = get_payload(token_data.refresh_token)
    except HTTPException as e:
        if e == auth_expired_token:
            user_session = (
                await session.execute(
                    select(UserSession).where(UserSession.refresh_token == token_data.refresh_token)
                )
            ).scalars().first()

            if user_session:
                await session.delete(user_session)
                await session.commit()
        
        raise e
    
    user = await get_user_by_login(session=session, username=payload["sub"])

    if not user:
        user_not_found_401 = user_not_found
        user_not_found_401.status_code = status.HTTP_401_UNAUTHORIZED
        raise user_not_found_401
    
    user_session = (
        await session.execute(
            select(UserSession)
            .where(UserSession.refresh_token == token_data.refresh_token)
            .where(UserSession.user_id == user.id)
        )
    ).scalars().first()

    if not user_session:
        raise session_not_found
    
    token = generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
    )
    
    user_session.refresh_token = token.refresh_token

    session.add(user_session)
    await session.commit()
    await session.refresh(user_session)
    
    return token
