from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.status import ServiceStatus
from last_and_end.summary import summarize_results


def test_summarize_results_counts_health():
endpoint = Endpoint("api", "https://example.com")
result = CheckResult(endpoint, 200, 18, datetime.now(timezone.utc))
summary = summarize_results([result])
assert summary[ServiceStatus.HEALTHY] == 1
