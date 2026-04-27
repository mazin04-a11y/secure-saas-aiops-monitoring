from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.monitoring import AgentAssessment, AgentPromptRequest
from app.services.aiops_assessment import run_aiops_assessment
from app.services.audit import record_audit_log

router = APIRouter()


@router.post("/kickoff", response_model=AgentAssessment)
def kickoff_agents(db: Session = Depends(get_db)) -> AgentAssessment:
    assessment = run_aiops_assessment(db)
    record_audit_log(
        db,
        action="agent_assessment_run",
        resource_type="agent_assessment",
        details=f"guardrail={assessment.guardrail_status}; incidents_created={assessment.incidents_created}",
    )
    return assessment


@router.post("/prompt", response_model=AgentAssessment)
def prompt_agents(payload: AgentPromptRequest, db: Session = Depends(get_db)) -> AgentAssessment:
    assessment = run_aiops_assessment(db, mission_prompt=payload.prompt)
    record_audit_log(
        db,
        action="agent_assessment_run",
        resource_type="agent_assessment",
        details=f"guardrail={assessment.guardrail_status}; incidents_created={assessment.incidents_created}",
    )
    return assessment
