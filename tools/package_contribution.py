"""Build an inspectable local contribution bundle without secrets or research decks."""

from __future__ import annotations

import hashlib
import json
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = str(tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
              ["project"]["version"])
DIRECTORIES = ("src", "spec", "tests", "tools", "docs", "examples", "integrations", "bench",
               "out", "handoffs", ".github")
FILES = ("README.md", "LICENSE", "NOTICE", "GOVERNANCE.md", "CONTRIBUTING.md",
         "CODE_OF_CONDUCT.md", "SECURITY.md", "MAINTAINERS.md", "THIRD_PARTY_LICENSES.md",
         "CHANGELOG.md", "pyproject.toml", "mkdocs.yml", "AGENTS.md", "HANDOFF.md",
         "READBACK.yaml", ".gitattributes", ".gitignore")


def include(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return not (
        any(part in {"__pycache__", ".pytest_cache", "results", "node_modules"} for part in parts)
        or path.suffix in {".pyc", ".pyo", ".pyd"}
        or path.is_symlink()
    )


def main() -> int:
    paths = [ROOT / name for name in FILES]
    for directory in DIRECTORIES:
        paths.extend(path for path in (ROOT / directory).rglob("*")
                     if path.is_file() and include(path))
    payloads = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in sorted(paths)}
    manifest = {
        "project": "RelayReady", "version": VERSION, "profile": "0.1-draft",
        "status": "local contribution candidate, not submitted or accepted",
        "files": {name: "sha256:" + hashlib.sha256(data).hexdigest()
                  for name, data in payloads.items()},
    }
    payloads["CONTRIBUTION_MANIFEST.json"] = (
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    ).encode()
    output = ROOT / "dist" / f"relayready-contribution-{VERSION}.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo("relayready/" + name, date_time=(2026, 9, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("Contribution archive failed CRC verification")
        for name, data in payloads.items():
            if archive.read("relayready/" + name) != data:
                raise ValueError(f"Contribution archive changed {name}")
    print(json.dumps({"path": str(output), "files": len(payloads),
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
