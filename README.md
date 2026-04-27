<div align="center">

# Secure SaaS AIOps Monitoring

<img src="https://img.shields.io/badge/backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/frontend-React%20%2B%20Vite-61dafb?style=for-the-badge&logo=react&logoColor=111827" />
<img src="https://img.shields.io/badge/database-PostgreSQL-4169e1?style=for-the-badge&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/runtime-Docker-2496ed?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/agents-raw--code%20AIOps-7c3aed?style=for-the-badge" />
<img src="https://img.shields.io/badge/external%20intel-context%20only-f59e0b?style=for-the-badge" />
<img src="https://img.shields.io/badge/tests-12%20backend%20passing-22c55e?style=for-the-badge" />
<img src="https://img.shields.io/badge/status-production--style%20MVP-111827?style=for-the-badge" />

<br /><br />

**A secure internal SaaS monitoring platform that ingests real operational data, detects incidents through identity-aware AIOps agents, and presents business-readable remediation evidence.**

*Built for a developer portfolio, but shaped like a production-style MVP: API-key-protected ingestion, PostgreSQL memory, Dockerized services, audit evidence, prompt guardrails, contextual external intelligence, and a clean React command center.*

</div>

---

## Live Deployment

| Service | URL |
|---|---|
| Dashboard | https://frontend-production-76ec8.up.railway.app |
| API base | https://backend-production-a65d.up.railway.app |
| API health | https://backend-production-a65d.up.railway.app/health |

Production smoke check on April 27, 2026: the dashboard returned `200` HTML, backend health returned `status=ok`, metric ingestion succeeded, and repeated agent assessment deduplicated incidents. The first assessment created 2 incidents from the ingested performance signal; the second assessment created 0 new incidents.

---

## Contents

