from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import pytest

from stafeta.bundle import MAX_BYTES, evaluate_bundle
from stafeta.cli import main
from stafeta.continuation import ContinuationError

ROOT = Path(__file__).parents[1]


@pytest.fixture
def bundle() -> dict[str, Any]:
    data = json.loads((ROOT / "out/demo-fixtures.json").read_text(encoding="utf-8"))
    scenario = data["scenarios"][0]
    return {
        "relayready_workbench": "0.1-draft",
        "evaluated_at": scenario["receipt"]["evaluated_at"],
        "artifacts": {name: scenario.get(name + "_raw", scenario.get(name))
                      for name in ("handoff", "readback", "checkpoint", "observation")},
        "assessment": {"decision": "invented"},
    }


def write_bundle(tmp_path: Path, value: object) -> Path:
    path = tmp_path / "experiment.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_full_validator_ignores_browser_claims(tmp_path: Path, bundle: dict[str, Any]) -> None:
    result = evaluate_bundle(write_bundle(tmp_path, bundle), replay=True)
    assert result["decision"] == "resume"
    assert "relayready_receipt" in result
    expired = evaluate_bundle(write_bundle(tmp_path, bundle), now=datetime(2030, 1, 1, tzinfo=UTC))
    assert expired["decision"] == "recheck"


def test_default_clock_is_current(tmp_path: Path, bundle: dict[str, Any]) -> None:
    result = evaluate_bundle(write_bundle(tmp_path, bundle))
    clock = datetime.fromisoformat(str(result["evaluated_at"]).replace("Z", "+00:00"))
    assert abs((clock - datetime.now(UTC)).total_seconds()) < 10


@pytest.mark.parametrize("raw", [
    b'{"relayready_workbench":"0.1-draft","relayready_workbench":"0.1-draft"}',
    b'{"x":NaN}', b"not json", b"\\xff", b" " * (MAX_BYTES + 1),
    b"[" * 2000 + b"]" * 2000,
], ids=["duplicate", "nan", "invalid", "invalid-utf8", "oversize", "nested"])
def test_malformed_bundle_rejected(tmp_path: Path, raw: bytes) -> None:
    path = tmp_path / "input.json"
    path.write_bytes(raw)
    with pytest.raises(ContinuationError):
        evaluate_bundle(path)


@pytest.mark.parametrize("target", ["profile", "extra", "missing", "empty", "type", "surrogate"])
def test_artifact_boundary(tmp_path: Path, bundle: dict[str, Any], target: str) -> None:
    if target == "profile":
        bundle["relayready_workbench"] = "unknown"
    elif target == "extra":
        bundle["artifacts"]["../../outside"] = "not written"
    elif target == "missing":
        del bundle["artifacts"]["handoff"]
    else:
        bundle["artifacts"]["handoff"] = {"empty": "", "type": 42, "surrogate": chr(0xD800)}[target]
    with pytest.raises(ContinuationError):
        evaluate_bundle(write_bundle(tmp_path, bundle), replay=True)


@pytest.mark.parametrize("clock", ["2026-09-20", "not a timestamp",
                                  "2026-02-30T12:00:00Z", "0001-01-01T00:00:00+01:00"])
def test_replay_time_errors(tmp_path: Path, bundle: dict[str, Any], clock: str) -> None:
    bundle["evaluated_at"] = clock
    with pytest.raises(ContinuationError):
        evaluate_bundle(write_bundle(tmp_path, bundle), replay=True)


def test_clock_options_are_exclusive(tmp_path: Path, bundle: dict[str, Any]) -> None:
    with pytest.raises(ContinuationError):
        evaluate_bundle(write_bundle(tmp_path, bundle), replay=True, now=datetime.now(UTC))


def test_bundle_cli(
    tmp_path: Path, bundle: dict[str, Any], capsys: pytest.CaptureFixture[str],
) -> None:
    path = write_bundle(tmp_path, bundle)
    assert main(["gate", "bundle", str(path), "--replay", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["decision"] == "resume"
    assert main(["gate", "bundle", str(path), "--now", "2030-01-01T00:00:00Z", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["decision"] == "recheck"
    assert main(["gate", "bundle", str(path) + ".missing", "--json"]) == 2
    assert "error" in json.loads(capsys.readouterr().out)


def test_browser_vectors_match_independent_python(tmp_path: Path) -> None:
    process = subprocess.run(["node", "tools/test_workbench.mjs", "--vectors"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", check=True)
    vectors = json.loads(process.stdout)
    assert len(vectors) == 23
    for vector in vectors:
        value = vector["bundle"]
        actual = evaluate_bundle(write_bundle(tmp_path, value), replay=True)
        expected = value["assessment"]
        assert actual["decision"] == expected["decision"], vector["name"]
        assert actual["bindings"] == expected["bindings"], vector["name"]
        actual_reasons = cast(list[dict[str, Any]], actual["reasons"])
        assert sorted(item["code"] for item in actual_reasons) == sorted(
            item["code"] for item in expected["reasons"]
        ), vector["name"]
        assert datetime.fromisoformat(str(actual["evaluated_at"])) == datetime.fromisoformat(
            expected["evaluated_at"]
        )
