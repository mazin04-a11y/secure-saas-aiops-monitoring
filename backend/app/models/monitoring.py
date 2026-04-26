from datetime import datetime
import re

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(30), default="viewer")
    department: Mapped[str] = mapped_column(String(80), default="operations")

    access_logs: Mapped[list["AccessLog"]] = relationship(back_populates="user")


class AccessLog(Base):
    __tablename__ = "access_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    action: Mapped[str] = mapped_column(String(120))
    ip_address: Mapped[str] = mapped_column(String(45))
    outcome: Mapped[str] = mapped_column(String(30), default="success")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[UserProfile] = relationship(back_populates="access_logs")


class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_name: Mapped[str] = mapped_column(String(80), index=True)
    cpu_usage: Mapped[float] = mapped_column(Float)
    memory_usage: Mapped[float] = mapped_column(Float)
    response_time_ms: Mapped[float] = mapped_column(Float)
    error_rate: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="healthy")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_type: Mapped[str] = mapped_column(String(80), index=True)
    severity: Mapped[str] = mapped_column(String(30), index=True)
    status: Mapped[str] = mapped_column(String(30), default="open")
    evidence: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def source_label(self) -> str:
        return _extract_metadata(self.evidence, "source") or "internal"

    @property
    def correlation_id(self) -> str:
        return _extract_metadata(self.evidence, "correlation") or f"incident:{self.id}"


class AgentTaskLog(Base):
    __tablename__ = "agent_task_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agent_name: Mapped[str] = mapped_column(String(80), index=True)
    task_name: Mapped[str] = mapped_column(String(120), index=True)
    permission_scope: Mapped[str] = mapped_column(String(160))
    guardrail_status: Mapped[str] = mapped_column(String(30), default="accepted")
    evidence: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def source_label(self) -> str:
        return _extract_metadata(self.evidence, "source") or "internal_agent"

    @property
    def correlation_id(self) -> str:
        return _extract_metadata(self.evidence, "correlation") or f"agent-log:{self.id}"


class ExternalIntelReport(Base):
    __tablename__ = "external_intel_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    query: Mapped[str] = mapped_column(String(240), index=True)
    source: Mapped[str] = mapped_column(String(80), default="serper")
    status: Mapped[str] = mapped_column(String(40), default="created")
    summary: Mapped[str] = mapped_column(Text)
    evidence: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def _extract_metadata(evidence: str, key: str) -> str | None:
    match = re.search(rf"\[{key}: ([^\]]+)\]", evidence)
    return match.group(1) if match else None
