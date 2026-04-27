# Handover: Secure SaaS AIOps Monitoring

## Project Location

Active WSL project:

```bash
~/projects/secure-saas-aiops-monitoring
```

Windows/Codex scaffold mirror:

```text
C:\Users\mazin\Documents\Codex\2026-04-26\what-shall-i-do\secure-saas-aiops-monitoring
```

## Current Stack

- Frontend: React + Vite + TypeScript
- Backend: FastAPI
- Database: PostgreSQL via Docker Compose
- Agent mode: raw-code deterministic agents
- External intelligence: optional Serper integration
- Deployment target: Railway deployed
- CI/CD: Jenkinsfile scaffold exists
- Public GitHub repo: https://github.com/mazin04-a11y/secure-saas-aiops-monitoring
- GitHub release: `v1.0.0-mvp`
- Latest pushed commit: `bc79ea7 Add ingestion security and audit trail`

## Current URLs

Local Docker services were stopped after deployment to save machine resources.

Local URLs when Docker is running:

- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

Railway production URLs:

- Frontend: https://frontend-production-76ec8.up.railway.app
- Backend: https://backend-production-a65d.up.railway.app
- Backend health: https://backend-production-a65d.up.railway.app/health

## Current Product Direction

This is a real API-ingestion AIOps monitoring app, not a simulator.

The app should:

- Wait for real internal operational/security data.
- Ingest metrics through `POST /metrics/ingest`.
- Ingest access logs through `POST /access-logs/ingest`.
- Require `X-API-Key` for metric/access-log ingestion when `INGEST_API_KEYS` is configured.
- Store operational state in PostgreSQL.
- Run raw-code AIOps assessment only when internal data exists.
- Use External Intel as context only, not as an incident by itself.
- Show empty states when data is not connected.
- Record audit events for ingestion and agent assessment actions.

The app should not:

- Show simulator controls in the product UI.
- Auto-seed demo rows on startup.
- Create incidents from missing data.
- Create incidents from external public intelligence alone.
- Save failed or not-configured external-intel checks as permanent reports.

## Important Recent Fixes

- Removed simulator UI and backend simulator routes.
- Removed `tools/traffic_generator.py`.
- Removed unused `backend/app/services/seed.py`.
- Cleared local PostgreSQL tables after user confirmation.
- Fixed raw agents so `No system metrics available` does not create incidents or evidence logs.
- Fixed raw agents so External Intel is context only.
- Fixed high-severity remediation so security findings keep `incident_type=security`.
- Fixed External Intel and rejected prompt findings so they do not persist evidence logs.
- Removed stale `backend/app/api/simulator.py` from the active WSL backend checkout.
- Added Docker-runnable backend guardrail tests in `backend/tests/test_aiops_guardrails.py`.
- Fixed rejected External Intel searches so they return a clean `status=rejected` response without saving a permanent report.
- Added `backend/tests/test_external_intel_guardrails.py`.
- Added External Intel status API.
- Wired `SERPER_API_KEY` into `docker-compose.yml`.
- Verified Serper works after user updated `.env`.
- Added incident source labels and correlation IDs.
- Added incident deduplication so repeated assessments update matching open incidents instead of creating duplicates.
- Added legacy incident upgrade logic for older open incidents without correlation metadata.
- Added UI timestamps, source labels, and correlation IDs for incidents/evidence/metrics/logs.
- Rewrote `README.md` into a comprehensive GitHub-facing project document.
- Removed public-facing provider-specific model-service naming from publishable files.
- Published public GitHub repository and release `v1.0.0-mvp`.
- Deployed Railway project with `backend`, `frontend`, and `Postgres` services.
- Backend Railway deployment uses dynamic `$PORT`.
- Frontend Railway deployment uses Vite preview with Railway host support.
- Backend CORS allows Railway frontend domains.
- Added `INGEST_API_KEYS` support for protected ingestion endpoints.
- Added lightweight in-memory rate limiting with `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS`.
- Added `audit_logs` table, `GET /audit-logs`, and audit events for metric ingestion, access-log ingestion, and agent assessments.
- Added frontend `Audit` tab.
- Updated README with Railway live links, buyer-facing data integrity wording, and production-style MVP positioning.
- Added backend API security/audit tests in `backend/tests/test_api_security_audit.py`.
- Backend test suite now has 12 passing tests.
- Pushed commit `bc79ea7 Add ingestion security and audit trail` to GitHub `main`.
- Redeployed Railway backend and frontend from a clean Windows checkout using service-folder roots.
- Latest Railway deployments:
  - Backend: `a1b3f749-e42e-4cd3-b26a-4d6fdac78b50`
  - Frontend: `cfe1d145-6d53-4df6-a7bf-c1213fd44c44`

