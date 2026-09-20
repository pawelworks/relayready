---
stafeta: "0.1"
id: "01M30E0S52Y20MASSZJGDMXZ21"
created: "2026-09-20T22:12:06Z"
task: "Prepare RelayReady for public source release and foundation review"
status: ready_for_review
profile: code
parent: "01M30DQ44B9E2RTMQWVVVSVR9D"
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
- [x] Publish the reviewed source import and verify hosted CI.
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
- The public pawelworks/relayready repository contains import d058b5f984347bb147bf98a5810c7a337ffbea54 with the authorized DCO sign-off. An anonymous README request succeeds. Private vulnerability reporting is enabled. [verified 2026-09-20: remote commit API, DCO check and anonymous HTTP 200]
- All twelve hosted Python 3.11-3.14 CI jobs across Linux, macOS and Windows passed for the public import in run 35540740611. Main requires these checks plus DCO, including for admins; force pushes and deletion are blocked. [verified 2026-09-20: terminal Actions result and branch-protection API]
- The owner authorized the reviewed Apache-2.0 source import and permanent public DCO sign-off using the approved name and email. The five unsigned website-era commits remain intact on local main, separate from public history. No foundation submission, transfer agreement, tagged package release, live pilot or independent audit has occurred. [verified 2026-09-20: owner reply, Git history and project records]

## Done so far

- Replaced the broad format extra with the required RFC 3339 dependency in pyproject.toml and documented its clean runtime resolution in THIRD_PARTY_LICENSES.md.
- Added explicit per-instance timestamp registration in src/stafeta/schema.py and wired all four production validators without changing frozen schema contracts.
- Added missing-registration and whitespace regressions; tests/test_schema_formats.py and S001/RB001 regressions pass. A second agent independently reviewed the fix and reran targeted tests.
- Removed generated root PKG-INFO and ignored future copies; Git history retains the old file, and package builds generate current metadata.
- Updated docs/SOURCE_PUBLICATION_REVIEW.md, docs/VERIFICATION.md and the release/application documents with current evidence and unresolved owner gates.
- Recorded the explicit source-publication authorization and reviewed candidate ZIP checksum in docs/SOURCE_PUBLICATION_REVIEW.md.
- Published the reviewed import and confirmed the exact remote SHA, public readability and successful hosted matrix in docs/SOURCE_PUBLICATION_REVIEW.md.
- Configured thirteen required GitHub Actions checks and protected-branch controls without requiring a nonexistent second maintainer's approval.
- Prepared publication-record documentation for the protected pull-request workflow; its eventual merge state must be checked in GitHub.
- Archived the parent handoff and readback byte-for-byte under handoffs/01M30DQ44B9E2RTMQWVVVSVR9D.

## Do not redo

- Do not rename frozen wire keys or remove the legacy CLI.
- Do not create another Site or republish unchanged static assets.
- Do not push to the personal placeholder repository or delete it without approval.
- Do not fabricate DCO signatures, infer attestation from account consent, rewrite deployment history or claim an import retroactively certifies earlier commits.
- Do not submit foundation forms, accept transfer commitments or run paid/live providers without separate explicit authority.

## Next steps

1. Check the publication-record pull request and final main CI state in GitHub; finish any outstanding protected merge checks before further publication work.
2. Review the foundation application with the owner, including the unconfirmed public handle, affiliation and country or legal-entity details.
3. Seek AAIF entry-route guidance and arrange independent review or live pilot evidence; disclose absence rather than inventing eligibility or adoption.
4. Obtain final-form authorization before foundation submission or any contribution/transfer agreement. The source authorization did not supply missing facts or approve unseen terms.

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
- `handoffs/01M30DQ44B9E2RTMQWVVVSVR9D.md`

## Environment

- Local main retains c4066a3f2215c4ff5192b7a9c4b950ef357f222d. Public-source tracks origin/main from the authorized parentless import. This successor is prepared on publication-record for a protected PR; query GitHub for its later result.
- Fresh environments: tmp/permissive-venv and tmp/permissive-wheel-venv. Current artifact directory: dist/permissive-0.1.3. Older dist artifacts are not this candidate.
- Run pytest, Ruff, Mypy, Node checks, fixture reproduction, mock bench, MkDocs strict and isolated wheel checks with these environments before release.
- Existing public Site: appgprj_6aaff178f66c81919fea06215bef5a2f; successful deployment appgdep_6ab00b91b270819188eb8d8e74ade8e9; no Site changes are needed for source publication.
- GitHub authentication is pavelpxp500; that is not a confirmed foundation affiliation. Intended origin is https://github.com/pawelworks/relayready.git.
- Use the exact repository safe.directory override for Git because the checkout has a different owner. Never print or commit credentials.
