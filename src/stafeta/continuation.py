"""Experimental, offline continuation checks over explicitly supplied observations.

A resume receipt describes consistency of supplied evidence at evaluation time. It
does not grant permission, authenticate the observer, reserve a resource, or
prevent changes between this check and an action.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, date, datetime
from pathlib import Path
from typing import cast

import jsonschema
import yaml
from yaml.nodes import MappingNode

from stafeta.models import RuleContext
from stafeta.parse import bullet_items, parse_text
from stafeta.readback import check_readback
from stafeta.rules import run
from stafeta.schema import format_checker, load_schema

RFC3339 = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}"
    r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])"
)
FULL_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class ContinuationError(Exception):
    """An input cannot be read or has an ambiguous or malformed representation."""


class _UniqueLoader(yaml.SafeLoader):
    """Reject repeated mapping keys, including keys introduced through merges."""

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[object, object]:
        self.flatten_mapping(node)
        result: dict[object, object] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                if key in result:
                    raise ContinuationError("duplicate YAML mapping key")
                result[key] = self.construct_object(value_node, deep=deep)
            except TypeError as error:
                raise ContinuationError("YAML mapping keys must be scalar values") from error
        return result


def _unique_json(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ContinuationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ContinuationError(f"non-JSON numeric constant: {value}")


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ContinuationError(f"{label} must be a mapping with string keys")
    return cast(dict[str, object], value)


def _yaml(text: str, label: str) -> dict[str, object]:
    try:
        return _mapping(yaml.load(text, Loader=_UniqueLoader), label)
    except (yaml.YAMLError, RecursionError, ValueError, OverflowError) as error:
        raise ContinuationError(f"{label}: malformed YAML") from error


def _json(text: str, label: str) -> dict[str, object]:
    try:
        value = json.loads(text, object_pairs_hook=_unique_json, parse_constant=_reject_constant)
    except (ValueError, RecursionError) as error:
        raise ContinuationError(f"{label}: malformed JSON") from error
    document = _mapping(value, label)
    schema = load_schema(label)
    validator = jsonschema.Draft202012Validator(schema, format_checker=format_checker())
    errors = sorted(validator.iter_errors(document), key=lambda error: str(list(error.path)))
    if errors:
        validation_error = errors[0]
        location = ".".join(str(part) for part in validation_error.path) or label
        raise ContinuationError(f"{label}.{location}: {validation_error.message}")
    for collection, key in (("resources", "id"), ("effects", "id"), ("run_inputs", "name")):
        _index(_rows(document, collection), key, f"{label}.{collection}")
    if label == "checkpoint":
        _index(_rows(document, "effects"), "idempotency_key", "checkpoint.effects")
    return document


def _rows(document: dict[str, object], name: str) -> list[dict[str, object]]:
    return cast(list[dict[str, object]], document[name])


def _index(rows: list[dict[str, object]], key: str, label: str) -> dict[str, dict[str, object]]:
    indexed: dict[str, dict[str, object]] = {}
    for row in rows:
        value = cast(str, row[key])
        if value in indexed:
            raise ContinuationError(f"{label}: duplicate {key}: {value}")
        indexed[value] = row
    return indexed


def _time(document: dict[str, object], key: str) -> datetime:
    raw = document.get(key)
    if not isinstance(raw, str) or RFC3339.fullmatch(raw) is None:
        raise ContinuationError(f"{key} is not a supported RFC3339 timestamp")
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, OverflowError) as error:
        raise ContinuationError(f"{key} is not a supported RFC3339 timestamp") from error
    if value.tzinfo is None or value.utcoffset() is None:
        raise ContinuationError(f"{key} requires an explicit offset")
    return value


def _digest(raw: bytes) -> str:
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def evaluate_files(
    handoff_path: Path,
    readback_path: Path,
    checkpoint_path: Path,
    observation_path: Path,
    now: datetime,
) -> dict[str, object]:
    """Return a deterministic draft receipt; never query or act on external systems.

    Each input is read exactly once. Its byte digest binds the same data that is
    parsed. Malformed sidecars raise ContinuationError. Contract failures and
    observed uncertainty produce an escalate or recheck receipt, never resume.
    """
    if now.tzinfo is None or now.utcoffset() is None:
        raise ContinuationError("now requires an explicit timezone offset")
    try:
        now = now.astimezone(UTC)
    except (ValueError, OverflowError) as error:
        raise ContinuationError("evaluation time is outside the supported UTC range") from error
    paths = {
        "handoff": handoff_path,
        "readback": readback_path,
        "checkpoint": checkpoint_path,
        "observation": observation_path,
    }
    raw: dict[str, bytes] = {}
    text: dict[str, str] = {}
    for label, path in paths.items():
        try:
            raw[label] = path.read_bytes()
            text[label] = raw[label].decode("utf-8")
        except (OSError, UnicodeError) as error:
            raise ContinuationError(f"cannot read {label} as UTF-8: {path}") from error
    bindings = {f"{label}_sha256": _digest(data) for label, data in raw.items()}
    checkpoint = _json(text["checkpoint"], "checkpoint")
    observation = _json(text["observation"], "observation")
    readback = _yaml(text["readback"], "readback")
    # The frozen parser is unchanged. Reject ambiguous front matter before using it.
    lines = text["handoff"].replace("\r\n", "\n").replace("\r", "\n").splitlines()
    if lines and lines[0] == "---" and "---" in lines[1:]:
        _yaml("\n".join(lines[1 : lines.index("---", 1)]), "handoff front matter")
    handoff = parse_text(text["handoff"], handoff_path)
    created = _time(checkpoint, "created")
    expires = _time(checkpoint, "expires_at")
    observed = _time(observation, "observed_at")
    if expires <= created:
        raise ContinuationError("expires_at must be later than created")

    reasons: list[dict[str, str]] = []
    severity = 0

    def reason(level: int, code: str, message: str) -> None:
        nonlocal severity
        severity = max(level, severity)
        reasons.append({"code": code, "message": message})

    for label in ("handoff", "readback"):
        if checkpoint[f"{label}_sha256"] != bindings[f"{label}_sha256"]:
            reason(2, f"{label}_digest_mismatch", f"Checkpoint does not bind these {label} bytes.")
    if observation["checkpoint_sha256"] != bindings["checkpoint_sha256"]:
        reason(2, "checkpoint_digest_mismatch", "Observation does not bind this checkpoint.")
    if handoff.front_matter is None or handoff.front_matter.get("id") != checkpoint["task_id"]:
        reason(2, "task_id_mismatch", "Checkpoint task_id does not match the handoff id.")
    findings = run(handoff, RuleContext(now=now.date()))
    # The frozen checker assumes hashable recheck indices after schema reporting.
    # Guard its input here so malformed nested values cannot escape as TypeError.
    readback_validator = jsonschema.Draft202012Validator(
        load_schema("readback"), format_checker=format_checker()
    )
    readback_errors = sorted(
        readback_validator.iter_errors(readback), key=lambda error: str(list(error.path))
    )
    if readback_errors:
        for validation_error in readback_errors:
            location = ".".join(str(part) for part in validation_error.path) or "readback"
            reason(2, "contract_RB001", f"{location}: {validation_error.message}")
    else:
        findings.extend(check_readback(handoff, readback, effective_date=now.date()))
    for finding in findings:
        if finding.severity == "error":
            reason(2, f"contract_{finding.rule_id}", finding.message)
    # jsonschema's date-time format support is optional. These direct checks are
    # required for the gate regardless of which optional packages are installed.
    artifact_times: dict[str, datetime] = {}
    for label, document, code in (
        ("handoff", handoff.front_matter or {}, "contract_S001"),
        ("readback", readback, "contract_RB001"),
    ):
        try:
            artifact_times[label] = _time(document, "created")
        except ContinuationError:
            reason(2, code, f"{label}.created must be a valid RFC3339 timestamp with offset.")
        else:
            if artifact_times[label] > now:
                reason(1, f"{label}_in_future", f"{label} creation is after evaluation time.")
    if (
        "handoff" in artifact_times
        and "readback" in artifact_times
        and artifact_times["handoff"] > artifact_times["readback"]
    ):
        reason(2, "handoff_after_readback", "Readback creation precedes handoff creation.")
    if "readback" in artifact_times and artifact_times["readback"] > created:
        reason(2, "readback_after_checkpoint", "Checkpoint creation precedes readback creation.")
    if handoff.front_matter is not None and "recheck_after" in handoff.front_matter:
        deadline = handoff.front_matter["recheck_after"]
        valid_date = isinstance(deadline, str) and FULL_DATE.fullmatch(deadline) is not None
        if valid_date:
            try:
                date.fromisoformat(cast(str, deadline))
            except ValueError:
                valid_date = False
        if not valid_date:
            reason(2, "contract_S001", "handoff.recheck_after must be a valid YYYY-MM-DD date.")
    if now < created:
        reason(1, "checkpoint_not_active", "Checkpoint creation is after evaluation time.")
    if now >= expires:
        reason(1, "checkpoint_expired", "Checkpoint has reached its expiry time.")
    if observed < created:
        reason(1, "observation_too_old", "Observation precedes checkpoint creation.")
    if observed > now:
        reason(1, "observation_in_future", "Observation is after evaluation time.")

    for collection, key, field in (
        ("resources", "id", "revision"),
        ("run_inputs", "name", "digest"),
        ("effects", "id", "status"),
    ):
        expected = _index(_rows(checkpoint, collection), key, collection)
        actual = _index(_rows(observation, collection), key, collection)
        for identity in actual:
            if identity not in expected:
                reason(2, f"unexpected_{collection}", f"Unexpected {collection} entry: {identity}.")
        for identity, planned in expected.items():
            if identity not in actual:
                reason(1, f"missing_{collection}", f"Missing {collection} observation: {identity}.")
                continue
            current = actual[identity]
            if collection == "effects":
                if current["status"] in {"applied", "unknown"}:
                    reason(
                        2,
                        "effect_requires_reconciliation",
                        f"Effect {identity} is {current['status']}; do not blindly replay it.",
                    )
                elif not isinstance(current["evidence"], str) or not current["evidence"].strip():
                    reason(
                        1, "effect_evidence_missing", f"Effect {identity} needs an evidence ref."
                    )
            elif current[field] is None or current[field] != planned[field]:
                reason(
                    1, f"{collection}_changed", f"{collection} entry {identity} needs rechecking."
                )

    if readback.get("conflicts"):
        reason(2, "readback_conflicts", "Readback declares unresolved conflicts.")
    questions = handoff.section("Open questions")
    has_questions = questions is not None and any(
        value != "None." for _, value in bullet_items(questions)
    )
    if has_questions or readback.get("questions_for_human"):
        reason(2, "human_questions_open", "Human questions require an answer before continuation.")
    rechecked = readback.get("rechecked")
    if isinstance(rechecked, list):
        seen: set[int] = set()
        for item in rechecked:
            if not isinstance(item, dict):
                continue
            index = item.get("item")
            if isinstance(index, int) and not isinstance(index, bool):
                if index in seen:
                    reason(2, "duplicate_recheck", f"Readback repeats State item {index}.")
                seen.add(index)
            result = item.get("result")
            if isinstance(result, str) and result in {"changed", "could_not_verify"}:
                reason(1, "state_needs_recheck", f"Readback State item {index} is not confirmed.")
    return {
        "relayready_receipt": "0.1-draft",
        "task_id": checkpoint["task_id"],
        "evaluated_at": now.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "decision": ("resume", "recheck", "escalate")[severity],
        "reasons": reasons,
        "bindings": bindings,
    }
