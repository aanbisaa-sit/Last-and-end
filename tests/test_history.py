from datetime import datetime, timezone

from last_and_end.history import ResultHistory
from last_and_end.models import CheckResult, Endpoint


def test_history_respects_limit():
endpoint = Endpoint("api", "https://example.com")
history = ResultHistory(max_items=1)
history.add(CheckResult(endpoint, 200, 10, datetime.now(timezone.utc)))
history.add(CheckResult(endpoint, 500, 11, datetime.now(timezone.utc)))
assert len(history.all()) == 1
