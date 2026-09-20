from __future__ import annotations

import copy
from collections.abc import Callable
from datetime import date
from pathlib import Path

import pytest
import yaml

from stafeta.models import Document
from stafeta.parse import parse_text
from stafeta.readback import (
    ReadbackError,
    check_readback,
    load_from_text,
    new_readback,
)


def handoff_text() -> str:
    return """---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PG"
created: "2026-09-20T16:00:00+03:00"
task: "Finish report"
status: in_progress
profile: knowledge
parent: null
sender:
  agent: "sender"
  vendor: "example"
  model: null
lang: "en"
---

## Goal

Finish the audited report without repeating rejected work.

## Done means

- [ ] The report passes review.

## Invariants

- Never publish the draft.

## State

- The source has 12 rows. [verified 2026-09-20: counted locally]
- The owner may have replaced the source. [recheck]

## Done so far

- Drafted the introduction in `report.md`.

## Do not redo

- Do not retry OCR; the source is structured text.
- Do not change the reporting period; it was approved.

## Next steps

1. Recheck the source.

## Open questions

- Which title should the report use?

## Pointers

- `report.md`
"""


def valid_pair() -> tuple[Document, dict[str, object]]:
    document = parse_text(handoff_text(), Path("HANDOFF.md"))
    readback = new_readback(document, date(2026, 9, 20))
    readback["goal_restated"] = "Complete a reviewed report while preserving prior decisions."
    readback["receiver"] = {"agent": "receiver", "vendor": "example", "model": None}
    return document, readback


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda value: value.update(handoff_id="01K5M85YQ6E6XM1YSE7YB7A9PH"), "RB002"),
        (lambda value: value.update(invariants_hash="sha256:" + "0" * 64), "RB003"),
        (lambda value: value.update(invariants_echo=["Different invariant."]), "RB004"),
        (lambda value: value.update(will_not_redo=[1]), "RB005"),
        (lambda value: value.update(rechecked=[]), "RB006"),
        (lambda value: value.update(questions_for_human=[]), "RB007"),
        (lambda value: value.update(first_action=""), "RB001"),
    ],
)
def test_each_required_readback_failure_mode(
    mutation: Callable[[dict[str, object]], None], expected: str
) -> None:
    document, baseline = valid_pair()
    readback = copy.deepcopy(baseline)
    mutation(readback)
    findings = check_readback(document, readback, date(2026, 9, 20))
    assert expected in {finding.rule_id for finding in findings}


def test_valid_readback_and_near_copy_warning() -> None:
    document, readback = valid_pair()
    assert check_readback(document, readback, date(2026, 9, 20)) == []
    readback["goal_restated"] = "Finish the audited report without repeating rejected work."
    findings = check_readback(document, readback, date(2026, 9, 20))
    assert [(item.rule_id, item.severity) for item in findings] == [("RB008", "warning")]


@pytest.mark.parametrize("timestamp", [
    "2026-99-99T99:99:99Z", "2026-02-30T12:00:00Z", "2026-09-20T25:00:00Z",
])
@pytest.mark.parametrize("remove_registration", [False, True])
def test_impossible_readback_timestamp_is_rejected(
    timestamp: str, remove_registration: bool, monkeypatch: pytest.MonkeyPatch,
) -> None:
    if remove_registration:
        import jsonschema

        monkeypatch.delitem(jsonschema.FormatChecker.checkers, "date-time", raising=False)
    document, readback = valid_pair()
    readback["created"] = timestamp
    findings = check_readback(document, readback, date(2026, 9, 20))
    assert {finding.rule_id for finding in findings} == {"RB001"}


def test_from_text_extracts_first_matching_yaml_fence(tmp_path: Path) -> None:
    _, readback = valid_pair()
    text = (
        "```yaml\nother: value\n```\n\n```yaml\n"
        + yaml.safe_dump(readback, sort_keys=False)
        + "```\n"
    )
    path = tmp_path / "reply.md"
    path.write_text(text, encoding="utf-8")
    assert load_from_text(path)["handoff_id"] == readback["handoff_id"]
    path.write_text("No readback here.", encoding="utf-8")
    with pytest.raises(ReadbackError):
        load_from_text(path)
