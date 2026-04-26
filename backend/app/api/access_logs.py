from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import AccessLog, UserProfile
from app.schemas.monitoring import AccessLogCreate, AccessLogRead

router = APIRouter()


@router.get("", response_model=list[AccessLogRead])
def list_access_logs(db: Session = Depends(get_db)) -> list[AccessLog]:
    return db.query(AccessLog).order_by(AccessLog.created_at.desc()).limit(100).all()


@router.post("/ingest", response_model=AccessLogRead)
def ingest_access_log(payload: AccessLogCreate, db: Session = Depends(get_db)) -> AccessLog:
    user = db.query(UserProfile).filter(UserProfile.username == payload.username).first()
    if user is None:
        user = UserProfile(username=payload.username, role="viewer", department="unknown")
        db.add(user)
        db.commit()
        db.refresh(user)

    access_log = AccessLog(
        user_id=user.id,
        action=payload.action,
        ip_address=payload.ip_address,
        outcome=payload.outcome,
    )
    db.add(access_log)
    db.commit()
    db.refresh(access_log)
    return access_log

