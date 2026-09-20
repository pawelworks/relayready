"""Create and verify Stafeta 0.1 receiver readbacks."""

from __future__ import annotations

import re
from contextlib import suppress
from datetime import date, datetime
from pathlib import Path
from typing import cast

import jsonschema
import yaml

from stafeta.hashing import invariants_hash
from stafeta.models import Document, Finding
from stafeta.parse import bullet_items, ordered_items
from stafeta.schema import format_checker, load_schema

YAML_FENCE = re.compile(r"```ya?ml\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)
TOKEN = re.compile(r"[\w'-]+", re.UNICODE)


class ReadbackError(Exception):
    """A readback input could not be loaded."""


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ReadbackError("readback must be a YAML mapping")
    return cast(dict[str, object], value)


def load_yaml(path: Path) -> dict[str, object]:
    """Load a readback YAML document."""
    try:
        return _mapping(yaml.safe_load(path.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ReadbackError(str(error)) from error


def load_from_text(path: Path) -> dict[str, object]:
    """Extract the first fenced YAML mapping whose first key is stafeta_readback."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ReadbackError(str(error)) from error
    for match in YAML_FENCE.finditer(text):
        try:
            value = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if isinstance(value, dict) and next(iter(value), None) == "stafeta_readback":
            return _mapping(value)
    raise ReadbackError("no fenced YAML readback was found")


def _items(document: Document, section_name: str, *, omit_none: bool) -> list[str]:
    section = document.section(section_name)
    if section is None:
        return []
    values = [value for _, value in bullet_items(section)]
    return [value for value in values if not (omit_none and value == "None.")]


def required_rechecks(document: Document, effective_date: date) -> list[int]:
    """Return one-based State item indices that the receiver must recheck."""
    state = document.section("State")
    if state is None:
        return []
    items = bullet_items(state)
    all_stale = False
    raw_deadline = document.front_matter.get("recheck_after") if document.front_matter else None
    if isinstance(raw_deadline, str):
        with suppress(ValueError):
            all_stale = date.fromisoformat(raw_deadline) < effective_date
    return [
        index
        for index, (_, value) in enumerate(items, start=1)
        if all_stale or value.endswith("[recheck]")
    ]


def new_readback(document: Document, effective_date: date | None = None) -> dict[str, object]:
    """Build a schema-valid readback skeleton from a handoff."""
    if document.front_matter is None:
        raise ReadbackError("handoff has no readable front matter")
    handoff_id = document.front_matter.get("id")
    if not isinstance(handoff_id, str):
        raise ReadbackError("handoff has no valid id")
    invariants = _items(document, "Invariants", omit_none=False)
    rejected = _items(document, "Do not redo", omit_none=True)
    questions = _items(document, "Open questions", omit_none=True)
    next_steps = document.section("Next steps")
    actions = ordered_items(next_steps) if next_steps else []
    today = effective_date or date.today()
    return {
        "stafeta_readback": "0.1",
        "handoff_id": handoff_id,
        "created": datetime.now().astimezone().isoformat(timespec="seconds"),
        "receiver": {"agent": "unknown", "vendor": "unknown", "model": None},
        "goal_restated": "Restate the handoff goal in your own words.",
        "invariants_hash": invariants_hash(invariants),
        "invariants_echo": invariants,
        "will_not_redo": list(range(1, len(rejected) + 1)),
        "rechecked": [
            {
                "item": item,
                "result": "could_not_verify",
                "note": "Replace with the verification result before acting.",
            }
            for item in required_rechecks(document, today)
        ],
        "conflicts": [],
        "questions_for_human": questions,
        "first_action": actions[0][1] if actions else "Identify the first safe action.",
    }


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _integer_list(value: object) -> list[int]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, int) and not isinstance(item, bool)]


def _overlap(left: str, right: str) -> float:
    left_tokens = {token.casefold() for token in TOKEN.findall(left)}
    right_tokens = {token.casefold() for token in TOKEN.findall(right)}
    union = left_tokens | right_tokens
    return len(left_tokens & right_tokens) / len(union) if union else 0.0


def check_readback(
    document: Document,
    readback: dict[str, object],
    effective_date: date | None = None,
) -> list[Finding]:
    """Check schema and all mechanical acknowledgment requirements."""
    validator = jsonschema.Draft202012Validator(
        load_schema("readback"),
        format_checker=format_checker(),
    )
    findings: list[Finding] = []
    for error in sorted(validator.iter_errors(readback), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "readback"
        findings.append(Finding("RB001", "error", f"{location}: {error.message}"))
    if document.front_matter is None:
        findings.append(Finding("RB002", "error", "handoff front matter is unreadable"))
        return findings

    handoff_id = document.front_matter.get("id")
    if readback.get("handoff_id") != handoff_id:
        findings.append(Finding("RB002", "error", "handoff_id does not match"))

    invariants = _items(document, "Invariants", omit_none=False)
    expected_hash = invariants_hash(invariants)
    if readback.get("invariants_hash") != expected_hash:
        findings.append(Finding("RB003", "error", "invariants_hash does not match"))
    if _string_list(readback.get("invariants_echo")) != invariants:
        findings.append(Finding("RB004", "error", "invariants_echo differs or is reordered"))

    rejected = _items(document, "Do not redo", omit_none=True)
    present_indices = set(_integer_list(readback.get("will_not_redo")))
    missing_rejected = [
        index for index in range(1, len(rejected) + 1) if index not in present_indices
    ]
    if missing_rejected:
        findings.append(
            Finding(
                "RB005",
                "error",
                "will_not_redo omits indices: " + ", ".join(map(str, missing_rejected)),
            )
        )

    rechecked = readback.get("rechecked")
    rechecked_indices = {
        item.get("item")
        for item in rechecked
        if isinstance(rechecked, list) and isinstance(item, dict)
    } if isinstance(rechecked, list) else set()
    required = required_rechecks(document, effective_date or date.today())
    missing_rechecks = [index for index in required if index not in rechecked_indices]
    if missing_rechecks:
        findings.append(
            Finding(
                "RB006",
                "error",
                "rechecked omits State items: " + ", ".join(map(str, missing_rechecks)),
            )
        )

    questions = _items(document, "Open questions", omit_none=True)
    acknowledged = set(_string_list(readback.get("questions_for_human")))
    missing_questions = [question for question in questions if question not in acknowledged]
    if missing_questions:
        findings.append(
            Finding("RB007", "error", "questions_for_human omits an Open questions item")
        )

    goal_section = document.section("Goal")
    goal = goal_section.text if goal_section else ""
    restated = readback.get("goal_restated")
    if isinstance(restated, str) and _overlap(goal, restated) > 0.80:
        findings.append(
            Finding(
                "RB008",
                "warning",
                "goal_restated has token Jaccard overlap above 0.80",
            )
        )
    return findings


def dump_yaml(readback: dict[str, object]) -> str:
    """Serialize a readback without sorting contract fields."""
    return yaml.safe_dump(readback, sort_keys=False, allow_unicode=True)
