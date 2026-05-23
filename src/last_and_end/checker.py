import time
import urllib.error
import urllib.request
from .errors   import RetryExhaustedError, TimeoutError
from .models   import CheckResult, Endpoint, utc_now


def check_endpoint(
    endpoint: Endpoint,
    timeout_seconds: float = 5.0,
    retries: int = 0,
) -> CheckResult:
    """HTTP-GET *endpoint* and return a :class:`CheckResult`.

    Args:
        endpoint: the endpoint to probe.
        timeout_seconds: per-attempt socket timeout (seconds, must be >= 0).
        retries: additional attempts after the first failure (must be >= 0).

    Returns:
        CheckResult with the HTTP status code and measured latency on success,
        or an error annotation on failure / timeout.
    """
    if timeout_seconds < 0:
        raise ValueError(f"timeout_seconds must be >= 0, got {timeout_seconds!r}")
    if retries < 0:
        raise ValueError(f"retries must be >= 0, got {retries!r}")

    deadline = time.monotonic() + timeout_seconds
    last_error: str | None = None

    for attempt in range(1, retries + 2):  # first try + retries
        remaining = max(deadline - time.monotonic(), 0.01)
        if remaining <= 0:
            break  # deadline exceeded

        started = time.perf_counter()
        try:
            request = urllib.request.Request(
                endpoint.url,
                method="GET",
                headers={"User-Agent": "last-and-end/0.1"},
            )
            with urllib.request.urlopen(request, timeout=remaining) as response:
                return CheckResult(
                    endpoint,
                    response.status,
                    int((time.perf_counter() - started) * 1000),
                    utc_now(),
                )
        except urllib.error.HTTPError as exc:
            # HTTP error codes like 404/500 are still valid responses
            return CheckResult(
                endpoint,
                exc.code,
                int((time.perf_counter() - started) * 1000),
                utc_now(),
            )
        except Exception as exc:
            last_error = exc.__class__.__name__

    # All attempts exhausted or deadline hit
    raise RetryExhaustedError(
        attempts=retries + 1,
        last_error=last_error,
    )
