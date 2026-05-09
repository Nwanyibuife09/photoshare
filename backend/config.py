from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "PhotoShare"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5175", "http://127.0.0.1:5175",
        "http://localhost:5176", "http://127.0.0.1:5176",
        "http://localhost:5177", "http://127.0.0.1:5177"
    ]
    DATABASE_URL: str = "sqlite:///./photoshare.db"  # Defaults to sqlite for local dev setup, update to postgres later
    SECRET_KEY: str = "super_secret_key_change_in_production"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"

settings = Settings()
