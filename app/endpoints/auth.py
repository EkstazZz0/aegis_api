from fastapi import APIRouter, status, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from sqlmodel import SQLModel, Field, select
import logging

from app.core.config import secret_key, pwd_context, jwt_algorithm
from app.core.exceptions import user_already_exists, auth_expired_token, medical_organisation_not_found, user_not_found, auth_token_invalid
from app.core.utils import generate_new_token, generate_access_user_data, generate_refresh_user_data, get_payload, generate_resolver_scopes
from app.db.models import User, MedicalOrganisation, UserSession
from app.db.session import SessionDep
from app.db.repository import authenticate_user, get_resolver_services_ids
from app.schemas.users import UserCreate
from app.schemas.auth import NewToken, RefreshToken


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class DeviceHeader(SQLModel):
    device_id: str = Field(max_length=128)
    fingerprint: str | None = Field(default=None, max_length=256)
    user_agent: str = Field(max_length=512)


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

    user_session = (
        await session.execute(
            select(UserSession)
            .where(UserSession.device_id == device_data.device_id)
        )
    ).scalars().first()
    
    token = generate_new_token(
        access_user_data=generate_access_user_data(
            user=user,
            scopes=generate_resolver_scopes(
                services_id=await get_resolver_services_ids(
                    session=session,
                    user_id=user.id
                )
            )
        ),
        refresh_user_data=generate_refresh_user_data(user=user)
    )
    
    if user_session:
        user_session.refresh_token = token.refresh_token

        if user_session.fingerprint != device_data.fingerprint:
            logger.info(f"Fingerprint changed for {user_session.user_id} from {user_session.fingerprint} to {device_data.fingerprint}")
            user_session.fingerprint = device_data.fingerprint
        if user_session.user_agent != device_data.user_agent:
            logger.info(f"User-Agent changed for {user_session.user_id} from {user_session.user_agent} to {user_session.user_agent}")
            user_session.user_agent = device_data.user_agent
    else:
        user_session = UserSession(**device_data.model_dump(), refresh_token=token.refresh_token, user_id=user.id)
    
    session.add(user_session)
    await session.commit()
    await session.refresh(user_session)

    return token


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=NewToken)
async def refresh_token(
    session: SessionDep,
    token_data: RefreshToken,
    device_data: Annotated[DeviceHeader, Header()]
):
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
    
    user = await session.get(User, int(payload["sub"]))

    if not user:
        raise auth_token_invalid
    
    user_session = (
        await session.execute(
            select(UserSession)
            .where(UserSession.refresh_token == token_data.refresh_token)
            .where(UserSession.user_id == user.id)
            .where(UserSession.device_id == device_data.device_id)
        )
    ).scalars().first()

    if not user_session:
        raise auth_token_invalid
    
    if user_session.fingerprint != device_data.fingerprint:
        logger.info(f"Fingerprint changed for {user_session.user_id} from {user_session.fingerprint} to {device_data.fingerprint}")
        user_session.fingerprint = device_data.fingerprint
    if user_session.user_agent != device_data.user_agent:
        logger.info(f"User-Agent changed for {user_session.user_id} from {user_session.user_agent} to {user_session.user_agent}")
        user_session.user_agent = device_data.user_agent
    
    token = generate_new_token(
        access_user_data=generate_access_user_data(
            user=user,
            scopes=generate_resolver_scopes(
                services_id=await get_resolver_services_ids(
                    session=session,
                    user_id=user.id
                )
            )
        ),
        refresh_user_data=generate_refresh_user_data(user=user)
    )
    
    user_session.refresh_token = token.refresh_token

    session.add(user_session)
    await session.commit()
    await session.refresh(user_session)
    
    return token
