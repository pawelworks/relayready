"""Required format checks must not depend on optional extra discovery."""

from __future__ import annotations

import jsonschema
import pytest

from stafeta.schema import format_checker, load_schema


@pytest.mark.parametrize("value", [
    "2026-09-20T16:00:00+03:00", "2026-09-20t13:00:00z",
    "2024-02-29T12:00:00.123Z", None, 42,
])
def test_explicit_datetime_checker_accepts_valid_values(value: object) -> None:
    # Non-strings are rejected by schema types, not by the format keyword.
    assert format_checker().conforms(value, "date-time")


@pytest.mark.parametrize("value", [
    "2026-09-20T13:00:00Z\n", " 2026-09-20T13:00:00Z",
    "2026-09-20T13:00:00Z\t", "2026-09-20T13:00:00Z\r\n",
])
def test_datetime_checker_rejects_surrounding_whitespace(value: str) -> None:
    assert not format_checker().conforms(value, "date-time")


def test_explicit_registration_is_local_and_survives_missing_global_checker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delitem(jsonschema.FormatChecker.checkers, "date-time", raising=False)
    checker = format_checker()
    assert not checker.conforms("2026-02-30T12:00:00Z", "date-time")
    assert checker.conforms("2024-02-29T12:00:00Z", "date-time")
    assert "date-time" not in jsonschema.FormatChecker.checkers


def test_full_date_format_remains_active_without_format_extras() -> None:
    checker = format_checker()
    assert checker.conforms("2024-02-29", "date")
    assert not checker.conforms("2026-02-30", "date")
    assert not checker.conforms("20260920", "date")


def test_all_shipped_schema_formats_are_registered() -> None:
    formats: set[str] = set()

    def visit(value: object) -> None:
        if isinstance(value, dict):
            if "format" in value:
                formats.add(value["format"])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    for name in ("handoff", "readback", "checkpoint", "observation"):
        visit(load_schema(name))
    assert formats == {"date", "date-time"}
    assert formats <= format_checker().checkers.keys()
