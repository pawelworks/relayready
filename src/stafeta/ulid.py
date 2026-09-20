"""Small dependency-free ULID generator."""

from __future__ import annotations

import secrets
import time

ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def _encode(value: int, length: int) -> str:
    chars = ["0"] * length
    for index in range(length - 1, -1, -1):
        chars[index] = ALPHABET[value & 31]
        value >>= 5
    return "".join(chars)


def new_ulid(timestamp_ms: int | None = None) -> str:
    """Generate a canonical 26-character ULID."""
    instant = int(time.time_ns() // 1_000_000) if timestamp_ms is None else timestamp_ms
    if not 0 <= instant < 2**48:
        raise ValueError("ULID timestamp is outside the 48-bit range")
    return _encode(instant, 10) + _encode(secrets.randbits(80), 16)

