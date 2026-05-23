from datetime import datetime
from .models import CheckResult, Endpoint

def result_to_dict(result: CheckResult) -> dict[str, object]:
    return {
        "name": result.endpoint.name,
        "url": result.endpoint.url,
        "expected_status": result.endpoint.expected_status,
        "status_code": result.status_code,
        "latency_ms": result.latency_ms,
        "checked_at": result.checked_at.isoformat(),
        "error": result.error,
    }

def result_from_dict(data: dict[str, object]) -> CheckResult:
    endpoint = Endpoint(str(data["name"]), str(data["url"]), int(data["expected_status"]))
    checked_at = datetime.fromisoformat(str(data["checked_at"]))
    status_code = data.get("status_code")
    latency_ms = data.get("latency_ms")
    return CheckResult(endpoint, None if status_code is None else int(status_code), None if latency_ms is None else int(latency_ms), checked_at, None if data.get("error") is None else str(data.get("error")))
