"""Check author-matching DCO trailers; this is not a legal rights audit."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

TRAILER = re.compile(
    r"Signed-off-by:[ \t]+[^<>\r\n]+[ \t]+<([^<>\s]+@[^<>\s]+)>[ \t]*", re.IGNORECASE
)


def commit_messages(revision_range: str) -> list[tuple[str, str, str]]:
    result = subprocess.run(
        ["git", "log", "--format=%H%x00%ae%x00%(trailers:only,unfold=false)%x1e",
         revision_range],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    fields = [field.strip("\r\n") for field in result.stdout.split("\x1e") if field.strip()]
    commits: list[tuple[str, str, str]] = []
    for field in fields:
        parts = field.split("\x00", 2)
        if len(parts) != 3:
            raise ValueError("unexpected git log output")
        sha, author_email, trailers = parts
        commits.append((sha.strip(), author_email.strip(), trailers.strip()))
    return commits


def has_author_signoff(author_email: str, trailers: str) -> bool:
    lines = trailers.split("\n")
    for index, line in enumerate(lines):
        if index + 1 < len(lines) and lines[index + 1].startswith((" ", "\t")):
            continue
        match = TRAILER.fullmatch(line.removesuffix("\r"))
        if match is not None and match.group(1).casefold() == author_email.casefold():
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("revision_range")
    args = parser.parse_args()
    missing = [
        sha
        for sha, author_email, trailers in commit_messages(args.revision_range)
        if not has_author_signoff(author_email, trailers)
    ]
    for sha in missing:
        print(f"missing author-matching Signed-off-by trailer: {sha}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
