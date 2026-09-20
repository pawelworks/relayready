---
stafeta: "0.1"
id: "01M2ZV10FVH9CSXAKQ65NE2RB7"
created: "2026-09-20T16:32:00Z"
task: "Publish the reviewed RelayReady workbench"
status: in_progress
profile: code
parent: "01M2ZQS1F7BQAW9ECBTNKXPJJ0"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Deliver the advanced RelayReady workbench and new brand asset, then publish its exact reviewed source through the existing private Site.

## Done means

- [x] Add editable observations, evidence comparison, a run notebook and regression studio.
- [x] Export and independently revalidate exact-byte bundles.
- [x] Add the RelayReady logo and favicon.
- [x] Verify deterministic behavior and responsive presentation without changing frozen contracts.
- [ ] Complete the supported source publication and record the returned deployment outcome.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- The application is a dependency-free local sandbox with five immutable example contracts, fresh browser checks and a ten-case regression studio. [verified 2026-09-20: inspected the running workbench]
- All 191 Python tests passed with 97.38 percent coverage of stafeta.rules only; 23 browser vectors match independent Python decisions, codes and bindings. [verified 2026-09-20: pytest and Node checks]
- All 150 deterministic mock runs passed; Ruff and strict Mypy passed. [verified 2026-09-20: local commands]
- The logo loads; desktop, 390px and 320px layouts were inspected, with narrow-screen clock overflow corrected. [verified 2026-09-20: browser checks]
- Publication is pending at this source snapshot; the existing private Site's source connection now succeeds. [recheck]
- Browser assessments are explicitly scoped, and no live provider integration, adoption, endorsement or accepted donation is claimed. [verified 2026-09-20: app copy and docs reviewed]
- The user authorized implementation and publication; no formal donation submission or ownership transfer occurred. [verified 2026-09-20: user requests and task actions]

## Done so far

- Implemented the workbench under `out/workbench*` and the brand asset `out/relayready-logo.png`.
- Added independent bundle validation in `src/stafeta/bundle.py` and regression tests.
- Documented product research, workbench boundaries, brand provenance and local verification.
- Archived the issued parent handoff and readback byte-for-byte.

## Do not redo

- Do not rename frozen wire keys or remove the legacy CLI.
- Do not create another Site or save a version before its exact source is pushed.
- Do not reuse expired credentials, fabricate DCO signatures or claim exclusive novelty.
- Do not conflate simulated observations, browser assessments and full Python receipts.
- Do not submit a donation or impersonate an organization without separate authority.

## Next steps

1. Push the exact committed source, verify HEAD, package that revision and save it.
2. Deploy privately through the existing Site and inspect the terminal native status.
3. Return the verified production URL; if continuing later, inspect Site state before retrying.
4. Resolve formal contribution provenance and owner identity details separately.

## Open questions

- What GitHub organization and repository URL should package metadata and repository links use?
- What private security reporting route should replace the placeholder in `SECURITY.md`?
- What public handle should identify the current maintainer?

## Pointers

- `docs/WORKBENCH.md`
- `docs/PRODUCT_RESEARCH.md`
- `docs/VERIFICATION.md`
- `docs/BRAND.md`
- `out/workbench.html`
- `handoffs/01M2ZQS1F7BQAW9ECBTNKXPJJ0.md`

## Environment

- Branch main; project version 0.1.2.dev0; no release tag or donation sign-off.
- Site project: appgprj_6aaff178f66c81919fea06215bef5a2f; slug relayready; static directory out.
- Sites portable helpers are available. The old missing-helper/network blocker no longer applies.
- The deployment outcome lives in the native Sites status; this source snapshot precedes publication.
- Temporary research files remain excluded from source and contribution packaging.
