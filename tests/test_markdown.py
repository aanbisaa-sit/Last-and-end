from datetime import datetime, timezone

from last_and_end.markdown import build_markdown_report
from last_and_end.models import CheckResult, Endpoint


def test_markdown_report_has_heading():
endpoint = Endpoint("api", "https://example.com")
text = build_markdown_report([CheckResult(endpoint, 200, 10, datetime.now(timezone.utc))])
assert text.startswith("# Status Report")
