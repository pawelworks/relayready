"""Generate one documentation page per lint rule from module docstrings."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
from types import ModuleType

RULE_IDS = tuple(f"S{number:03d}" for number in range(1, 14))


def page(module: ModuleType, rule_id: str) -> str:
    summary = (module.__doc__ or "").strip().splitlines()[0]
    extra = ""
    if rule_id == "S004":
        secrets = importlib.import_module("stafeta.rules.secrets")
        detail = (secrets.__doc__ or "").strip()
        extra = f"\n\n## Detection limits\n\n{detail}\n"
    return (
        f"# {summary}\n\n"
        f"Generated from `stafeta.rules.{rule_id.lower()}`. "
        "The normative requirement is in `spec/SPEC.md`."
        f"{extra}\n"
    )


def expected_files() -> dict[str, str]:
    files: dict[str, str] = {}
    links = []
    for rule_id in RULE_IDS:
        module = importlib.import_module(f"stafeta.rules.{rule_id.lower()}")
        filename = f"{rule_id}.md"
        files[filename] = page(module, rule_id)
        links.append(f"- [{rule_id}]({filename})")
    files["index.md"] = "# Lint rules\n\n" + "\n".join(links) + "\n"
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("docs/rules"))
    args = parser.parse_args()
    files = expected_files()
    if args.check:
        stale = [
            name
            for name, content in files.items()
            if not (args.output / name).is_file()
            or (args.output / name).read_text(encoding="utf-8") != content
        ]
        if stale:
            print("stale rule documentation: " + ", ".join(stale))
            return 1
        return 0
    args.output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (args.output / name).write_text(content, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

