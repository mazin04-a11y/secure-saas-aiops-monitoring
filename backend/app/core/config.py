from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://aiops:aiops@localhost:5432/aiops_saas"
    app_environment: str = "local"
    crewai_mode: str = "raw"
    serper_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
