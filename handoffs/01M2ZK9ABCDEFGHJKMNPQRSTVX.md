---
stafeta: "0.1"
id: "01M2ZK9ABCDEFGHJKMNPQRSTVX"
created: "2026-09-20T17:36:49+03:00"
task: "Finish the RelayReady rebrand"
status: done
profile: code
parent: "01M2ZK9ABCDEFGHJKMNPQRSTVW"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Publish the repository locally under the RelayReady public name while preserving the accepted Stafeta 0.1 compatibility contract.

## Done means

- [x] Public branding, package metadata, documentation, and integrations use RelayReady.
- [x] `relayready` is the primary CLI and Python package while `stafeta` remains compatible.
- [x] Frozen wire keys and benchmark arm identifiers remain unchanged.
- [x] Available local tests, lint, mock bench, docs, syntax, and package builds pass, with unavailable external gates disclosed.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- RelayReady is the public product and distribution name. [verified 2026-09-20 by codex-desktop: inspected package metadata, README, integrations, and built wheel]
- The accepted 0.1 schemas still use `stafeta` and `stafeta_readback`. [verified 2026-09-20 by codex-desktop: inspected normative and packaged schemas]
- The test suite has 78 passing tests and 97 percent rule coverage. [verified 2026-09-20 by codex-desktop: ran pytest under Python 3.14]
- Relay Bench has 150 passing deterministic mock runs. [verified 2026-09-20 by codex-desktop: ran relayready bench verify-mock]
- Strict MkDocs, Ruff, syntax compilation, wheel, and source distribution builds pass. [verified 2026-09-20 by codex-desktop: ran each local check]
- The current sandbox could not rerun Mypy because the available cached binary targets Python 3.12 and that interpreter is blocked; Mypy passed before the rebrand. [unverified]

## Done so far

- Added the `relayready` command and Python compatibility package in `pyproject.toml` and `src/relayready`.
- Updated public documentation, schemas, CI commands, and harness integrations to RelayReady.
- Preserved the legacy `stafeta` command, module, wire fields, and benchmark arm.
- Built `dist/relayready-0.1.0-py3-none-any.whl` and `dist/relayready-0.1.0.tar.gz`.
- Rebuilt the documentation site under the RelayReady name.

## Do not redo

- Do not rename frozen `stafeta` or `stafeta_readback` wire fields.
- Do not remove the legacy `stafeta` CLI or Python module in version 0.1.
- Do not reuse RelayCraft, ThreadKeep, ContextCarry, RelayProof, or Threadmark; they have relevant public collisions.

## Next steps

1. None.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `README.md`
- `pyproject.toml`
- `spec/SPEC.md`
- `src/relayready/__init__.py`
- `src/stafeta/cli.py`
- `dist/relayready-0.1.0-py3-none-any.whl`
- `dist/relayready-0.1.0.tar.gz`

## Environment

- Branch: unavailable; this directory is not a Git repository.
- Commit: unavailable.
- Local checks: 78 tests passed at 97 percent rule coverage; Ruff passed; Relay Bench passed 150 mock runs; strict docs and packages built.
- External checks: hosted CI, real-runner Relay Bench, and the manual two-vendor relay remain owner-only publication gates.
