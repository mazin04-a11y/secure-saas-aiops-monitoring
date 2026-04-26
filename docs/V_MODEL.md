# V-Model Mapping

## Business Requirements

- Reduce manual monitoring effort for a mid-sized digital services company.
- Provide visibility into performance, availability, security events, and incidents.
- Present business-readable remediation recommendations.

## System Requirements

- Ingest application performance metrics through REST APIs.
- Store users, logs, metrics, and incidents in PostgreSQL.
- Display operational health in a React dashboard.
- Coordinate AIOps assessments through identity-aware agents.

## Architecture Design

- React dashboard as the user-facing sensory layer.
- FastAPI bridge as the application nervous system.
- CrewAI orchestration as the agentic reasoning layer.
- PostgreSQL as relational operational memory.

## Module Design

- `backend/app/api`: REST endpoints.
- `backend/app/models`: relational data model.
- `backend/app/services`: incident and assessment logic.
- `backend/app/agents`: CrewAI implementation area.
- `frontend/src`: operational dashboard.

## Validation

- Unit testing: backend services and frontend components.
- Integration testing: API, database, and dashboard.
- System testing: Docker Compose runtime.
- User acceptance testing: dashboard clarity and business KPI evidence.

## Traceability Snapshot

| Requirement | Implementation Evidence | Test Evidence |
| --- | --- | --- |
| Monitor SaaS performance | `/metrics/ingest`, dashboard chart | `tests/api_smoke_test.py` |
| Detect security events | `/access-logs/ingest`, Security Events panel | failed login smoke payload |
| Run identity-aware agents | raw-code agents and `config/agents.yaml` | `/agents/prompt` accepted prompt |
| Apply prompt safeguards | `PromptGuard` service | blocked destructive prompt |
| Preserve audit evidence | `agent_task_logs` table | Agent Reports dashboard |
| Gather public external intelligence | optional Serper integration | `/external-intel/search` with local key |
