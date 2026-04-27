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
- Store operational state in PostgreSQL.
- Run raw-code AIOps assessment only when internal data exists.
- Use External Intel as context only, not as an incident by itself.
- Show empty states when data is not connected.

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

Verified clean baseline before ingestion:

- `metrics`: 0
- `access_logs`: 0
- `incidents`: 0
- `agent_task_logs`: 0
- No simulator paths in `/openapi.json`.
- `POST /agents/prompt` with no internal data returned `incidents_created=0` and left incidents/evidence empty.
- `POST /agents/prompt` with a rejected destructive prompt returned `guardrail_status=rejected`, `incidents_created=0`, and did not change incidents/evidence counts.
- Invalid metric payloads return HTTP 422.

## Environment Notes

`.env` should include:

```bash
DATABASE_URL=postgresql+psycopg://aiops:aiops@postgres:5432/aiops_saas
CREWAI_MODE=raw
SERPER_API_KEY=your_local_key
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

Railway frontend variables:

- `VITE_API_BASE_URL=https://backend-production-a65d.up.railway.app`

## Real API Test Payloads

Send a performance metric:

```bash
curl -X POST http://localhost:8000/metrics/ingest \
  -H "Content-Type: application/json" \
  -d '{"service_name":"payment-api","cpu_usage":91,"memory_usage":88,"response_time_ms":1100,"error_rate":8.1,"status":"degraded"}'
```

Send an access log:

```bash
curl -X POST http://localhost:8000/access-logs/ingest \
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

## Next Recommended Work

1. Open the Railway frontend and confirm the UI loads:
   - https://frontend-production-76ec8.up.railway.app
2. Light-test the deployed API:
   - Ingest one metric into the Railway backend.
   - Run the assessment twice.
   - Confirm the second run creates `0` duplicate incidents.
3. Update `README.md` with Railway live links after confirming the public UI.
4. Add screenshots later when local disk space allows restarting the app briefly.
5. Consider adding a guarded DB reset/dev cleanup command for future demos.
