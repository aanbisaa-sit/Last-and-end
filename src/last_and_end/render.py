from .status import ServiceStatus

LABELS = {
    ServiceStatus.HEALTHY: "Healthy",
    ServiceStatus.DEGRADED: "Degraded",
    ServiceStatus.DOWN: "Down",
    ServiceStatus.UNKNOWN: "Unknown",
}

def render_summary(summary: dict[ServiceStatus, int]) -> str:
    return " | ".join(f"{LABELS[status]}: {summary.get(status, 0)}" for status in ServiceStatus)
