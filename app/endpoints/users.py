from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.config import oauth2_scheme
from app.core.exceptions import medical_organisation_not_found
from app.core.utils import get_user
from app.db.models import MedicalOrganisation, User
from app.db.session import SessionDep
from app.schemas.users import UserPublic, UserUpdate

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


@router.patch("/{user_id}")
async def edit_user():
    pass


