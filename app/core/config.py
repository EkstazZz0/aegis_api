import os
from typing import Any

from app.core.enums import AppEnv

app_env = AppEnv(os.getenv("APP_ENV", "test")).value

secret_key = os.environ["SECRET_KEY"]


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