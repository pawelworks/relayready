"""Generate simulated inputs and real, reproducible local gate receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from stafeta.continuation import evaluate_files
from stafeta.parse import parse_text
from stafeta.readback import dump_yaml, new_readback

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime.fromisoformat("2026-09-20T12:05:00+00:00")
CASES = (
    ("clean", "Ready to continue", "All declared observations match the checkpoint.", "resume"),
    ("revision-drift", "Resource changed", "Staging moved from revision 42 to 43.", "recheck"),
    ("uncertain-effect", "Interrupted mutation", "The previous attempt has an unknown outcome.",
     "escalate"),
    ("changed-input", "Skill bytes changed",
     "Skill bytes changed under the same release label 1.2.0.", "recheck"),
    ("human-decision", "Owner decision pending", "A correctly acknowledged question is unresolved.",
     "escalate"),
)


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def serialized(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def artifacts(case: str) -> tuple[bytes, bytes, dict[str, Any], dict[str, Any]]:
    question = "Does the owner approve a longer staging lock window?" if case == "human-decision" \
        else "None."
    handoff = f'''---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PG"
created: "2026-09-20T12:00:00Z"
task: "Continue the simulated staging migration review"
status: in_progress
profile: code
parent: null
sender:
  agent: "demo-sender"
  vendor: "example"
  model: null
lang: "en"
---

## Goal

Complete the staging migration review using the pinned inputs and a checked continuation decision.

## Done means

- [ ] The continuation receipt identifies unresolved prerequisites before any action.

## Invariants

- Never execute a production database mutation.
- Never retry an operation with an unknown prior outcome.

## State

- The simulated staging resource has revision 42. [recheck]
- All observations are simulated. [verified 2026-09-20: inspect this fixture]

## Done so far

- Recorded the simulation checkpoint in `CHECKPOINT.json`.

## Do not redo

- Do not apply the migration directly; the task is a staging review only.

## Next steps

1. Compare the current observations with the checkpoint before continuing the staging review.

## Open questions

- {question}

## Pointers

- `CHECKPOINT.json`
- `OBSERVATION.json`

## Environment

- This is a deterministic simulation; no external system is accessed.
- Evaluation time: 2026-09-20T12:05:00Z.
'''.encode()
    readback = new_readback(parse_text(handoff.decode(), Path("HANDOFF.md")), date(2026, 9, 20))
    readback.update(
        created="2026-09-20T12:01:00Z",
        receiver={"agent": "demo-receiver", "vendor": "example", "model": None},
        goal_restated="Review the staged change with the execution limits and recovery checks.",
        rechecked=[{"item": 1, "result": "confirmed",
                    "note": "Simulated revision 42; the gate compares a later observation."}],
    )
    readback_bytes = dump_yaml(readback).encode()
    checkpoint: dict[str, Any] = {
        "relayready_checkpoint": "0.1-draft",
        "task_id": readback["handoff_id"],
        "created": "2026-09-20T12:02:00Z",
        "expires_at": "2026-09-20T13:00:00Z",
        "handoff_sha256": digest(handoff),
        "readback_sha256": digest(readback_bytes),
        "resources": [{"id": "urn:demo:staging-db", "revision": "42"}],
        "effects": [{"id": "staging-review-attempt", "idempotency_key": "demo-attempt-001"}],
        "run_inputs": [
            {"name": "skill:review@1.2.0", "digest": digest(b"demo skill original bytes")},
            {"name": "policy:staging-review", "digest": digest(b"demo policy original bytes")},
        ],
    }
    observation: dict[str, Any] = {
        "relayready_observation": "0.1-draft",
        "checkpoint_sha256": digest(serialized(checkpoint)),
        "observed_at": "2026-09-20T12:04:00Z",
        "resources": [{"id": "urn:demo:staging-db", "revision": "42"}],
        "effects": [{"id": "staging-review-attempt", "status": "not_applied",
                     "evidence": "urn:demo:reconciliation:no-write-observed"}],
        "run_inputs": [dict(item) for item in checkpoint["run_inputs"]],
    }
    if case == "revision-drift":
        observation["resources"][0]["revision"] = "43"
    if case == "uncertain-effect":
        observation["effects"][0].update(status="unknown", evidence=None)
    if case == "changed-input":
        observation["run_inputs"][0]["digest"] = digest(b"demo skill changed bytes")
    return handoff, readback_bytes, checkpoint, observation


def generate(destination: Path) -> list[Path]:
    paths = []
    scenarios = []
    for case, label, summary, expected in CASES:
        folder = destination / "examples" / "continuation" / case
        folder.mkdir(parents=True, exist_ok=True)
        handoff, readback, checkpoint, observation = artifacts(case)
        inputs = [handoff, readback, serialized(checkpoint), serialized(observation)]
        filenames = ["HANDOFF.md", "READBACK.yaml", "CHECKPOINT.json", "OBSERVATION.json"]
        input_paths = []
        for filename, contents in zip(filenames, inputs, strict=True):
            path = folder / filename
            path.write_bytes(contents)
            paths.append(path)
            input_paths.append(path)
        receipt = evaluate_files(
            input_paths[0], input_paths[1], input_paths[2], input_paths[3], now=NOW,
        )
        if receipt["decision"] != expected:
            raise ValueError(f"{case}: expected {expected}, got {receipt}")
        receipt_path = folder / "RECEIPT.json"
        receipt_path.write_bytes(serialized(receipt))
        paths.append(receipt_path)
        front_matter = parse_text(handoff.decode(), Path("HANDOFF.md")).front_matter
        assert front_matter is not None
        contract_codes = {
            "human_questions_open", "readback_conflicts",
            "state_needs_recheck", "duplicate_recheck",
        }
        receipt_reasons = receipt["reasons"]
        assert isinstance(receipt_reasons, list)
        scenarios.append({"id": case, "label": label, "summary": summary,
                          "contract": {
                              "handoff_created": front_matter["created"],
                              "readback_created": yaml.safe_load(readback)["created"],
                              "findings": [
                                  reason for reason in receipt_reasons
                                  if reason["code"] in contract_codes
                              ],
                          },
                          "handoff": handoff.decode(), "readback": readback.decode(),
                          "checkpoint": checkpoint, "observation": observation, "receipt": receipt,
                          "checkpoint_raw": serialized(checkpoint).decode(),
                          "observation_raw": serialized(observation).decode(),
                          "receipt_raw": serialized(receipt).decode()})
    web_path = destination / "out" / "demo-fixtures.json"
    web_path.parent.mkdir(parents=True, exist_ok=True)
    web_path.write_bytes(serialized({"profile": "0.1-draft", "scenarios": scenarios}))
    paths.append(web_path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        print(f"Generated {len(generate(ROOT))} files from simulated observations.")
        return 0
    scratch = ROOT / "tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="relayready-fixtures-", dir=scratch) as temp:
        base = Path(temp)
        stale = []
        for generated in generate(base):
            relative = generated.relative_to(base)
            actual = ROOT / relative
            if not actual.is_file() or actual.read_bytes() != generated.read_bytes():
                stale.append(str(relative))
        if stale:
            print("Stale generated fixtures: " + ", ".join(stale))
            return 1
    print("All five scenario receipts reproduce byte-for-byte.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
