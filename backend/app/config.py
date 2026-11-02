from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://scriptcut:scriptcut@localhost:5432/scriptcut"
    media_dir: str = "./media"
    static_dir: str = "./static"
    transcribe_provider: str = "stub"
    max_upload_mb: int = 500

    @property
    def sqlalchemy_url(self) -> str:
        """Normalise URLs from PaaS providers (postgres://, postgresql://)."""
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url


@lru_cache
def get_settings() -> Settings:
    return Settings()
