from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.monitoring import AccessLog, SystemMetric
from app.schemas.monitoring import AgentAssessment
from app.services.prompt_guard import guard_prompt
from app.services.raw_agents import ManagerAgent, create_incident_from_finding


def run_aiops_assessment(db: Session, mission_prompt: str | None = None) -> AgentAssessment:
    has_internal_data = db.query(SystemMetric).first() is not None or db.query(AccessLog).first() is not None
    guarded_prompt = guard_prompt(mission_prompt)

    if guarded_prompt.accepted and not has_internal_data:
        return AgentAssessment(
            mode=settings.crewai_mode,
            summary="No live internal operational data is available for assessment.",
            tools_used=["PromptGuard", "SafeQueryTool", "ManagerAgent"],
            incidents_created=0,
            recommendations=["Send data to /metrics/ingest or /access-logs/ingest before running an AIOps assessment."],
            guardrail_status="accepted",
            prompt_feedback=guarded_prompt.reason,
        )

    manager = ManagerAgent()
    findings = manager.run(db, guarded_prompt)
    incidents_created = sum(create_incident_from_finding(db, finding) for finding in findings)
    recommendations = [finding.recommendation for finding in findings]

    if not recommendations:
        recommendations.append("Current metrics are inside the raw-code operating threshold.")

    return AgentAssessment(
        mode=settings.crewai_mode,
        summary="Raw-code identity-aware AIOps crew completed guarded assessment.",
        tools_used=[
            "PromptGuard",
            "SafeQueryTool",
            "ManagerAgent",
            "PerformanceAuditor",
            "SecuritySentinel",
            "ExternalIntelAnalyst",
            "RemediationSpecialist",
        ],
        incidents_created=incidents_created,
        recommendations=recommendations,
        guardrail_status="accepted" if guarded_prompt.accepted else "rejected",
        prompt_feedback=guarded_prompt.reason,
    )
