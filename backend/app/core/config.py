"""
SatQuery AI - Core Configuration
Pydantic v2 Settings for application configuration.
"""
from typing import List, Union
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


import os

is_vercel = bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))
default_storage_base = "/tmp/satquery_storage" if is_vercel else "./storage"
default_db_url = "sqlite+aiosqlite:////tmp/satquery.db" if is_vercel else "sqlite+aiosqlite:///./storage/satquery.db"

class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "SatQuery AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "production" if is_vercel else "development"
    DEBUG: bool = not is_vercel
    DEMO_MODE: bool = True
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security & Auth
    SECRET_KEY: str = "satquery-super-secret-key-change-in-production-sih26167"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = default_db_url
    DB_ECHO: bool = False

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Storage Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    STORAGE_DIR: str = default_storage_base
    UPLOAD_DIR: str = f"{default_storage_base}/uploads"
    EVIDENCE_DIR: str = f"{default_storage_base}/evidence"
    MODEL_CACHE_DIR: str = f"{default_storage_base}/models"

    # Upload Constraints
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: List[str] = ["tif", "tiff", "png", "jpg", "jpeg", "jp2"]

    # Geospatial Processing
    DEFAULT_CRS: str = "EPSG:4326"
    REGISTRATION_METHOD: str = "ecc"
    MAX_IMAGE_DIMENSION: int = 4096
    ENABLE_AUTO_REGISTRATION: bool = True

    # AI Model Settings
    MODEL_DEVICE: str = "cpu"
    MOCK_MODEL_LATENCY: float = 0.2

    # AI Chat Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()

# Ensure critical storage paths exist
try:
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.EVIDENCE_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
except Exception:
    pass

