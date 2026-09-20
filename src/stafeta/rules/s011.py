"""S011 — Require Environment when the handoff profile is code."""

from __future__ import annotations

from stafeta.models import Document, Finding, RuleContext


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    profile = document.front_matter.get("profile") if document.front_matter else None
    if profile == "code" and document.section("Environment") is None:
        return [Finding("S011", "error", "code profile requires an Environment section")]
    return []

