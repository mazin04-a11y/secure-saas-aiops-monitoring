import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.monitoring import ExternalIntelReport
from app.services.external_intel import run_external_intel_search


class ExternalIntelGuardrailTests(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        self.session = sessionmaker(bind=engine)()

    def tearDown(self) -> None:
        self.session.close()

    def test_blocked_external_intel_query_is_not_persisted(self) -> None:
        report = run_external_intel_search(self.session, "api key exposure check")

        self.assertIsNone(report.id)
        self.assertEqual(report.status, "rejected")
        self.assertIn("blocked term", report.summary)
        self.assertEqual(self.session.query(ExternalIntelReport).count(), 0)


if __name__ == "__main__":
    unittest.main()
