"""S003 — Require exactly one valid terminal status tag on every State item."""

from __future__ import annotations

import re

from stafeta.models import Document, Finding, RuleContext
from stafeta.parse import bullet_items

TAG = re.compile(
    r"\[(?:unverified|recheck|verified \d{4}-\d{2}-\d{2}"
    r"(?: by [^:\]]+)?: [^\]]+)\]"
)


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    state = document.section("State")
    if state is None:
        return []
    findings = []
    for line, item in bullet_items(state):
        matches = list(TAG.finditer(item))
        if len(matches) != 1 or matches[0].end() != len(item):
            findings.append(
                Finding("S003", "error", "State item must end in exactly one valid tag", line)
            )
    return findings

