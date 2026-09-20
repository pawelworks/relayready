"""Secret-pattern definitions used by S004.

The scanner is deliberately pattern-based. It can miss novel, encoded, split,
or context-specific credentials, and placeholder-like strings can produce false
positives. Passing S004 is not proof that a handoff is safe to disclose.
"""

from __future__ import annotations

import re

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "private key block",
        re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    ),
    ("bearer token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{8,}={0,2}")),
    (
        "credential-bearing URL",
        re.compile(r"(?i)https?://[^\s/:@]+:[^\s/@]+@[^\s]+"),
    ),
    (
        "secret-style assignment",
        re.compile(
            r"(?im)^\s*[A-Z][A-Z0-9_]*(?:PASSWORD|PASSWD|TOKEN|SECRET|API_KEY|PRIVATE_KEY)"
            r"[A-Z0-9_]*\s*=\s*\S+"
        ),
    ),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b")),
    ("GitHub-style token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
)

