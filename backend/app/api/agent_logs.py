from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.monitoring import AgentTaskLog
from app.schemas.monitoring import AgentTaskLogRead

router = APIRouter()


@router.get("", response_model=list[AgentTaskLogRead])
def list_agent_logs(db: Session = Depends(get_db)) -> list[AgentTaskLog]:
    return db.query(AgentTaskLog).order_by(AgentTaskLog.created_at.desc()).limit(100).all()

