from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://aiops:aiops@localhost:5432/aiops_saas"
    app_environment: str = "local"
    crewai_mode: str = "raw"
    serper_api_key: str | None = None
    ingest_api_keys: str | None = None
    rate_limit_requests: int = 120
    rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def configured_ingest_api_keys(self) -> set[str]:
        if not self.ingest_api_keys:
            return set()
        return {key.strip() for key in self.ingest_api_keys.split(",") if key.strip()}


settings = Settings()
