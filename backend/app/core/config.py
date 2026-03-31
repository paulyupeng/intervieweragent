"""
Application Configuration
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "dev-secret-key-change-in-production"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Database
    DATABASE_URL: str = "postgresql://interview:interview_secret@postgres:5432/interviewer"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # LiveKit
    LIVEKIT_URL: str = "ws://livekit:7880"
    LIVEKIT_API_KEY: str = "devkey"
    LIVEKIT_API_SECRET: str = "devsecret"

    # External APIs
    DEEPGRAM_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Storage
    STORAGE_TYPE: str = "local"
    STORAGE_LOCAL_PATH: str = "/app/recordings"

    # Interview Settings
    DEFAULT_INTERVIEW_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,zh,es,fr,de"
    MAX_INTERVIEW_DURATION_MINUTES: int = 60

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
