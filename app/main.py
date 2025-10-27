from fastapi import FastAPI

from app.core.utils import app_lifespan
from app.endpoints.auth import router as auth_router
from app.endpoints.comments import router as comment_router
from app.endpoints.medical_organisations import router as mo_router
from app.endpoints.requests import router as requests_router
from app.endpoints.services import router as service_router
from app.endpoints.users import router as user_router

app = FastAPI(lifespan=app_lifespan, root_path="/api")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mo_router)
app.include_router(requests_router)
app.include_router(comment_router)
app.include_router(service_router)
