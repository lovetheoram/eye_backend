from pydantic_settings import BaseSettings
from functools import lru_cache


VERSION = "v3"


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database connection pool
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_RECYCLE: int = 300

    # CORS — comma-separated origins, or "*" for dev
    CORS_ORIGINS: str = "*"

    # Rate limiting
    RATE_LIMIT: str = "100/minute"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()