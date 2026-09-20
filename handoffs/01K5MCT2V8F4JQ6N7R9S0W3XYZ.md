---
stafeta: "0.1"
id: "01K5MCT2V8F4JQ6N7R9S0W3XYZ"
created: "2026-09-20T16:04:40+03:00"
task: "Complete Stafeta M0 and M1"
status: blocked
profile: code
parent: null
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
recheck_after: "2026-09-27"
lang: "en"
---

## Goal

Establish Stafeta's repository skeleton and version 0.1 contracts, then obtain the owner's evidence and decisions required to accept M0 and M1 before implementation proceeds.

## Done means

- [x] The M0 repository, governance, CI, release, DCO, documentation, and packaging skeleton exists.
- [x] The M1 normative specification, schemas, vectors, and per-rule examples exist and pass local checks.
- [ ] Hosted CI is green on Linux, macOS, and Windows.
- [ ] The owner converts one sanitized real-world handoff and records what did not fit.
- [ ] The owner accepts M1 and freezes the section names and readback fields.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- The repository contains the complete M0 and M1 file inventory. [verified 2026-09-20 by codex-desktop: inspected the generated tree and ran repository tests]
- The CI matrix targets Linux, macOS, Windows, and Python 3.11 through 3.14. [verified 2026-09-20 by codex-desktop: inspected `.github/workflows/ci.yml`]
- Hosted CI status is not available because no Git repository or remote exists in this delivery. [verified 2026-09-20 by codex-desktop: checked the delivery root for `.git`]
- The security reporting contact is still an explicit placeholder. [verified 2026-09-20 by codex-desktop: inspected `SECURITY.md`]
- M1 acceptance requires the owner's sanitized real-world conversion. [verified 2026-09-20 by codex-desktop: checked milestone M1 in `docs/BUILD_BRIEF.md`]
- Relay Bench has no real-runner results. [verified 2026-09-20 by codex-desktop: inspected `bench/results` and `docs/matrix.md`]

## Done so far

- Added packaging and an empty typed Python package in `pyproject.toml` and `src/stafeta/`.
- Added license, notice, governance, contribution, maintenance, conduct, security, DCO, CI, and release files at the repository root and under `.github/`.
- Added the normative version 0.1 contract in `spec/SPEC.md` and both JSON Schema 2020-12 schemas.
- Added invariant-hash, front-matter, and readback test vectors under `spec/test-vectors/`.
- Added 13 valid and 13 intentionally invalid handoff examples under `examples/`.
- Added local schema, hash-vector, and repository-inventory tests under `tests/`.
- Recorded ambiguities and deviations in `docs/DECISIONS.md`.

## Do not redo

- Do not implement the CLI or lint-rule modules in this milestone; they belong to M2 and would cross the acceptance gate.
- Do not invent the GitHub URL, maintainer handle, or security contact; the brief reserves those decisions for the owner.
- Do not treat the workflow matrix as proof that hosted CI passed; only an actual remote run supplies that evidence.

## Next steps

1. Have the owner convert one sanitized real-world handoff to version 0.1 and list what did not fit.
2. Ask the owner to confirm the GitHub organization and repository URL.
3. Ask the owner to provide the private security reporting route and public maintainer handle.
4. Initialize the approved repository with DCO-signed commits and run hosted CI.
5. Record M1 acceptance or revise the contract from the conversion findings.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?
- Which sanitized real-world handoff should be converted for the M1 acceptance exercise?

## Pointers

- `docs/BUILD_BRIEF.md` [sha256:3916dfb14d6e2d045f1c494bf6efcac2ba8d7970b595e3fb9497628ae4c19e9a as of 2026-09-20]
- `spec/SPEC.md` [sha256:e2411d27b03576f017c4b27651d17532ac5c123c99b627ae0221382b06d79ea3 as of 2026-09-20]
- `docs/DECISIONS.md`
- `python -m pip install -e .[dev]`
- `ruff check .`
- `mypy --strict`
- `pytest`
- `mkdocs build --strict`
- `python -m build`

## Environment

- Branch: unavailable; this delivery is not initialized as a Git repository.
- Commit: unavailable; no commit was invented because DCO sign-off requires the contributor's identity.
- Uncommitted files: all files in this delivery are outside Git.
- Python: 3.11 or newer is required.
- Install: `python -m pip install -e .[dev]`
- Verify: `ruff check . && mypy --strict && pytest && python tools/audit_m1_handoff.py HANDOFF.md && mkdocs build --strict && python -m build`

