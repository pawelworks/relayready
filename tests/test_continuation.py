"""Continuation receipts must fail closed when supplied state becomes uncertain."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

import jsonschema
import pytest
import yaml

from stafeta.continuation import ContinuationError, evaluate_files
from stafeta.parse import parse_text
from stafeta.readback import check_readback, new_readback
from stafeta.schema import load_schema

NOW = datetime(2026, 9, 20, 14, 0, tzinfo=UTC)
TASK_ID = "01K5M85YQ6E6XM1YSE7YB7A9PG"
HANDOFF = """---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PG"
created: "2026-09-20T13:00:00Z"
task: "Review an unpublished report"
status: in_progress
profile: knowledge
parent: null
sender:
  agent: sender
  vendor: example
lang: en
---

## Goal

Complete a source review while preserving the unpublished report.

## Done means

- [ ] The report has a reviewed source.

## Invariants

- Never publish the report.

## State

- Source version needs checking. [recheck]

## Done so far

- Prepared `report.md` for review.

## Do not redo

- None.

## Next steps

1. Review the source.

## Open questions

- None.

## Pointers

- `report.md`
"""


def digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


class Case:
    """Fixture which rebinds edited payloads unless a test deliberately tampers."""

    def __init__(self, root: Path) -> None:
        self.paths = (
            root / "HANDOFF.md",
            root / "READBACK.yaml",
            root / "CHECKPOINT.json",
            root / "OBSERVATION.json",
        )
        self.handoff = HANDOFF
        self.readback = new_readback(parse_text(HANDOFF, self.paths[0]), NOW.date())
        self.readback["created"] = "2026-09-20T13:01:00Z"
        self.readback["goal_restated"] = "Check references before finalizing the private document."
        self.readback["rechecked"] = [
            {"item": 1, "result": "confirmed", "note": "Source inspected."}
        ]
        self.checkpoint: dict[str, object] = {
            "relayready_checkpoint": "0.1-draft",
            "task_id": TASK_ID,
            "created": "2026-09-20T13:30:00Z",
            "expires_at": "2026-09-20T15:00:00Z",
            "handoff_sha256": "",
            "readback_sha256": "",
            "resources": [{"id": "report", "revision": "rev-7"}],
            "effects": [{"id": "save-review", "idempotency_key": "review:7"}],
            "run_inputs": [{"name": "review-skill", "digest": "sha256:" + "a" * 64}],
        }
        self.observation: dict[str, object] = {
            "relayready_observation": "0.1-draft",
            "checkpoint_sha256": "",
            "observed_at": "2026-09-20T13:59:00Z",
            "resources": [{"id": "report", "revision": "rev-7"}],
            "effects": [{"id": "save-review", "status": "not_applied", "evidence": "ledger:7"}],
            "run_inputs": [{"name": "review-skill", "digest": "sha256:" + "a" * 64}],
        }

    def write(self) -> None:
        self.paths[0].write_bytes(self.handoff.encode())
        self.paths[1].write_bytes(yaml.safe_dump(self.readback).encode())
        for index, label in enumerate(("handoff", "readback")):
            self.checkpoint[f"{label}_sha256"] = digest(self.paths[index].read_bytes())
        self.paths[2].write_bytes(json.dumps(self.checkpoint).encode())
        self.observation["checkpoint_sha256"] = digest(self.paths[2].read_bytes())
        self.paths[3].write_bytes(json.dumps(self.observation).encode())

    def evaluate(self, now: datetime = NOW) -> dict[str, object]:
        return evaluate_files(*self.paths, now=now)


@pytest.fixture
def case(tmp_path: Path) -> Case:
    return Case(tmp_path)


def rows(value: dict[str, object], name: str) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], value[name])


def codes(receipt: dict[str, object]) -> set[str]:
    return {str(item["code"]) for item in rows(receipt, "reasons")}


def test_resume_is_deterministic_and_binds_exact_bytes(case: Case) -> None:
    case.handoff = case.handoff.replace("\n", "\r\n")
    case.write()
    first = case.evaluate()
    assert first == case.evaluate()
    assert first["decision"] == "resume"
    assert first["reasons"] == []
    assert first["evaluated_at"] == "2026-09-20T14:00:00Z"
    bindings = cast(dict[str, str], first["bindings"])
    assert bindings["handoff_sha256"] == digest(case.paths[0].read_bytes())
    assert bindings["handoff_sha256"] != digest(HANDOFF.encode())
    assert set(bindings) == {
        "handoff_sha256",
        "readback_sha256",
        "checkpoint_sha256",
        "observation_sha256",
    }


def test_reads_each_input_once(case: Case, monkeypatch: pytest.MonkeyPatch) -> None:
    case.write()
    real_read = Path.read_bytes
    counts: dict[Path, int] = {}

    def tracked_read(path: Path) -> bytes:
        counts[path] = counts.get(path, 0) + 1
        return real_read(path)

    monkeypatch.setattr(Path, "read_bytes", tracked_read)
    assert case.evaluate()["decision"] == "resume"
    assert counts == dict.fromkeys(case.paths, 1)


@pytest.mark.parametrize("index", [0, 1, 2])
def test_even_whitespace_tampering_breaks_byte_binding(case: Case, index: int) -> None:
    case.write()
    case.paths[index].write_bytes(case.paths[index].read_bytes() + b"\n")
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert f"{('handoff', 'readback', 'checkpoint')[index]}_digest_mismatch" in codes(receipt)


@pytest.mark.parametrize(
    ("collection", "field", "replacement"),
    [
        ("resources", "revision", "rev-8"),
        ("resources", "revision", None),
        ("run_inputs", "digest", "sha256:" + "b" * 64),
        ("run_inputs", "digest", None),
    ],
)
def test_revision_and_run_input_drift_require_recheck(
    case: Case, collection: str, field: str, replacement: object
) -> None:
    rows(case.observation, collection)[0][field] = replacement
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "recheck"
    assert f"{collection}_changed" in codes(receipt)


@pytest.mark.parametrize("status", ["unknown", "applied"])
def test_effects_never_blindly_replay(case: Case, status: str) -> None:
    rows(case.observation, "effects")[0]["status"] = status
    rows(case.observation, "resources")[0]["revision"] = None
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"  # Escalation wins over recheck.
    assert "effect_requires_reconciliation" in codes(receipt)


def test_not_applied_requires_supplied_evidence(case: Case) -> None:
    rows(case.observation, "effects")[0]["evidence"] = None
    case.write()
    assert case.evaluate()["decision"] == "recheck"


@pytest.mark.parametrize("collection", ["resources", "effects", "run_inputs"])
def test_missing_observation_requires_recheck(case: Case, collection: str) -> None:
    case.observation[collection] = []
    case.write()
    assert case.evaluate()["decision"] == "recheck"


@pytest.mark.parametrize("collection", ["resources", "effects", "run_inputs"])
def test_unknown_observation_escalates(case: Case, collection: str) -> None:
    row = rows(case.observation, collection)[0].copy()
    row["name" if collection == "run_inputs" else "id"] = "unknown"
    rows(case.observation, collection).append(row)
    case.write()
    assert case.evaluate()["decision"] == "escalate"


@pytest.mark.parametrize("label", ["checkpoint", "observation"])
@pytest.mark.parametrize("collection", ["resources", "effects", "run_inputs"])
def test_duplicate_logical_identity_is_malformed(case: Case, label: str, collection: str) -> None:
    value = case.checkpoint if label == "checkpoint" else case.observation
    row = rows(value, collection)[0].copy()
    changed_key = {"resources": "revision", "run_inputs": "digest", "effects": "idempotency_key"}
    key = (
        changed_key[collection] if label == "checkpoint" or collection != "effects" else "evidence"
    )
    row[key] = "sha256:" + "b" * 64
    rows(value, collection).append(row)
    case.write()
    with pytest.raises(ContinuationError, match="duplicate"):
        case.evaluate()


def test_duplicate_idempotency_key_is_malformed(case: Case) -> None:
    rows(case.checkpoint, "effects").append({"id": "other", "idempotency_key": "review:7"})
    case.write()
    with pytest.raises(ContinuationError, match="duplicate idempotency_key"):
        case.evaluate()


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("observed_at", "2026-09-20T14:00:01Z", "observation_in_future"),
        ("observed_at", "2026-09-20T13:29:59Z", "observation_too_old"),
        ("expires_at", "2026-09-20T14:00:00Z", "checkpoint_expired"),
        ("created", "2026-09-20T14:01:00Z", "checkpoint_not_active"),
    ],
)
def test_time_window_rechecks(case: Case, field: str, value: str, expected: str) -> None:
    target = case.observation if field == "observed_at" else case.checkpoint
    target[field] = value
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "recheck"
    assert expected in codes(receipt)


@pytest.mark.parametrize("value", ["2026-09-20T13:00:00Z", "2026-09-20T13:30:00Z"])
def test_reversed_or_empty_checkpoint_window_is_malformed(case: Case, value: str) -> None:
    case.checkpoint["expires_at"] = value
    case.write()
    with pytest.raises(ContinuationError, match="later than"):
        case.evaluate()


@pytest.mark.parametrize("field", ["conflicts", "questions_for_human"])
def test_readback_conflicts_or_questions_escalate(case: Case, field: str) -> None:
    case.readback[field] = ["The owner must resolve the disagreement."]
    case.write()
    assert case.evaluate()["decision"] == "escalate"


def test_unacknowledged_human_question_escalates(case: Case) -> None:
    case.handoff = case.handoff.replace(
        "## Open questions\n\n- None.", "## Open questions\n\n- Which source is approved?"
    )
    case.write()
    assert "human_questions_open" in codes(case.evaluate())
    assert "contract_RB007" in codes(case.evaluate())


@pytest.mark.parametrize("result", ["changed", "could_not_verify"])
def test_rechecked_state_must_be_confirmed(case: Case, result: str) -> None:
    rows(case.readback, "rechecked")[0]["result"] = result
    case.write()
    assert case.evaluate()["decision"] == "recheck"


def test_duplicate_readback_recheck_escalates(case: Case) -> None:
    rows(case.readback, "rechecked").append(rows(case.readback, "rechecked")[0].copy())
    case.write()
    assert "duplicate_recheck" in codes(case.evaluate())


def test_invalid_readback_and_handoff_escalate(case: Case) -> None:
    case.readback["invariants_echo"] = ["Changed invariant."]
    case.handoff = case.handoff.replace("[recheck]", "[unknown]")
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert {"contract_S003", "contract_RB004"} <= codes(receipt)


@pytest.mark.parametrize("value", [[], {}, ["not-an-index"]])
def test_malformed_readback_indices_escalate_without_crashing(case: Case, value: object) -> None:
    rows(case.readback, "rechecked")[0]["item"] = value
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert "contract_RB001" in codes(receipt)


def test_required_rechecks_use_supplied_evaluation_date(case: Case) -> None:
    case.handoff = case.handoff.replace("lang: en", 'lang: en\nrecheck_after: "2026-09-19"')
    case.handoff = case.handoff.replace("[recheck]", "[verified 2026-09-18: inspected]")
    case.readback["rechecked"] = []
    case.write()
    assert "contract_RB006" in codes(case.evaluate())


def test_effective_date_is_canonical_utc_for_equivalent_instants(case: Case) -> None:
    case.handoff = case.handoff.replace("lang: en", 'lang: en\nrecheck_after: "2026-09-20"')
    case.handoff = case.handoff.replace("[recheck]", "[verified 2026-09-20: inspected]")
    case.readback["rechecked"] = []
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "resume"
    assert receipt == case.evaluate(datetime.fromisoformat("2026-09-21T04:00:00+14:00"))


@pytest.mark.parametrize("index", [2, 3])
def test_duplicate_json_mapping_key_is_malformed(case: Case, index: int) -> None:
    case.write()
    original = case.paths[index].read_text()
    case.paths[index].write_text(original.replace("{", '{"resources": [],', 1))
    with pytest.raises(ContinuationError, match="duplicate JSON key"):
        case.evaluate()


@pytest.mark.parametrize("index", [0, 1])
def test_duplicate_yaml_mapping_key_is_malformed(case: Case, index: int) -> None:
    case.write()
    path = case.paths[index]
    text = path.read_text()
    duplicate = 'stafeta: "0.1"\n' if index == 0 else 'stafeta_readback: "0.1"\n'
    text = text.replace("---\n", "---\n" + duplicate, 1) if index == 0 else text + duplicate
    path.write_text(text)
    with pytest.raises(ContinuationError, match="duplicate YAML"):
        case.evaluate()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("created", "2026-09-20T13:30:00"),
        ("task_id", "not-a-ulid"),
        ("expires_at", "2026-13-20T15:00:00Z"),
        ("extra", "unexpected"),
    ],
)
def test_strict_checkpoint_schema(case: Case, field: str, value: str) -> None:
    case.checkpoint[field] = value
    case.write()
    with pytest.raises(ContinuationError):
        case.evaluate()


def test_nested_properties_and_whitespace_identifiers_rejected(case: Case) -> None:
    rows(case.checkpoint, "resources")[0]["id"] = " \t"
    case.write()
    with pytest.raises(ContinuationError):
        case.evaluate()
    rows(case.checkpoint, "resources")[0]["id"] = "report"
    rows(case.observation, "resources")[0]["unexpected"] = True
    case.write()
    with pytest.raises(ContinuationError):
        case.evaluate()


def test_naive_evaluation_time_and_missing_inputs_are_errors(case: Case) -> None:
    with pytest.raises(ContinuationError, match="timezone"):
        case.evaluate(NOW.replace(tzinfo=None))
    with pytest.raises(ContinuationError, match="cannot read"):
        case.evaluate()


def test_task_binding_mismatch_escalates(case: Case) -> None:
    case.checkpoint["task_id"] = "01K5M85YQ6E6XM1YSE7YB7A9PH"
    case.write()
    assert "task_id_mismatch" in codes(case.evaluate())


def test_empty_sets_allowed_and_wire_contracts_remain_frozen(case: Case) -> None:
    for key in ("resources", "effects", "run_inputs"):
        case.checkpoint[key] = []
        case.observation[key] = []
    case.write()
    assert case.evaluate()["decision"] == "resume"
    handoff = parse_text(case.handoff, case.paths[0])
    assert check_readback(handoff, case.readback, NOW.date()) == []
    assert load_schema("handoff")["$id"] == "urn:stafeta:schema:handoff:0.1"
    assert load_schema("readback")["$id"] == "urn:stafeta:schema:readback:0.1"
    jsonschema.validate(case.readback, load_schema("readback"))


@pytest.mark.parametrize("name", ["checkpoint", "observation"])
def test_packaged_schemas_match_normative_draft(name: str) -> None:
    root = Path(__file__).resolve().parents[1]
    assert load_schema(name) == json.loads((root / "spec" / f"{name}.schema.json").read_text())


@pytest.mark.parametrize("index", [0, 1])
@pytest.mark.parametrize("value", ["2026-13-20T12:00:00Z", "9" * 5000])
def test_yaml_constructor_failures_are_input_errors(case: Case, index: int, value: str) -> None:
    case.write()
    path = case.paths[index]
    original = path.read_text(encoding="utf-8")
    original_created = next(line for line in original.splitlines() if line.startswith("created:"))
    path.write_text(original.replace(original_created, f"created: {value}"), encoding="utf-8")
    with pytest.raises(ContinuationError, match="malformed YAML"):
        case.evaluate()


@pytest.mark.parametrize("artifact", ["handoff", "readback"])
@pytest.mark.parametrize(
    "value",
    [
        "2026-13-20T12:00:00Z",
        "2026-09-20T13:00:00+01:99",
        "20260920T13:00:00Z",
        "2026-09-20 13:00:00Z",
        "2026-09-20T13:00:00",
    ],
)
def test_artifact_timestamp_validation_is_independent_of_optional_formats(
    case: Case, monkeypatch: pytest.MonkeyPatch, artifact: str, value: str
) -> None:
    monkeypatch.delitem(jsonschema.FormatChecker.checkers, "date-time", raising=False)
    if artifact == "handoff":
        case.handoff = case.handoff.replace(
            'created: "2026-09-20T13:00:00Z"', f'created: "{value}"'
        )
    else:
        case.readback["created"] = value
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert ("contract_S001" if artifact == "handoff" else "contract_RB001") in codes(receipt)


@pytest.mark.parametrize("value", ["2026-09-31", "20260920", "2026-09-20T00:00:00Z"])
def test_recheck_date_validation_is_independent_of_optional_formats(
    case: Case, monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    monkeypatch.delitem(jsonschema.FormatChecker.checkers, "date", raising=False)
    case.handoff = case.handoff.replace("lang: en", f'lang: en\nrecheck_after: "{value}"')
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert "contract_S001" in codes(receipt)


@pytest.mark.parametrize(
    ("handoff_created", "readback_created", "expected"),
    [
        ("2026-09-20T13:02:00Z", "2026-09-20T13:01:00Z", "handoff_after_readback"),
        ("2026-09-20T13:00:00Z", "2026-09-20T13:31:00Z", "readback_after_checkpoint"),
        ("2026-09-20T14:01:00Z", "2026-09-20T14:02:00Z", "handoff_in_future"),
    ],
)
def test_artifact_causality_cannot_resume(
    case: Case, handoff_created: str, readback_created: str, expected: str
) -> None:
    case.handoff = case.handoff.replace(
        'created: "2026-09-20T13:00:00Z"', f'created: "{handoff_created}"'
    )
    case.readback["created"] = readback_created
    case.write()
    receipt = case.evaluate()
    assert receipt["decision"] == "escalate"
    assert expected in codes(receipt)


def test_equal_artifact_creation_times_allow_resume(case: Case) -> None:
    case.readback["created"] = "2026-09-20T13:00:00Z"
    case.checkpoint["created"] = "2026-09-20T13:00:00Z"
    case.write()
    assert case.evaluate()["decision"] == "resume"
