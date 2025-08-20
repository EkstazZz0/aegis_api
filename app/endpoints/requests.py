from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID

from app.schemas.requests import RequestCreate
from app.db.session import SessionDep
from app.db.models import User, Service, Request
from app.core.utils import get_user, get_payload
from app.core.exceptions import service_not_found, request_not_available, request_not_found
from app.core.config import oauth2_scheme
from app.core.enums import UserRole

router = APIRouter(
    prefix="/requests",
    tags=["requests"]
)


@router.post("", response_model=Request)
async def create_request(session: SessionDep,
                         request_data: RequestCreate,
                         user: Annotated[User, Depends(get_user)]):
    
    if not await session.get(Service, request_data.service_id):
        raise service_not_found
    
    request = Request(**request_data.model_dump_json(), id=user.id)

    session.add(request)
    await session.commit()
    session.refresh(request)

    return request


@router.get("/{request_id}")
async def get_request(user: Annotated[User, Depends(get_user)], session: SessionDep, request_id: UUID, token: str = Depends(oauth2_scheme)):
    request = await session.get(Request, request_id)

    if not request:
        raise request_not_found

    payload = get_payload(token=token)

    if payload["role"] == UserRole.customer and request.customer_id != user.id:
        raise request_not_available
    elif payload["role"] == UserRole.resolver and not(request.service_id in payload["scopes"]):
        raise request_not_available
    
    return request



