import jwt
from datetime import datetime
import copy
from fastapi import FastAPI
import os

from app.schemas.auth import NewToken
from app.core.config import access_token_expire_time, refresh_token_expire_time, jwt_algorithm, secret_key, app_env
from app.core.enums import UserRole
from app.db.models import User
from app.db.session import engine
from app.db.repository import init_db


async def app_lifespan(app: FastAPI):
    await init_db()
    yield
    if app_env == "test":
        await engine.dispose()
        os.unlink("./test.db")


def generate_new_token(access_user_data: dict, refresh_user_data: dict) -> NewToken:
    access_token_data = copy.deepcopy(access_user_data)
    access_token_data.update({"exp": datetime.now() + access_token_expire_time})

    refresh_token_data = copy.deepcopy(refresh_user_data)
    refresh_token_data.update({"exp": datetime.now() + refresh_token_expire_time})
    return NewToken(
        access_token=jwt.encode(access_token_data, secret_key, jwt_algorithm),
        refresh_token=jwt.encode(refresh_token_data, secret_key, jwt_algorithm)
        )


def generate_access_user_data(user: User, scopes: list[int]):
    if user.role == UserRole.resolver:
        return {
            "sub": user.username,
            "role": user.role,
            "scopes": scopes
        }
    else:
        return {
            "sub": user.username,
            "role": user.role
        }


def generate_refresh_user_data(user: User):
    return {
        "sub": user.username
    }
