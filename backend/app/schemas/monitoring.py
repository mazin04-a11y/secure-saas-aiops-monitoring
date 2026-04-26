from datetime import datetime

from pydantic import BaseModel, Field


class MetricCreate(BaseModel):
    service_name: str = Field(examples=["checkout-api"])
    cpu_usage: float = Field(ge=0, le=100)
    memory_usage: float = Field(ge=0, le=100)
    response_time_ms: float = Field(ge=0)
    error_rate: float = Field(ge=0, le=100)
    status: str = "healthy"


class MetricRead(MetricCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AccessLogCreate(BaseModel):
    username: str = Field(examples=["ops_lead"])
    action: str = Field(examples=["login"])
    ip_address: str = Field(examples=["203.0.113.42"])
    outcome: str = Field(default="success", examples=["failed"])


class AccessLogRead(BaseModel):
    id: int
    user_id: int
    action: str
    ip_address: str
    outcome: str
    created_at: datetime

    class Config:
        from_attributes = True


class IncidentRead(BaseModel):
    id: int
    incident_type: str
    severity: str
    status: str
    evidence: str
    recommendation: str
    created_at: datetime
    source_label: str
    correlation_id: str

    class Config:
        from_attributes = True


class AgentTaskLogRead(BaseModel):
    id: int
    agent_name: str
    task_name: str
    permission_scope: str
    guardrail_status: str
    evidence: str
    recommendation: str
    created_at: datetime
    source_label: str
    correlation_id: str

    class Config:
        from_attributes = True


class AgentAssessment(BaseModel):
    mode: str
    summary: str
    tools_used: list[str]
    incidents_created: int
    recommendations: list[str]
    guardrail_status: str = "accepted"
    prompt_feedback: str = "No mission prompt supplied. Default AIOps assessment used."


class AgentPromptRequest(BaseModel):
    prompt: str | None = Field(
        default=None,
        max_length=500,
        description="Optional non-destructive mission prompt used to focus the raw-code agent assessment.",
    )


class ExternalIntelRequest(BaseModel):
    query: str = Field(min_length=3, max_length=240, examples=["payment-api outage indicators"])


class ExternalIntelRead(BaseModel):
    id: int | None = None
    query: str
    source: str
    status: str
    summary: str
    evidence: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ExternalIntelStatus(BaseModel):
    connected: bool
    status: str
    latest_summary: str | None = None
