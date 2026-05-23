from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.report import build_report


def test_report_includes_availability():
endpoint = Endpoint("api", "https://example.com")
report = build_report([CheckResult(endpoint, 200, 10, datetime.now(timezone.utc))])
assert "Availability: 100.00%" in report
