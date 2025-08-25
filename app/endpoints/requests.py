from fastapi import APIRouter, Depends, Query
from typing import Annotated, Any
from uuid import UUID
from sqlmodel import select

from app.schemas.requests import RequestCreate, GetRequests
from app.db.session import SessionDep
from app.db.models import Service, Request
from app.core.utils import get_payload, check_request_available
from app.core.exceptions import service_not_found, request_not_found
from app.core.enums import UserRole

router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@router.post("", response_model=Request)
async def create_request(session: SessionDep,
                         request_data: RequestCreate,
                         payload: Annotated[dict[str, Any], Depends(get_payload)]):
    
    if not await session.get(Service, request_data.service_id):
        raise service_not_found
    
    request = Request(**request_data.model_dump_json(), id=payload["user_id"])

    session.add(request)
    await session.commit()
    await session.refresh(request)

    return request


@router.get("/{request_id}")
async def get_request(session: SessionDep, request_id: UUID, payload: Annotated[dict[str, Any], Depends(get_payload)]):
    request = await session.get(Request, request_id)

    if not request:
        raise request_not_found

    check_request_available(payload=payload, request=request)
    
    return request


@router.get("", response_model=list[Request])
async def get_requests(session: SessionDep, get_data: Annotated[GetRequests, Query()], payload: Annotated[dict[str, Any], Depends(get_payload)]):
    statement = select(Request).limit(limit=get_data.limit).offset(offset=get_data.offset)

    if payload["role"] == UserRole.customer:
        statement = statement.where(Request.customer_id == payload["user_id"])
    elif payload["role"] == UserRole.resolver:
        statement = statement.where(Request.service_id.in_(list(set(payload["scopes"]) & set(get_data.services_id))))
    else:
        if get_data.services_id:
            statement = statement.where(Request.service_id.in_(get_data.services_id))

    if get_data.statuses:
        statement = statement.where(Request.status.in_(get_data.statuses))
    
    return (await session.execute(statement)).scalars().all()
