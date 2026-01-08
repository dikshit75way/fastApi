import os
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    APP_NAME: str
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    
    # JWT Settings
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Stripe Settings
    
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET: str = os.getenv("STRIPE_WEBHOOK_SECRET")

    class Config:
        env_file = ".env"


settings = Settings()
