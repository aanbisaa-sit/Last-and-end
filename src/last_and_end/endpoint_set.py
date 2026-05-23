from .models import Endpoint

def dedupe_endpoints(endpoints: list[Endpoint]) -> list[Endpoint]:
    seen: set[str] = set()
    output: list[Endpoint] = []
    for endpoint in endpoints:
        if endpoint.url in seen:
            continue
        seen.add(endpoint.url)
        output.append(endpoint)
    return output
