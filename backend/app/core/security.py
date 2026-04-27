import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_ingest_api_key(x_api_key: str | None = Header(default=None)) -> str:
    configured_keys = settings.configured_ingest_api_keys
    if not configured_keys:
        return "development"

    if x_api_key and any(secrets.compare_digest(x_api_key, key) for key in configured_keys):
        return "api_key"

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Valid X-API-Key header required for ingestion.",
    )
