import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    # MongoDB Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "adhi_blood_connect"

    # Security JWT Settings
    # Standard security key (fallback only used in development if not supplied)
    JWT_SECRET_KEY: str = "9caee98436cd934cd5603e8ff89c8942b083b063ffc38a2e2cd729eb102d99d3"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Redis Cache Settings (Optional)
    REDIS_URL: Union[str, None] = None

    # Artificial Intelligence API Keys
    GEMINI_API_KEY: Union[str, None] = None
    OPENAI_API_KEY: Union[str, None] = None

    # CORS Settings
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:5173,http://localhost:8080",


    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = Settings()
