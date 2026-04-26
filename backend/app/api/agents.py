from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.monitoring import AgentAssessment, AgentPromptRequest
from app.services.aiops_assessment import run_aiops_assessment

router = APIRouter()


@router.post("/kickoff", response_model=AgentAssessment)
def kickoff_agents(db: Session = Depends(get_db)) -> AgentAssessment:
    return run_aiops_assessment(db)


@router.post("/prompt", response_model=AgentAssessment)
def prompt_agents(payload: AgentPromptRequest, db: Session = Depends(get_db)) -> AgentAssessment:
    return run_aiops_assessment(db, mission_prompt=payload.prompt)
