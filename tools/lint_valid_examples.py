"""Run the installed CLI against every valid example and require zero findings."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).parents[1]
    failed = False
    for path in sorted((root / "examples" / "valid").glob("*.md")):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "stafeta",
                "lint",
                str(path),
                "--check-pointers",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode not in {0, 1}:
            print(result.stderr or result.stdout, file=sys.stderr)
            failed = True
            continue
        payload = json.loads(result.stdout)
        findings = payload["findings"]
        if findings:
            print(f"{path}: {findings}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

