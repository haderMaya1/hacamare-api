from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data.db"
    TEST_DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "SuperClave"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENV: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()