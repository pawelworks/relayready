"""S012 — Warn when recheck_after is earlier than the effective lint date."""

from __future__ import annotations

from datetime import date

from stafeta.models import Document, Finding, RuleContext


def check(document: Document, context: RuleContext) -> list[Finding]:
    value = document.front_matter.get("recheck_after") if document.front_matter else None
    if not isinstance(value, str):
        return []
    try:
        deadline = date.fromisoformat(value)
    except ValueError:
        return []
    if deadline < context.now:
        return [
            Finding(
                "S012",
                "warning",
                f"recheck_after {deadline.isoformat()} is before {context.now.isoformat()}",
                document.front_matter_line,
            )
        ]
    return []

