from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import SystemMetric
from app.schemas.monitoring import MetricCreate, MetricRead

router = APIRouter()


@router.get("", response_model=list[MetricRead])
def list_metrics(db: Session = Depends(get_db)) -> list[SystemMetric]:
    return db.query(SystemMetric).order_by(SystemMetric.created_at.desc()).limit(50).all()


@router.post("/ingest", response_model=MetricRead)
def ingest_metric(payload: MetricCreate, db: Session = Depends(get_db)) -> SystemMetric:
    metric = SystemMetric(**payload.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

