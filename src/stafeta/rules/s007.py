"""S007 — Warn when the body reaches the 1,500-word soft limit."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext
from stafeta.rules.common import word_count


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    count = word_count(document.body)
    if count >= 1500:
        return [Finding("S007", "warning", f"body has {count} words; target is under 1,500")]
    return []

