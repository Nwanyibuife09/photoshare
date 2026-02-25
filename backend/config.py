from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "PhotoShare"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    DATABASE_URL: str = "sqlite:///./photoshare.db"  # Defaults to sqlite for local dev setup, update to postgres later
    SECRET_KEY: str = "super_secret_key_change_in_production"
    
    class Config:
        env_file = ".env"

settings = Settings()
