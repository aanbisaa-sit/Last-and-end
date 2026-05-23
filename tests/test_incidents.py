from datetime import datetime, timezone

from last_and_end.incidents import detect_incident
from last_and_end.models import CheckResult, Endpoint


def test_detect_incident_after_failures():
endpoint = Endpoint("api", "https://example.com")
results = [
    CheckResult(endpoint, 500, 10, datetime.now(timezone.utc)),
    CheckResult(endpoint, 500, 10, datetime.now(timezone.utc)),
]
incident = detect_incident(results)
assert incident is not None
assert incident.result_count == 2
