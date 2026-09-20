"""Parse the bounded Markdown structure used by Stafeta handoffs."""

from __future__ import annotations

import re
from pathlib import Path
from typing import cast

import yaml

from stafeta.models import Document, Section

HEADING = re.compile(r"^## (.+?)\s*$")


def parse_text(text: str, path: Path) -> Document:
    """Parse YAML front matter and H2 sections without rewriting the source."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = tuple(normalized.splitlines())
    front_matter: dict[str, object] | None = None
    front_matter_error: str | None = None
    front_matter_line = 1
    body_index = 0

    if lines and lines[0] == "---":
        try:
            closing = lines.index("---", 1)
        except ValueError:
            front_matter_error = "front matter has no closing delimiter"
            body_index = len(lines)
        else:
            raw_front = "\n".join(lines[1:closing])
            body_index = closing + 1
            try:
                loaded = yaml.safe_load(raw_front)
                if not isinstance(loaded, dict) or not all(
                    isinstance(key, str) for key in loaded
                ):
                    front_matter_error = "front matter must be a YAML mapping"
                else:
                    front_matter = cast(dict[str, object], loaded)
            except yaml.YAMLError as error:
                mark = getattr(error, "problem_mark", None)
                if mark is not None:
                    front_matter_line = int(mark.line) + 2
                front_matter_error = str(error).splitlines()[0]

    body_lines = lines[body_index:]
    sections: list[Section] = []
    heading_positions: list[tuple[int, str]] = []
    for offset, line in enumerate(body_lines):
        match = HEADING.fullmatch(line)
        if match:
            heading_positions.append((offset, match.group(1)))
    for index, (offset, name) in enumerate(heading_positions):
        next_offset = (
            heading_positions[index + 1][0]
            if index + 1 < len(heading_positions)
            else len(body_lines)
        )
        heading_line = body_index + offset + 1
        sections.append(
            Section(
                name=name,
                heading_line=heading_line,
                content_start_line=heading_line + 1,
                lines=tuple(body_lines[offset + 1 : next_offset]),
            )
        )

    return Document(
        path=path,
        text=normalized,
        lines=lines,
        body="\n".join(body_lines),
        body_start_line=body_index + 1,
        front_matter=front_matter,
        front_matter_error=front_matter_error,
        front_matter_line=front_matter_line,
        sections=tuple(sections),
    )


def parse_file(path: Path) -> Document:
    """Read and parse a UTF-8 handoff file."""
    return parse_text(path.read_text(encoding="utf-8"), path)


def bullet_items(section: Section) -> list[tuple[int, str]]:
    """Return one-based source lines and top-level unordered-list text."""
    items: list[tuple[int, str]] = []
    for offset, line in enumerate(section.lines):
        match = re.match(r"^\s*[-*+]\s+(.+?)\s*$", line)
        if match:
            items.append((section.content_start_line + offset, match.group(1)))
    return items


def ordered_items(section: Section) -> list[tuple[int, str]]:
    """Return one-based source lines and ordered-list text."""
    items: list[tuple[int, str]] = []
    for offset, line in enumerate(section.lines):
        match = re.match(r"^\s*\d+[.)]\s+(.+?)\s*$", line)
        if match:
            items.append((section.content_start_line + offset, match.group(1)))
    return items

