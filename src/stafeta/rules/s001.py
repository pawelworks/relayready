"""S001 — Validate YAML front matter against the Stafeta 0.1 schema."""

from __future__ import annotations

import jsonschema

from stafeta.models import Document, Finding, RuleContext
from stafeta.schema import format_checker, load_schema


def check(document: Document, context: RuleContext) -> list[Finding]:
    if document.front_matter_error:
        return [
            Finding("S001", "error", document.front_matter_error, document.front_matter_line)
        ]
    if document.front_matter is None:
        if context.compat:
            return [Finding("S001", "warning", "front matter is missing", 1)]
        return [Finding("S001", "error", "front matter is missing", 1)]
    validator = jsonschema.Draft202012Validator(
        load_schema("handoff"),
        format_checker=format_checker(),
    )
    findings = []
    errors = sorted(
        validator.iter_errors(document.front_matter),
        key=lambda item: list(item.path),
    )
    for error in errors:
        location = ".".join(str(part) for part in error.path) or "front matter"
        findings.append(
            Finding("S001", "error", f"{location}: {error.message}", document.front_matter_line)
        )
    return findings
