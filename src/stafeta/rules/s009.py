"""S009 — Keep Next steps non-empty for active work and at most seven items."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext
from stafeta.parse import ordered_items


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    section = document.section("Next steps")
    if section is None:
        return []
    items = ordered_items(section)
    if len(items) > 7:
        return [
            Finding(
                "S009",
                "warning",
                f"Next steps has {len(items)} items; maximum is 7",
                section.heading_line,
            )
        ]
    status = document.front_matter.get("status") if document.front_matter else None
    if status == "in_progress" and not items:
        return [
            Finding(
                "S009",
                "warning",
                "Next steps is empty while status is in_progress",
                section.heading_line,
            )
        ]
    return []

