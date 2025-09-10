from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.config import oauth2_scheme
from app.core.exceptions import medical_organisation_not_found, forbidden, user_not_found
from app.core.utils import get_user, get_payload, check_request_available
from app.core.enums import UserRole
from app.db.models import MedicalOrganisation, User, Request
from app.db.session import SessionDep
from app.schemas.users import UserPublic, UserUpdate, UserUpdateAdmin

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def get_my_user(user: Annotated[User, Depends(get_user)]):
    return user


@router.patch("/me", response_model=UserPublic)
async def edit_my_user(
    session: SessionDep,
    user: Annotated[User, Depends(get_user)],
    update_data: UserUpdate,
):
    if update_data.medical_organisation_id and not (
        await session.get(MedicalOrganisation, update_data.medical_organisation_id)
    ):
        raise medical_organisation_not_found

    user.sqlmodel_update(update_data.model_dump(exclude_unset=True))

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/password/me")
async def change_my_password(
    sesion: SessionDep,
    user: Annotated[User, Depends(get_user)]
):
    pass


@router.get("/{user_id}")
async def get_user(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload)],
    request_id: Annotated[int | None, Query()]
):
    if payload["role"] == UserRole.customer:
        raise forbidden
    elif payload["role"] == UserRole.resolver:
        request = await session.get(Request, request_id)

        if not request:
            raise forbidden
        
        if not check_request_available(payload, request) or not request.customer_id == user_id:
            raise forbidden


    return await session.get(User, user_id)


@router.patch("/{user_id}", response_model=UserPublic)
async def edit_user(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload)],
    update_data: UserUpdate
):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    user = await session.get(User, user_id)

    if not user:
        raise user_not_found

    if update_data.medical_organisation_id and not(
        await session.get(MedicalOrganisation, update_data.medical_organisation_id)
    ):
        raise medical_organisation_not_found
    
    user.sqlmodel_update(update_data.model_dump(exclude_unset=True))

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
