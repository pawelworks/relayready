from __future__ import annotations

import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def test_handoff_front_matter_schema_accepts_reference_instance() -> None:
    schema = load_json(ROOT / "spec" / "handoff.schema.json")
    instance = load_json(ROOT / "spec" / "test-vectors" / "handoff-front-matter.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        instance=instance,
        schema=schema,
        format_checker=jsonschema.FormatChecker(),
    )


def test_readback_schema_accepts_reference_instance() -> None:
    schema = load_json(ROOT / "spec" / "readback.schema.json")
    instance = load_json(ROOT / "spec" / "test-vectors" / "readback.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        instance=instance,
        schema=schema,
        format_checker=jsonschema.FormatChecker(),
    )


def test_repository_handoff_front_matter_conforms() -> None:
    text = (ROOT / "HANDOFF.md").read_text(encoding="utf-8")
    front_matter = yaml.safe_load(text.split("---", 2)[1])
    schema = load_json(ROOT / "spec" / "handoff.schema.json")
    jsonschema.validate(
        instance=front_matter,
        schema=schema,
        format_checker=jsonschema.FormatChecker(),
    )


def test_repository_readback_conforms() -> None:
    readback = yaml.safe_load((ROOT / "READBACK.yaml").read_text(encoding="utf-8"))
    schema = load_json(ROOT / "spec" / "readback.schema.json")
    jsonschema.validate(
        instance=readback,
        schema=schema,
        format_checker=jsonschema.FormatChecker(),
    )


def test_all_valid_examples_have_conforming_front_matter() -> None:
    schema = load_json(ROOT / "spec" / "handoff.schema.json")
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    for path in sorted((ROOT / "examples" / "valid").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        front_matter = yaml.safe_load(text.split("---", 2)[1])
        assert not list(validator.iter_errors(front_matter)), path


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFC", value.strip())
    if len(value) >= 2 and value[0] in "-*+" and value[1].isspace():
        value = value[2:]
    return " ".join(value.split())


def test_invariant_hash_vectors() -> None:
    vectors = load_json(ROOT / "spec" / "test-vectors" / "invariants.json")
    for vector in vectors:
        normalized = "\n".join(normalize(item) for item in vector["input"])
        actual = "sha256:" + hashlib.sha256(normalized.encode()).hexdigest()
        assert normalized == vector["normalized"]
        assert actual == vector["hash"]
