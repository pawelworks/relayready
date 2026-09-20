---
stafeta: '0.1'
id: 01M2ZHVSGG8WT03RMH9NZTCVVE
created: '2026-09-20T17:00:02+03:00'
task: Implement Stafeta M4
status: done
profile: code
parent: 01M2ZHGGTGMVZ7ZH5TDMVQBHF5
sender:
  agent: codex-desktop
  vendor: openai
  model: null
lang: en
---

## Goal

Package the accepted Stafeta writer and reader behavior for target harnesses without claiming unperformed runtime or cross-vendor evidence.

## Done means

- [x] Portable project instructions cover resume, checked readback, and unfinished-session handoff.
- [x] Codex, Claude Code, goose, and Kimi packages use documented native mechanisms.
- [x] Chat prompts enforce a fenced YAML readback before work and require a human go-ahead.
- [x] Unavailable runtime and manual relay evidence is labeled explicitly.
- [x] Lint, strict typing, 70 tests, and strict documentation build pass locally.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- Codex and Claude Code integration formats and installed CLI help were verified. [verified 2026-09-20 by codex-desktop: official docs plus local `--help` and version output]
- goose and Kimi package formats were verified from official documentation; their binaries are absent locally. [verified 2026-09-20 by codex-desktop: authoritative docs and `Get-Command`]
- The owner-run two-vendor chat relay remains pending and no acceptance result is claimed. [verified 2026-09-20 by codex-desktop: recorded in `integrations/VERIFICATION.md`]
- The local suite has 70 passing tests with 97 percent rule coverage. [verified 2026-09-20 by codex-desktop: pytest]

## Done so far

- Added portable, native-harness, and chat integrations under `integrations/`.
- Added authoritative-source and local-runtime evidence boundaries.
- Added deterministic integration contract tests.

## Do not redo

- Do not invent runtime validation for goose or Kimi while their binaries are absent.
- Do not claim the M4 manual cross-vendor chat relay passed until the owner performs it.

## Next steps

1. Build the five-fixture deterministic Relay Bench and mock runner.
2. Add all required modes, arms, metrics, result files, and public report generation.
3. Prove each mock misbehavior is caught by its matching metric.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `HANDOFF.md`
- `integrations/VERIFICATION.md`
- `integrations/chat/RESUME_PROMPT.md`


## Environment

- Branch: unavailable; this directory is not a Git repository.
- Commit: unavailable.
- Uncommitted files: unavailable.
- Run and test commands: `pytest`, `ruff check .`, `mypy --strict`, `mkdocs build --strict`.
