from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pytest
import yaml

from stafeta.cli import main
from stafeta.parse import bullet_items, parse_file
from stafeta.writer import sanitize_remote

ROOT = Path(__file__).parents[1]


def test_lint_json_and_exit_codes(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["lint", str(ROOT / "examples" / "valid" / "S001.md")]) == 0
    capsys.readouterr()
    assert main(["lint", str(ROOT / "examples" / "invalid" / "S001.md")]) == 1
    capsys.readouterr()
    assert main(["lint", str(ROOT / "examples" / "invalid" / "S007.md")]) == 0
    capsys.readouterr()


def test_lint_json_output_and_io_error(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(
        [
            "lint",
            str(ROOT / "examples" / "invalid" / "S003.md"),
            "--json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["errors"] == 1
    assert payload["findings"][0]["rule_id"] == "S003"
    assert main(["lint", "missing.md", "--json"]) == 2
    assert "error" in json.loads(capsys.readouterr().out)


def test_hash_and_schema_commands(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["hash", str(ROOT / "examples" / "valid" / "S001.md"), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["hash"].startswith("sha256:")
    assert main(["schema", "handoff", "--json"]) == 0
    schema = json.loads(capsys.readouterr().out)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_fresh_init_creates_a_clean_code_handoff(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["init", "--profile", "code", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert re.fullmatch(r"[0-7][0-9A-HJKMNP-TV-Z]{25}", payload["id"])
    handoff = tmp_path / "HANDOFF.md"
    assert handoff.is_file()
    assert main(["lint", str(handoff), "--now", "2026-09-20"]) == 0
    capsys.readouterr()
    assert main(["init", "--json"]) == 2


def test_successor_archives_and_carries_critical_sections(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "HANDOFF.md"
    shutil.copyfile(ROOT / "examples" / "acceptance" / "HANDOFF.md", source)
    old = parse_file(source)
    old_section = old.section("Invariants")
    assert old_section is not None
    old_invariants = bullet_items(old_section)
    monkeypatch.chdir(tmp_path)
    assert main(["init", "--from", str(source), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert old.front_matter is not None
    assert payload["parent"] == old.front_matter["id"]
    assert Path(payload["archived"]).is_file()
    successor = parse_file(tmp_path / "HANDOFF.md")
    new_section = successor.section("Invariants")
    assert new_section is not None
    new_invariants = bullet_items(new_section)
    assert [item for _, item in new_invariants] == [item for _, item in old_invariants]


def test_remote_sanitization_removes_credentials() -> None:
    assert sanitize_remote("https://user:password@example.com/org/repo.git?token=x") == (
        "https://example.com/org/repo.git"
    )
    assert sanitize_remote("git@example.com:org/repo.git") == "example.com:org/repo.git"


def test_readback_and_chain_commands(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    handoff = ROOT / "examples" / "acceptance" / "HANDOFF.md"
    assert main(["readback", "new", str(handoff), "--json"]) == 0
    generated = json.loads(capsys.readouterr().out)
    readback_path = tmp_path / "READBACK.yaml"
    readback_path.write_text(yaml.safe_dump(generated, sort_keys=False), encoding="utf-8")
    assert main(["readback", "check", str(handoff), str(readback_path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["errors"] == 0
    assert main(["chain", "check", str(tmp_path / "missing"), "--json"]) == 2
    capsys.readouterr()
