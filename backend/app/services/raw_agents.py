from dataclasses import dataclass, replace
import re

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.monitoring import AccessLog, AgentTaskLog, ExternalIntelReport, Incident, SystemMetric
from app.services.prompt_guard import GuardedPrompt


@dataclass(frozen=True)
class AgentFinding:
    agent_name: str
    task_name: str
    severity: str
    evidence: str
    recommendation: str
    incident_type: str = "performance"
    create_incident: bool = True
    persist_evidence: bool = True
    source_label: str = "internal_metrics"
    correlation_id: str | None = None


class PerformanceAuditor:
    name = "PerformanceAuditor"
    role = "Performance monitoring specialist"
    permissions = {"read_system_metrics", "create_performance_incident"}

    def run(self, db: Session, prompt: GuardedPrompt) -> list[AgentFinding]:
        latest = db.query(SystemMetric).order_by(SystemMetric.created_at.desc()).first()
        if not latest:
            return []

        average_response_time = db.query(func.avg(SystemMetric.response_time_ms)).scalar() or 0
        average_error_rate = db.query(func.avg(SystemMetric.error_rate)).scalar() or 0
        findings: list[AgentFinding] = []

        if latest.cpu_usage >= 85 or latest.memory_usage >= 85:
            findings.append(
                AgentFinding(
                    self.name,
                    "detect_resource_pressure",
                    "high",
                    f"{latest.service_name} CPU={latest.cpu_usage}% memory={latest.memory_usage}%",
                    "Scale the affected service or inspect resource-heavy background tasks.",
                    "performance",
                    True,
                    True,
                    "internal_metrics",
                    _safe_correlation_id("performance", "detect_resource_pressure", latest.service_name),
                )
            )

        if average_response_time >= 750 or average_error_rate >= 5:
            findings.append(
                AgentFinding(
                    self.name,
                    "detect_availability_risk",
                    "medium",
                    f"avg_response_time={average_response_time:.1f}ms avg_error_rate={average_error_rate:.1f}%",
                    "Check API logs, database latency, and recent deployment changes.",
                    "performance",
                    True,
                    True,
                    "internal_metrics",
                    _safe_correlation_id("performance", "detect_availability_risk", "aggregate"),
                )
            )

        if prompt.accepted and "response time" in prompt.normalized and average_response_time >= 500:
            findings.append(
                AgentFinding(
                    self.name,
                    "mission_prompt_focus",
                    "medium",
                    f"Mission prompt focused on response time; current average is {average_response_time:.1f}ms.",
                    "Prioritise slow endpoint tracing in the next investigation cycle.",
                    "performance",
                    False,
                    True,
                    "internal_metrics",
                    _safe_correlation_id("performance", "mission_prompt_focus", "aggregate"),
                )
            )

        return findings


class SecuritySentinel:
    name = "SecuritySentinel"
    role = "Security monitoring specialist"
    permissions = {"read_access_logs", "create_security_incident"}

    def run(self, db: Session, prompt: GuardedPrompt) -> list[AgentFinding]:
        findings: list[AgentFinding] = []
        failed_logins = (
            db.query(AccessLog)
            .filter(AccessLog.outcome == "failed")
            .order_by(AccessLog.created_at.desc())
            .limit(20)
            .all()
        )

        if len(failed_logins) >= 3:
            suspicious_ips = sorted({log.ip_address for log in failed_logins})
            findings.append(
                AgentFinding(
                    self.name,
                    "detect_failed_login_burst",
                    "high",
                    f"{len(failed_logins)} recent failed access attempts from {', '.join(suspicious_ips[:4])}.",
                    "Temporarily raise authentication monitoring sensitivity and review affected user accounts.",
                    "security",
                    True,
                    True,
                    "access_logs",
                    _safe_correlation_id("security", "detect_failed_login_burst", "failed-login-burst"),
                )
            )

        if prompt.accepted and failed_logins and any(
            term in prompt.normalized for term in ["security", "failed login", "unauthorized"]
        ):
            findings.append(
                AgentFinding(
                    self.name,
                    "mission_prompt_security_review",
                    "medium",
                    f"Mission prompt requested a security-focused review across {len(failed_logins)} failed access logs.",
                    "Inspect access logs for failed login spikes and unusual admin activity.",
                    "security",
                    False,
                    True,
                    "access_logs",
                    _safe_correlation_id("security", "mission_prompt_security_review", "failed-logins"),
                )
            )

        return findings


class ExternalIntelAnalyst:
    name = "ExternalIntelAnalyst"
    role = "Public operational intelligence reviewer"
    permissions = {"read_external_intel_reports", "recommend_contextual_review"}

    def run(self, db: Session, prompt: GuardedPrompt) -> list[AgentFinding]:
        latest = (
            db.query(ExternalIntelReport)
            .filter(ExternalIntelReport.status == "completed")
            .order_by(ExternalIntelReport.created_at.desc())
            .first()
        )
        if latest is None:
            return []

        return [
            AgentFinding(
                self.name,
                "review_public_intelligence",
                "low",
                latest.summary,
                "Compare public vendor signals against internal incidents before escalating business risk.",
                "external_intel",
                False,
                False,
                "external_intel",
                _safe_correlation_id("external_intel", "review_public_intelligence", latest.query),
            )
        ]



