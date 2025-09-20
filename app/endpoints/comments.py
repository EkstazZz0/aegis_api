from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Body, Depends, Query

from app.core.exceptions import (
    comment_forbidden,
    comment_not_found,
    request_forbidden,
    request_not_found,
)
from app.core.utils import check_comment_available, check_request_available, get_payload_from_access_token
from app.db.models import Comment, Request
from app.db.repository import get_comments as db_get_comments
from app.db.session import SessionDep
from app.schemas.comments import CommentCreate, GetComments

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("", response_model=Comment)
async def write_comment(
    session: SessionDep,
    comment_data: CommentCreate,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    request = await session.get(Request, comment_data.request_id)

    if not request:
        raise request_not_found

    if not check_request_available(payload=payload, request=request):
        raise request_forbidden

    comment = Comment(**comment_data.model_dump(), author_id=int(payload['sub']))

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


@router.put("/{comment_id}")
async def edit_comment(
    session: SessionDep,
    comment_id: UUID,
    content: Annotated[str, Body(max_length=500)],
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise comment_not_found

    if not check_comment_available(payload=payload, comment=comment):
        raise comment_forbidden

    comment.content = content

    return comment


@router.get("", response_model=list[Comment])
async def get_comments(
    session: SessionDep,
    filter_data: Annotated[GetComments, Query()],
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    request = await session.get(Request, filter_data.request_id)

    if not request:
        raise request_not_found

    if not check_request_available(payload=payload, request=request):
        raise request_forbidden

    return await db_get_comments(session=session, filter_data=filter_data)


@router.delete("/{comment_id}")
async def delete_comment(
    session: SessionDep,
    comment_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise comment_not_found

    if not check_comment_available(payload=payload, comment=comment):
        raise comment_forbidden

    await session.delete(comment)

    return {"success": True}
