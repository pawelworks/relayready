"""Create fresh and successor handoffs for the ``relayready init`` command."""

from __future__ import annotations

import re
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml

from stafeta.parse import bullet_items, parse_file
from stafeta.ulid import new_ulid


class InitError(Exception):
    """A recoverable initialization or filesystem error."""


def sanitize_remote(value: str) -> str:
    """Remove user information, query strings, and fragments from a Git remote."""
    stripped = value.strip()
    if "://" in stripped:
        parsed = urlsplit(stripped)
        host = parsed.hostname or ""
        if parsed.port:
            host = f"{host}:{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path, "", ""))
    match = re.fullmatch(r"[^@\s]+@([^:\s]+):(.+)", stripped)
    if match:
        return f"{match.group(1)}:{match.group(2)}"
    return stripped


def _git(base: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(base), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def environment_lines(base: Path) -> list[str]:
    """Describe a Git environment without exposing remote credentials."""
    inside = _git(base, "rev-parse", "--is-inside-work-tree")
    if inside != "true":
        return [
            "Branch: unavailable; this directory is not a Git repository.",
            "Commit: unavailable.",
            "Uncommitted files: unavailable.",
            "Run and test commands: replace this placeholder.",
        ]
    branch = _git(base, "branch", "--show-current") or "detached HEAD"
    commit = _git(base, "rev-parse", "HEAD") or "unavailable"
    status = _git(base, "status", "--short")
    changed = "none" if not status else ", ".join(line[3:] for line in status.splitlines())
    remote = _git(base, "remote", "get-url", "origin")
    lines = [
        f"Branch: `{branch}`",
        f"Commit: `{commit}`",
        f"Uncommitted files: {changed}",
    ]
    if remote:
        lines.append(f"Remote: `{sanitize_remote(remote)}`")
    lines.append("Run and test commands: replace this placeholder.")
    return lines


def _front_matter(
    *,
    handoff_id: str,
    task: str,
    profile: str,
    parent: str | None,
) -> str:
    data = {
        "stafeta": "0.1",
        "id": handoff_id,
        "created": datetime.now().astimezone().isoformat(timespec="seconds"),
        "task": task,
        "status": "in_progress",
        "profile": profile,
        "parent": parent,
        "sender": {"agent": "unknown", "vendor": "unknown", "model": None},
        "lang": "en",
    }
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()


def _render(
    *,
    handoff_id: str,
    task: str,
    profile: str,
    parent: str | None,
    invariants: list[str],
    questions: list[str],
    base: Path,
) -> str:
    invariant_lines = "\n".join(f"- {value}" for value in invariants or ["None."])
    question_lines = "\n".join(f"- {value}" for value in questions or ["None."])
    sections = f"""## Goal

Describe why this task exists.

## Done means

- [ ] Replace this item with an observable acceptance criterion.

## Invariants

{invariant_lines}

## State

- No task state has been recorded. [unverified]

## Done so far

- Created this handoff with `relayready init`.

## Do not redo

- None.

## Next steps

1. Replace this item with the next concrete action.

## Open questions

{question_lines}

## Pointers

- `HANDOFF.md`
"""
    if profile == "code":
        environment = "\n".join(f"- {line}" for line in environment_lines(base))
        sections += f"""

## Environment

{environment}
"""
    front = _front_matter(
        handoff_id=handoff_id,
        task=task,
        profile=profile,
        parent=parent,
    )
    return f"---\n{front}\n---\n\n{sections}"


def initialize(base: Path, profile: str | None, source: Path | None) -> dict[str, object]:
    """Write a new handoff or archive one and create its successor."""
    base = base.resolve()
    output = base / "HANDOFF.md"
    parent: str | None = None
    invariants: list[str] = []
    questions: list[str] = []
    task = "Describe the task"
    archived: Path | None = None

    if source is not None:
        source = source.resolve()
        try:
            document = parse_file(source)
        except OSError as error:
            raise InitError(str(error)) from error
        if document.front_matter is None:
            raise InitError("source handoff has no readable front matter")
        raw_id = document.front_matter.get("id")
        if not isinstance(raw_id, str):
            raise InitError("source handoff has no valid id")
        parent = raw_id
        raw_task = document.front_matter.get("task")
        task = str(raw_task) if raw_task else task
        raw_profile = document.front_matter.get("profile")
        if profile is None and raw_profile in {"code", "knowledge"}:
            profile = str(raw_profile)
        invariant_section = document.section("Invariants")
        question_section = document.section("Open questions")
        if invariant_section:
            invariants = [item for _, item in bullet_items(invariant_section)]
        if question_section:
            questions = [
                item for _, item in bullet_items(question_section) if item != "None."
            ]
        archive_dir = base / "handoffs"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived = archive_dir / f"{parent}.md"
        if archived.exists():
            raise InitError(f"archive already exists: {archived}")
        if output.exists() and source != output:
            raise InitError(f"output already exists: {output}")
        try:
            source.replace(archived)
        except OSError as error:
            raise InitError(str(error)) from error
    elif output.exists():
        raise InitError(f"output already exists: {output}")

    selected_profile = profile or "knowledge"
    handoff_id = new_ulid()
    text = _render(
        handoff_id=handoff_id,
        task=task,
        profile=selected_profile,
        parent=parent,
        invariants=invariants,
        questions=questions,
        base=base,
    )
    try:
        output.write_text(text, encoding="utf-8", newline="\n")
    except OSError as error:
        if archived is not None and not output.exists():
            archived.replace(source)  # type: ignore[arg-type]
        raise InitError(str(error)) from error
    return {
        "path": str(output),
        "id": handoff_id,
        "parent": parent,
        "archived": str(archived) if archived else None,
    }
