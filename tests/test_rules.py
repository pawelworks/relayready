from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from stafeta.models import RuleContext
from stafeta.parse import parse_file, parse_text
from stafeta.rules import run

ROOT = Path(__file__).parents[1]
NOW = date(2026, 9, 20)


@pytest.mark.parametrize("path", sorted((ROOT / "examples" / "valid").glob("*.md")))
def test_valid_rule_examples_are_clean(path: Path) -> None:
    findings = run(parse_file(path), RuleContext(now=NOW, check_pointers=True))
    assert findings == []


@pytest.mark.parametrize("path", sorted((ROOT / "examples" / "invalid").glob("*.md")))
def test_invalid_rule_examples_have_exact_findings(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<!-- EXPECT:([A-Z0-9,]+) -->", text)
    assert match is not None
    expected = set(match.group(1).split(","))
    findings = run(parse_file(path), RuleContext(now=NOW, check_pointers=True))
    assert {finding.rule_id for finding in findings} == expected


def test_repository_and_acceptance_handoffs_are_clean() -> None:
    repository_findings = run(
        parse_file(ROOT / "HANDOFF.md"), RuleContext(now=NOW, check_pointers=True)
    )
    assert all(finding.severity == "warning" for finding in repository_findings)
    acceptance = ROOT / "examples" / "acceptance" / "HANDOFF.md"
    assert run(parse_file(acceptance), RuleContext(now=NOW, check_pointers=True)) == []


def test_compat_missing_front_matter_is_a_warning() -> None:
    document = parse_text("## Goal\n\nLegacy handoff.\n", Path("legacy.md"))
    findings = run(document, RuleContext(now=NOW, compat=True))
    s001 = [finding for finding in findings if finding.rule_id == "S001"]
    assert len(s001) == 1
    assert s001[0].severity == "warning"


def test_pointer_hash_mismatch_is_reported(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("changed", encoding="utf-8")
    source = (ROOT / "examples" / "valid" / "S013.md").read_text(encoding="utf-8")
    source = source.replace(
        "`../../docs/BUILD_BRIEF.md`",
        "`target.txt`",
    )
    handoff = tmp_path / "HANDOFF.md"
    handoff.write_text(source, encoding="utf-8")
    findings = run(parse_file(handoff), RuleContext(now=NOW, check_pointers=True))
    assert [finding.rule_id for finding in findings] == ["S013"]
    assert "does not match" in findings[0].message


def test_empty_next_steps_and_unterminated_long_fence_are_reported() -> None:
    source = (ROOT / "examples" / "valid" / "S001.md").read_text(encoding="utf-8")
    source = source.replace("1. Run the matching rule check.", "")
    source += "\n## Notes\n\n```text\n" + "\n".join("line" for _ in range(41))
    findings = run(parse_text(source, Path("HANDOFF.md")), RuleContext(now=NOW))
    assert {finding.rule_id for finding in findings} == {"S009", "S010"}


def test_extra_section_cannot_interrupt_required_sequence() -> None:
    source = (ROOT / "examples" / "valid" / "S002.md").read_text(encoding="utf-8")
    source = source.replace("## State", "## Notes\n\nInterruption.\n\n## State")
    findings = run(parse_text(source, Path("HANDOFF.md")), RuleContext(now=NOW))
    assert {finding.rule_id for finding in findings} == {"S002"}


def test_invalid_recheck_date_is_left_to_schema_rule() -> None:
    source = (ROOT / "examples" / "valid" / "S001.md").read_text(encoding="utf-8")
    source = source.replace('lang: "en"', 'recheck_after: "not-a-date"\nlang: "en"')
    findings = run(parse_text(source, Path("HANDOFF.md")), RuleContext(now=NOW))
    assert {finding.rule_id for finding in findings} == {"S001"}


@pytest.mark.parametrize("timestamp", [
    "2026-99-99T99:99:99Z", "2026-02-30T12:00:00Z", "2026-09-20T25:00:00Z",
])
@pytest.mark.parametrize("remove_registration", [False, True])
def test_impossible_created_timestamp_is_rejected(
    timestamp: str, remove_registration: bool, monkeypatch: pytest.MonkeyPatch,
) -> None:
    if remove_registration:
        import jsonschema

        monkeypatch.delitem(jsonschema.FormatChecker.checkers, "date-time", raising=False)
    source = (ROOT / "examples" / "valid" / "S001.md").read_text(encoding="utf-8")
    source = source.replace("2026-09-20T16:00:00+03:00", timestamp)
    findings = run(parse_text(source, Path("HANDOFF.md")), RuleContext(now=NOW))
    assert {finding.rule_id for finding in findings} == {"S001"}
