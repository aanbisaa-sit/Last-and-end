import pytest

from last_and_end.scheduler import Schedule


def test_schedule_rejects_tiny_interval():
with pytest.raises(ValueError):
    Schedule(interval_seconds=1).validate()
