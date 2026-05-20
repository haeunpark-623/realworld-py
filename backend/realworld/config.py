from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./data/realworld.db")
    JWT_SECRET: str = Field(default="changeme-please-generate-random-32-chars")
    JWT_ALG: str = Field(default="HS256")
    JWT_EXPIRE_MINUTES: int = Field(default=10080)
    CORS_ORIGINS: str = Field(default="http://localhost:5173")
    LOG_LEVEL: str = Field(default="INFO")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
