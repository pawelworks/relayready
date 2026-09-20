"""Validate parent links, cycles, and invariant inheritance across handoffs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from stafeta.models import Document, Finding
from stafeta.parse import bullet_items, parse_file

WAIVER = re.compile(r"^(.*?) \[waived by (.+?) on (\d{4}-\d{2}-\d{2})\]$")


@dataclass(frozen=True, slots=True)
class ChainNode:
    handoff_id: str
    parent: str | None
    document: Document


def _invariants(document: Document) -> list[str]:
    section = document.section("Invariants")
    return [item for _, item in bullet_items(section)] if section else []


def _waivers(document: Document) -> set[str]:
    section = document.section("Waived invariants")
    if section is None:
        return set()
    waived = set()
    for _, item in bullet_items(section):
        match = WAIVER.fullmatch(item)
        if match and match.group(2).strip():
            waived.add(match.group(1))
    return waived


def load_chain(directory: Path) -> tuple[dict[str, ChainNode], list[Finding]]:
    """Load every Markdown handoff in a directory tree."""
    nodes: dict[str, ChainNode] = {}
    findings: list[Finding] = []
    for path in sorted(directory.rglob("*.md")):
        try:
            document = parse_file(path)
        except (OSError, UnicodeError) as error:
            findings.append(Finding("C001", "error", f"{path}: {error}"))
            continue
        if document.front_matter is None:
            findings.append(Finding("C001", "error", f"{path}: unreadable front matter"))
            continue
        handoff_id = document.front_matter.get("id")
        parent = document.front_matter.get("parent")
        if not isinstance(handoff_id, str) or not (parent is None or isinstance(parent, str)):
            findings.append(Finding("C001", "error", f"{path}: invalid id or parent"))
            continue
        if handoff_id in nodes:
            findings.append(Finding("C002", "error", f"duplicate handoff id: {handoff_id}"))
            continue
        nodes[handoff_id] = ChainNode(handoff_id, parent, document)
    return nodes, findings


def check_chain(directory: Path) -> list[Finding]:
    """Report missing parents, cycles, and unwaived dropped invariants."""
    nodes, findings = load_chain(directory)
    for node in nodes.values():
        if node.parent is not None and node.parent not in nodes:
            findings.append(
                Finding("C003", "error", f"{node.handoff_id} has missing parent {node.parent}")
            )

    for start in nodes:
        seen: set[str] = set()
        current: str | None = start
        while current is not None and current in nodes:
            if current in seen:
                findings.append(Finding("C004", "error", f"cycle detected from {start}"))
                break
            seen.add(current)
            current = nodes[current].parent

    for node in nodes.values():
        if node.parent is None or node.parent not in nodes:
            continue
        parent = nodes[node.parent]
        child_invariants = _invariants(node.document)
        waived = _waivers(node.document)
        for invariant in _invariants(parent.document):
            if invariant not in child_invariants and invariant not in waived:
                findings.append(
                    Finding(
                        "C005",
                        "error",
                        f"{node.handoff_id} dropped invariant without waiver: {invariant}",
                    )
                )
    return findings

