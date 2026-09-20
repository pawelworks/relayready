"""S013 — Optionally verify local file pointers and their SHA-256 hashes."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from stafeta.models import Document, Finding, RuleContext

PATH_TOKEN = re.compile(r"`([^`]+)`")
HASH = re.compile(r"\[sha256:([0-9a-f]{64}) as of \d{4}-\d{2}-\d{2}\]")


def _looks_local(value: str) -> bool:
    if any(character.isspace() for character in value):
        return False
    if "://" in value or value.startswith("git@"):
        return False
    candidate = Path(value)
    return bool(candidate.suffix or "/" in value or "\\" in value)


def check(document: Document, context: RuleContext) -> list[Finding]:
    if not context.check_pointers:
        return []
    section = document.section("Pointers")
    if section is None:
        return []
    findings = []
    for offset, text in enumerate(section.lines):
        hash_match = HASH.search(text)
        for token in PATH_TOKEN.findall(text):
            if not _looks_local(token):
                continue
            candidate = Path(token)
            if not candidate.is_absolute():
                candidate = document.path.parent / candidate
            line = section.content_start_line + offset
            if not candidate.is_file():
                findings.append(
                    Finding("S013", "warning", f"local pointer does not exist: {token}", line)
                )
                continue
            if hash_match:
                actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
                expected = hash_match.group(1)
                if actual != expected:
                    findings.append(
                        Finding(
                            "S013",
                            "warning",
                            f"pointer hash does not match: {token}",
                            line,
                        )
                    )
    return findings

