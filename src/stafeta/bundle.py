"""Recheck an exported workbench bundle with the full local Python validator."""

from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from stafeta.continuation import RFC3339, ContinuationError, evaluate_files

ARTIFACT_NAMES = ("handoff", "readback", "checkpoint", "observation")
FILENAMES = ("HANDOFF.md", "READBACK.yaml", "CHECKPOINT.json", "OBSERVATION.json")
MAX_BYTES = 2_000_000


def _unique(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ContinuationError(f"duplicate bundle JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> object:
    raise ContinuationError(f"non-JSON numeric constant: {value}")


def evaluate_bundle(
    path: Path, *, replay: bool = False, now: datetime | None = None,
) -> dict[str, object]:
    """Ignore claimed assessments; validate exact artifact bytes independently.

    Normal use evaluates current UTC. Explicit replay uses the supplied historical
    clock and is for reproduction only. Artifacts are never executed or fetched.
    """
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ContinuationError("bundle exceeds the 2 MB input limit")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique,
                           parse_constant=_constant)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise ContinuationError("bundle cannot be read as unambiguous UTF-8 JSON") from error
    if not isinstance(value, dict) or value.get("relayready_workbench") != "0.1-draft":
        raise ContinuationError("unsupported workbench bundle profile")
    artifacts = value.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != set(ARTIFACT_NAMES):
        raise ContinuationError("bundle must contain exactly four named artifact strings")
    if any(not isinstance(artifacts[name], str) or not artifacts[name]
           for name in ARTIFACT_NAMES):
        raise ContinuationError("bundle artifacts must be nonempty UTF-8 strings")
    evaluated_at = now or datetime.now(UTC)
    if replay:
        if now is not None:
            raise ContinuationError("replay and an explicit evaluation time are mutually exclusive")
        timestamp = value.get("evaluated_at")
        if not isinstance(timestamp, str) or RFC3339.fullmatch(timestamp) is None:
            raise ContinuationError("replay requires an RFC 3339 evaluated_at with offset")
        try:
            evaluated_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except (ValueError, OverflowError) as error:
            raise ContinuationError("bundle replay timestamp is invalid") from error
    try:
        with tempfile.TemporaryDirectory(prefix="relayready-bundle-") as directory:
            files = []
            for name, filename in zip(ARTIFACT_NAMES, FILENAMES, strict=True):
                target = Path(directory) / filename
                target.write_bytes(cast(str, artifacts[name]).encode("utf-8"))
                files.append(target)
            return evaluate_files(files[0], files[1], files[2], files[3], now=evaluated_at)
    except (OSError, UnicodeError) as error:
        raise ContinuationError("bundle artifacts could not be checked locally") from error
