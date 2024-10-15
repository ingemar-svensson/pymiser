# app/core/config.py

from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    MONGO_URI: str = Field(..., env='MONGO_URI')
    DATABASE_NAME: str = Field(..., env='DATABASE_NAME')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env='ACCESS_TOKEN_EXPIRE_MINUTES')

    # OAuth2 configuration
    GOOGLE_CLIENT_ID: str = Field(..., env='GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = Field(..., env='GOOGLE_CLIENT_SECRET')

    class Config:
        env_file = ".env"

settings = Settings()
