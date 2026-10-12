from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SONORA"
    app_env: str = "development"
    app_debug: bool = True
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./sonora.db"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    media_storage_backend: str = "local"
    media_bucket_url: str = ""
    log_level: str = "INFO"

    @property
    def database_url_for_sqlalchemy(self) -> str:
        return self.database_url

settings = Settings()
