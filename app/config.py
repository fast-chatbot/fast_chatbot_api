import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    PG_HOST: str
    PG_PORT: str
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_settings():
    return {"secret_key": settings.JWT_SECRET_KEY,
            "algorithm": settings.JWT_ALGORITHM,
            "smtp_server": settings.SMTP_SERVER,
            "smtp_port": settings.SMTP_PORT,
            "smtp_username": settings.SMTP_USERNAME,
            "smtp_password": settings.SMTP_PASSWORD,
            "redis_host": settings.REDIS_HOST,
            "redis_port": settings.REDIS_PORT,
            "redis_password": settings.REDIS_PASSWORD,
            "pg_host": settings.PG_HOST,
            "pg_port": settings.PG_PORT,
            "pg_user": settings.PG_USER,
            "pg_password": settings.PG_PASSWORD,
            "pg_database": settings.PG_DATABASE,
            "openai_api_key": settings.OPENAI_API_KEY}
