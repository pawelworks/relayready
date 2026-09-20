from __future__ import annotations

import json
import re
import tomllib
from importlib.metadata import version
from pathlib import Path

import pytest

import relayready
import stafeta
from stafeta.hashing import invariants_hash, normalize_invariant
from stafeta.parse import parse_text
from stafeta.schema import load_schema
from stafeta.ulid import new_ulid

ROOT = Path(__file__).parents[1]


def test_relayready_and_legacy_module_report_same_version() -> None:
    project_version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert relayready.__version__ == stafeta.__version__ == project_version["project"]["version"]
    assert relayready.__version__ == version("relayready")


def test_packaged_schemas_match_normative_copies() -> None:
    for name in ("handoff", "readback"):
        source = json.loads((ROOT / "spec" / f"{name}.schema.json").read_text(encoding="utf-8"))
        assert load_schema(name) == source


def test_schema_loader_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="unknown schema"):
        load_schema("other")


def test_ulid_shape_and_timestamp_bounds() -> None:
    assert re.fullmatch(r"[0-7][0-9A-HJKMNP-TV-Z]{25}", new_ulid(0))
    with pytest.raises(ValueError):
        new_ulid(2**48)


def test_hash_normalization() -> None:
    assert normalize_invariant("  * Cafe\u0301\tdata  ") == "Café data"
    assert invariants_hash(["Never run deploy scripts."]) == (
        "sha256:f3ef86e95eb441cb51d2f99602ab322f6accb1c6e875e934457851518e552527"
    )


def test_parser_reports_front_matter_failures() -> None:
    unclosed = parse_text("---\nstafeta: '0.1'\n", Path("HANDOFF.md"))
    assert unclosed.front_matter_error == "front matter has no closing delimiter"
    not_mapping = parse_text("---\n- item\n---\n", Path("HANDOFF.md"))
    assert not_mapping.front_matter_error == "front matter must be a YAML mapping"