- [1. Developer Requirements](#1-developer-requirements)
- [2. Product Brochure](#2-product-brochure)
- [3. Step-by-Step Usage](#3-step-by-step-usage)
- [4. Agent and Code Breakdown](#4-agent-and-code-breakdown)
- [5. API Reference](#5-api-reference)
- [6. Data Model](#6-data-model)
- [7. Guardrails and Production Rules](#7-guardrails-and-production-rules)
- [8. Testing and Verification](#8-testing-and-verification)
- [9. Deployment Notes](#9-deployment-notes)
- [10. Portfolio Evidence](#10-portfolio-evidence)

---

## 1. Developer Requirements

### The original engineering problem

A mid-sized digital services company needs an internal application that can monitor the health of its SaaS services, detect performance and security issues, and give operators clear recommendations without relying on hidden manual checks.

From a developer point of view, the system needed to prove:

| Requirement | Developer interpretation | Implemented by |
|---|---|---|
| Ingest real operational data | Accept service metrics and access logs through API-key-protected endpoints | `POST /metrics/ingest`, `POST /access-logs/ingest` |
| Store operational memory | Persist metrics, logs, incidents, and agent evidence in a relational database | PostgreSQL, SQLAlchemy models |
| Detect incidents | Run deterministic AIOps assessment logic over internal data | `backend/app/services/raw_agents.py` |
| Avoid duplicate incidents | Correlate repeated findings to the same open incident | Source labels and correlation IDs |
| Preserve evidence | Store readable agent task logs for audit and demonstration | `agent_task_logs` table |
| Track operational actions | Record important ingestion and assessment activity for review | `audit_logs` table |
| Protect the system from unsafe prompts | Reject destructive mission prompts before agent work starts | `PromptGuard` service |
| Keep public intelligence contextual | Allow public search context without creating incidents from it | External Intel service and `ExternalIntelAnalyst` |
| Give business-readable output | Display status, incidents, recommendations, timestamps, and sources | React dashboard |
| Be runnable locally | One command should start database, backend, and frontend | Docker Compose |
| Be testable | Backend tests and frontend builds must verify core guardrails | `unittest`, `npm run build` |

### Data integrity principles

The platform is designed to give operators trustworthy signals from connected systems, with clear evidence and minimal alert noise.

| Principle | Client benefit |
|---|---|
| Ingestion-driven monitoring | The dashboard reports data received from connected systems |
| Clear empty states | If no data source is connected, the product shows that clearly instead of inventing activity |
| Evidence-based incidents | Incidents are created only when internal metrics or access logs support them |
| Context-aware external intelligence | Public vendor information can enrich analysis, but does not create incidents by itself |
| Deduplicated alerting | Repeated assessments update existing incidents instead of creating noisy duplicates |
| Audit-ready evidence | Agent findings are linked to internal telemetry and readable evidence logs |

### V-Model traceability

| V-Model layer | Evidence in this repo |
|---|---|
| Business requirements | `docs/V_MODEL.md`, dashboard command center |
| System requirements | API ingestion, PostgreSQL persistence, React UI |
| Architecture design | FastAPI + PostgreSQL + React + agent services |
| Module design | `backend/app/api`, `backend/app/services`, `frontend/src` |
| Unit validation | Backend guardrail tests |
| Integration validation | Docker Compose runtime and API smoke flow |
| User acceptance | Dashboard empty states, source labels, correlation IDs, evidence logs |

---

## 2. Product Brochure

### What the product does

**Secure SaaS AIOps Monitoring** gives an operations team a single command center for service health, security activity, incidents, and agent recommendations.

It answers four practical questions:

1. Are our services healthy?
2. Are there signs of performance degradation or suspicious access?
3. What incident evidence exists, and where did it come from?
4. What should an operator do next?

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>Live Operational Visibility</h3>
      <p>Ingest CPU, memory, response time, error rate, and status metrics from internal services. The dashboard updates around real data, not static demo content.</p>
    </td>
    <td width="33%" valign="top">
      <h3>Security Event Awareness</h3>
      <p>Capture access logs, failed login bursts, IP evidence, and user activity patterns. Security findings are separated from performance findings.</p>
    </td>
    <td width="33%" valign="top">
      <h3>Agentic Recommendations</h3>
      <p>Raw-code AIOps agents assess internal data, create incidents, and preserve clear evidence with permission scopes and correlation IDs.</p>
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top">
      <h3>Incident Correlation</h3>
      <p>Repeated assessments update the same open incident instead of generating duplicates. Operators see one continuing event, not alert noise.</p>
    </td>
    <td width="33%" valign="top">
      <h3>External Context</h3>
      <p>Optional Serper search can collect public status context, but public intelligence never creates incidents unless internal telemetry supports the risk.</p>
    </td>
    <td width="33%" valign="top">
      <h3>Portfolio-Ready Delivery</h3>
      <p>Docker, FastAPI, React, PostgreSQL, Jenkins scaffold, Railway config, docs, tests, and a clean GitHub README make the system easy to review.</p>
    </td>
  </tr>
</table>

### Product promise

> Connect internal metrics and access logs. Run a guarded AIOps assessment. Get a concise incident register with source labels, timestamps, correlation IDs, and recommendations that a business stakeholder can understand.

### Dashboard pages

| Page | Purpose |
|---|---|
| Overview | System status, live data state, latest external signal, recent agent activity |
| Performance | CPU, memory, response-time chart plus metric source/timestamp table |
| Security | Internal access logs with outcome, IP address, source, and timestamp |
| Incidents | Deduplicated internal incidents with severity, status, source, timestamp, and correlation ID |
| Agents | Guarded mission prompt and AIOps assessment output |
| External Intel | Optional public search reports marked as context-only |
| Evidence | Agent task logs, permission scopes, recommendations, source labels, and correlation IDs |

---

## 3. Step-by-Step Usage

### 3.1 Prerequisites

- Docker Desktop or Docker Engine
- WSL/Linux shell recommended for local development
- Optional: `SERPER_API_KEY` for public External Intel search

### 3.2 Configure environment

```bash
cp .env.example .env
```

Recommended local values:

```env
DATABASE_URL=postgresql+psycopg://aiops:aiops@postgres:5432/aiops_saas
CREWAI_MODE=raw
SERPER_API_KEY=
INGEST_API_KEYS=local-dev-ingest-key
RATE_LIMIT_REQUESTS=120
RATE_LIMIT_WINDOW_SECONDS=60
VITE_API_BASE_URL=http://localhost:8000
```

Do not commit local API keys.

### 3.3 Start the application

```bash
docker compose up --build
```

Open:

| Service | URL |
|---|---|
| Dashboard | http://localhost:5173 |
| API docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

### 3.4 Confirm the empty state

Before sending internal data, the product should show:

- System Status: `No Data`
- Live Data Source: `Not Connected`
- Incidents: empty
- Evidence: empty
- AIOps assessment button: waiting for data

This is expected. The app does not invent operational risk.

### 3.5 Send a performance metric

```bash
curl -X POST http://localhost:8000/metrics/ingest \
  -H "X-API-Key: local-dev-ingest-key" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "payment-api",
    "cpu_usage": 91,
    "memory_usage": 88,
    "response_time_ms": 1100,
    "error_rate": 8.1,
    "status": "degraded"
  }'
```

Expected behavior:

- Performance page shows the metric.
- Overview changes from `No Data` to an active status.
- No incident is created until an AIOps assessment runs.

### 3.6 Send access logs

```bash
curl -X POST http://localhost:8000/access-logs/ingest \
  -H "X-API-Key: local-dev-ingest-key" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "security_user",
    "action": "login",
    "ip_address": "203.0.113.77",
    "outcome": "failed"
  }'
```

Send three failed login logs to trigger the security burst detector.

### 3.7 Run a guarded AIOps assessment

```bash
curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest payment-api performance and failed login risk."}'
```

Expected output:

- Assessment summary
- Tools used
- Recommendations
- `incidents_created` count
- Guardrail status

### 3.8 Verify incident deduplication

Run the same assessment twice:

```bash
curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest payment-api performance."}'

curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest payment-api performance."}'
```

Expected behavior:

- First run may create a new incident if no matching open incident exists.
- Second run should return `incidents_created: 0`.
- The existing open incident is updated and retains its correlation ID.

### 3.9 Use External Intel as context only

```bash
curl -X POST http://localhost:8000/external-intel/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Stripe public status page outage"}'
```

Expected behavior:

- A completed External Intel report can appear on the External Intel page.
- External Intel is shown as public context.
- No internal incident is created from public search alone.
- No agent evidence log is created from External Intel alone.

### 3.10 Run verification

```bash
docker compose build backend
docker compose run --rm backend python -m unittest discover -s tests
docker compose run --rm frontend npm run build
```

Expected result:

- Backend tests pass.
- Frontend TypeScript and Vite build pass.
- Vite may warn about chunk size; this is not a build failure.

---

## 4. Agent and Code Breakdown

### High-level architecture

```mermaid
flowchart LR
    subgraph INPUT["Internal Inputs"]
        METRIC["POST /metrics/ingest<br/>system metrics"]
        ACCESS["POST /access-logs/ingest<br/>access logs"]
    end

    subgraph API["FastAPI Backend"]
        ROUTES["API routers"]
        DBSESSION["SQLAlchemy session"]
        ASSESS["AIOps assessment service"]
        EXT["External Intel service<br/>context only"]
    end

    subgraph DATA["PostgreSQL Memory"]
        M1[system_metrics]
        M2[access_logs]
        M3[incidents]
        M4[agent_task_logs]
        M5[external_intel_reports]
        M6[audit_logs]
    end

    subgraph AGENTS["Raw-Code AIOps Agents"]
        GUARD["PromptGuard"]
        MANAGER["ManagerAgent"]
        PERF["PerformanceAuditor"]
        SEC["SecuritySentinel"]
        INTEL["ExternalIntelAnalyst"]
        REMED["RemediationSpecialist"]
    end

    subgraph UI["React Command Center"]
        OVERVIEW["Overview"]
        DASH["Performance / Security"]
        INCIDENTS["Incidents"]
        EVIDENCE["Evidence"]
        CONTEXT["External Intel"]
    end

    METRIC --> ROUTES --> DBSESSION --> M1
    ACCESS --> ROUTES --> DBSESSION --> M2
    ROUTES --> ASSESS --> GUARD --> MANAGER
    MANAGER --> PERF --> M1
    MANAGER --> SEC --> M2
    MANAGER --> INTEL --> M5
    PERF --> REMED
    SEC --> REMED
    REMED --> M3
    REMED --> M4
    EXT --> M5
    M1 --> UI
    M2 --> UI
    M3 --> INCIDENTS
    M4 --> EVIDENCE
    M5 --> CONTEXT
```

### Agent pipeline

```mermaid
flowchart TD
    START([Operator runs assessment]) --> DATA_CHECK{Any internal<br/>metrics or access logs?}
    DATA_CHECK -- No --> EMPTY["Return accepted empty-state response<br/>0 incidents, 0 evidence logs"]
    DATA_CHECK -- Yes --> PROMPT["PromptGuard<br/>normalize and validate mission prompt"]

    PROMPT --> SAFE{Prompt accepted?}
    SAFE -- No --> REJECT["Rejected response<br/>no incident, no evidence"]
    SAFE -- Yes --> MANAGER["ManagerAgent<br/>delegate identity-aware tasks"]

    MANAGER --> PERF["PerformanceAuditor<br/>read_system_metrics"]
    MANAGER --> SEC["SecuritySentinel<br/>read_access_logs"]
    MANAGER --> INTEL["ExternalIntelAnalyst<br/>read_external_intel_reports"]

    PERF --> FINDINGS["Internal findings"]
    SEC --> FINDINGS
    INTEL --> CONTEXT["Context recommendation only<br/>create_incident=false<br/>persist_evidence=false"]

    FINDINGS --> REMED["RemediationSpecialist<br/>recommend_only<br/>adds human approval note to high severity"]
    REMED --> DEDUPE["Correlation and dedupe<br/>source label + correlation ID"]
    DEDUPE --> INCIDENT["Create or update open incident"]
    DEDUPE --> EVIDENCE["Persist agent task log"]
```

### Agent responsibilities

| Agent / service | Role | Reads | Writes | Incident behavior |
|---|---|---|---|---|
| `PromptGuard` | Reject destructive or unsafe mission prompts | Mission prompt | Guarded prompt object | Never creates incidents |
| `ManagerAgent` | Coordinates specialist agents | Guarded prompt | Finding list | Delegates only |
| `PerformanceAuditor` | Detects resource pressure and availability risk | `system_metrics` | Performance findings | Can create performance incidents from internal metrics |
| `SecuritySentinel` | Detects failed login bursts and security-focused reviews | `access_logs` | Security findings | Can create security incidents from internal access logs |
| `ExternalIntelAnalyst` | Reads public intelligence reports for context | `external_intel_reports` | Context recommendation | Cannot create incidents or evidence |
| `RemediationSpecialist` | Adds controlled remediation guidance | Findings | Validated findings | Adds human approval note for high severity |
| `create_incident_from_finding` | Persists evidence and deduplicates incidents | Findings and open incidents | `incidents`, `agent_task_logs` | Creates or updates internal incidents only |

### Incident correlation design

Every internal finding carries:

| Field | Example | Purpose |
|---|---|---|
| `source_label` | `internal_metrics`, `access_logs` | Shows where evidence came from |
| `correlation_id` | `performance:detect_resource_pressure:payment-api` | Reuses the same open incident on repeated assessments |
| `incident_type` | `performance`, `security` | Separates operational and security events |
| `severity` | `high`, `medium`, `low` | Drives priority |

```mermaid
flowchart LR
    FINDING["New finding<br/>payment-api CPU high"] --> CID["Build correlation ID<br/>performance:detect_resource_pressure:payment-api"]
    CID --> SEARCH{Matching open<br/>incident exists?}
    SEARCH -- Yes --> UPDATE["Update existing incident<br/>return incidents_created = 0"]
    SEARCH -- No --> CREATE["Create new incident<br/>return incidents_created = 1"]
    UPDATE --> UI["UI shows one correlated incident"]
    CREATE --> UI
```

### Code map

```text
secure-saas-aiops-monitoring/
  backend/
    app/
      api/
        metrics.py             REST ingestion and listing for system metrics
        access_logs.py         REST ingestion and listing for access logs
        incidents.py           Incident register API
        agent_logs.py          Agent evidence API
        agents.py              AIOps kickoff and guarded prompt API
        external_intel.py      Public intelligence API
        health.py              Health check
      models/
        monitoring.py          SQLAlchemy tables and API metadata properties
      schemas/
        monitoring.py          Pydantic request and response contracts
      services/
        aiops_assessment.py    Assessment orchestration and no-data guard
        raw_agents.py          Raw-code agents, findings, dedupe, evidence persistence
        prompt_guard.py        Prompt safety validation
        external_intel.py      Serper integration and blocked query handling
      db/
        session.py             SQLAlchemy engine and session factory
    tests/
      test_aiops_guardrails.py
      test_external_intel_guardrails.py
  frontend/
    src/
      main.tsx                 React dashboard, API calls, page routing
      styles.css               Dashboard layout and responsive UI
  docs/
    V_MODEL.md                 Requirements traceability
    SSADM_NOTES.md             Data flow and security notes
    HANDOVER.md                Current product state and operating notes
```

### Frontend data flow

```mermaid
sequenceDiagram
    participant User as Operator
    participant UI as React dashboard
    participant API as FastAPI
    participant DB as PostgreSQL
    participant Agents as AIOps agents

    User->>UI: Open dashboard
    UI->>API: GET metrics, logs, incidents, evidence, external status
    API->>DB: Query latest operational state
    DB-->>API: Structured records
    API-->>UI: JSON
    User->>UI: Run AIOps crew
    UI->>API: POST /agents/prompt
    API->>Agents: Guard and assess internal data
    Agents->>DB: Create/update incidents and evidence
    API-->>UI: Assessment result
    UI->>API: Refresh dashboard data
```

---

## 5. API Reference

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Backend health check |
| `GET` | `/metrics` | List latest system metrics |
| `POST` | `/metrics/ingest` | Ingest one internal performance metric with `X-API-Key` |
| `GET` | `/access-logs` | List latest access logs |
| `POST` | `/access-logs/ingest` | Ingest one internal access log with `X-API-Key` |
| `GET` | `/incidents` | List deduplicated incidents |
| `GET` | `/agent-logs` | List agent evidence logs |
| `GET` | `/audit-logs` | List recent ingestion and assessment audit events |
| `POST` | `/agents/kickoff` | Run default guarded AIOps assessment |
| `POST` | `/agents/prompt` | Run assessment with a non-destructive mission prompt |
| `GET` | `/external-intel` | List completed public intelligence reports |
| `GET` | `/external-intel/status` | Show External Intel connection state |
| `POST` | `/external-intel/search` | Run guarded public search if Serper is configured |

<details>
<summary><strong>Example assessment response</strong></summary>

```json
{
  "mode": "raw",
  "summary": "Raw-code identity-aware AIOps crew completed guarded assessment.",
  "tools_used": [
    "PromptGuard",
    "SafeQueryTool",
    "ManagerAgent",
    "PerformanceAuditor",
    "SecuritySentinel",
    "ExternalIntelAnalyst",
    "RemediationSpecialist"
  ],
  "incidents_created": 1,
  "recommendations": [
    "Scale the affected service or inspect resource-heavy background tasks. Human approval required before operational changes."
  ],
  "guardrail_status": "accepted",
  "prompt_feedback": "Mission prompt accepted as non-destructive assessment guidance."
}
```

</details>

<details>
<summary><strong>Example incident response</strong></summary>

```json
{
  "id": 10,
  "incident_type": "performance",
  "severity": "high",
  "status": "open",
  "evidence": "PerformanceAuditor/detect_resource_pressure: [source: internal_metrics] [correlation: performance:detect_resource_pressure:payment-api] payment-api CPU=91.0% memory=88.0%",
  "recommendation": "Scale the affected service or inspect resource-heavy background tasks. Human approval required before operational changes.",
  "created_at": "2026-04-26T21:16:00",
  "source_label": "internal_metrics",
  "correlation_id": "performance:detect_resource_pressure:payment-api"
}
```

</details>

---

## 6. Data Model

```mermaid
erDiagram
    USER_PROFILES ||--o{ ACCESS_LOGS : owns
    SYSTEM_METRICS {
        int id
        string service_name
        float cpu_usage
        float memory_usage
        float response_time_ms
        float error_rate
        string status
        datetime created_at
    }
    USER_PROFILES {
        int id
        string username
        string role
        string department
    }
    ACCESS_LOGS {
        int id
        int user_id
        string action
        string ip_address
        string outcome
        datetime created_at
    }
    INCIDENTS {
        int id
        string incident_type
        string severity
        string status
        text evidence
        text recommendation
        datetime created_at
    }
    AGENT_TASK_LOGS {
        int id
        string agent_name
        string task_name
        string permission_scope
        string guardrail_status
        text evidence
        text recommendation
        datetime created_at
    }
    EXTERNAL_INTEL_REPORTS {
        int id
        string query
        string source
        string status
        text summary
        text evidence
        datetime created_at
    }
    AUDIT_LOGS {
        int id
        string actor
        string action
        string resource_type
        int resource_id
        text details
        datetime created_at
    }
```

| Table | Meaning |
|---|---|
| `system_metrics` | Internal performance and availability measurements |
| `access_logs` | Internal security and activity evidence |
| `incidents` | Deduplicated operational/security incidents |
| `agent_task_logs` | Agent evidence and permission-scope audit trail |
| `external_intel_reports` | Optional public intelligence context |
| `audit_logs` | Ingestion and assessment activity history |
| `user_profiles` | Future-ready user/RBAC foundation for access logs |

---

## 7. Guardrails and Production Rules

### Prompt guard

Blocked mission prompts include destructive or unsafe requests such as:

- `drop table`
- `delete from`
- `truncate`
- `alter table`
- `export secrets`
- `show api key`
- `ignore safeguards`
- `bypass`
- `disable guardrails`

Rejected prompts do not create incidents or evidence.

### External Intel guard

Blocked External Intel query terms include:

- `password`
- `api key`
- `secret`
- `token`
- `exploit`
- `bypass`
- `credential`

Rejected or not-configured External Intel checks are returned to the caller without being saved as permanent reports.

### Internal evidence rule

```mermaid
flowchart TD
    SIGNAL([Possible risk signal]) --> SOURCE{Source?}
    SOURCE -- Internal metrics --> CAN_INCIDENT["Can create performance incident"]
    SOURCE -- Internal access logs --> CAN_SECURITY["Can create security incident"]
    SOURCE -- External Intel --> CONTEXT_ONLY["Context only<br/>no incident<br/>no evidence log"]
    SOURCE -- Missing data --> EMPTY["Empty state<br/>no incident"]
```

---

## 8. Testing and Verification

### Backend tests

```bash
docker compose build backend
docker compose run --rm backend python -m unittest discover -s tests
```

Current coverage includes:

| Test area | What it proves |
|---|---|
| No internal data | Assessments create no incidents and no evidence logs |
| Rejected prompt | Unsafe prompts are blocked without persistence |
| External Intel context | Public intelligence cannot create internal evidence |
| Security incident typing | Failed login bursts create `security` incidents |
| Repeated assessment dedupe | Second run does not duplicate open incidents |
| Legacy incident upgrade | Older open incidents can be correlated safely |
| Service-specific dedupe | A new service does not get merged into an unrelated legacy incident |
| External Intel guardrails | Blocked queries are not persisted |

### Frontend build

```bash
docker compose run --rm frontend npm run build
```

This runs:

- TypeScript compile
- Vite production build

### Manual light test

```bash
curl -X POST http://localhost:8000/metrics/ingest \
  -H "X-API-Key: local-dev-ingest-key" \
  -H "Content-Type: application/json" \
  -d '{"service_name":"codex-mini-api","cpu_usage":92,"memory_usage":41,"response_time_ms":120,"error_rate":0.1,"status":"degraded"}'

curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest codex-mini-api performance."}'

curl -X POST http://localhost:8000/agents/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Assess latest codex-mini-api performance."}'
```

Expected:

- First assessment creates one performance incident.
- Second assessment creates zero duplicate incidents.
- Incident source is `internal_metrics`.
- Incident correlation ID is `performance:detect_resource_pressure:codex-mini-api`.

---

## 9. Deployment Notes

### Local Docker

```bash
docker compose up --build
docker compose logs -f backend
docker compose logs -f frontend
```

### Restart after environment changes

```bash
docker compose up -d --force-recreate backend
```

### Railway deployment

The MVP is live on Railway with separate `frontend`, `backend`, and `Postgres` services.

| Service | Live URL |
|---|---|
| Frontend | https://frontend-production-76ec8.up.railway.app |
| Backend | https://backend-production-a65d.up.railway.app |
| Backend health | https://backend-production-a65d.up.railway.app/health |

The backend uses Railway's runtime `$PORT`, and the frontend is configured with `VITE_API_BASE_URL=https://backend-production-a65d.up.railway.app`.

### Jenkins scaffold

`Jenkinsfile` is included to show CI/CD intent:

1. Install/build backend and frontend
2. Run tests
3. Build Docker images
4. Deploy to target environment
5. Verify health endpoint

---

## 10. Portfolio Evidence

This repository is designed to demonstrate:

- Full-stack delivery with React, TypeScript, FastAPI, SQLAlchemy, and PostgreSQL
- Real API ingestion instead of a simulator
- AIOps-style incident detection through identity-aware agents
- Security-focused prompt and public-intel guardrails
- Incident deduplication and correlation design
- Business-readable dashboard UX
- Dockerized local operation
- Testable backend behavior
- V-Model and SSADM documentation awareness
- DevOps readiness through Docker, Jenkins, and Railway scaffolding

### Related documentation

| File | Purpose |
|---|---|
| `docs/HANDOVER.md` | Current operating state and recommended next work |
| `docs/V_MODEL.md` | Requirements and validation mapping |
| `docs/SSADM_NOTES.md` | Data flow, logical model, security notes |
| `docs/NO_LLM_SETUP_GUIDE.md` | How to run without optional model-service dependencies |
| `docs/ROADMAP_20_WEEKS.md` | Development roadmap |

---

<div align="center">

**Secure SaaS AIOps Monitoring turns raw internal telemetry into correlated incidents, visible evidence, and operator-ready recommendations.**

*Ingestion-driven data, contextual public intelligence, deduplicated incidents, and audit-ready evidence in a focused production-style MVP.*

</div>
