from sqlalchemy.orm import Session

from app.models.monitoring import AuditLog


def record_audit_log(
    db: Session,
    *,
    action: str,
    actor: str = "system",
    resource_type: str,
    resource_id: int | None = None,
    details: str = "",
) -> AuditLog:
    audit_log = AuditLog(
        actor=actor,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    return audit_log
