from __future__ import annotations

from pathlib import Path

from stafeta.chain import check_chain


def write_handoff(
    path: Path,
    handoff_id: str,
    parent: str | None,
    invariants: list[str],
    waiver: str | None = None,
) -> None:
    parent_yaml = f'"{parent}"' if parent else "null"
    invariant_lines = "\n".join(f"- {item}" for item in invariants)
    waiver_section = f"\n## Waived invariants\n\n- {waiver}\n" if waiver else ""
    path.write_text(
        f"""---
stafeta: "0.1"
id: "{handoff_id}"
created: "2026-09-20T16:00:00+03:00"
task: "Chain fixture"
status: in_progress
profile: knowledge
parent: {parent_yaml}
sender:
  agent: "fixture"
  vendor: "example"
  model: null
lang: "en"
---

## Invariants

{invariant_lines}
{waiver_section}
""",
        encoding="utf-8",
    )


def test_chain_reports_silently_dropped_invariant(tmp_path: Path) -> None:
    parent = "01K5M85YQ6E6XM1YSE7YB7A9PG"
    child = "01K5M85YQ6E6XM1YSE7YB7A9PH"
    write_handoff(tmp_path / "parent.md", parent, None, ["Never deploy."])
    write_handoff(tmp_path / "child.md", child, parent, ["Never delete data."])
    findings = check_chain(tmp_path)
    assert "C005" in {finding.rule_id for finding in findings}


def test_chain_accepts_explicit_waiver(tmp_path: Path) -> None:
    parent = "01K5M85YQ6E6XM1YSE7YB7A9PG"
    child = "01K5M85YQ6E6XM1YSE7YB7A9PH"
    write_handoff(tmp_path / "parent.md", parent, None, ["Never deploy."])
    write_handoff(
        tmp_path / "child.md",
        child,
        parent,
        ["Never delete data."],
        "Never deploy. [waived by @owner on 2026-09-20]",
    )
    assert check_chain(tmp_path) == []


def test_chain_reports_missing_parent_and_cycle(tmp_path: Path) -> None:
    first = "01K5M85YQ6E6XM1YSE7YB7A9PG"
    second = "01K5M85YQ6E6XM1YSE7YB7A9PH"
    write_handoff(tmp_path / "first.md", first, second, ["Never deploy."])
    write_handoff(tmp_path / "second.md", second, first, ["Never deploy."])
    write_handoff(
        tmp_path / "orphan.md",
        "01K5M85YQ6E6XM1YSE7YB7A9PJ",
        "01K5M85YQ6E6XM1YSE7YB7A9PK",
        ["Never deploy."],
    )
    rules = {finding.rule_id for finding in check_chain(tmp_path)}
    assert {"C003", "C004"} <= rules

