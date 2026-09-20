"""Command-line interface for RelayReady and its Stafeta 0.1 wire format."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path

from stafeta.bench import BEHAVIORS, BenchError, run_mock_suite, verify_mock, write_report
from stafeta.bundle import evaluate_bundle
from stafeta.chain import check_chain
from stafeta.continuation import ContinuationError, evaluate_files
from stafeta.hashing import invariants_hash
from stafeta.models import Finding, RuleContext
from stafeta.parse import bullet_items, parse_file
from stafeta.readback import (
    ReadbackError,
    check_readback,
    dump_yaml,
    load_from_text,
    load_yaml,
    new_readback,
)
from stafeta.rules import run
from stafeta.schema import load_schema
from stafeta.writer import InitError, initialize


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="relayready")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a handoff or successor")
    init.add_argument("--profile", choices=("code", "knowledge"))
    init.add_argument("--from", dest="source", type=Path)
    init.add_argument("--json", action="store_true")

    lint = subparsers.add_parser("lint", help="lint a handoff")
    lint.add_argument("file", nargs="?", type=Path, default=Path("HANDOFF.md"))
    lint.add_argument("--compat", action="store_true")
    lint.add_argument("--now", type=date.fromisoformat, default=date.today())
    lint.add_argument("--check-pointers", action="store_true")
    lint.add_argument("--json", action="store_true")

    hash_command = subparsers.add_parser("hash", help="hash handoff invariants")
    hash_command.add_argument("file", type=Path)
    hash_command.add_argument("--json", action="store_true")

    schema = subparsers.add_parser("schema", help="print a bundled schema")
    schema.add_argument("name", choices=("handoff", "readback", "checkpoint", "observation"))
    schema.add_argument("--json", action="store_true")

    readback = subparsers.add_parser("readback", help="create or check a receiver readback")
    readback_subparsers = readback.add_subparsers(dest="readback_command", required=True)
    readback_new = readback_subparsers.add_parser("new", help="emit a readback skeleton")
    readback_new.add_argument("handoff", type=Path)
    readback_new.add_argument("--json", action="store_true")
    readback_check = readback_subparsers.add_parser("check", help="verify a readback")
    readback_check.add_argument("handoff", type=Path)
    readback_check.add_argument("readback", nargs="?", type=Path)
    readback_check.add_argument("--from-text", type=Path)
    readback_check.add_argument("--json", action="store_true")

    chain = subparsers.add_parser("chain", help="check a directory of chained handoffs")
    chain_subparsers = chain.add_subparsers(dest="chain_command", required=True)
    chain_check = chain_subparsers.add_parser("check", help="verify parent and invariant chains")
    chain_check.add_argument("directory", type=Path)
    chain_check.add_argument("--json", action="store_true")

    gate = subparsers.add_parser("gate", help="evaluate an experimental continuation checkpoint")
    gate_subparsers = gate.add_subparsers(dest="gate_command", required=True)
    gate_bundle = gate_subparsers.add_parser(
        "bundle", help="independently validate a workbench bundle",
    )
    gate_bundle.add_argument("bundle", type=Path)
    bundle_clock = gate_bundle.add_mutually_exclusive_group()
    bundle_clock.add_argument(
        "--replay", action="store_true", help="use the recorded historical clock",
    )
    bundle_clock.add_argument("--now", type=_timestamp)
    gate_bundle.add_argument("--json", action="store_true")
    gate_check = gate_subparsers.add_parser("check", help="emit a bound continuation receipt")
    gate_check.add_argument("handoff", type=Path)
    gate_check.add_argument("readback", type=Path)
    gate_check.add_argument("checkpoint", type=Path)
    gate_check.add_argument("observation", type=Path)
    gate_check.add_argument("--now", type=_timestamp, default=None,
                            help="explicit RFC 3339 evaluation time for reproducible fixtures")
    gate_check.add_argument("--json", action="store_true")

    bench = subparsers.add_parser("bench", help="run or report Relay Bench results")
    bench_subparsers = bench.add_subparsers(dest="bench_command", required=True)
    bench_run_mock = bench_subparsers.add_parser("run-mock", help="run deterministic mock cases")
    bench_run_mock.add_argument("--fixtures", type=Path, default=Path("bench/fixtures"))
    bench_run_mock.add_argument("--output", type=Path, default=Path("bench/results/mock-local"))
    bench_run_mock.add_argument("--behavior", choices=BEHAVIORS)
    bench_run_mock.add_argument("--seed", type=int, default=1)
    bench_run_mock.add_argument("--json", action="store_true")
    bench_verify = bench_subparsers.add_parser("verify-mock", help="check every mock behavior")
    bench_verify.add_argument("--fixtures", type=Path, default=Path("bench/fixtures"))
    bench_verify.add_argument("--json", action="store_true")
    bench_report = bench_subparsers.add_parser("report", help="render the public result matrix")
    bench_report.add_argument("--results", type=Path, default=Path("bench/results"))
    bench_report.add_argument("--runners", type=Path, default=Path("bench/runners.toml"))
    bench_report.add_argument("--output", type=Path, default=Path("docs/matrix.md"))
    bench_report.add_argument("--json", action="store_true")
    return parser


def _timestamp(value: str) -> datetime:
    if not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
        r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])", value
    ):
        raise argparse.ArgumentTypeError("--now requires an RFC 3339 timestamp with offset")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError("--now requires an RFC 3339 timestamp") from error
    if result.utcoffset() is None:
        raise argparse.ArgumentTypeError("--now requires an explicit UTC offset")
    return result


def _emit_error(message: str, as_json: bool) -> int:
    if as_json:
        print(json.dumps({"error": message}, ensure_ascii=False))
    else:
        print(f"error: {message}", file=sys.stderr)
    return 2


def _lint(path: Path, context: RuleContext, as_json: bool) -> int:
    try:
        document = parse_file(path)
    except (OSError, UnicodeError) as error:
        return _emit_error(str(error), as_json)
    findings = run(document, context)
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    if as_json:
        print(
            json.dumps(
                {
                    "file": str(path),
                    "ok": errors == 0,
                    "errors": errors,
                    "warnings": warnings,
                    "findings": [item.as_dict() for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_findings(path, findings)
        print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def _print_findings(path: Path, findings: list[Finding]) -> None:
    current = ""
    for finding in findings:
        if finding.rule_id != current:
            current = finding.rule_id
            print(f"{current} {finding.severity}")
        location = f"{path}:{finding.line}" if finding.line else str(path)
        print(f"  {location}: {finding.message}")


def _hash(path: Path, as_json: bool) -> int:
    try:
        document = parse_file(path)
    except (OSError, UnicodeError) as error:
        return _emit_error(str(error), as_json)
    section = document.section("Invariants")
    if section is None:
        return _emit_error("Invariants section is missing", as_json)
    values = [item for _, item in bullet_items(section)]
    digest = invariants_hash(values)
    if as_json:
        print(json.dumps({"hash": digest}))
    else:
        print(digest)
    return 0


def _readback_new(path: Path, as_json: bool) -> int:
    try:
        result = new_readback(parse_file(path))
    except (OSError, UnicodeError, ReadbackError) as error:
        return _emit_error(str(error), as_json)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(dump_yaml(result), end="")
    return 0


def _readback_check(
    handoff_path: Path,
    readback_path: Path | None,
    from_text: Path | None,
    as_json: bool,
) -> int:
    if from_text is None and readback_path is None:
        return _emit_error("READBACK.yaml or --from-text FILE is required", as_json)
    try:
        document = parse_file(handoff_path)
        readback = load_from_text(from_text) if from_text is not None else load_yaml(readback_path)  # type: ignore[arg-type]
    except (OSError, UnicodeError, ReadbackError) as error:
        return _emit_error(str(error), as_json)
    findings = check_readback(document, readback)
    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    if as_json:
        print(
            json.dumps(
                {
                    "ok": errors == 0,
                    "errors": errors,
                    "warnings": warnings,
                    "findings": [item.as_dict() for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_findings(readback_path or from_text or handoff_path, findings)
        print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


def _chain_check(directory: Path, as_json: bool) -> int:
    if not directory.is_dir():
        return _emit_error(f"not a directory: {directory}", as_json)
    findings = check_chain(directory)
    errors = sum(item.severity == "error" for item in findings)
    if as_json:
        print(
            json.dumps(
                {
                    "ok": errors == 0,
                    "errors": errors,
                    "findings": [item.as_dict() for item in findings],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_findings(directory, findings)
        print(f"{errors} error(s)")
    return 1 if errors else 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return its documented process exit code."""
    args = _parser().parse_args(argv)
    if args.command == "lint":
        context = RuleContext(
            now=args.now,
            compat=args.compat,
            check_pointers=args.check_pointers,
        )
        return _lint(args.file, context, args.json)
    if args.command == "hash":
        return _hash(args.file, args.json)
    if args.command == "schema":
        print(json.dumps(load_schema(args.name), ensure_ascii=False, indent=2))
        return 0
    if args.command == "readback":
        if args.readback_command == "new":
            return _readback_new(args.handoff, args.json)
        return _readback_check(args.handoff, args.readback, args.from_text, args.json)
    if args.command == "chain":
        return _chain_check(args.directory, args.json)
    if args.command == "gate":
        try:
            if args.gate_command == "bundle":
                receipt = evaluate_bundle(args.bundle, replay=args.replay, now=args.now)
            else:
                receipt = evaluate_files(
                    args.handoff, args.readback, args.checkpoint, args.observation,
                    args.now or datetime.now(UTC),
                )
        except (OSError, UnicodeError, ContinuationError) as error:
            return _emit_error(str(error), args.json)
        if args.json:
            print(json.dumps(receipt, ensure_ascii=False, indent=2))
        else:
            print(f"Experimental Continuation Gate: {receipt['decision']}")
            print("Receipt checks supplied observations; it does not grant execution authority.")
            print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0 if receipt["decision"] == "resume" else 1
    if args.command == "bench":
        try:
            if args.bench_command == "run-mock":
                paths = run_mock_suite(args.fixtures, args.output, args.behavior, args.seed)
                payload = {"ok": True, "runs": len(paths), "output": str(args.output)}
            elif args.bench_command == "verify-mock":
                payload = verify_mock(args.fixtures)
            else:
                write_report(args.results, args.runners, args.output)
                payload = {"ok": True, "output": str(args.output)}
        except BenchError as error:
            return _emit_error(str(error), args.json)
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        elif args.bench_command == "report":
            print(f"created {payload['output']}")
        else:
            print(f"{payload['runs']} mock run(s); ok={str(payload['ok']).lower()}")
        return 0 if payload["ok"] else 1
    if args.command == "init":
        try:
            result = initialize(Path.cwd(), args.profile, args.source)
        except InitError as error:
            return _emit_error(str(error), args.json)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"created {result['path']}")
            if result["archived"]:
                print(f"archived {result['archived']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
