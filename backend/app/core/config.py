from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "PitchPilot AI"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/pitchpilot"
    
    # Security
    JWT_SECRET: str = "supersecretkey_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    CORS_ORIGIN: str = "http://localhost:5173"
    
    # AI Configuration
    AI_MODE: str = "mock"  # live | mock | scripted-demo
    LLM_PRIMARY: str = "gemini"  # gemini | openai
    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    
    # Search Configuration
    SEARCH_MODE: str = "cached"  # live | cached | off
    TAVILY_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
