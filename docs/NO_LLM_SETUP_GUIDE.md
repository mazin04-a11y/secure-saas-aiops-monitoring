# No-LLM Setup Guide

Use this guide to rebuild the project manually without AI help.

## Prerequisites

- WSL Ubuntu
- Docker Desktop with WSL integration enabled
- VS Code with WSL and Dev Containers extensions
- Git

## Setup

```bash
cd ~/projects/secure-saas-aiops-monitoring
cp .env.example .env
docker compose up --build
```

## Verification

```bash
curl http://localhost:8000/health
python3 tests/api_smoke_test.py
```

Then open:

- http://localhost:5173
- http://localhost:8000/docs

## Development Workflow

1. Update backend models or API routes.
2. Update frontend API calls or dashboard panels.
3. Run Docker Compose locally.
4. Capture screenshots and test evidence.
5. Commit changes to GitHub.

## Real API Testing

Send real test payloads through the public ingestion endpoints:

```bash
curl -X POST http://localhost:8000/metrics/ingest \
  -H "Content-Type: application/json" \
  -d '{"service_name":"payment-api","cpu_usage":91,"memory_usage":88,"response_time_ms":1100,"error_rate":8.1,"status":"degraded"}'

curl -X POST http://localhost:8000/access-logs/ingest \
  -H "Content-Type: application/json" \
  -d '{"username":"security_user","action":"login","ip_address":"203.0.113.77","outcome":"failed"}'
```

Refresh the dashboard and review Performance, Security, Incidents, Agents, and Evidence.

## Optional Serper Search

Add this locally in `.env` only if you want public external intelligence:

```bash
SERPER_API_KEY=your_serper_key_here
```

Restart the backend:

```bash
docker compose restart backend
```

Then use the External Intel page or call:

```bash
curl -X POST http://localhost:8000/external-intel/search \
  -H "Content-Type: application/json" \
  -d '{"query":"payment provider public status outage"}'
```
