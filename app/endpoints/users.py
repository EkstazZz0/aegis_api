from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlmodel import select

from app.core.config import pwd_context
from app.core.enums import UserRole
from app.core.exceptions import (
    forbidden,
    invlaid_change_password,
    medical_organisation_not_found,
    user_not_found,
)
from app.core.utils import check_request_available, get_payload_from_access_token, get_user as get_user_from_payload
from app.db.models import MedicalOrganisation, Request, User, UserSession, ResolverService, Service
from app.db.repository import get_user as db_get_user, update_resolver_services as db_update_resolver_services, get_resolver_services_ids
from app.db.session import SessionDep
from app.schemas.users import (
    AdminChangePassword,
    UserChangePasword,
    UserPublic,
    UserUpdateAdmin,
    UserCreateResolverServices,
    GetUsersFilterData,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/password/me")
async def change_my_password(
    session: SessionDep,
    user: Annotated[User, Depends(get_user_from_payload)],
    password_data: UserChangePasword,
):
    if not pwd_context.verify(password_data.current_password, user.password):
        raise invlaid_change_password

    user_sessions = (
        (
            await session.execute(
                select(UserSession).where(UserSession.user_id == user.id)
            )
        )
        .scalars()
        .all()
    )

    if user_sessions:
        for user_session in user_sessions:
            await session.delete(user_session)

    user.password = pwd_context.hash(password_data.new_password)

    session.add()
    await session.commit()

    return {"success": True}


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
    request_id: int | None = Query(default=None),
):
    if int(payload['sub']) == user_id:
        return await db_get_user(session=session, user_id=user_id)
    
    if payload["role"] == UserRole.customer:
        raise forbidden
    elif payload["role"] == UserRole.resolver:
        request = await session.get(Request, request_id)

        if not request:
            raise forbidden

        if (
            not check_request_available(payload, request)
            or not request.customer_id == user_id
        ):
            raise forbidden

    return await session.get(User, user_id)


@router.get("", response_model=list[UserPublic])
async def get_users(
    session: SessionDep,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
    get_users_data: Annotated[GetUsersFilterData, Query()]
):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    statement = select(User)

    if get_users_data.username:
        statement = statement.where(User.username == get_users_data.username)
    
    if get_users_data.phone_number:
        statement = statement.where(User.phone_number == get_users_data.phone_number)
    
    if get_users_data.full_name:
        substrings = get_users_data.full_name.split(" ")

        for substring in substrings:
            statement = statement.where(User.full_name.ilike(f"%{substring}%"))
    
    if get_users_data.role:
        statement = statement.where(User.role==get_users_data.role)
    
    if get_users_data.active:
        statement = statement.where(User.active == get_users_data.active)
    
    if get_users_data.medical_organisation_id:
        statement = statement.where(User.medical_organisation_id == get_users_data.medical_organisation_id)

    statement = statement.order_by(User.id).limit(get_users_data.limit).offset(get_users_data.offset)

    return (await session.execute(statement)).scalars().all()


@router.patch("/{user_id}", response_model=UserPublic)
async def edit_user(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
    update_data: UserUpdateAdmin,
):
    if payload["role"] != UserRole.admin and int(payload['sub']) != user_id:
        raise forbidden
    if int(payload['sub']) == user_id and update_data.role:
        raise forbidden

    user = await session.get(User, user_id)

    if not user:
        raise user_not_found

    if update_data.medical_organisation_id and not (
        await session.get(MedicalOrganisation, update_data.medical_organisation_id)
    ):
        raise medical_organisation_not_found

    user.sqlmodel_update(update_data.model_dump(exclude_unset=True))

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.put("/{user_id}/status", response_model=UserPublic)
async def change_user_status(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
    active: Annotated[bool, Query()],
):
    if payload["role"] != UserRole.admin:
        raise forbidden

    user = await session.get(User, user_id)

    if not user:
        raise user_not_found

    user.active = active

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.put("/{user_id}/password")
async def change_user_password(
    session: SessionDep,
    user_id: int,
    password_data: AdminChangePassword,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    if payload["role"] != UserRole.admin:
        raise forbidden

    user = await session.get(User, user_id)

    if not user:
        raise user_not_found

    user.password = pwd_context.hash(password_data.new_password)

    session.add(user)
    await session.commit(user)

    return {"success": True}


@router.put("/{user_id}/services")
async def update_resolver_services(
    session: SessionDep,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
    user_id: int,
    service_data: UserCreateResolverServices,
):
    if payload['role'] != UserRole.admin:
        raise forbidden
    
    user = await db_get_user(session=session, user_id=user_id)
    
    if user.role != UserRole.resolver:
        raise forbidden
    
    await db_update_resolver_services(session=session, resolver=user, services_ids=service_data.services_id)

    return {"success": True}

@router.get("/{user_id}/services", response_model=list[Service])
async def get_resolver_services(
    session: SessionDep,
    user_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    if payload['role'] != UserRole.admin:
        raise forbidden
    
    user = await db_get_user(session=session, user_id=user_id)

    if user.role != UserRole.resolver:
        raise forbidden
    
    resolver_services = await get_resolver_services_ids(session=session, user_id=user.id)
    
    return (await session.execute(select(Service).where(Service.id.in_(resolver_services)))).scalars().all()
