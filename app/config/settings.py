from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    UPLOAD_DIR: str = "./uploads"

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
