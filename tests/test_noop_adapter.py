from last_and_end.noop_adapter import NoopNotificationAdapter
from last_and_end.notifications import build_notification


def test_noop_adapter_records_messages():
adapter = NoopNotificationAdapter()
adapter.send(build_notification("title", "body"))
assert len(adapter.messages) == 1
