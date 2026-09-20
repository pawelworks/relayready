"""S008 — Warn on certain numeric claims whose State tag is unverified."""

from __future__ import annotations

import re

from stafeta.models import Document, Finding, RuleContext
from stafeta.parse import bullet_items
from stafeta.rules.common import contains_term, data_terms, language

NUMBER = re.compile(r"(?<!\w)\d+(?:[.,]\d+)?(?!\w)")


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    state = document.section("State")
    if state is None:
        return []
    terms = data_terms("certainty", language(document))
    findings = []
    for line, item in bullet_items(state):
        if item.endswith("[unverified]") and NUMBER.search(item):
            certainty = contains_term(item, terms)
            if certainty:
                findings.append(
                    Finding(
                        "S008",
                        "warning",
                        f"unverified numeric claim uses certainty term {certainty!r}",
                        line,
                    )
                )
    return findings

