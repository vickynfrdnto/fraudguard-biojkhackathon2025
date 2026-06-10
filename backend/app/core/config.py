from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PROJECT_NAME: str = "FraudGuard"
   # DATABASE_URL: str = "postgresql+psycopg://fraudguard:fraudguard@db:5432/fraudguard" 
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = Field(default="change-me-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: list[str | AnyHttpUrl] = ["http://localhost:5173", "http://localhost:3000"]
    RATE_LIMIT: str = "120/minute"


settings = Settings()
