from datetime import datetime, timezone

from last_and_end.classifier import classify_result
from last_and_end.models import CheckResult, Endpoint
from last_and_end.status import ServiceStatus


def make_result(status_code=200, error=None):
endpoint = Endpoint("api", "https://example.com")
return CheckResult(endpoint, status_code, 25, datetime.now(timezone.utc), error=error)


def test_healthy_status():
assert classify_result(make_result()) == ServiceStatus.HEALTHY


def test_down_status_from_error():
assert classify_result(make_result(None, "timeout")) == ServiceStatus.DOWN
