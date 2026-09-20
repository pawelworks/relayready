---
stafeta: "0.1"
id: "01M2ZK9ABCDEFGHJKMNPQRSTVW"
created: "2026-09-20T17:30:00+03:00"
task: "Rebrand Stafeta in English"
status: in_progress
profile: code
parent: "01M2ZJGNFDW7TB29VT0CS3DZ3T"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Rebrand the public project as RelayReady while preserving the frozen Stafeta 0.1 wire identifiers and compatibility surfaces.

## Done means

- [ ] Public branding and package metadata use RelayReady.
- [ ] `relayready` is the primary CLI and Python import while `stafeta` remains compatible.
- [ ] Frozen wire keys and benchmark arm identifiers do not change.
- [ ] Tests, typing, linting, mock bench, docs, and package builds pass.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- RelayReady had no obvious AI-handoff or package collision in the performed web search. [verified 2026-09-20 by codex-desktop: searched exact candidate across public web and package-index results]
- The accepted 0.1 schemas use `stafeta` and `stafeta_readback` keys that must remain stable. [verified 2026-09-20 by codex-desktop: inspected accepted schemas]

## Done so far

- Archived the completed M5 handoff and readback.

## Do not redo

- Do not rename frozen `stafeta` or `stafeta_readback` wire fields.
- Do not remove the legacy `stafeta` CLI or Python module in version 0.1.
- Do not reuse RelayCraft, ThreadKeep, ContextCarry, RelayProof, or Threadmark; they have relevant public collisions.

## Next steps

1. Apply RelayReady to public metadata, docs, integration packaging, and compatibility entry points.
2. Rebuild and verify all release gates.
3. Rename the deliverable directory and write the final handoff.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `pyproject.toml`
- `README.md`
- `spec/SPEC.md`
- `src/stafeta/`

## Environment

- Branch: unavailable; this directory is not a Git repository.
- Commit: unavailable.
- Uncommitted files: this rebrand is in progress.
- Run and test commands: `pytest`, `ruff check .`, `mypy --strict`, `relayready bench verify-mock`, `mkdocs build --strict`, `python -m build`.
