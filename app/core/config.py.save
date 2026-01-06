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
    STRIPE_SECRET_KEY: str = "sk_test_51SVWMlFlnwfqrHjipgcnZaQstqhHD9dHHp2HrP3QKozZ62yU8JIBp8tagAS2yEyJmr0ksGbW7naJF3TwsOXeilV100UNrp1MQ1"
    STRIPE_WEBHOOK_SECRET: str = "whsec_754a328554d444d76a3312bd20addb47c8a1b519d01ac9f4cbb7c5e5773f7672"

    class Config:
        env_file = ".env"


settings = Settings()
