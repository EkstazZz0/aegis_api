import copy
import os
from datetime import datetime
from typing import Annotated, Any

import jwt
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import (
    access_token_expire_time,
    app_env,
    jwt_algorithm,
    oauth2_scheme,
    refresh_token_expire_time,
    secret_key,
)
from app.core.enums import UserRole
from app.core.exceptions import (
    auth_expired_token,
    auth_token_invalid,
    request_forbidden,
    auth_wrong_token_provided,
)
from app.db.models import Comment, Request, User
from app.db.repository import init_db
from app.db.session import SessionDep, engine
from app.migrations.insert_preset_data import set_preset_data
from app.schemas.auth import NewToken


async def app_lifespan(app: FastAPI):
    await init_db()
    await set_preset_data()
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
        refresh_token=jwt.encode(refresh_token_data, secret_key, jwt_algorithm),
    )


def generate_access_user_data(user: User, scopes: list[str]):
    user_data = {"sub": str(user.id), "role": user.role, "token_type": "access"}

    if user.role == UserRole.resolver:
        user_data.update({"scopes": scopes})
        return user_data
    elif user.role == UserRole.admin:
        user_data.update({"scopes": ["*"]})
        return user_data
    else:
        return user_data


def generate_refresh_user_data(user: User):
    return {
        "sub": str(user.id),
        "token_type": "refresh"
    }


def generate_resolver_scopes(services_id: list[int]):
    return [f"service:{service_id}" for service_id in services_id]


def get_payload(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> dict[str, Any]:
    if isinstance(token, HTTPAuthorizationCredentials):
        token = token.credentials
    try:
        print(jwt.decode(token, secret_key, jwt_algorithm))
        return jwt.decode(token, secret_key, jwt_algorithm)
    except ExpiredSignatureError:
        raise auth_expired_token
    except InvalidTokenError:
        raise auth_token_invalid
    

def get_payload_from_access_token(payload: Annotated[dict[str, Any], Depends(get_payload)]):
    if payload["token_type"] != "access":
        raise auth_wrong_token_provided

    return payload


async def get_user(
    session: SessionDep, payload: Annotated[dict[str, Any], Depends(get_payload_from_access_token)]
):
    return await session.get(User, int(payload["sub"]))


def check_request_available(
    payload: Annotated[dict[str, Any], Depends(get_payload)], request: Request
) -> bool:
    if payload.get("scopes") and set(["*", f"service:{request.service_id}"]) & set(payload["scopes"]) or request.customer_id == int(payload["sub"]):
        return True

    return False


def check_comment_available(
    payload: Annotated[dict[str, Any], Depends(get_payload)], comment: Comment
) -> bool:
    if payload["role"] != UserRole.admin and int(payload["sub"]) != comment.author_id:
        return False

    return True
