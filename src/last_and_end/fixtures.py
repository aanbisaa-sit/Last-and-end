from datetime import datetime, timezone

from .models import CheckResult, Endpoint


def sample_result(name: str = "homepage", status_code: int = 200) -> CheckResult:
endpoint = Endpoint(name=name, url="https://example.com")
return CheckResult(endpoint, status_code, 32, datetime.now(timezone.utc))
