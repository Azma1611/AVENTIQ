import os
from typing import List

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        PROJECT_NAME: str = "AVENTIQ API"
        VERSION: str = "0.1.0"
        API_V1_STR: str = "/api/v1"
        ENVIRONMENT: str = "development"

        # CORS
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

        # Database / Supabase (Planned)
        SUPABASE_URL: str = ""
        SUPABASE_KEY: str = ""

        # AI Providers (Planned)
        OPENAI_API_KEY: str = ""
        GEMINI_API_KEY: str = ""

        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore",
        )

except ImportError:
    from pydantic import BaseModel

    class Settings(BaseModel):  # type: ignore[no-redef]
        PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AVENTIQ API")
        VERSION: str = os.getenv("VERSION", "0.1.0")
        API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]

        SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
        SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
        GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


settings = Settings()
