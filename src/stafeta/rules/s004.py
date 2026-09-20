"""S004 — Reject text matching documented secret patterns."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext
from stafeta.rules.common import source_line
from stafeta.rules.secrets import PATTERNS


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    findings = []
    for label, pattern in PATTERNS:
        for match in pattern.finditer(document.text):
            findings.append(
                Finding(
                    "S004",
                    "error",
                    f"possible {label} detected",
                    source_line(document, match.start()),
                )
            )
    return findings

