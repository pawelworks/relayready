"""S005 — Reject relative-time phrases in State, Done so far, and Next steps."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext
from stafeta.rules.common import contains_term, data_terms, language

SECTIONS = ("State", "Done so far", "Next steps")


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    terms = data_terms("relative_time", language(document))
    findings = []
    for name in SECTIONS:
        section = document.section(name)
        if section is None:
            continue
        for offset, line_text in enumerate(section.lines):
            term = contains_term(line_text, terms)
            if term:
                findings.append(
                    Finding(
                        "S005",
                        "error",
                        f"relative-time expression is not portable: {term!r}",
                        section.content_start_line + offset,
                    )
                )
    return findings

