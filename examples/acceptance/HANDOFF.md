---
stafeta: "0.1"
id: "01K5MDW4Z9A2BC3DE4FG5H6JKM"
created: "2026-09-20T16:26:50+03:00"
task: "Implement Stafeta M2"
status: in_progress
profile: code
parent: "01K5MCT2V8F4JQ6N7R9S0W3XYZ"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Implement the deterministic Stafeta CLI core and all version 0.1 lint rules without starting later milestone work.

## Done means

- [ ] `init`, `lint`, `hash`, and `schema` satisfy the M2 command contract.
- [ ] Rules S001 through S013 live in separate modules with generated documentation.
- [ ] Every example produces exactly its declared findings.
- [ ] Rule-module coverage is at least 90 percent.
- [ ] Ruff, strict mypy, tests, documentation, and package builds pass.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- The owner accepted moving to phase 2 and requested a self-created acceptance example. [verified 2026-09-20 by codex-desktop: recorded from the owner's instruction]
- M0 and M1 local verification passed before phase 2 began. [verified 2026-09-20 by codex-desktop: Ruff, mypy, seven tests, MkDocs, and package builds exited successfully]
- No approved Git remote exists in the delivery. [verified 2026-09-20 by codex-desktop: checked for `.git`]

## Done so far

- Created this sanitized conversion from `examples/acceptance/NOTES.md`.
- Preserved every prior invariant verbatim and carried unresolved owner questions into the current repository handoff.

## Do not redo

- Do not rework the section names or readback fields; the owner advanced the accepted M1 contract to phase 2.
- Do not implement readback or chain commands; they are M3.
- Do not implement integrations or Relay Bench; they are M4 and M5.

## Next steps

1. Implement the shared parser, diagnostic model, hashing, schema loading, and ULID generation.
2. Implement rules S001 through S013 in separate modules.
3. Implement CLI output and exit-code behavior.
4. Add exact example and command tests with the coverage gate.
5. Run the complete M2 verification suite.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `../../docs/BUILD_BRIEF.md`
- `../../spec/SPEC.md`
- `NOTES.md`
- `../../pyproject.toml`

## Decisions

- The owner-directed self-created example substitutes for the unavailable private real-world source.
- The free-form notes exposed one format gap: a handoff can record owner decisions as State, but version 0.1 has no dedicated approval field. State plus evidence is sufficient for M1 and does not justify changing the frozen fields.

## Environment

- Branch: unavailable; the delivery is not a Git repository.
- Commit: unavailable.
- Install: `python -m pip install -e .[dev]`
- Verify: `ruff check .`, `mypy --strict`, `pytest`, `mkdocs build --strict`, and `python -m build`.
