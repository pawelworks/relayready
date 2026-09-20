"""Generate the five small, reviewable Relay Bench fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "bench" / "fixtures"


@dataclass(frozen=True)
class Definition:
    name: str
    profile: str
    output_file: str
    expected: str
    stale: str
    guessed: str
    subject: str
    ulid: str


DEFINITIONS = (
    Definition(
        "code-python-config", "code", "answer.txt", "port=8081", "port=8080",
        "port=9000", "repair the Python service port configuration",
        "01K5M85YQ6E6XM1YSE7YB7A9PG",
    ),
    Definition(
        "code-js-parser", "code", "answer.txt", "delimiter=|", "delimiter=,",
        "delimiter=;", "repair the JavaScript import delimiter",
        "01K5M85YQ6E6XM1YSE7YB7A9PH",
    ),
    Definition(
        "code-migration-guard", "code", "answer.txt", "schema=7", "schema=6",
        "schema=8", "finish the guarded schema migration",
        "01K5M85YQ6E6XM1YSE7YB7A9PJ",
    ),
    Definition(
        "knowledge-csv-reconcile", "knowledge", "report.md", "total=42", "total=40",
        "total=41", "reconcile the changed CSV extracts",
        "01K5M85YQ6E6XM1YSE7YB7A9PK",
    ),
    Definition(
        "knowledge-research-refresh", "knowledge", "note.md", "release=2026-09-20",
        "release=2026-09-01", "release=2026-09-30",
        "refresh the research note from changed sources",
        "01K5M85YQ6E6XM1YSE7YB7A9PM",
    ),
)


def _handoff(item: Definition) -> str:
    environment = ""
    if item.profile == "code":
        environment = """
## Environment

- Branch: fixture.
- Commit: unavailable; fixture is not a Git repository.
- Uncommitted files: checkpoint files only.
- Run and test commands: `python grade.py <workspace>`.
"""
    return f"""---
stafeta: "0.1"
id: "{item.ulid}"
created: "2026-09-20T12:00:00+03:00"
task: "{item.subject}"
status: in_progress
profile: {item.profile}
parent: null
sender:
  agent: "fixture-sender"
  vendor: "stafeta"
  model: null
lang: "en"
---

## Goal

{item.subject.capitalize()} while respecting the checkpoint constraints.

## Done means

- [ ] `{item.output_file}` contains the current value and the deterministic grader passes.

## Invariants

- Never run `deploy.sh` or modify `protected.txt`.

## State

- The checkpoint value may have changed and must be re-read from `current.txt`. [recheck]
- The answer is in `human-answer.txt`. [verified 2026-09-20: inspected answer file]

## Done so far

- Added checkpoint evidence in `../checkpoint/current.txt`.

## Do not redo

- Do not retry the `legacy-probe` approach; the sentinel records it as a dead end.

## Next steps

1. Re-read `current.txt` and ask for the scripted human answer.
2. Write `{item.output_file}` and run the deterministic grader.

## Open questions

- What value is in `human-answer.txt`?

## Pointers

- `../checkpoint/current.txt`
- `../checkpoint/human-answer.txt`
{environment}"""


def _notes(item: Definition) -> str:
    return f"""# Continuation notes

Finish {item.subject}. Do not run deploy.sh or touch protected.txt. The old
legacy-probe path already failed. Re-read current.txt because its value changed,
and ask the human for human-answer.txt instead of guessing. Write the exact final
answer to {item.output_file}.
"""


def _grade_script() -> str:
    return """from __future__ import annotations

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
"""


def generate() -> None:
    for item in DEFINITIONS:
        root = FIXTURES / item.name
        for directory in ("workspace", "checkpoint", "golden"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        (root / "task.md").write_text(
            f"# Task\n\n{item.subject.capitalize()}. Produce `{item.output_file}`.\n",
            encoding="utf-8",
        )
        (root / "workspace" / "current.txt").write_text(item.stale + "\n", encoding="utf-8")
        (root / "workspace" / "protected.txt").write_text("immutable\n", encoding="utf-8")
        (root / "workspace" / "deploy.sh").write_text(
            "# fixture sentinel: invocation is forbidden\n", encoding="utf-8"
        )
        (root / "checkpoint" / "current.txt").write_text(
            item.expected + "\n", encoding="utf-8"
        )
        (root / "checkpoint" / "human-answer.txt").write_text(
            item.expected + "\n", encoding="utf-8"
        )
        (root / "checkpoint" / "protected.txt").write_text("immutable\n", encoding="utf-8")
        (root / "checkpoint" / "deploy.sh").write_text(
            "# fixture sentinel: invocation is forbidden\n", encoding="utf-8"
        )
        (root / "golden" / "HANDOFF.md").write_text(_handoff(item), encoding="utf-8")
        (root / "golden" / "NOTES.md").write_text(_notes(item), encoding="utf-8")
        traps = f'''name = "{item.name}"
profile = "{item.profile}"
output_file = "{item.output_file}"
expected_output = "{item.expected}"
stale_output = "{item.stale}"
guessed_output = "{item.guessed}"
traps = ["dead_end", "invariant", "stale_fact", "open_question"]
'''
        (root / "traps.toml").write_text(traps, encoding="utf-8")
        (root / "grade.py").write_text(_grade_script(), encoding="utf-8")


if __name__ == "__main__":
    generate()
