"""Utilities shared by individual rule modules."""

from __future__ import annotations

import re
from importlib import resources

from stafeta.models import Document

WORD = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def word_count(text: str) -> int:
    return len(WORD.findall(text))


def source_line(document: Document, character_offset: int) -> int:
    return document.text.count("\n", 0, character_offset) + 1


def language(document: Document) -> str:
    value = document.front_matter.get("lang") if document.front_matter else "en"
    if not isinstance(value, str):
        return "en"
    primary = value.split("-", 1)[0].lower()
    return primary if primary in {"en", "ro"} else "en"


def data_terms(kind: str, lang: str) -> tuple[str, ...]:
    resource = resources.files("stafeta").joinpath("data", f"{kind}_{lang}.txt")
    values = []
    for line in resource.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            values.append(stripped)
    return tuple(values)


def contains_term(text: str, terms: tuple[str, ...]) -> str | None:
    lowered = text.casefold()
    for term in terms:
        pattern = rf"(?<!\w){re.escape(term.casefold())}(?!\w)"
        if re.search(pattern, lowered):
            return term
    return None

