---
stafeta: "0.1"
id: "01M2ZHGGTGMVZ7ZH5TDMVQBHF5"
created: "2026-09-20T16:53:53+03:00"
task: "Implement Stafeta M3"
status: done
profile: code
parent: "01M2ZGJ4AFQKA03ACQB8DM57WC"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Complete deterministic readback and handoff-chain enforcement so receivers mechanically acknowledge every critical item before acting.

## Done means

- [x] `readback new` emits a schema-valid pre-filled skeleton.
- [x] `readback check` covers every specification failure mode and fenced chat YAML.
- [x] `chain check` reports missing parents, cycles, duplicates, and unwaived dropped invariants.
- [x] Tests include every readback failure mode and a silently dropped invariant.
- [x] Local lint, strict typing, 65 tests, documentation, and package builds pass.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- M3 commands are implemented and documented. [verified 2026-09-20 by codex-desktop: exercised the installed console commands]
- The M2 readback passes with zero errors and zero warnings. [verified 2026-09-20 by codex-desktop: ran `stafeta readback check`]
- The test suite has 65 passing tests and rule coverage remains 97.38 percent. [verified 2026-09-20 by codex-desktop: ran pytest with the configured coverage gate]
- Hosted CI remains unavailable without an approved remote repository. [verified 2026-09-20 by codex-desktop: no `.git` directory exists]

## Done so far

- Added `src/stafeta/readback.py` with skeleton generation, schema checks, mechanical acknowledgment checks, and fenced-YAML extraction.
- Added `src/stafeta/chain.py` with parent, cycle, duplicate, inheritance, and waiver validation.
- Added nested readback and chain commands to the CLI with human and JSON output.
- Added exact readback failure-mode and chain tests in `tests/test_readback.py` and `tests/test_chain.py`.
- Documented the 0.80 Jaccard overlap threshold and waiver syntax in the specification and CLI guide.

## Do not redo

- Do not change frozen headings or readback fields.
- Do not weaken invariant comparison or infer waivers from omissions.
- Do not claim semantic goal understanding from a passing mechanical readback.
- Do not implement unverified native integration formats by guessing.
- Do not publish or deploy the repository or documentation.

## Next steps

1. Verify each target harness's native integration mechanism from installed help or official documentation.
2. Add the shared AGENTS snippet and chat write/resume prompts.
3. Package verified Codex, Claude Code, goose, and Kimi integrations; label unavailable mechanisms unverified.
4. Run the M4 manual-format checks and prepare the M4 handoff.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `spec/SPEC.md` [sha256:3024e5702269f36bba915a8d879fc3078b1e8d10572e3b3ea43fb25ddc096477 as of 2026-09-20]
- `src/stafeta/readback.py`
- `src/stafeta/chain.py`
- `tests/test_readback.py`
- `tests/test_chain.py`
- `docs/CLI.md`
- `handoffs/01M2ZGJ4AFQKA03ACQB8DM57WC.md`

## Environment

- Branch: unavailable; this delivery is not a Git repository.
- Commit: unavailable.
- Install: `python -m pip install -e .[dev]`
- Verify: `ruff check .`, `mypy --strict`, `pytest`, `stafeta readback check`, `mkdocs build --strict`, and `python -m build`.

