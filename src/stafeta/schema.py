"""Load the versioned JSON Schemas shipped with the package."""

from __future__ import annotations

import json
from importlib import resources
from typing import cast

import jsonschema
from rfc3339_validator import validate_rfc3339  # type: ignore[import-untyped]


def format_checker() -> jsonschema.FormatChecker:
    """Register required timestamps explicitly, without unrelated format extras."""
    checker = jsonschema.FormatChecker()

    @checker.checks("date-time")
    def is_datetime(value: object) -> bool:
        # JSON Schema leaves non-string rejection to the schema's type keyword.
        # Case normalization matches jsonschema's built-in RFC 3339 checker.
        return not isinstance(value, str) or (
            value == value.strip() and bool(validate_rfc3339(value.upper()))
        )

    return checker


def load_schema(name: str) -> dict[str, object]:
    """Load a named bundled schema."""
    if name not in {"handoff", "readback", "checkpoint", "observation"}:
        raise ValueError(f"unknown schema: {name}")
    resource = resources.files("stafeta").joinpath("schemas", f"{name}.schema.json")
    return cast(dict[str, object], json.loads(resource.read_text(encoding="utf-8")))
