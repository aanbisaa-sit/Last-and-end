from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.report import build_report

def test_project_smoke():
    endpoint = Endpoint("api", "https://example.com")
    result = CheckResult(endpoint, 200, 10, datetime.now(timezone.utc))
    assert "Availability: 100.00%" in build_report([result])
