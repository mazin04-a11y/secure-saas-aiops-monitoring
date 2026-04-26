from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import access_logs, agent_logs, agents, external_intel, health, incidents, metrics
from app.db.session import Base, engine

app = FastAPI(
    title="Secure SaaS AIOps Monitoring API",
    version="0.1.0",
    description="Project 4 backend for an AIOps-enabled SaaS monitoring platform.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https://.*\.up\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(access_logs.router, prefix="/access-logs", tags=["access logs"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(agent_logs.router, prefix="/agent-logs", tags=["agent logs"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(external_intel.router, prefix="/external-intel", tags=["external intelligence"])


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
