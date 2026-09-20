---
stafeta: '0.1'
id: 01M2ZJGNFDW7TB29VT0CS3DZ3T
created: '2026-09-20T17:11:26+03:00'
task: Implement Stafeta M5
status: done
profile: code
parent: 01M2ZHVSGG8WT03RMH9NZTCVVE
sender:
  agent: codex-desktop
  vendor: openai
  model: null
lang: en
---

## Goal

Deliver a deterministic Relay Bench that can distinguish clean continuation from repeated dead ends, broken invariants, stale-fact failures, and guessed human answers.

## Done means

- [x] Five fixtures ship with the required anatomy, profiles, and at least three traps each.
- [x] Golden and relay modes exercise none, freeform, and stafeta arms.
- [x] External runner entries are disabled and their help evidence is recorded honestly.
- [x] One JSON result is written per mock run and the public matrix excludes mock data.
- [x] All five mock behaviors pass the M5 acceptance assertions across 150 combinations.
- [x] Lint, strict typing, 77 tests, documentation, and package builds pass locally.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- Relay Bench has three code and two knowledge fixtures. [verified 2026-09-20 by codex-desktop: `discover_fixtures` and fixture tests]
- The full mock suite executes 150 cases and every acceptance check is true. [verified 2026-09-20 by codex-desktop: `stafeta bench verify-mock --json`]
- Mock metrics are derived from sentinels, protected-file content, outputs, and question markers. [verified 2026-09-20 by codex-desktop: inspected `src/stafeta/bench.py`]
- The public matrix contains no mock cells and all unrun external pairs say `not run`. [verified 2026-09-20 by codex-desktop: regenerated `docs/matrix.md`]
- The complete suite has 77 passing tests and 97 percent rule coverage. [verified 2026-09-20 by codex-desktop: pytest]
- The sdist and wheel build successfully. [verified 2026-09-20 by codex-desktop: `python -m build`]

## Done so far

- Added the Relay Bench harness, CLI commands, runners registry, and five fixtures.
- Added deterministic acceptance tests for all mock fault behaviors.
- Generated the public all-`not run` matrix solely from the absence of real results.
- Updated CI to run the mock suite and regenerate the public matrix without API keys.

## Do not redo

- Do not treat mock results as evidence of model or harness quality.
- Do not enable goose or Kimi runners until their installed `--help` flags are recorded.
- Do not continue feature work if the owner-run stafeta arm fails to beat freeform.

## Next steps

1. None.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `HANDOFF.md`
- `bench/README.md`
- `bench/runners.toml`
- `bench/fixtures/`
- `src/stafeta/bench.py`
- `docs/matrix.md`


## Environment

- Branch: unavailable; this directory is not a Git repository.
- Commit: unavailable.
- Uncommitted files: unavailable.
- Run and test commands: `pytest`, `ruff check .`, `mypy --strict`, `stafeta bench verify-mock`, `mkdocs build --strict`, `python -m build`.
