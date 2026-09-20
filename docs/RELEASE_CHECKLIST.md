# Release and submission gates

Working checklist, 20 September 2026. Accountable project owner: **Pavel Mihai
Lucian**, <lucian.pavel@pawelworks.com>. This records preparation, not external
approval, legal clearance or an already completed contribution.

## Prepared locally

- [x] Apache-2.0 license, contribution instructions and governance documents.
- [x] Confirmed project-side role assignments and approved private contact.
- [x] Public website with clearly labelled simulated workbench.
- [x] Twelve-month roadmap, pilot protocol and unsubmitted application draft.
- [x] CI/release definitions covering Python, browser checks and exact tag version.

## Before the first source release

- [x] Make `pawelworks/relayready` accessible to the authenticated GitHub account.
  The Free-plan organization and public source repository exist; admin access
  was verified. The earlier not-found result is superseded.
- [x] Publish reviewed source to that destination and verify public access.
  The signed-off import is `d058b5f984347bb147bf98a5810c7a337ffbea54`;
  implementation, tests, specifications, app and integrations match the reviewed candidate.
- [x] Enable and verify private vulnerability reporting on the intended repository.
  API verification returned enabled; email remains an available private route.
- [x] Run the hosted Linux/macOS/Windows and Python 3.11-3.14 CI matrix.
  All 12 jobs passed for the initial public import in
  [run 35540740611](https://github.com/pawelworks/relayready/actions/runs/35540740611).
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

## Before foundation submission

- [ ] Ask AAIF to confirm the applicable entry route; the current form and
  linked lifecycle policy differ on early-stage terminology.
- [ ] Complete independent review and the live pilot, or disclose their absence.
- [ ] Recruit genuine additional maintainers/contributors and document any
  adoption with permission. Current Growth/Impact expectations are not met.
- [ ] Confirm public GitHub identity, affiliation, individual country or legal
  entity details, and authority to contribute each asset.
- [ ] Inventory name/logo rights, domains, repositories, hosting and other
  project accounts; confirm which are owned and transferable.
- [ ] Owner reviews the final form and any trademark/account-transfer commitment.
- [ ] Obtain explicit authorization to submit the public issue. Preparation
  and contact approval are not authorization to sign a contribution agreement.

Foundation review, votes and the contribution agreement are separate external
steps. Do not label RelayReady donated, contributed or an official AAIF project
before the foundation's process is complete.

Later acceptance steps also include the TC presentation and an LF-approved
technical charter under the current lifecycle policy. A Growth-stage TC sponsor
is a policy gate even though identifying one in the intake form is optional.
These are not roles or approvals the project can assign to itself.

## Official references

- [Submission entry point](https://aaif.io/submit-a-project)
- [Current proposal form](https://github.com/aaif/project-proposals/blob/main/.github/ISSUE_TEMPLATE/project-proposal.yml)
- [Lifecycle policy](https://github.com/aaif/project-proposals/blob/main/governance/project-lifecycle-policy.md)

Recheck these sources at submission time; this checklist is not legal advice or
a guarantee of eligibility.
