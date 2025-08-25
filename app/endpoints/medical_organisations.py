from fastapi import APIRouter, Query
from sqlmodel import select
from typing import Annotated

from app.db.models import MedicalOrganisation
from app.db.session import SessionDep
from app.schemas.medical_organisations import GetMedicalOrganisations
from app.core.utils import get_payload


router = APIRouter(
    prefix="/medical_organisations",
    tags=["Medical Organisations"]
)


@router.get("/{mo_id}")
async def get_medical_organisation(mo_id: int, session: SessionDep):
    return await session.get(MedicalOrganisation, mo_id)


@router.get("")
async def get_medical_organisations(search_data: Annotated[GetMedicalOrganisations, Query()], session: SessionDep):
    statement = select(MedicalOrganisation)

    if search_data.mo_code:
        statement = statement.where(MedicalOrganisation.mo_code==search_data.mo_code)
    
    if search_data.mo_name:
        substrings = search_data.mo_name.split(" ")

        for substring in substrings:
            statement = statement.where(MedicalOrganisation.mo_name.ilike(f"%{substring}%"))
        
    return (await session.execute(statement)).scalars().all()


@router.patch("")
async def edit_medical_organisation():
    pass


@router.post("")
async def create_medical_organisation():
    pass
