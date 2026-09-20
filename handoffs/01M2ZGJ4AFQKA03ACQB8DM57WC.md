---
stafeta: "0.1"
id: "01M2ZGJ4AFQKA03ACQB8DM57WC"
created: "2026-09-20T16:37:17+03:00"
task: "Implement Stafeta M2"
status: ready_for_review
profile: code
parent: "01K5MCT2V8F4JQ6N7R9S0W3XYZ"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
recheck_after: "2026-09-27"
lang: "en"
---

## Goal

Deliver the deterministic Stafeta CLI core and all version 0.1 lint rules, with exact example expectations and the required coverage gate, for owner review before M3 begins.

## Done means

- [x] `init`, `lint`, `hash`, and `schema` implement the M2 command contract.
- [x] Rules S001 through S013 live in separate modules with generated documentation pages.
- [x] Every valid and invalid rule example produces exactly its declared findings.
- [x] Rule-module test coverage exceeds 90 percent.
- [x] Ruff, strict mypy, tests, documentation, installed-console checks, and package builds pass locally.
- [ ] Hosted CI is green on Linux, macOS, and Windows.
- [ ] The owner accepts M2 before M3 begins.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- The owner accepted M1 and directed work to start on phase 2. [verified 2026-09-20 by codex-desktop: recorded from the owner's instruction]
- The package exposes `stafeta init`, `lint`, `hash`, and `schema` with human and JSON output. [verified 2026-09-20 by codex-desktop: installed the built wheel in a fresh environment and exercised its console script]
- All 13 valid examples are clean and every invalid example yields exactly its declared rule ids. [verified 2026-09-20 by codex-desktop: `tests/test_rules.py` and `tools/lint_valid_examples.py` passed]
- Rule-module coverage is 97 percent. [verified 2026-09-20 by codex-desktop: pytest-cov reported 97.38 percent]
- The prior issued handoff is immutable in `handoffs/01K5MCT2V8F4JQ6N7R9S0W3XYZ.md`. [verified 2026-09-20 by codex-desktop: created and inspected through `stafeta init --from`]
- Hosted CI status is unavailable because this delivery has no approved Git repository or remote. [verified 2026-09-20 by codex-desktop: checked the delivery root for `.git`]

## Done so far

- Added the shared models, Markdown/YAML parser, invariant hashing, bundled schema loader, and dependency-free ULID generator under `src/stafeta/`.
- Added S001 through S013 under `src/stafeta/rules/`, English and Romanian rule data, documented secret patterns, and generated pages under `docs/rules/`.
- Added the M2 CLI and safe successor writer in `src/stafeta/cli.py` and `src/stafeta/writer.py`.
- Added exact rule, CLI, initialization, schema, hash, readback-schema, and repository tests under `tests/`.
- Updated CI to run the installed linter on the repository handoff and every valid example.
- Completed the owner-authorized M1 acceptance exercise in `examples/acceptance/` and `docs/M1_EXERCISE.md`.
- Archived the M1 handoff using the newly implemented successor command.

## Do not redo

- Do not change the frozen section names or readback fields without the specification-change process.
- Do not replace the bounded Markdown parser with a general parser unless a failing contract case demonstrates the need; the dependency decision is recorded in `docs/DECISIONS.md`.
- Do not implement readback or chain commands in M2; those are M3.
- Do not infer the repository URL, security contact, or maintainer handle.
- Do not edit the archived M1 handoff referenced by `READBACK.yaml`.

## Next steps

1. Have the owner review the M2 CLI behavior and acceptance evidence.
2. Confirm the repository URL, security route, and public maintainer handle.
3. Run the CI matrix after the approved repository exists.
4. Record M2 acceptance or requested corrections.
5. Start M3 only after acceptance.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `docs/BUILD_BRIEF.md` [sha256:3916dfb14d6e2d045f1c494bf6efcac2ba8d7970b595e3fb9497628ae4c19e9a as of 2026-09-20]
- `spec/SPEC.md` [sha256:e2411d27b03576f017c4b27651d17532ac5c123c99b627ae0221382b06d79ea3 as of 2026-09-20]
- `pyproject.toml` [sha256:7f8963984dbe4c5c40a8344092a6def633524145266a894a1daddfb6619a0328 as of 2026-09-20]
- `docs/CLI.md`
- `docs/rules/index.md`
- `examples/acceptance/HANDOFF.md`
- `READBACK.yaml`
- `handoffs/01K5MCT2V8F4JQ6N7R9S0W3XYZ.md`

## Decisions

- A bounded parser implements only the Markdown constructs the fixed contract needs; PyYAML and jsonschema are the only runtime dependencies.
- Warnings alone return exit code 0; any error returns 1; usage and I/O failures return 2.
- Pointer checking is opt-in because referenced files may not exist in a receiver environment.

## Environment

- Branch: unavailable; this delivery is not a Git repository.
- Commit: unavailable; no DCO identity was invented.
- Uncommitted files: all delivery files are outside Git.
- Install: `python -m pip install -e .[dev]`
- Verify: `ruff check .`, `mypy --strict`, `pytest`, `stafeta lint HANDOFF.md --check-pointers`, `python tools/lint_valid_examples.py`, `python tools/generate_rule_docs.py --check`, `mkdocs build --strict`, and `python -m build`.
