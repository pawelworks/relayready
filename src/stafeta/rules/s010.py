"""S010 — Warn when a fenced block contains more than 40 lines."""

from __future__ import annotations

import re

from stafeta.models import Document, Finding, RuleContext

OPENING = re.compile(r"^\s*(`{3,}|~{3,})")


def check(document: Document, context: RuleContext) -> list[Finding]:
    del context
    findings = []
    fence_char: str | None = None
    fence_length = 0
    opening_line = 0
    content_lines = 0
    for line_number, line in enumerate(document.lines, start=1):
        if fence_char is None:
            match = OPENING.match(line)
            if match:
                token = match.group(1)
                fence_char = token[0]
                fence_length = len(token)
                opening_line = line_number
                content_lines = 0
            continue
        if re.match(rf"^\s*{re.escape(fence_char)}{{{fence_length},}}\s*$", line):
            if content_lines > 40:
                findings.append(
                    Finding(
                        "S010",
                        "warning",
                        f"fenced block contains {content_lines} lines",
                        opening_line,
                    )
                )
            fence_char = None
        else:
            content_lines += 1
    if fence_char is not None and content_lines > 40:
        findings.append(
            Finding(
                "S010",
                "warning",
                f"unterminated fenced block contains {content_lines} lines",
                opening_line,
            )
        )
    return findings

