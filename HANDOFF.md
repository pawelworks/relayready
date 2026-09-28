---
stafeta: "0.1"
id: "01M30JDN1HRJYAW56J34R6TA6R"
created: "2026-09-20T23:29:02Z"
task: "Complete reviewed RelayReady domain and public-source follow-up"
status: ready_for_review
profile: code
parent: "01M30G0BT2AFSE59FBHJNCH1PY"
sender:
  agent: "codex-desktop"
  vendor: "openai"
  model: null
lang: "en"
---

## Goal

Keep RelayReady's public records aligned with its registered domain and published footer credit, then complete the explicitly authorized PR 2 merge only after full review and current protected checks.

## Done means

- [x] Update the GitHub homepage and existing AAIF proposal to relayready.org.
- [x] Add the domain and renewal/transfer considerations to the proposed asset inventory.
- [x] Preserve the original submission body hash and immutable supporting revision.
- [x] Submit the already-deployed logo source in a separate public pull request.
- [x] Schedule an eligible PR 2 merge check without enabling early auto-merge.
- [ ] Complete PR 2 after its review period with passing current checks and no unresolved objection.
- [ ] Respond to actual AAIF review and legal/onboarding requests without treating submission as acceptance.

## Invariants

- Never publish artifacts or deploy documentation without owner approval.
- Never invent evidence, adoption claims, benchmark results, identities, or security contacts.
- Never begin M2 until the owner accepts M1.

## State

- AAIF proposal 44 was amended at 2026-09-20T23:26:14Z; API readback matched the intended body. Its normalized hash and original submission evidence are recorded in docs/AAIF_SUBMISSION_RECORD.md. [verified 2026-09-20: GitHub issue API and SHA-256 calculation]
- GitHub repository homepage now reads https://relayready.org/; domain/application documentation was pushed at b9a4995769baa3eb25f3f69179efe57358dd47b7 in PR 2. [verified 2026-09-20: repository API and source push]
- The domain is registered with Cloudflare and routes to the existing public Site; registrar expiration was reported as 2027-09-20T23:03:43Z. Public site/app returned HTTP 200 and Sites reported active TLS. This is technical evidence, not a legal ownership audit. [verified 2026-09-20: registrar/Sites APIs and HTTPS requests]
- The logo public-source PR is https://github.com/pawelworks/relayready/pull/3 at f250a60c79ded07e3ebe2946c6aede066de04c93; its static output matches deployed source 367ff0b5d79d9795c2417ad887492020ca76fc7c. [verified 2026-09-20: PR creation and Git tree diff]
- The owner explicitly authorized DCO sign-off Pavel Mihai Lucian <lucian.pavel@pawelworks.com> for domain and logo commits. The PAWELWORKS company mark is separate from project trademarks and is not offered for donation. [verified 2026-09-20: explicit owner reply]
- A thread follow-up was created for 28 September 2026 at 10:00 Europe/Bucharest, no earlier than seven full days after the substantive amendment. Its merge remains conditional on the actual latest head, required checks, governance and unresolved objections. Later material changes require a fresh allowance. [verified 2026-09-20: native automation creation and saved schedule]
- Static site checks, 23 workbench vectors and JavaScript syntax checks passed for the logo import; strict MkDocs passed for the domain amendment. Hosted checks for subsequent commits must be inspected separately. [verified 2026-09-20: local command output]
- No live pilot, independent human review, foundation acceptance, LF signature or project-asset transfer has been established. [verified 2026-09-20: task actions and retained public disclosures]

## Done so far

- Updated the repository homepage and amended existing AAIF issue 44 without a duplicate or changed original supporting snapshots; see docs/AAIF_SUBMISSION_RECORD.md.
- Published the domain inventory amendment at b9a4995 with explicit owner-authorized DCO and kept it in PR 2 for review.
- Submitted the focused owner-supplied logo import in PR 3; no unsigned deployment history was imported into public source.
- Scheduled the user-authorized PR 2 follow-up with date, current-head, CI/DCO, objection and branch-protection guards.
- Archived the issued predecessor handoff and readback byte-for-byte under handoffs/01M30G0BT2AFSE59FBHJNCH1PY.

## Do not redo

- Do not rename frozen wire keys or remove the legacy CLI; compatibility remains accepted.
- Do not create another Site or redeploy unchanged static assets; logo publication already succeeded.
- Do not push deployment history to GitHub main, fabricate DCO signatures or infer new rights from an old attestation.
- Do not duplicate the AAIF application, sign unseen agreements or transfer company/personal accounts; the authorized update is project-scoped.
- Do not merge PR 2 before its review window or bypass required checks; the future check is conditional, not early auto-merge.
- Do not merge PR 3 merely because PR 2 was authorized for completion; only submission of the logo PR was requested.
- Do not run paid providers, send sales outreach or claim pilot efficacy from deterministic mocks; those need separate scope and authority.

## Next steps

1. Inspect the exact latest CI/DCO outcomes for both PRs; fix scoped failures without importing unrelated history.
2. On or after 28 September 2026 at 10:00 Europe/Bucharest, recheck PR 2 and any later substantive amendment date, then perform the user-authorized protected merge only if eligible.
3. If PR 2 is merged, record its verified merge and stop its follow-up; if a new authority or unresolved objection blocks it, report that condition.
4. Respond to genuine AAIF questions and coordinate actual LF agreements and asset arrangements with the authorized representative.
5. Discuss a permissioned cross-vendor pilot offer using docs/PILOT_PROTOCOL.md, preserving its proposed/not-executed status.

## Open questions

- None.

## Pointers

- docs/AAIF_SUBMISSION_RECORD.md
- docs/AAIF_ASSET_INVENTORY.md
- docs/BRAND.md
- docs/PILOT_PROTOCOL.md
- https://github.com/aaif/project-proposals/issues/44
- https://github.com/pawelworks/relayready/pull/2
- https://github.com/pawelworks/relayready/pull/3
- handoffs/01M30G0BT2AFSE59FBHJNCH1PY.md

## Environment

- Current documentation branch aaif-sandbox-proposal tracks origin/aaif-sandbox-proposal; public logo branch public-pawelworks-logo tracks its own origin branch.
- Local main and site-pawelworks-logo contain separate deployment history. Preserve them; do not rewrite or push them to public main.
- Repository: https://github.com/pawelworks/relayready.git. Use only the exact project safe.directory override.
- Site: appgprj_6aaff178f66c81919fea06215bef5a2f; published logo deployment appgdep_6ab068b924ac8191b869fed91590f2e4. No website redeployment is required for these public-record changes.
- Python environment: tmp/permissive-venv/Scripts/python.exe. Original issue body remains in ignored tmp/AAIF_SUBMISSION_ORIGINAL_44.md; do not commit credential-bearing or unrelated temporary files.
