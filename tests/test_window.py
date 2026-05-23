from datetime import datetime, timedelta, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.window import recent_results


def test_recent_results_filters_old_items():
endpoint = Endpoint("api", "https://example.com")
now = datetime.now(timezone.utc)
old = CheckResult(endpoint, 200, 10, now - timedelta(hours=2))
new = CheckResult(endpoint, 200, 10, now)
assert recent_results([old, new], minutes=30) == [new]
