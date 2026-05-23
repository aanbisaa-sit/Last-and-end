from last_and_end.notifications import build_notification


def test_build_notification_trims_fields():
message = build_notification(" Status ", " Body ", "warning")
assert message.title == "Status"
assert message.body == "Body"
assert message.severity == "warning"
