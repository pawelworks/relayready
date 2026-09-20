"""Shared immutable models for parsed handoffs and lint findings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

Severity = Literal["error", "warning"]


@dataclass(frozen=True, slots=True)
class Finding:
    """One deterministic lint result."""

    rule_id: str
    severity: Severity
    message: str
    line: int | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "message": self.message,
            "line": self.line,
        }


@dataclass(frozen=True, slots=True)
class Section:
    """A level-two Markdown section with source positions."""

    name: str
    heading_line: int
    content_start_line: int
    lines: tuple[str, ...]

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip()


@dataclass(frozen=True, slots=True)
class Document:
    """A parsed handoff container."""

    path: Path
    text: str
    lines: tuple[str, ...]
    body: str
    body_start_line: int
    front_matter: dict[str, object] | None
    front_matter_error: str | None
    front_matter_line: int
    sections: tuple[Section, ...]

    def section(self, name: str) -> Section | None:
        return next((section for section in self.sections if section.name == name), None)


@dataclass(frozen=True, slots=True)
class RuleContext:
    """Options shared by lint rules."""

    now: date
    compat: bool = False
    check_pointers: bool = False

