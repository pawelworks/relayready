# Release and submission gates

Working checklist, 21 September 2026. Accountable project owner: **Pavel Mihai
Lucian**, <lucian.pavel@pawelworks.com>. This records preparation, not external
approval, legal clearance or an already completed contribution.

## Prepared locally

- [x] Apache-2.0 license, contribution instructions and governance documents.
- [x] Confirmed project-side role assignments and approved private contact.
- [x] Public website with clearly labelled simulated workbench.
- [x] Twelve-month roadmap, pilot protocol and unsubmitted application draft.
- [x] Sandbox thesis and preliminary project-asset inventory.
- [x] CI/release definitions covering Python, browser checks and exact tag version.

## Public source baseline and package-release gates

- [x] Make `pawelworks/relayready` accessible to the authenticated GitHub account.
  The Free-plan organization and public source repository exist; admin access
  was verified. The earlier not-found result is superseded.
- [x] Publish reviewed source to that destination and verify public access.
  The signed-off import is `d058b5f984347bb147bf98a5810c7a337ffbea54`;
  implementation, tests, specifications, app and integrations match the reviewed candidate.
- [x] Enable and verify private vulnerability reporting on the intended repository.
  API verification returned enabled; email remains an available private route.
- [x] Run the hosted Linux/macOS/Windows and Python 3.11-3.14 CI matrix.
  All 12 jobs passed for public main `c3c91545f6c7584a7f093e8904a7e8d26fc22d1a`
  in [run 35541220709](https://github.com/pawelworks/relayready/actions/runs/35541220709).
  Publication-record PR #1 merged and passed its hosted DCO check.
- [x] Configure protected-branch checks, including DCO for new PRs. Main requires
  all 12 CI jobs plus DCO, an up-to-date branch and resolved conversations, including
  for administrators. Force pushes and deletion are blocked. No second-person
  approval is required while there is only one maintainer.
- [x] Record the owner's contribution-rights attestation for the reviewed import.
  The five unsigned website-era commits remain intact in local deployment history,
  outside the new public import. They were audited but not retroactively signed;
  future publication of that history needs its own provenance decision.
- [x] Record a resolved direct/transitive runtime dependency and license inventory;
  scan the candidate for secrets and review findings without publishing secrets.
- [x] Correct the dependency-policy conflict. Plain jsonschema plus an explicit
  rfc3339-validator registration removes the broad extra and `fqdn`; the fresh
  runtime-only wheel has nine dependencies declaring MIT or PSF-2.0 licenses.
  Timestamp regressions and clean-environment package checks pass.
- [x] Remove stale tracked root `PKG-INFO` reporting version 0.1.0; build metadata
  is generated from the current project version.
- [x] Verify a clean installed wheel, source distribution and contribution ZIP.
  The corrected 0.1.3.dev0 artifacts build locally; the ZIP verifies per-file
  hashes. They are local review artifacts, not a tagged or package-registry release.
- [ ] Have the owner approve the exact release revision, artifact checksums and
  unresolved limitations before tagging or publishing package artifacts.

Keep cryptographic commit signatures, DCO declarations, checksums and legal
rights review distinct. None substitutes for the others. Do not add a personal
`Signed-off-by` declaration on the owner's behalf without explicit attestation.
Use current-version artifact paths, not `dist/*`, which may contain old builds.
The first public import and exact owner attestation are described in
[source-publication review](SOURCE_PUBLICATION_REVIEW.md). The original local
deployment history must remain intact; an import does not retroactively sign it.

## Before a Sandbox submission

- [x] Identify the Sandbox route in the current TC policy and September 1
  announcement; the older project-proposals policy copy is not the latest route.
- [x] Supply a working implementation, permissive license and candid
  [pre-adoption thesis](AAIF_SANDBOX_THESIS.md) with contributor-growth intent.
- [x] Disclose the absence of production adoption, live pilots and independent
  security review. These cannot be replaced by mock benchmark results.
- [x] Confirm public identity: Pavel Mihai Lucian, @pavelpxp500, PAWELWORKS,
  Romania. The owner selected a registered company as contributor.
- [x] Record owner-supplied company details: PAWELWORKS S.R.L., Romanian SRL,
  registered office and Mihai-Lucian Pavel, Administrator. These are not
  independently registry-verified; no title or legal name was invented.
- [x] Prepare a [project-asset inventory](AAIF_ASSET_INVENTORY.md), including
  shared hosting and company/personal account boundaries.
- [x] Record the owner's company contribution-authority attestation and declaration
  of no additional project assets, accounts, sponsorship or obligations.
  This is not an independent IP or legal audit.
- [x] Owner approves the final public application, including company/address
  details and the required conditional trademark/account-transfer commitment.
  Proposed inventory exclusions are not negotiated exceptions to LF terms.
- [x] Obtain explicit submission and documentation-publication authorization,
  including the existing owner DCO sign-off. It does not authorize signatures
  on unseen LF contracts or immediate account transfers.
- [ ] Publish approved supporting documents through the protected project
  workflow, with appropriate DCO authority, before relying on their public links.

The owner authorized the company details and application documents on 21 September;
publication is still pending at this checkpoint. They are not part of the linked successful CI
revision. No foundation issue, outreach message or contribution agreement has
been sent on the basis of these drafts.

Foundation review, votes and the contribution agreement are separate external
steps. Do not label RelayReady donated, contributed or an official AAIF project
before the foundation's process is complete.

Later steps include LF paperwork/technical charter, project-asset arrangements,
foundation votes and onboarding. The current procedure is asynchronous; a live
TC presentation is required only if requested. No TC sponsor has been identified,
but an upfront sponsor is not listed as a Sandbox admission criterion. Confirm
the legal paperwork sequence with staff because published process documents
contain differing timing language. These are not approvals the project can
assign to itself.

## After admission, if granted

- [ ] State explicitly in the README that Sandbox status is not endorsement.
- [ ] Participate in the six-month checkpoint and aim to apply for Growth
  within twelve months of admission if evidence supports it; otherwise expect
  an archival discussion. Do not treat those dates as already running.
- [ ] Gather permissioned production-use evidence from two unaffiliated
  organizations and contribution history spanning at least two organizations
  over six months, with named committers and a committer-acceptance process.
- [ ] Agree a growth plan with a TC sponsor, including a project-specific
  Impact goal. No adoption or staffing outcome is promised.

Those later Growth criteria are not fabricated immediate Sandbox prerequisites.
The [roadmap](ROADMAP.md) and [pilot protocol](PILOT_PROTOCOL.md) propose the
work; foundation review remains discretionary.

## Official references

- [Submission entry point](https://aaif.io/submit-a-project)
- [Current proposal form](https://github.com/aaif/project-proposals/blob/main/.github/ISSUE_TEMPLATE/project-proposal.yml)
- [Current TC lifecycle policy](https://github.com/aaif/technical-committee/blob/main/governance/project-lifecycle-policy.md)
- [Sandbox announcement, September 1](https://aaif.io/blog/aaif-sandbox-phase)
- [Current proposal procedure](https://github.com/aaif/technical-committee/blob/main/project_proposal_process.md)
- [Foundation charter PDF](https://github.com/aaif/foundation/blob/main/foundation-charter.pdf)

Recheck these sources at submission time; this checklist is not legal advice or
a guarantee of eligibility.
