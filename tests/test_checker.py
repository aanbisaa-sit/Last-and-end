from last_and_end.checker import check_endpoint
from last_and_end.models import Endpoint


def test_check_endpoint_handles_bad_domain():
result = check_endpoint(Endpoint("bad", "http://127.0.0.1:9"), timeout_seconds=0.1)
assert result.ok is False
assert result.error is not None
