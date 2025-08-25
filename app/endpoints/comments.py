from fastapi import APIRouter, Query, Depends
from typing import Annotated, Any

from app.core.exceptions import request_not_found, comment_not_found
from app.core.utils import get_payload, check_request_available
from app.core.enums import UserRole
from app.schemas.comments import GetComments, CommentPublic, CommentCreate
from app.db.session import SessionDep
from app.db.repository import get_comments as db_get_comments
from app.db.models import Request, Comment


router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@router.post("", response_model=CommentPublic)
async def write_comment(comment_data: CommentCreate, payload: Annotated[dict[str, Any], Depends(get_payload)], session: SessionDep):
    request = await session.get(Request, comment_data.request_id)

    if not request:
        raise request_not_found
    
    check_request_available(payload=payload, request=request)

    comment = Comment.model_validate(**comment_data.model_dump_json())

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


@router.get("", response_model=list[CommentPublic])
async def get_comments(filter_data: Annotated[GetComments, Query()], payload: Annotated[dict[str, Any], Depends(get_payload)], session: SessionDep):
    request = await session.get(Request, filter_data.request_id)

    if not request:
        raise request_not_found

    check_request_available(payload=payload, request=request)
         
    return await db_get_comments(session=session, filter_data=filter_data)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, session: SessionDep):
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise comment_not_found
    
    await session.delete(comment)
