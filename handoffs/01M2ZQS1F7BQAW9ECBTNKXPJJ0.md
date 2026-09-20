---
stafeta: "0.1"
id: "01M2ZQS1F7BQAW9ECBTNKXPJJ0"
created: "2026-09-20T15:43:24+00:00"
task: "Publish the RelayReady continuation contribution candidate"
status: blocked
profile: code
parent: "01M2ZK9ABCDEFGHJKMNPQRSTVX"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Deliver the verified RelayReady contribution candidate and publish its interactive website through the existing Site when the supported hosting workflow becomes available, without claiming unverified novelty or donation acceptance.

## Done means

- [x] Implement optional continuation sidecars and deterministic receipts.
- [x] Demonstrate five simulated cases with real recorded validator outputs.
- [x] Preserve frozen wire contracts and the legacy command.
- [x] Verify local code, fixtures and responsive frontend; prepare contribution documentation and packaging.
- [ ] Push and deploy the exact committed source with the supported Sites workflow and verify its production URL.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- Continuation Gate 0.1-draft is implemented as optional sidecars and a local CLI. [verified 2026-09-20: inspected src/stafeta/continuation.py and its tests]
- The full suite passed 170 tests with 97.38 percent coverage of the existing lint-rule module. [verified 2026-09-20: ran pytest on Python 3.12.14]
- All 150 deterministic mock benchmark runs matched expected outcomes. [verified 2026-09-20: ran stafeta bench verify-mock --json]
- Five browser receipts reproduce byte-for-byte; desktop and mobile behavior were inspected. [verified 2026-09-20: generator check, Node harness and browser inspection]
- The existing Site is private and unpublished, with no production URL. [recheck]
- Required Sites skill helpers are absent and outbound Git access remains restricted. [recheck]
- The user approved implementation and publishing; no donation submission or ownership transfer has occurred. [verified 2026-09-20: reviewed user requests and task actions]

## Done so far

- Implemented the draft schemas, local validator and tests in `src/stafeta/continuation.py` and `tests/test_continuation*.py`.
- Added reproducible cases under `examples/continuation/` and the static application under `out/`.
- Documented the offer, integration boundaries and checks in `docs/CONTRIBUTION_PROPOSAL.md`, `docs/INTEGRATION_PROFILE.md` and `docs/VERIFICATION.md`.
- Added `tools/package_contribution.py`, excluding research decks, temporary files and hosting configuration.
- Archived the issued parent handoff and readback unchanged under `handoffs/01M2ZK9ABCDEFGHJKMNPQRSTVX.*`.

## Do not redo

- Do not rename frozen wire keys or remove the legacy CLI; that breaks compatibility.
- Do not create a replacement Site; reuse the registered project.
- Do not save a Sites version before its exact committed source is pushed; the remote branch does not yet exist.
- Do not reuse expired credentials or present simulated observations as live integrations.
- Do not claim exclusive novelty or fabricate sign-offs; related ideas already exist and provenance requires review.

## Next steps

1. Recheck required Sites skill availability and supported outbound source-push access before attempting publication.
2. Retrieve the existing Site, obtain a fresh credential, review provenance, commit and push exact source, verify HEAD, and package that revision with supported helpers.
3. Save and deploy privately, poll to a terminal state, then verify the user-approved public URL.
4. Handle formal donation intake and owner identities separately; do not impersonate the owner or receiving organization.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `docs/CONTINUATION_GATE.md`
- `docs/CONTRIBUTION_PROPOSAL.md`
- `docs/VERIFICATION.md`
- `tools/package_contribution.py`
- `out/index.html`
- `handoffs/01M2ZK9ABCDEFGHJKMNPQRSTVX.md`

## Environment

- Branch: `main`; base HEAD: `52c2b5bbcf497e82a8d9585cdfbaca731315e890`.
- The contribution candidate is in uncommitted working-tree changes. Do not invent DCO identities or rewrite history.
- Site project: `appgprj_6aaff178f66c81919fea06215bef5a2f`; slug: `relayready`; static root: `out/`.
- Bundled Python 3.12 works with dependencies in `../../work/stafeta-venv/Lib/site-packages`; the old virtualenv launcher is broken.
- Local preview: `python -m http.server 4321 --bind 127.0.0.1 --directory out`.
- Repeatable checks and external limitations are in `docs/VERIFICATION.md`.
