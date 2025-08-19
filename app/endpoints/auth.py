from fastapi import APIRouter, status, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from typing import Annotated
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import secret_key, pwd_context, jwt_algorithm
from app.core.exceptions import user_already_exists, auth_expired_token, auth_token_invalid, medical_organisation_not_found, user_not_found
from app.core.utils import generate_new_token, generate_access_user_data, generate_refresh_user_data, get_payload
from app.db.models import User, MedicalOrganisation
from app.db.session import SessionDep
from app.db.repository import authenticate_user, get_user_scopes, get_user_by_login
from app.schemas.users import UserPublic, UserCreate
from app.schemas.auth import NewToken, RefreshToken


router = APIRouter(
    prefix="/auth"
)


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
async def authentication(session: SessionDep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(session=session, username=form.username, password=form.password)

    return generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
        )


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=NewToken)
async def refresh_token(session: SessionDep, token_data: RefreshToken):
    payload = get_payload(token_data.refresh_token)
    
    user = await get_user_by_login(session=session, username=payload["sub"])

    if not user:
        raise user_not_found
    
    return generate_new_token(
        access_user_data=generate_access_user_data(user=user, scopes=(await get_user_scopes(session=session, user_id=user.id))),
        refresh_user_data=generate_refresh_user_data(user=user)
    )
