from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.core.enums import UserRole
from app.core.exceptions import (
    forbidden,
    medical_organisation_exists,
    medical_organisation_not_found,
)
from app.core.utils import get_payload_from_access_token
from app.db.models import MedicalOrganisation
from app.db.session import SessionDep
from app.schemas.medical_organisations import (
    CreateMedicalOrganisation,
    EditMedicalOrganisation,
    GetMedicalOrganisations,
)

router = APIRouter(prefix="/medical_organisations", tags=["Medical Organisations"])


@router.get("/{mo_id}")
async def get_medical_organisation(session: SessionDep, mo_id: int):
    return await session.get(MedicalOrganisation, mo_id)


@router.get("", response_model=list[MedicalOrganisation])
async def get_medical_organisations(
    session: SessionDep, search_data: Annotated[GetMedicalOrganisations, Query()]
):
    statement = select(MedicalOrganisation)

    if search_data.mo_code:
        statement = statement.where(MedicalOrganisation.mo_code == search_data.mo_code)

    if search_data.mo_name:
        substrings = search_data.mo_name.split(" ")

        for substring in substrings:
            statement = statement.where(
                MedicalOrganisation.mo_name.ilike(f"%{substring}%")
            )

    statement = (
        statement.order_by(MedicalOrganisation.id)
        .limit(limit=search_data.limit)
        .offset(offset=search_data.offset)
    )

    return (await session.execute(statement)).scalars().all()


@router.patch("/{mo_id}")
async def edit_medical_organisation(
    session: SessionDep,
    mo_id: int,
    update_data: EditMedicalOrganisation,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):

    if payload["role"] != UserRole.admin:
        raise forbidden

    medical_organisation = await session.get(MedicalOrganisation, mo_id)

    if not medical_organisation:
        raise medical_organisation_not_found

    medical_organisation.sqlmodel_update(update_data.model_dump(exclude_unset=True))

    session.add(medical_organisation)

    try:
        await session.commit()
    except IntegrityError:
        raise medical_organisation_exists

    await session.refresh(medical_organisation)

    return medical_organisation


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_medical_organisation(
    session: SessionDep,
    create_data: CreateMedicalOrganisation,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):
    if payload["role"] != UserRole.admin:
        raise forbidden

    medical_organisation = MedicalOrganisation.model_validate(create_data)
    session.add(medical_organisation)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise medical_organisation_exists

    await session.refresh(medical_organisation)
    return medical_organisation


@router.delete("/{mo_id}")
async def delete_medical_organisation(
    session: SessionDep,
    mo_id: int,
    payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)],
):

    if payload["role"] != UserRole.admin:
        raise forbidden

    medical_organisation = await session.get(MedicalOrganisation, mo_id)

    if not medical_organisation:
        raise medical_organisation_not_found

    await session.delete(medical_organisation)
    await session.commit()

    return {"success": True}
