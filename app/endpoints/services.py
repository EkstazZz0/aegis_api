from fastapi import APIRouter, Query, Depends
from typing import Annotated, Any
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionDep
from app.db.models import Service
from app.schemas.services import GetServiceFilterData
from app.core.utils import get_payload
from app.core.exceptions import forbidden
from app.core.enums import UserRole

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/{service_id}")
async def get_service(session: SessionDep, service_id: int):
    return await session.get(Service, service_id)


@router.get("", response_model=list[Service])
async def get_services(session: SessionDep, filter_data: Annotated[GetServiceFilterData, Query()]):
    statement = select(Service)

    if filter_data.service_name:
        substrings = filter_data.service_name.split(" ")

        for substring in substrings:
            statement = statement.where(
                Service.name.ilike(f"%{substring}%")
            )
    
    statement = (
        statement.order_by(Service.id)
        .limit(limit=filter_data.limit)
        .offset(offset=filter_data.offset)
    )

    return (await session.execute(statement)).scalars().all()



@router.post("")
async def create_service(session: SessionDep, payload: Annotated[dict[str, Any], Depends(get_payload)]):
    if payload["role"] != UserRole.admin:
        raise forbidden
    
    


@router.delete("/{service_id}")
async def delete_service():
    pass

@router.put("/{service_id}")
async def edit_service():
    pass
