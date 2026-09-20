from __future__ import annotations

import json
import sys
from pathlib import Path

from stafeta.bench import grade_fixture


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: grade.py WORKSPACE", file=sys.stderr)
        return 2
    metrics = grade_fixture(Path(__file__).parent, Path(sys.argv[1]))
    print(json.dumps(metrics, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
