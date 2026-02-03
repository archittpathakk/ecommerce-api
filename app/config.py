# app/config.py

from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field
from typing import Optional


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Loaded automatically from environment variables or .env file.
    """

    # --- Database ---
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # --- JWT / Auth ---
    JWT_SECRET_KEY: SecretStr = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Testing ---
    TEST_DATABASE_URL: Optional[str] = Field(None, env="TEST_DATABASE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
