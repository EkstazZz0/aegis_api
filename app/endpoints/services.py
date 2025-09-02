from fastapi import APIRouter


router = APIRouter(
    prefix="/services",
    tags=["Services"]
)


@router.get("/{service_id}")
async def get_service():
    pass


@router.get("")
async def get_services():
    pass



