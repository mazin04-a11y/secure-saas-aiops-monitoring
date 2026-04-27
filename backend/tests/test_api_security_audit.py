import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.models.monitoring import AuditLog, SystemMetric


class ApiSecurityAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine(
            "sqlite+pysqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()

        def override_get_db():
            yield self.session

        app.dependency_overrides[get_db] = override_get_db
        settings.ingest_api_keys = "test-ingest-key"
        settings.rate_limit_requests = 100
        settings.rate_limit_window_seconds = 60
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        settings.ingest_api_keys = None
        settings.rate_limit_requests = 120
        settings.rate_limit_window_seconds = 60
        self.session.close()

    def test_ingest_requires_configured_api_key(self) -> None:
        response = self.client.post(
            "/metrics/ingest",
            json={
                "service_name": "checkout-api",
                "cpu_usage": 91,
                "memory_usage": 82,
                "response_time_ms": 950,
                "error_rate": 4.2,
                "status": "degraded",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.session.query(SystemMetric).count(), 0)
        self.assertEqual(self.session.query(AuditLog).count(), 0)

    def test_metric_ingest_with_api_key_creates_audit_log(self) -> None:
        response = self.client.post(
            "/metrics/ingest",
            headers={"X-API-Key": "test-ingest-key"},
            json={
                "service_name": "checkout-api",
                "cpu_usage": 91,
                "memory_usage": 82,
                "response_time_ms": 950,
                "error_rate": 4.2,
                "status": "degraded",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.session.query(SystemMetric).count(), 1)
        audit_log = self.session.query(AuditLog).one()
        self.assertEqual(audit_log.actor, "api_key")
        self.assertEqual(audit_log.action, "metric_ingested")
        self.assertEqual(audit_log.resource_type, "system_metric")
        self.assertIn("checkout-api", audit_log.details)

    def test_agent_assessment_creates_audit_log(self) -> None:
        response = self.client.post("/agents/prompt", json={"prompt": "Assess current service health."})

        self.assertEqual(response.status_code, 200)
        audit_log = self.session.query(AuditLog).one()
        self.assertEqual(audit_log.action, "agent_assessment_run")
        self.assertEqual(audit_log.resource_type, "agent_assessment")
        self.assertIn("incidents_created=0", audit_log.details)

    def test_rate_limit_returns_429_after_threshold(self) -> None:
        settings.rate_limit_requests = 1

        first = self.client.get("/incidents")
        second = self.client.get("/incidents")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.json()["detail"], "Rate limit exceeded. Try again shortly.")


if __name__ == "__main__":
    unittest.main()
