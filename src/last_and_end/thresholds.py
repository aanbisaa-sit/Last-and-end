from dataclasses import dataclass

@dataclass(frozen=True)
class LatencyThresholds:
    warning_ms: int = 750
    critical_ms: int = 1500

    def level_for(self, latency_ms: int | None) -> str:
        if latency_ms is None:
            return "unknown"
        if latency_ms >= self.critical_ms:
            return "critical"
        if latency_ms >= self.warning_ms:
            return "warning"
        return "normal"
