from fastapi import APIRouter, Query, Depends, Body
from typing import Annotated, Any

from app.core.exceptions import request_not_found, comment_not_found, comment_forbidden, request_forbidden
from app.core.utils import get_payload, check_request_available, check_comment_available
from app.core.enums import UserRole
from app.schemas.comments import GetComments, CommentPublic, CommentCreate
from app.db.session import SessionDep
from app.db.repository import get_comments as db_get_comments
from app.db.models import Request, Comment


router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@router.post("", response_model=Comment)
async def write_comment(session: SessionDep,
                        comment_data: CommentCreate,
                        payload: Annotated[dict[str, Any], Depends(get_payload)]):
    request = await session.get(Request, comment_data.request_id)

    if not request:
        raise request_not_found
    
    if not check_request_available(payload=payload, request=request):
        raise request_forbidden

    comment = Comment.model_validate(**comment_data.model_dump_json())

    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


@router.put("/{comment_id}")
async def edit_comment(session: SessionDep,
                       comment_id: int,
                       content: Annotated[str, Body(max_length=500)],
                       payload: Annotated[dict[str, Any], Depends(get_payload)]):
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise comment_not_found
    
    if not check_comment_available(
        payload=payload,
        comment=comment
    ):
        raise comment_forbidden
    
    comment.content = content

    return comment


@router.get("", response_model=list[Comment])
async def get_comments(session: SessionDep,
                       filter_data: Annotated[GetComments, Query()],
                       payload: Annotated[dict[str, Any], Depends(get_payload)]):
    request = await session.get(Request, filter_data.request_id)

    if not request:
        raise request_not_found

    if not check_request_available(payload=payload, request=request):
        raise request_forbidden
         
    return await db_get_comments(session=session, filter_data=filter_data)


@router.delete("/{comment_id}")
async def delete_comment(session: SessionDep,
                         comment_id: int,
                         payload: Annotated[dict[str, Any], Depends(get_payload)]):
    comment = await session.get(Comment, comment_id)

    if not comment:
        raise comment_not_found
    
    if not check_comment_available(
        payload=payload,
        comment=comment
    ):
        raise comment_forbidden
    
    await session.delete(comment)

    return {"success": True}
