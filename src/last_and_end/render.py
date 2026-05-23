from .status import ServiceStatus


LABELS = {
ServiceStatus.HEALTHY: "Healthy",
ServiceStatus.DEGRADED: "Degraded",
ServiceStatus.DOWN: "Down",
ServiceStatus.UNKNOWN: "Unknown",
}


def render_summary(summary: dict[ServiceStatus, int]) -> str:
parts = []
for status in ServiceStatus:
    count = summary.get(status, 0)
    parts.append(f"{LABELS[status]}: {count}")
return " | ".join(parts)
