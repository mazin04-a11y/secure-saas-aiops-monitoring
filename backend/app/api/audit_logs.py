from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import AuditLog
from app.schemas.monitoring import AuditLogRead

router = APIRouter()


@router.get("", response_model=list[AuditLogRead])
def list_audit_logs(db: Session = Depends(get_db)) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
