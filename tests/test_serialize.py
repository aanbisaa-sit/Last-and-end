from datetime import datetime, timezone

from last_and_end.models import CheckResult, Endpoint
from last_and_end.serialize import result_from_dict, result_to_dict


def test_result_round_trip():
endpoint = Endpoint("api", "https://example.com")
result = CheckResult(endpoint, 200, 12, datetime.now(timezone.utc))
loaded = result_from_dict(result_to_dict(result))
assert loaded.endpoint.name == result.endpoint.name
assert loaded.status_code == result.status_code
