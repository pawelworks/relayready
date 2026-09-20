from __future__ import annotations

import json
import tomllib
from datetime import date
from pathlib import Path

import pytest

from stafeta.bench import (
    ARMS,
    BEHAVIORS,
    MODES,
    BenchError,
    discover_fixtures,
    render_report,
    run_mock_suite,
    verify_mock,
    write_report,
)
from stafeta.cli import main
from stafeta.models import RuleContext
from stafeta.parse import parse_file
from stafeta.rules import run

ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "bench" / "fixtures"
RUNNERS = ROOT / "bench" / "runners.toml"


def test_fixture_anatomy_profiles_traps_and_golden_handoffs() -> None:
    fixtures = discover_fixtures(FIXTURES)
    assert len(fixtures) == 5
    assert sum(item.profile == "code" for item in fixtures) == 3
    assert sum(item.profile == "knowledge" for item in fixtures) == 2
    for fixture in fixtures:
        assert set(fixture.traps) == {
            "dead_end",
            "invariant",
            "stale_fact",
            "open_question",
        }
        for relative in (
            "task.md",
            "workspace",
            "checkpoint",
            "golden/HANDOFF.md",
            "golden/NOTES.md",
            "traps.toml",
            "grade.py",
        ):
            assert (fixture.root / relative).exists()
        findings = run(
            parse_file(fixture.root / "golden" / "HANDOFF.md"),
            RuleContext(now=date(2026, 9, 20)),
        )
        assert not [item for item in findings if item.severity == "error"]


def test_external_runners_are_disabled_and_help_evidence_is_honest() -> None:
    runners = tomllib.loads(RUNNERS.read_text(encoding="utf-8"))["runners"]
    for name in ("codex-cli", "claude-code", "goose", "kimi-cli"):
        assert runners[name]["enabled"] is False
    assert runners["codex-cli"]["help_verified"] is True
    assert runners["claude-code"]["help_verified"] is True
    assert runners["goose"]["help_verified"] is False
    assert runners["kimi-cli"]["command"] == []


def test_full_mock_acceptance_catches_every_behavior() -> None:
    result = verify_mock(FIXTURES)
    assert result["ok"] is True
    assert result["runs"] == 5 * len(MODES) * len(ARMS) * len(BEHAVIORS)
    assert all(result["checks"].values())


def test_mock_writes_one_result_per_run(tmp_path: Path) -> None:
    paths = run_mock_suite(FIXTURES, tmp_path, behavior="perfect", seed=7)
    assert len(paths) == 5 * len(MODES) * len(ARMS)
    payload = json.loads(paths[0].read_text(encoding="utf-8"))
    assert payload["runner"] == "mock"
    assert payload["seed"] == 7
    assert payload["receiver"] == {"harness": "mock", "version": "1", "model": None}
    assert payload["metrics"]["task_completed"] is True
    for path in paths:
        item = json.loads(path.read_text(encoding="utf-8"))
        expected = True if item["arm"] == "stafeta" else None
        assert item["metrics"]["readback_valid"] is expected


def test_report_excludes_mock_and_marks_missing_pairs(tmp_path: Path) -> None:
    results = tmp_path / "results"
    results.mkdir()
    run_mock_suite(FIXTURES, results / "mock", behavior="perfect")
    real = {
        "mode": "relay",
        "arm": "stafeta",
        "runner": "codex-cli",
        "sender": {"harness": "codex-cli", "version": "0.155.0", "model": None},
        "receiver": {"harness": "claude-code", "version": "2.1.241", "model": None},
        "metrics": {
            "task_completed": True,
            "dead_end_repeats": 0,
            "invariant_violations": 0,
            "questions_guessed": 0,
        },
    }
    (results / "real.json").write_text(json.dumps(real), encoding="utf-8")
    report = render_report(results, RUNNERS)
    assert "pass 1/1" in report
    assert "not run" in report
    assert "mock (model" not in report
    output = tmp_path / "matrix.md"
    write_report(results, RUNNERS, output)
    assert output.read_text(encoding="utf-8") == report


def test_bench_cli_and_invalid_fixture_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["bench", "verify-mock", "--fixtures", str(FIXTURES), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert main(["bench", "report", "--results", str(tmp_path), "--runners", str(RUNNERS),
                 "--output", str(tmp_path / "matrix.md"), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert main(["bench", "verify-mock", "--fixtures", str(tmp_path), "--json"]) == 2
    assert "error" in json.loads(capsys.readouterr().out)


def test_discover_rejects_wrong_fixture_count(tmp_path: Path) -> None:
    with pytest.raises(BenchError, match="expected 5 fixtures"):
        discover_fixtures(tmp_path)
