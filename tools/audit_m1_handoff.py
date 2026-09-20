"""Small M1-only audit for the repository handoff.

This is not the Stafeta CLI and does not claim L1 conformance. It guards the
repository's own handoff until the rule engine is implemented in M2.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "Goal",
    "Done means",
    "Invariants",
    "State",
    "Done so far",
    "Do not redo",
    "Next steps",
    "Open questions",
    "Pointers",
)
STATUS_TAG = re.compile(
    r"\[(?:unverified|recheck|verified \d{4}-\d{2}-\d{2}"
    r"(?: by [^:\]]+)?: [^\]]+)\]$"
)


def section(text: str, name: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(name)}\s*$\n(.*?)(?=^## |\Z)", text)
    return match.group(1).strip() if match else ""


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    headings = re.findall(r"(?m)^## (.+?)\s*$", text)
    positions = [headings.index(name) if name in headings else -1 for name in REQUIRED_SECTIONS]
    if any(position < 0 for position in positions):
        errors.append("missing a required section")
    elif positions != sorted(positions):
        errors.append("required sections are out of order")
    if not text.startswith("---\n"):
        errors.append("front matter is missing")
    for line in section(text, "State").splitlines():
        if line.startswith("- ") and not STATUS_TAG.search(line):
            errors.append(f"State item lacks a valid terminal tag: {line}")
    body = text.split("---", 2)[-1]
    if len(re.findall(r"\b\w+\b", body)) >= 4000:
        errors.append("body reaches the hard word limit")
    if "profile: code" in text and "Environment" not in headings:
        errors.append("code profile lacks Environment")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = audit(args.path)
    for error in errors:
        print(f"error: {error}")
    if errors:
        return 1
    print(f"M1 draft audit passed: {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

