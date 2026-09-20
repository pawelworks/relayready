"""Canonical invariant hashing for Stafeta 0.1."""

from __future__ import annotations

import hashlib
import re
import unicodedata


def normalize_invariant(value: str) -> str:
    """Normalize one invariant exactly as specification section 8.1 requires."""
    normalized = unicodedata.normalize("NFC", value).strip()
    normalized = re.sub(r"^[-*+]\s+", "", normalized, count=1)
    return " ".join(normalized.split())


def invariants_hash(invariants: list[str]) -> str:
    """Return the version 0.1 SHA-256 invariant digest."""
    payload = "\n".join(normalize_invariant(value) for value in invariants)
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()

