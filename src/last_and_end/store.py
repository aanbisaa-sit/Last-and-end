import json
from pathlib import Path
from .models import CheckResult
from .serialize import result_from_dict, result_to_dict

def append_result(path: Path, result: CheckResult) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(result_to_dict(result), sort_keys=True) + "\n")

def read_results(path: Path) -> list[CheckResult]:
    if not path.exists():
        return []
    return [result_from_dict(json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line]
