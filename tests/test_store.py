from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.store import append_result, read_results


def test_append_and_read_result(tmp_path):
path = tmp_path / "results.jsonl"
endpoint = Endpoint("api", "https://example.com")
append_result(path, CheckResult(endpoint, 200, 12, datetime.now(timezone.utc)))
assert read_results(path)[0].endpoint.name == "api"
