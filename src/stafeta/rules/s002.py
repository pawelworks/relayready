"""S002 — Require the fixed handoff sections in their specified order."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext

REQUIRED = (
    "Goal",
    "Done means",
    "Invariants",
    "State",
    "Done so far",
    "Do not redo",
    "Next steps",
    "Open questions",
    "Pointers",
)


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    names = [section.name for section in document.sections]
    required_seen = [name for name in names if name in REQUIRED]
    missing = [name for name in REQUIRED if name not in names]
    duplicates = [name for name in REQUIRED if names.count(name) > 1]
    findings = []
    if missing:
        findings.append(Finding("S002", "error", f"missing sections: {', '.join(missing)}"))
    if required_seen != list(REQUIRED):
        findings.append(Finding("S002", "error", "required sections are out of order"))
    if duplicates:
        findings.append(
            Finding("S002", "error", f"duplicate sections: {', '.join(duplicates)}")
        )
    if "Pointers" in names:
        last_required = names.index("Pointers")
        interleaved = [name for name in names[:last_required] if name not in REQUIRED]
        if interleaved:
            findings.append(
                Finding(
                    "S002",
                    "error",
                    "extra sections must follow all required sections: "
                    + ", ".join(interleaved),
                )
            )
    return findings
