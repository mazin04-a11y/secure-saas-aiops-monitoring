from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import ExternalIntelReport
from app.schemas.monitoring import ExternalIntelRead, ExternalIntelRequest, ExternalIntelStatus
from app.services.external_intel import get_external_intel_status, run_external_intel_search

router = APIRouter()


@router.get("", response_model=list[ExternalIntelRead])
def list_external_intel_reports(db: Session = Depends(get_db)) -> list[ExternalIntelReport]:
    return (
        db.query(ExternalIntelReport)
        .filter(ExternalIntelReport.status == "completed")
        .order_by(ExternalIntelReport.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/status", response_model=ExternalIntelStatus)
def external_intel_status(db: Session = Depends(get_db)) -> dict:
    return get_external_intel_status(db)


@router.post("/search", response_model=ExternalIntelRead)
def search_external_intel(payload: ExternalIntelRequest, db: Session = Depends(get_db)) -> ExternalIntelReport:
    return run_external_intel_search(db, payload.query)
