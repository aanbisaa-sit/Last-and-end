from last_and_end.policy import AlertPolicy


def test_default_alert_policy():
policy = AlertPolicy()
assert policy.minimum_failures == 2
assert policy.alert_on_degraded is False
