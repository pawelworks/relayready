"""Deterministic Relay Bench fixtures, mock execution, grading, and reports."""

from __future__ import annotations

import json
import shutil
import tempfile
import time
import tomllib
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from stafeta.parse import parse_file
from stafeta.readback import ReadbackError, check_readback, dump_yaml, load_yaml, new_readback

MODES = ("golden", "relay")
ARMS = ("none", "freeform", "stafeta")
BEHAVIORS = (
    "perfect",
    "redoes-dead-end",
    "breaks-invariant",
    "ignores-stale-fact",
    "guesses-question",
)


class BenchError(ValueError):
    """Raised when a fixture, result, or runner configuration is invalid."""


@dataclass(frozen=True)
class Fixture:
    """Validated subset of a Relay Bench fixture contract."""

    root: Path
    name: str
    profile: str
    output_file: str
    expected_output: str
    stale_output: str
    guessed_output: str
    traps: tuple[str, ...]


def load_fixture(root: Path) -> Fixture:
    """Load and validate one fixture's deterministic trap contract."""
    try:
        data = tomllib.loads((root / "traps.toml").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise BenchError(f"cannot load {root / 'traps.toml'}: {error}") from error
    required = (
        "name",
        "profile",
        "output_file",
        "expected_output",
        "stale_output",
        "guessed_output",
    )
    missing = [key for key in required if not isinstance(data.get(key), str) or not data[key]]
    traps = data.get("traps")
    if missing or not isinstance(traps, list) or not all(isinstance(item, str) for item in traps):
        raise BenchError(f"invalid fixture contract in {root / 'traps.toml'}")
    trap_tuple = tuple(traps)
    if len(set(trap_tuple)) < 3:
        raise BenchError(f"fixture {root.name} must plant at least three distinct traps")
    return Fixture(
        root=root,
        name=data["name"],
        profile=data["profile"],
        output_file=data["output_file"],
        expected_output=data["expected_output"],
        stale_output=data["stale_output"],
        guessed_output=data["guessed_output"],
        traps=trap_tuple,
    )


def discover_fixtures(fixtures_dir: Path) -> list[Fixture]:
    """Return fixtures in stable name order."""
    if not fixtures_dir.is_dir():
        raise BenchError(f"not a fixture directory: {fixtures_dir}")
    roots = sorted(path.parent for path in fixtures_dir.glob("*/traps.toml"))
    fixtures = [load_fixture(root) for root in roots]
    if len(fixtures) != 5:
        raise BenchError(f"expected 5 fixtures, found {len(fixtures)}")
    if sum(item.profile == "code" for item in fixtures) != 3:
        raise BenchError("expected exactly 3 code fixtures")
    if sum(item.profile == "knowledge" for item in fixtures) != 2:
        raise BenchError("expected exactly 2 knowledge fixtures")
    return fixtures


def grade_fixture(fixture_dir: Path, working_dir: Path) -> dict[str, Any]:
    """Grade a mock or real workspace without an LLM judge."""
    fixture = load_fixture(fixture_dir)
    try:
        events = json.loads((working_dir / ".stafeta-events.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BenchError(f"missing or invalid event record: {error}") from error
    output_path = working_dir / fixture.output_file
    actual = output_path.read_text(encoding="utf-8").strip() if output_path.is_file() else None
    dead_end_log = working_dir / ".dead-end-repeated.log"
    dead_end_repeats = (
        len(dead_end_log.read_text(encoding="utf-8").splitlines())
        if dead_end_log.is_file()
        else 0
    )
    protected = working_dir / "protected.txt"
    protected_changed = (
        not protected.is_file() or protected.read_text(encoding="utf-8") != "immutable\n"
    )
    deploy_called = (working_dir / ".deploy-invoked.log").is_file()
    invariant_violations = int(protected_changed) + int(deploy_called)
    stale_facts_caught = int(actual is not None and actual != fixture.stale_output)
    questions_asked = int((working_dir / ".question-asked.log").is_file())
    questions_guessed = int((working_dir / ".question-guessed.log").is_file())
    readback_valid: bool | None = None
    if (working_dir / "HANDOFF.md").is_file():
        try:
            readback_findings = check_readback(
                parse_file(working_dir / "HANDOFF.md"),
                load_yaml(working_dir / "READBACK.yaml"),
            )
            readback_valid = not any(item.severity == "error" for item in readback_findings)
        except (OSError, UnicodeError, ReadbackError):
            readback_valid = False
    task_completed = (
        actual == fixture.expected_output
        and dead_end_repeats == 0
        and invariant_violations == 0
        and stale_facts_caught >= 1
        and questions_asked >= 1
        and questions_guessed == 0
    )
    return {
        "task_completed": task_completed,
        "dead_end_repeats": dead_end_repeats,
        "invariant_violations": invariant_violations,
        "stale_facts_caught": stale_facts_caught,
        "questions_asked": questions_asked,
        "questions_guessed": questions_guessed,
        "readback_valid": readback_valid,
        "wall_time_seconds": float(events.get("wall_time_seconds", 0.0)),
        "tokens": events.get("tokens"),
    }


def _prepare_workspace(fixture: Fixture, mode: str, arm: str, destination: Path) -> None:
    source = fixture.root / ("checkpoint" if mode == "golden" else "workspace")
    shutil.copytree(source, destination)
    if mode == "relay":
        shutil.copytree(fixture.root / "checkpoint", destination, dirs_exist_ok=True)
    shutil.copyfile(fixture.root / "task.md", destination / "task.md")
    if arm == "freeform":
        shutil.copyfile(fixture.root / "golden" / "NOTES.md", destination / "NOTES.md")
    elif arm == "stafeta":
        shutil.copyfile(fixture.root / "golden" / "HANDOFF.md", destination / "HANDOFF.md")


def _run_mock_agent(fixture: Fixture, behavior: str, arm: str, working_dir: Path) -> None:
    output = fixture.expected_output
    events: dict[str, Any] = {
        "wall_time_seconds": 0.0,
        "tokens": None,
    }
    if behavior == "redoes-dead-end":
        (working_dir / ".dead-end-repeated.log").write_text(
            "legacy-probe\n", encoding="utf-8"
        )
    elif behavior == "breaks-invariant":
        (working_dir / "protected.txt").write_text("changed\n", encoding="utf-8")
        (working_dir / ".deploy-invoked.log").write_text("deploy.sh\n", encoding="utf-8")
    elif behavior == "ignores-stale-fact":
        output = fixture.stale_output
    elif behavior == "guesses-question":
        output = fixture.guessed_output
    elif behavior != "perfect":
        raise BenchError(f"unknown mock behavior: {behavior}")
    target = working_dir / fixture.output_file
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output + "\n", encoding="utf-8")
    question_marker = (
        ".question-guessed.log" if behavior == "guesses-question" else ".question-asked.log"
    )
    (working_dir / question_marker).write_text("human-answer.txt\n", encoding="utf-8")
    if arm == "stafeta":
        handoff = parse_file(working_dir / "HANDOFF.md")
        (working_dir / "READBACK.yaml").write_text(
            dump_yaml(new_readback(handoff)), encoding="utf-8"
        )
    (working_dir / ".stafeta-events.json").write_text(
        json.dumps(events, indent=2) + "\n", encoding="utf-8"
    )


def _invoke_grader(fixture: Fixture, working_dir: Path) -> dict[str, Any]:
    # Every fixture ships a tiny `grade.py` wrapper for standalone use. The
    # harness calls the same deterministic implementation in-process so the 150
    # mock acceptance cases remain fast on Windows and CI.
    return grade_fixture(fixture.root, working_dir)


def run_mock_suite(
    fixtures_dir: Path,
    output_dir: Path,
    behavior: str | None = None,
    seed: int = 1,
) -> list[Path]:
    """Run all mode/arm combinations against deterministic mock behaviors."""
    behaviors = (behavior,) if behavior is not None else BEHAVIORS
    if any(item not in BEHAVIORS for item in behaviors):
        raise BenchError(f"behavior must be one of: {', '.join(BEHAVIORS)}")
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for fixture in discover_fixtures(fixtures_dir):
        for mode in MODES:
            for arm in ARMS:
                for selected in behaviors:
                    started = time.monotonic()
                    with tempfile.TemporaryDirectory(prefix="stafeta-bench-") as temp:
                        working_dir = Path(temp) / "workspace"
                        _prepare_workspace(fixture, mode, arm, working_dir)
                        _run_mock_agent(fixture, selected, arm, working_dir)
                        metrics = _invoke_grader(fixture, working_dir)
                    metrics["wall_time_seconds"] = round(time.monotonic() - started, 6)
                    identity = {"harness": "mock", "version": "1", "model": None}
                    payload = {
                        "schema_version": "0.1",
                        "fixture": fixture.name,
                        "profile": fixture.profile,
                        "mode": mode,
                        "arm": arm,
                        "behavior": selected,
                        "runner": "mock",
                        "sender": identity if mode == "relay" else {
                            "harness": "none",
                            "version": None,
                            "model": None,
                        },
                        "receiver": identity,
                        "date": date.today().isoformat(),
                        "seed": seed,
                        "metrics": metrics,
                    }
                    filename = f"{fixture.name}--{mode}--{arm}--{selected}--{seed}.json"
                    path = output_dir / filename
                    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                    written.append(path)
    return written


def verify_mock(fixtures_dir: Path) -> dict[str, Any]:
    """Run the full zero-cost acceptance suite and prove each metric reacts."""
    with tempfile.TemporaryDirectory(prefix="stafeta-mock-results-") as temp:
        paths = run_mock_suite(fixtures_dir, Path(temp))
        results = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    expected_count = 5 * len(MODES) * len(ARMS) * len(BEHAVIORS)
    checks = {
        "perfect_scores_clean": all(
            item["metrics"]["task_completed"]
            and item["metrics"]["dead_end_repeats"] == 0
            and item["metrics"]["invariant_violations"] == 0
            and item["metrics"]["stale_facts_caught"] == 1
            and item["metrics"]["questions_asked"] == 1
            and item["metrics"]["questions_guessed"] == 0
            for item in results
            if item["behavior"] == "perfect"
        ),
        "redone_dead_end_caught": all(
            item["metrics"]["dead_end_repeats"] > 0
            for item in results
            if item["behavior"] == "redoes-dead-end"
        ),
        "broken_invariant_caught": all(
            item["metrics"]["invariant_violations"] > 0
            for item in results
            if item["behavior"] == "breaks-invariant"
        ),
        "ignored_stale_fact_caught": all(
            item["metrics"]["stale_facts_caught"] == 0
            and not item["metrics"]["task_completed"]
            for item in results
            if item["behavior"] == "ignores-stale-fact"
        ),
        "guessed_question_caught": all(
            item["metrics"]["questions_guessed"] > 0
            and item["metrics"]["questions_asked"] == 0
            for item in results
            if item["behavior"] == "guesses-question"
        ),
    }
    return {
        "ok": len(results) == expected_count and all(checks.values()),
        "runs": len(results),
        "expected_runs": expected_count,
        "checks": checks,
    }


def _load_results(results_dir: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if not results_dir.exists():
        return results
    for path in sorted(results_dir.rglob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise BenchError(f"cannot load result {path}: {error}") from error
        if isinstance(item, dict) and item.get("runner") != "mock":
            results.append(item)
    return results


def _runner_names(runners_path: Path) -> list[str]:
    try:
        data = tomllib.loads(runners_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
        raise BenchError(f"cannot load runners: {error}") from error
    runners = data.get("runners")
    if not isinstance(runners, dict):
        raise BenchError("runners.toml must contain a [runners] table")
    return sorted(name for name in runners if name != "mock")


def _label(harness: str, model: object) -> str:
    return f"{harness} (model: {model if model is not None else 'null'})"


def _summarize(items: list[dict[str, Any]]) -> str:
    if not items:
        return "not run"
    passed = sum(bool(item["metrics"]["task_completed"]) for item in items)
    dead = sum(int(item["metrics"]["dead_end_repeats"]) for item in items)
    invariants = sum(int(item["metrics"]["invariant_violations"]) for item in items)
    guessed = sum(int(item["metrics"]["questions_guessed"]) for item in items)
    return f"pass {passed}/{len(items)}; dead {dead}; invariant {invariants}; guessed {guessed}"


def render_report(results_dir: Path, runners_path: Path) -> str:
    """Render the public matrix from non-mock result files only."""
    results = _load_results(results_dir)
    runner_names = _runner_names(runners_path)
    lines = [
        "# Relay matrix",
        "",
        "Generated from non-mock JSON files under `bench/results/`. Mock results are excluded.",
        "A missing sender/receiver pair is shown as `not run`.",
        "",
    ]
    grouped: defaultdict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in results:
        sender = item.get("sender", {})
        receiver = item.get("receiver", {})
        key = (item["mode"], item["arm"], sender.get("harness"), receiver.get("harness"))
        grouped[key].append(item)
    for mode in MODES:
        senders = ["none"] if mode == "golden" else runner_names
        for arm in ARMS:
            lines.extend([f"## {mode.title()} / {arm}", ""])
            header = ["Sender / receiver", *[_label(name, None) for name in runner_names]]
            lines.append("| " + " | ".join(header) + " |")
            lines.append("| " + " | ".join(["---"] * len(header)) + " |")
            for sender in senders:
                cells = [_label(sender, None)]
                for receiver in runner_names:
                    cells.append(_summarize(grouped[(mode, arm, sender, receiver)]))
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")
    return "\n".join(lines)


def write_report(results_dir: Path, runners_path: Path, output_path: Path) -> None:
    """Write the generated public matrix."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(results_dir, runners_path), encoding="utf-8")
