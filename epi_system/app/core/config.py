from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Controle de EPI"
    environment: str = "dev"
    database_url: str = "sqlite:///./epi.db"
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    fernet_key: str
    cpf_pepper: str
    cors_origins: str = "http://localhost:8000"
    dpo_contact: str = "dpo@empresa.com.br"
    privacy_policy_version: str = "2026-05-25"
    signature_storage_dir: str = "storage/signatures"
    backup_dir: str = "backups"
    backup_retention_years: int = 5
    data_retention_years: int = 5
    auth_rate_limit: str = "5/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
