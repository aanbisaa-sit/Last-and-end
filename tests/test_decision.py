from datetime import datetime, timezone

from last_and_end.decision import should_alert
from last_and_end.models import CheckResult, Endpoint
from last_and_end.policy import AlertPolicy


def test_should_alert_with_policy_threshold():
endpoint = Endpoint("api", "https://example.com")
result = CheckResult(endpoint, 500, 10, datetime.now(timezone.utc))
assert should_alert([result], AlertPolicy(minimum_failures=1)) is True
