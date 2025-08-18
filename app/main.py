from fastapi import FastAPI

from app.endpoints.auth import router as auth_router
from app.core.utils import app_lifespan

app = FastAPI(lifespan=app_lifespan)

app.include_router(auth_router)
