from last_and_end.thresholds import LatencyThresholds


def test_latency_threshold_levels():
thresholds = LatencyThresholds(warning_ms=100, critical_ms=200)
assert thresholds.level_for(50) == "normal"
assert thresholds.level_for(150) == "warning"
assert thresholds.level_for(250) == "critical"
