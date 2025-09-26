from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import select

from app.core.enums import RequestStatus, UserRole
from app.core.exceptions import (request_forbidden, request_not_found,
                                 service_not_found)
from app.core.utils import (check_request_available,
                            get_payload_from_access_token)
from app.db.models import Request, Service
from app.db.session import SessionDep
from app.schemas.requests import GetRequests, RequestCreate

router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("", response_model=Request, status_code=status.HTTP_201_CREATED)
async def create_request(
    session: SessionDep,
    request_data: RequestCreate,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):

    if not await session.get(Service, request_data.service_id):
        raise service_not_found

    request = Request(**request_data.model_dump(), customer_id=payload["sub"])

    session.add(request)
    await session.commit()
    await session.refresh(request)

    return request


@router.get("/{request_id}")
async def get_request(
    session: SessionDep,
    request_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    request = await session.get(Request, request_id)

    if not request:
        raise request_not_found

    if not check_request_available(payload=payload, request=request):
        raise request_forbidden

    return request


@router.get("", response_model=list[Request])
async def get_requests(
    session: SessionDep,
    get_data: Annotated[GetRequests, Query()],
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    statement = select(Request)

    if payload["role"] == UserRole.customer:
        statement = statement.where(Request.customer_id == int(payload["sub"]))
    elif payload["role"] == UserRole.resolver:
        scopes_services_ids = [
            int(scope.split("service:")[1]) for scope in payload["scopes"]
        ]

        filter_service_ids = list(set(scopes_services_ids) & set(get_data.services_id))

        if not filter_service_ids:
            filter_service_ids = scopes_services_ids

        statement = statement.where(Request.service_id.in_(filter_service_ids))
    else:
        if get_data.services_id:
            statement = statement.where(Request.service_id.in_(get_data.services_id))

    if get_data.statuses:
        statement = statement.where(Request.status.in_(get_data.statuses))

    statement = (
        statement.order_by(Request.id)
        .limit(limit=get_data.limit)
        .offset(offset=get_data.offset)
    )

    return (await session.execute(statement)).scalars().all()


@router.put("/status/{request_id}", response_model=Request)
async def change_request_status(
    session: SessionDep,
    request_id: int,
    request_status: Annotated[RequestStatus, Query()],
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    request = await session.get(Request, request_id)

    if not request:
        raise request_not_found

    if (
        payload["role"] == UserRole.customer
        and (
            request_status != RequestStatus.done
            or int(payload["sub"]) != request.customer_id
        )
    ) or (
        payload["role"] == UserRole.resolver
        and not (f"service:{request.service_id}" in payload["scopes"])
    ):
        raise request_forbidden

    request.status = request_status

    session.add(request)
    await session.commit()
    await session.refresh(request)

    return request
