from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Scalingo fournit SCALINGO_POSTGRESQL_URL ; en local on utilise DATABASE_URL
    database_url: str = Field(
        default="postgresql://app:app@localhost:5432/app",
        validation_alias=AliasChoices("SCALINGO_POSTGRESQL_URL", "DATABASE_URL"),
    )
    cors_origins: str = "http://localhost:5173"

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url
        # Scalingo donne postgres:// ; SQLAlchemy veut postgresql://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip().rstrip("/") for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
