from fastapi import FastAPI

from app.endpoints.auth import router as auth_router
from app.endpoints.users import router as user_router
from app.endpoints.medical_organisations import router as mo_router
from app.core.utils import app_lifespan

app = FastAPI(lifespan=app_lifespan)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mo_router)
