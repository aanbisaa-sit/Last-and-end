from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint


def test_check_result_ok_when_status_matches():
endpoint = Endpoint(name="api", url="https://example.com")
result = CheckResult(endpoint, 200, 42, datetime.now(timezone.utc))
assert result.ok is True


def test_check_result_not_ok_when_error_exists():
endpoint = Endpoint(name="api", url="https://example.com")
result = CheckResult(endpoint, None, None, datetime.now(timezone.utc), error="timeout")
assert result.ok is False
