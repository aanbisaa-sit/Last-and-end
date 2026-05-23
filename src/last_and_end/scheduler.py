from dataclasses import dataclass


@dataclass(frozen=True)
class Schedule:
interval_seconds: int = 60

def validate(self) -> None:
    if self.interval_seconds < 5:
        raise ValueError("interval_seconds must be at least 5")
