"""S006 — Enforce the body hard limit of fewer than 4,000 words."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext
from stafeta.rules.common import word_count


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    count = word_count(document.body)
    if count >= 4000:
        return [Finding("S006", "error", f"body has {count} words; maximum is 3,999")]
    return []

