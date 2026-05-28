from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolves to project root (consulting-platform/) both locally and as fallback in Docker
_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    DATABASE_URL: str = "sqlite+aiosqlite:///./consulting.db"
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_MB: int = 50
    DEFAULT_MODEL: str = "claude-sonnet-4-6"

    AUTH_USERNAME: str = ""
    AUTH_PASSWORD_HASH: str = ""
    JWT_SECRET: str = ""
    JWT_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(env_file=str(_ENV_FILE), extra="ignore")


settings = Settings()
