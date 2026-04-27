from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import SystemMetric
from app.schemas.monitoring import MetricCreate, MetricRead
from app.core.security import require_ingest_api_key
from app.services.audit import record_audit_log

router = APIRouter()


@router.get("", response_model=list[MetricRead])
def list_metrics(db: Session = Depends(get_db)) -> list[SystemMetric]:
    return db.query(SystemMetric).order_by(SystemMetric.created_at.desc()).limit(50).all()


@router.post("/ingest", response_model=MetricRead)
def ingest_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
    actor: str = Depends(require_ingest_api_key),
) -> SystemMetric:
    metric = SystemMetric(**payload.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    record_audit_log(
        db,
        actor=actor,
        action="metric_ingested",
        resource_type="system_metric",
        resource_id=metric.id,
        details=f"{metric.service_name} status={metric.status}",
    )
    return metric