## Current Database State

Local database after live verification on April 26, 2026:

- `system_metrics`: 1 real API-ingested `payment-api` degraded metric.
- `access_logs`: 3 real API-ingested failed login records for `security_user`.
- `incidents`: 6, all created from internal metric/access-log evidence after an additional UI agent workflow test.
- `agent_task_logs`: 9, all tied to internal metric/access-log evidence after an additional UI agent workflow test.
- External Intel has one successful Stripe public status report.
- External Intel appears as assessment context/recommendation only and did not create an incident or evidence log.
- Rejected External Intel queries show a UI/API rejection and do not change completed report count.
- Later light tests added additional `codex-light-api` and `codex-mini-api` metric/incident records to verify deduplication behavior.

Railway production database:

- Managed Railway Postgres service is deployed.
- It starts empty unless data is ingested through the deployed API.
- External Intel is still context-only.
- Latest live security smoke test created a `secure-live-api` metric through the protected ingestion path.
- `GET /audit-logs` is live and returned a `metric_ingested` event with actor `api_key`.

Verified clean baseline before ingestion:

- `metrics`: 0
- `access_logs`: 0
- `incidents`: 0
- `agent_task_logs`: 0
- No simulator paths in `/openapi.json`.
- `POST /agents/prompt` with no internal data returned `incidents_created=0` and left incidents/evidence empty.
- `POST /agents/prompt` with a rejected destructive prompt returned `guardrail_status=rejected`, `incidents_created=0`, and did not change incidents/evidence counts.
- Invalid metric payloads return HTTP 422.

Verified after security/audit deployment on April 27, 2026:

- Backend health returned `{"status":"ok","service":"secure-saas-aiops-monitoring"}`.
- OpenAPI includes `/audit-logs`.
- OpenAPI includes `x-api-key` header support for ingestion.
- Unauthenticated `POST /metrics/ingest` returned HTTP 401.
- Authenticated `POST /metrics/ingest` returned HTTP 200.
- `GET /audit-logs` returned at least one `metric_ingested` audit event.
- Frontend returned HTTP 200.
- Frontend bundle contains the new `Audit Trail` tab and `/audit-logs` API call.
- Live screenshot saved locally at:
  `C:\Users\mazin\Documents\Codex\2026-04-27\files-mentioned-by-the-user-handover\railway-audit-tab-live.png`

## Environment Notes

`.env` should include:

```bash
DATABASE_URL=postgresql+psycopg://aiops:aiops@postgres:5432/aiops_saas
CREWAI_MODE=raw
SERPER_API_KEY=your_local_key
INGEST_API_KEYS=local-dev-ingest-key
RATE_LIMIT_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60
VITE_API_BASE_URL=http://localhost:8000
```

Do not paste API keys into chat. If `.env` changes, recreate/restart the backend:

```bash
cd ~/projects/secure-saas-aiops-monitoring
docker compose up -d --force-recreate backend
```

Railway backend variables:

- `DATABASE_URL` references Railway Postgres.
- `APP_ENVIRONMENT=production`
- `CREWAI_MODE=raw`
- `INGEST_API_KEYS` is set in Railway and should not be printed or committed.
- `RATE_LIMIT_REQUESTS=120`
- `RATE_LIMIT_WINDOW_SECONDS=60`
- `SERPER_API_KEY` is optional; add it if External Intel search should be enabled.

Railway frontend variables:

- `VITE_API_BASE_URL=https://backend-production-a65d.up.railway.app`

## Real API Test Payloads

Send a performance metric:

```bash
curl -X POST http://localhost:8000/metrics/ingest \
  -H "X-API-Key: local-dev-ingest-key" \
  -H "Content-Type: application/json" \
  -d '{"service_name":"payment-api","cpu_usage":91,"memory_usage":88,"response_time_ms":1100,"error_rate":8.1,"status":"degraded"}'
```

