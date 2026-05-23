from dataclasses import dataclass

@dataclass(frozen=True)
class AlertPolicy:
    minimum_failures: int = 2
    alert_on_degraded: bool = False
