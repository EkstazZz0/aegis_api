from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.core.enums import UserRole
from app.core.exceptions import forbidden, service_not_found
from app.core.utils import get_payload
from app.db.models import Service
from app.db.session import SessionDep
from app.schemas.services import GetServiceFilterData, EditService, CreateService

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/{service_id}")
async def get_service(session: SessionDep, service_id: int):
    return await session.get(Service, service_id)


@router.get("", response_model=list[Service])
async def get_services(
    session: SessionDep, filter_data: Annotated[GetServiceFilterData, Query()]
):
    statement = select(Service)

    if filter_data.service_name:
        substrings = filter_data.service_name.split(" ")

        for substring in substrings:
            statement = statement.where(Service.name.ilike(f"%{substring}%"))

    statement = (
        statement.order_by(Service.id)
        .limit(limit=filter_data.limit)
        .offset(offset=filter_data.offset)
    )

    return (await session.execute(statement)).scalars().all()


@router.post("")
async def create_service(
    session: SessionDep,
    payload: Annotated[dict[str, Any], Depends(get_payload)],
    service_data: CreateService
):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    service = Service.model_validate(service_data)

    await session.add(service)
    await session.commit()
    await session.refresh(service)

    return service


@router.delete("/{service_id}")
async def delete_service(
    session: SessionDep,
    service_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload)]
):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    service = await session.get(Service, service_id)

    if not service:
        raise service_not_found
    
    await session.delete(service)
    await session.commit()

    return {"success": True}


@router.put("/{service_id}")
async def edit_service(
    session: SessionDep,
    service_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload)],
    service_data: EditService
):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    service = await session.get(Service, service_id)

    if not service:
        raise service_not_found
    
    service.sqlmodel_update(service_data.model_dump(exclude_unset=True))

    session.add(service)
    await session.commit()
    await session.refresh(service)

    return service
