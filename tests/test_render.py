from last_and_end.render import render_summary
from last_and_end.status import ServiceStatus


def test_render_summary_contains_counts():
text = render_summary({ServiceStatus.HEALTHY: 2, ServiceStatus.DOWN: 1})
assert "Healthy: 2" in text
assert "Down: 1" in text
