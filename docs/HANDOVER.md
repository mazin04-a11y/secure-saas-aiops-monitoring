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
- Deployment target: Railway later
- CI/CD: Jenkinsfile scaffold exists

## Current Running URLs

- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

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

## Current Database State

After live verification on April 26, 2026:

- `system_metrics`: 1 real API-ingested `payment-api` degraded metric.
- `access_logs`: 3 real API-ingested failed login records for `security_user`.
- `incidents`: 6, all created from internal metric/access-log evidence after an additional UI agent workflow test.
- `agent_task_logs`: 9, all tied to internal metric/access-log evidence after an additional UI agent workflow test.
- External Intel has one successful Stripe public status report.
- External Intel appears as assessment context/recommendation only and did not create an incident or evidence log.
- Rejected External Intel queries show a UI/API rejection and do not change completed report count.

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

1. Hard refresh dashboard and confirm the post-verification state:
   - Performance shows the real `payment-api` metric.
   - Security shows the three real failed login records.
   - Incidents shows 2 performance incidents and 1 security incident.
   - Evidence shows 5 internal evidence logs and no External Intel evidence log.
2. Improve UI empty states and add timestamps/source labels.
3. Add a convenient DB reset/dev cleanup command for future demos, guarded by explicit confirmation.
4. Prepare GitHub commit after UI behavior is checked.
