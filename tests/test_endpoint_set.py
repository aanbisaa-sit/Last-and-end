from last_and_end.endpoint_set import dedupe_endpoints
from last_and_end.models import Endpoint


def test_dedupe_endpoints_by_url():
endpoints = [Endpoint("a", "https://example.com"), Endpoint("b", "https://example.com")]
assert len(dedupe_endpoints(endpoints)) == 1