Send an access log:

```bash
curl -X POST http://localhost:8000/access-logs/ingest \
  -H "X-API-Key: local-dev-ingest-key" \
  -H "Content-Type: application/json" \
  -d '{"username":"security_user","action":"login","ip_address":"203.0.113.77","outcome":"failed"}'
```

Run guarded agent assessment:

```bash
curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest payment-api performance and failed login risk."}'
```

Run external public intelligence search:

```bash
curl -X POST http://localhost:8000/external-intel/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Stripe public status page outage"}'
```

## Current UI Pages

- Overview: command center and data-source status
- Performance: metric chart
- Security: access logs
- Incidents: internal incidents only
- Agents: guarded mission prompt
- External Intel: public Serper search and completed reports
- Evidence: agent task logs
- Audit: ingestion and assessment audit trail

## New Repo Direction

The next major product should be a new public repo:

```text
governed-saas-aiops-copilot
```

Product goal:

- Build a real SaaS monitoring copilot, not just a class project.
- Use real ingestion, stateful memory, governed LLM reporting, human approval gates, and auditability.

Recommended stack:

- FastAPI: API bridge / nervous system
- PostgreSQL: stateful relational memory and audit storage
- React/Vite: operator dashboard / senses
- LangGraph: durable workflow control layer, explicit state machine, approval gates
- CrewAI: multi-agent specialist reasoning team inside selected workflow nodes
- OpenAI: LLM reasoning and structured report generation
- Pydantic: schema validation and reliability
- Serper: optional external intelligence context

Core principle:

```text
Raw code detects.
LangGraph controls.
CrewAI analyzes.
OpenAI explains.
Pydantic validates.
Human approves.
PostgreSQL audits.
```

Suggested product description:

```text
A governed SaaS monitoring copilot using LangGraph workflows, CrewAI specialist agents, OpenAI structured outputs, human approval, and audit logging.
```

Important implementation direction:

- Use both LangGraph and CrewAI, but for different roles.
- LangGraph should control the workflow state machine and human approval gates.
- CrewAI should provide the multi-agent product story: manager agent, specialist agents, role/goal/backstory.
- Do not let LLMs directly create incidents.
- Deterministic code should detect incidents from internal metrics/access logs.
- LLMs should generate evidence-grounded operational reports.
- Pydantic should validate all structured LLM output before saving.
- High-risk remediation should remain pending until human approval.
- PostgreSQL should store evidence bundles, reports, approvals, validation status, and audit logs.

Candidate new repo pages:

- Overview
- Metrics
- Security
- Incidents
- AI Reports
- Approvals
- Audit

Candidate workflow nodes:

- `BuildEvidenceBundle`
- `RunCrewAIAnalysis`
- `ValidateStructuredOutput`
- `SafetyReview`
- `HumanApprovalGate`
- `SaveOperationalReport`

Candidate CrewAI agents:

- `ManagerAgent`
- `PerformanceAnalystAgent`
- `SecurityAnalystAgent`
- `ExternalIntelAgent`
- `RemediationReviewerAgent`

Important claims to avoid:

- Do not claim autonomous remediation unless implemented.
- Do not claim Datadog/New Relic replacement.
- Do not claim real-time monitoring unless continuous ingestion is implemented.
- Do not claim LLM-based detection if detection is deterministic.

Honest positioning:

```text
A governed SaaS AIOps copilot MVP with real ingestion, stateful memory, multi-agent orchestration, validated LLM reports, human approval gates, and auditability.
```

## Next Recommended Work

1. Start a new chat and create the new public repo `governed-saas-aiops-copilot`.
2. Scaffold the new product with FastAPI, React/Vite, PostgreSQL, LangGraph, CrewAI, OpenAI, Pydantic, and Serper.
3. Implement ingestion, deterministic incident detection, evidence bundles, validated LLM operational reports, approval gates, and audit logging.
4. Keep the current repo `secure-saas-aiops-monitoring` as the deployed raw-code MVP baseline.
5. Optionally add `SERPER_API_KEY` to the current Railway backend if External Intel should be active live.
