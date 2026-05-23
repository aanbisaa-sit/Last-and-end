from datetime import datetime, timezone

from last_and_end.availability import availability_ratio
from last_and_end.models import CheckResult, Endpoint


def test_availability_ratio():
endpoint = Endpoint("api", "https://example.com")
results = [
    CheckResult(endpoint, 200, 10, datetime.now(timezone.utc)),
    CheckResult(endpoint, 500, 10, datetime.now(timezone.utc)),
]
assert availability_ratio(results) == 0.5
