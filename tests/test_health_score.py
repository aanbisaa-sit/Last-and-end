from datetime import datetime, timezone

from last_and_end.health_score import health_score
from last_and_end.models import CheckResult, Endpoint


def test_health_score_returns_percentage():
endpoint = Endpoint("api", "https://example.com")
results = [CheckResult(endpoint, 200, 10, datetime.now(timezone.utc))]
assert health_score(results) == 100
