import os
from typing import Any
from passlib.context import CryptContext
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
import logging

from app.core.enums import AppEnv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app_env = AppEnv(os.getenv("APP_ENV", "test")).value

secret_key = os.environ["SECRET_KEY"]
access_token_expire_time = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", "30")))
refresh_token_expire_time = timedelta(days=int(os.getenv("REFRESH_TOKEN_DAYS", "7")))
jwt_algorithm = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

admin_password = os.environ["ADMIN_PASSWORD"]


def get_db_configuration() -> dict[str, Any]:
    if app_env == "production":
        try:
            return {
                "url": "postgresql+asyncpg://"
                + os.environ["DB_USER"]
                + ":"
                + os.environ["DB_PASSWORD"]
                + "@db:5432/"
                + os.environ["DB_NAME"]
            }
        except KeyError as e:
            raise KeyError(f"Env variable {e.args[0]} must be specified")
    else:
        return {
            "url": "sqlite+aiosqlite:///test.db",
            "connect_args": {"check_same_thread": False},
            "echo": True,
        }


db_connect_configuration = get_db_configuration()