class RemediationSpecialist:
    name = "RemediationSpecialist"
    role = "Controlled remediation advisor"
    permissions = {"read_incidents", "recommend_only"}

    def validate(self, finding: AgentFinding) -> AgentFinding:
        if finding.severity == "high":
            return replace(
                finding,
                recommendation=(
                    f"{finding.recommendation} Human approval required before operational changes."
                ),
            )
        return finding


class ManagerAgent:
    name = "ManagerAgent"
    role = "Identity-aware coordinator"
    permissions = {"delegate_tasks", "validate_findings", "log_agent_activity"}

    def __init__(self) -> None:
        self.performance_auditor = PerformanceAuditor()
        self.security_sentinel = SecuritySentinel()
        self.external_intel_analyst = ExternalIntelAnalyst()
        self.remediation_specialist = RemediationSpecialist()

    def run(self, db: Session, prompt: GuardedPrompt) -> list[AgentFinding]:
        if not prompt.accepted:
            return [
                AgentFinding(
                    self.name,
                    "prompt_guard_validation",
                "low",
                    prompt.reason,
                    "Revise the mission prompt so it asks for assessment, not destructive action.",
                    "guardrail",
                    False,
                    False,
                    "prompt_guard",
                    _safe_correlation_id("guardrail", "prompt_guard_validation", "rejected"),
                )
            ]

        findings = [
            *self.performance_auditor.run(db, prompt),
            *self.security_sentinel.run(db, prompt),
            *self.external_intel_analyst.run(db, prompt),
        ]
        return [self.remediation_specialist.validate(finding) for finding in findings]


def create_incident_from_finding(db: Session, finding: AgentFinding) -> int:
    if not finding.persist_evidence:
        return 0

    correlation_id = finding.correlation_id or _safe_correlation_id(
        finding.incident_type, finding.task_name, finding.evidence
    )
    source_label = finding.source_label
    evidence = _annotate_evidence(finding.evidence, source_label, correlation_id)

    db.add(
        AgentTaskLog(
            agent_name=finding.agent_name,
            task_name=finding.task_name,
            permission_scope=",".join(sorted(_permission_scope_for(finding.agent_name))),
            guardrail_status="accepted" if finding.agent_name != "ManagerAgent" else "rejected",
            evidence=evidence,
            recommendation=finding.recommendation,
        )
    )

    if not finding.create_incident:
        db.commit()
        return 0

    existing = (
        db.query(Incident)
        .filter(Incident.status == "open")
        .filter(Incident.incident_type == finding.incident_type)
        .filter(Incident.evidence.contains(f"[correlation: {correlation_id}]"))
        .first()
    )
    if existing is None:
        legacy_query = (
            db.query(Incident)
            .filter(Incident.status == "open")
            .filter(Incident.incident_type == finding.incident_type)
            .filter(Incident.evidence.startswith(f"{finding.agent_name}/{finding.task_name}:"))
            .filter(~Incident.evidence.contains("[correlation:"))
        )
        legacy_token = _legacy_match_token(correlation_id)
        if legacy_token is not None:
            legacy_query = legacy_query.filter(Incident.evidence.contains(legacy_token))
        existing = legacy_query.order_by(Incident.created_at.desc()).first()

    if existing is not None:
        existing.severity = finding.severity
        existing.evidence = f"{finding.agent_name}/{finding.task_name}: {evidence}"
        existing.recommendation = finding.recommendation
        db.commit()
        return 0

    incident = Incident(
        incident_type=finding.incident_type,
        severity=finding.severity,
        evidence=f"{finding.agent_name}/{finding.task_name}: {evidence}",
        recommendation=finding.recommendation,
    )
    db.add(incident)
    db.commit()
    return 1


def _permission_scope_for(agent_name: str) -> set[str]:
    scopes = {
        "PerformanceAuditor": PerformanceAuditor.permissions,
        "SecuritySentinel": SecuritySentinel.permissions,
        "ExternalIntelAnalyst": ExternalIntelAnalyst.permissions,
        "RemediationSpecialist": RemediationSpecialist.permissions,
        "ManagerAgent": ManagerAgent.permissions,
    }
    return scopes.get(agent_name, {"unknown"})


def _annotate_evidence(evidence: str, source_label: str, correlation_id: str) -> str:
    return f"[source: {source_label}] [correlation: {correlation_id}] {evidence}"


def _safe_correlation_id(*parts: str) -> str:
    raw = ":".join(part.strip().lower() for part in parts if part and part.strip())
    return re.sub(r"[^a-z0-9:_-]+", "-", raw).strip("-")[:120]


def _legacy_match_token(correlation_id: str) -> str | None:
    token = correlation_id.rsplit(":", maxsplit=1)[-1]
    if token in {"aggregate", "failed-login-burst", "failed-logins", "rejected"}:
        return None
    return token
