from pydantic_settings import BaseSettings
from typing import Optional, Dict, List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # You should generate a secure random key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API Keys
    OPENAI_API_KEY: str

    # Paddle Integration
    PADDLE_API_TOKEN: Optional[str] = None
    PADDLE_WEBHOOK_SECRET: Optional[str] = None
    BASIC_PRICE_ID: Optional[str] = None
    PRO_PRICE_ID: Optional[str] = None

    # Email and OAuth
    ALLOWED_EMAIL_DOMAINS: List[str] = []

    # Google OAuth (new)
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str


    # Frontend-specific settings (optional in backend)
    VITE_GOOGLE_CLIENT_ID: Optional[str] = None
    VITE_GOOGLE_REDIRECT_URI: Optional[str] = None
    VITE_API_BASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"  # This will ignore any extra env vars not defined in the model


settings = Settings()