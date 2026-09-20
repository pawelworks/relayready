---
stafeta: "0.1"
id: "01M30DQ44B9E2RTMQWVVVSVR9D"
created: "2026-09-20T22:06:50Z"
task: "Prepare RelayReady for public source release and foundation review"
status: in_progress
profile: code
parent: "01M30D77TJ5CAD62DMT21SM1WM"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Publish an honestly documented, reviewed RelayReady source candidate at the owner's intended GitHub destination after contribution-rights attestation, then verify hosted CI before proceeding toward foundation review.

## Done means

- [x] Publish the interactive website and record approved project contacts.
- [x] Prepare an application draft, roadmap, pilot protocol and release checklist.
- [x] Create the intended GitHub organization and public empty repository.
- [x] Correct dependency policy, stale metadata and timestamp validation; verify locally.
- [x] Obtain the owner's reviewed contribution-rights attestation and sign-off authorization.
- [ ] Publish the reviewed source import and verify hosted CI.
- [ ] Obtain separate authority before foundation submission or transfer commitments.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- The website is public at https://relayready.pavel752770.chatgpt.site/ and serves deployed source c4066a3; out and the frozen schemas remain unchanged by this candidate. [verified 2026-09-20: previous successful deployment and source diff]
- Pavel Mihai Lucian is the owner, lead maintainer, security lead, application contact and proposed signatory; the approved address is lucian.pavel@pawelworks.com. [verified 2026-09-20: owner replies]
- The corrected 0.1.3.dev0 candidate passed 223 tests, 97.38 percent stafeta.rules coverage, Ruff, strict Mypy over 53 files, 23 browser vectors, five reproduced fixtures and 150 deterministic mock runs. [verified 2026-09-20: clean local environment checks]
- A runtime-only wheel installation has nine dependencies declaring MIT or PSF-2.0 licenses and no fqdn; both CLI names, all four schemas and invalid timestamp rejection pass. [verified 2026-09-20: isolated wheel installation and metadata inspection]
- The public pawelworks/relayready repository is still empty and grants admin access; its private vulnerability reporting was enabled. Origin points to that intended repository. [recheck]
- The owner authorized the reviewed Apache-2.0 source import and permanent public DCO sign-off using the approved name and email. The five website-era commits remain unsigned; the import preserves their local history and does not retroactively sign them. No source push, foundation submission, transfer agreement, live pilot or independent audit has occurred. [verified 2026-09-20: explicit owner reply, Git history and repository API]

## Done so far

- Replaced the broad format extra with the required RFC 3339 dependency in pyproject.toml and documented its clean runtime resolution in THIRD_PARTY_LICENSES.md.
- Added explicit per-instance timestamp registration in src/stafeta/schema.py and wired all four production validators without changing frozen schema contracts.
- Added missing-registration and whitespace regressions; tests/test_schema_formats.py and S001/RB001 regressions pass. A second agent independently reviewed the fix and reran targeted tests.
- Removed generated root PKG-INFO and ignored future copies; Git history retains the old file, and package builds generate current metadata.
- Updated docs/SOURCE_PUBLICATION_REVIEW.md, docs/VERIFICATION.md and the release/application documents with current evidence and unresolved owner gates.
- Recorded the explicit source-publication authorization and reviewed candidate ZIP checksum in docs/SOURCE_PUBLICATION_REVIEW.md.
- Archived the parent handoff and readback byte-for-byte under handoffs/01M30D77TJ5CAD62DMT21SM1WM.

## Do not redo

- Do not rename frozen wire keys or remove the legacy CLI.
- Do not create another Site or republish unchanged static assets.
- Do not push to the personal placeholder repository or delete it without approval.
- Do not fabricate DCO signatures, infer attestation from account consent, rewrite deployment history or claim an import retroactively certifies earlier commits.
- Do not submit foundation forms, accept transfer commitments or run paid/live providers without separate explicit authority.

## Next steps

1. Prepare the authorized first public source import while retaining local deployment history; verify its tree and DCO trailer, then push only to pawelworks/relayready.
2. Verify the remote source revision and public access; record actual publication evidence without claiming package-registry or foundation release.
3. Inspect actual hosted CI results and configure appropriate branch checks. Do not claim a local test run is hosted verification.
4. Review the final application, affiliation/signatory details and rights inventory separately; seek AAIF route guidance and independent/live pilot evidence without inventing them.

## Open questions

- What public GitHub identity and affiliation should the application list?
- What country or legal entity details apply to the proposed signatory?
- Does the owner approve the actual foundation submission and transfer commitments after reviewing them?

## Pointers

- `docs/SOURCE_PUBLICATION_REVIEW.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/VERIFICATION.md`
- `THIRD_PARTY_LICENSES.md`
- `docs/AAIF_APPLICATION_DRAFT.md`
- `docs/ROADMAP.md`
- `docs/PILOT_PROTOCOL.md`
- `handoffs/01M30D77TJ5CAD62DMT21SM1WM.md`

## Environment

- At this checkpoint, local main retains c4066a3f2215c4ff5192b7a9c4b950ef357f222d. Create a separate public-source branch for the authorized parentless import; do not rewrite main or the deployed source history.
- Fresh environments: tmp/permissive-venv and tmp/permissive-wheel-venv. Current artifact directory: dist/permissive-0.1.3. Older dist artifacts are not this candidate.
- Run pytest, Ruff, Mypy, Node checks, fixture reproduction, mock bench, MkDocs strict and isolated wheel checks with these environments before release.
- Existing public Site: appgprj_6aaff178f66c81919fea06215bef5a2f; successful deployment appgdep_6ab00b91b270819188eb8d8e74ade8e9; no Site changes are needed for source publication.
- GitHub authentication is pavelpxp500; that is not a confirmed foundation affiliation. Intended origin is https://github.com/pawelworks/relayready.git.
- Use the exact repository safe.directory override for Git because the checkout has a different owner. Never print or commit credentials.
