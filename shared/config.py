from pydantic import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    TELEGRAM_BOT_TOKEN: str
    ALEXA_APP_ID: str
    DOMAIN_NAME: str
    LETSENCRYPT_EMAIL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()