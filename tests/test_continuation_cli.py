from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from stafeta.cli import main
from stafeta.schema import load_schema

ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize(("scenario", "decision", "exit_code"), [
    ("clean", "resume", 0),
    ("revision-drift", "recheck", 1),
    ("uncertain-effect", "escalate", 1),
    ("changed-input", "recheck", 1),
    ("human-decision", "escalate", 1),
])
def test_cli_reproduces_presentation_receipts(
    scenario: str, decision: str, exit_code: int, capsys: pytest.CaptureFixture[str],
) -> None:
    folder = ROOT / "examples" / "continuation" / scenario
    files = [folder / name for name in (
        "HANDOFF.md", "READBACK.yaml", "CHECKPOINT.json", "OBSERVATION.json",
    )]
    assert main(["gate", "check", *map(str, files),
                 "--now", "2026-09-20T12:05:00Z", "--json"]) == exit_code
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["decision"] == decision
    assert receipt == json.loads((folder / "RECEIPT.json").read_text(encoding="utf-8"))


def test_legacy_module_supports_same_gate() -> None:
    folder = ROOT / "examples" / "continuation" / "clean"
    result = subprocess.run([
        sys.executable, "-m", "stafeta", "gate", "check",
        *[str(folder / name) for name in (
            "HANDOFF.md", "READBACK.yaml", "CHECKPOINT.json", "OBSERVATION.json",
        )], "--now", "2026-09-20T12:05:00Z", "--json",
    ], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["decision"] == "resume"


def test_draft_schema_copies_are_identical() -> None:
    for name in ("checkpoint", "observation"):
        assert load_schema(name) == json.loads(
            (ROOT / "spec" / f"{name}.schema.json").read_text(encoding="utf-8")
        )


def test_generated_browser_and_cli_fixtures_are_current() -> None:
    result = subprocess.run([
        sys.executable, "tools/generate_continuation_fixtures.py", "--check",
    ], cwd=ROOT, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr


def test_gate_cli_missing_file_is_input_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["gate", "check", *(["missing-file"] * 4), "--json"]) == 2
    assert "error" in json.loads(capsys.readouterr().out)


@pytest.mark.parametrize("timestamp", [
    "2026-09-20", "2026-09-20T12:05:00", "20260920T120500Z", "2026-09-20T12:05:00+01:60",
    "2026-09-20T12:05:00+24:00",
])
def test_cli_requires_rfc3339_time(timestamp: str) -> None:
    with pytest.raises(SystemExit) as error:
        main(["gate", "check", *(["unused"] * 4), "--now", timestamp])
    assert error.value.code == 2
