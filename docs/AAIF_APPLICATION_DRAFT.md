# AAIF application working draft

Updated 21 September 2026. Requested stage: **Sandbox**.
**Owner-authorized for submission; not yet submitted at this checkpoint.**
This is not a statement that the foundation has approved eligibility or admission.
The [short technical thesis](AAIF_SANDBOX_THESIS.md) sets out intended users,
the pre-adoption rationale and evidence that would justify progression.

## Project and technical offer

**RelayReady** is an Apache-2.0, vendor-neutral handoff and receiver-readback
contract with a deterministic local Python validator. It preserves task goals,
invariants, stale facts, rejected approaches and human questions across agent
boundaries. The experimental Continuation Gate additionally compares declared
resource revisions, pinned input bytes and unresolved prior effects. A receipt
can request continuation, rechecking or escalation; it does not grant authority
to act or prove that observations are true.

The project was developed in September 2026 with AI-assisted implementation,
initially named Stafeta and renamed RelayReady before release. The frozen
`stafeta` and `stafeta_readback` wire identifiers and legacy `stafeta` command
remain compatible. The published-source development candidate is `0.1.3.dev0`;
the published presentation app is the earlier `0.1.2.dev0` workbench snapshot.

The intended contribution is the specification, schemas, implementation, CLI,
portable integration instructions, negative tests, reproducible fixtures,
benchmark harness and demonstration app. Third-party conference slides are not
included. See [the technical proposal](CONTRIBUTION_PROPOSAL.md).

## Ecosystem fit

The project aims to make cross-harness continuation inspectable and testable,
without requiring a particular model vendor or a hosted service. An A2A task
could carry these artifacts; MCP could expose the underlying resources; project
instructions such as AGENTS.md can teach a receiver to emit a readback. A goose
recipe and portable harness instructions are included. This complements open
agent interoperability by providing a shared, inspectable validation surface.
These are integration designs or instruction packages, not accepted extensions
or verified live adapters. See
[integration boundaries](INTEGRATION_PROFILE.md) and
[research comparisons](PRODUCT_RESEARCH.md). No company is claimed to lack an
equivalent, and no foundation affiliation, endorsement or exclusive invention
is claimed.

## Usage and evidence

Implemented demonstrations include interrupted code work, document work,
resource drift, changed inputs, unresolved decisions and uncertain prior effects.
The static workbench lets reviewers edit simulated observations, compare runs
and independently validate exported evidence with Python.

There are **no substantiated production adopters or live cross-vendor benchmark
results**. Deterministic fixtures and mock benchmark results establish local
checker behavior only. [Candidate verification](VERIFICATION.md) records the
earlier app checks; [the pilot protocol](PILOT_PROTOCOL.md) describes future live
evaluation. No executed pilot or improvement estimate is implied.

## Project locations

- Website: <https://relayready.pavel752770.chatgpt.site/> (published publicly).
- Repository: <https://github.com/pawelworks/relayready> (public source).
- Issue tracker location: <https://github.com/pawelworks/relayready/issues>.

The earlier namespace-access blocker is resolved. The Pawelworks organization
exists on GitHub's Free plan under `pavelpxp500`; the intended public repository
has administrative access, issues and private vulnerability reporting enabled.
The reviewed, corrected source was imported at commit
`d058b5f984347bb147bf98a5810c7a337ffbea54` with the owner's authorized DCO
sign-off. [Publication-record PR #1](https://github.com/pawelworks/relayready/pull/1)
merged under branch protection; its public main revision is
`c3c91545f6c7584a7f093e8904a7e8d26fc22d1a`. This draft's additional edits are
local and have not yet been published. No code has been pushed to the personal
placeholder repository.

## People, governance and contributions

Pavel Mihai Lucian is the sole confirmed maintainer, project owner, security
lead and application contact. Email: <lucian.pavel@pawelworks.com>.
His approved public handle is [@pavelpxp500](https://github.com/pavelpxp500),
affiliation PAWELWORKS, Romania. He confirms Romania as his country and reports
being the company's sole owner and sole worker. The proposed contributing legal
entity is PAWELWORKS S.R.L.; its owner-supplied details appear below. AI assistants
are not counted as independent maintainers or community contributors.

The repository's `GOVERNANCE.md` records maintainer-led decisions, a seven-day
normal review window, and at least two weeks for normative specification
changes. `CONTRIBUTING.md` describes DCO sign-offs and review; issue templates
cover bugs, rule proposals, fixtures and specification changes. The initial public
import discloses AI-assisted preparation and records the owner's contribution-rights
attestation. Earlier unsigned website-era commits remain in local deployment
history, separate from the public import; no retroactive signature was fabricated.
Branch protection requires the CI matrix and DCO checks without pretending there
is an independent second maintainer.

## Engineering, security and roadmap

The hosted CI matrix passed all 12 Python 3.11 through 3.14 jobs on Linux, macOS
and Windows, including Node 24 browser checks, for public main revision
`c3c91545f6c7584a7f093e8904a7e8d26fc22d1a` in
[run 35541220709](https://github.com/pawelworks/relayready/actions/runs/35541220709).
The publication-record PR also passed the hosted DCO check. These results apply
to the linked revision, not automatically to subsequent edits.
Tagged artifact builds must pass the same matrix and match package metadata;
that tag-triggered release path has not been exercised. Release artifacts are not
automatically uploaded to PyPI. There is no established release cadence.

Direct runtime dependencies are jsonschema (MIT), PyYAML (MIT) and
rfc3339-validator (MIT). The corrected
candidate uses explicit date-time registration instead of broad format extras;
the clean installed wheel's nine resolved runtime dependencies declare MIT or
PSF-2.0 licenses. `THIRD_PARTY_LICENSES.md` records that dated inventory, not a
cross-platform lock or legal clearance. No completed independent security audit
or OpenSSF Best Practices badge is claimed. Private security and conduct reports
go to Pavel Mihai Lucian at the email above; no independent conduct appeal
channel is yet staffed.

The [12-month roadmap](ROADMAP.md) prioritizes provenance, independent review,
two separately implemented adapters, live pilots and broader governance.

## Requested route and communication

Request Sandbox under the current
[TC lifecycle policy](https://github.com/aaif/technical-committee/blob/main/governance/project-lifecycle-policy.md),
also described in AAIF's [1 September announcement](https://aaif.io/blog/aaif-sandbox-phase).
The older policy copy in the project-proposals repository should not be used to
exclude this route. RelayReady offers a working permissively licensed
implementation, one maintainer and a pre-adoption thesis, not Growth-stage
adoption. The foundation decides whether that case is sufficient.

No TC sponsor has been identified; one is not an upfront Sandbox intake
requirement. Under the [current operating procedure](https://github.com/aaif/technical-committee/blob/main/project_proposal_process.md),
review is normally asynchronous and a live presentation occurs if requested.
Growth milestones are future goals in the thesis, not fabricated current users.
If admitted to Sandbox, the README must explicitly disclaim endorsement.

Public project discussion currently uses GitHub issues; private security and
conduct reports use the approved email. The owner reports no additional
project-specific social accounts, domains, sponsors or contractual obligations
beyond the repository and website. This is an owner declaration, not an
independent audit. Infrastructure requested is public Git hosting,
CI and static hosting. No grant or funding request is made; shared hosting account
boundaries require coordination before any transfer.

## Company and signatory details for final owner review

The owner selected company contribution and supplied these details on
21 September 2026. They are not independently registry-verified.

| Field | Owner-supplied value |
|---|---|
| Registered legal name | PAWELWORKS S.R.L. |
| Legal form | Societate cu Răspundere Limitată (SRL), Romanian limited liability company |
| Registered office | B-dul Gloriei Nr. 70, Et. 2, Ap. 6, Sector 1, București, Romania |
| Legal representative / signing title | Mihai-Lucian Pavel, Administrator |
| Agreement contact | lucian.pavel@pawelworks.com |
| Public maintainer / application contact | Pavel Mihai Lucian, @pavelpxp500 |

The legal representative spelling is retained exactly as supplied; the public
maintainer identity is not silently substituted into a legal agreement. Tax,
registry and activity identifiers are not reproduced because this form does not
request them. Supplying company details does not itself attest ownership of each
asset or accept a transfer agreement.

## Owner authorization and remaining external steps

The [proposal form](https://github.com/aaif/project-proposals/blob/main/.github/ISSUE_TEMPLATE/project-proposal.yml)
requires the applicant's agreement about project trademarks and accounts if
accepted. On 21 September 2026 (owner's local date), the owner explicitly
confirmed company authority and authorized that conditional commitment, the
public application including company/address/signatory details, and publication
of these supporting documents with the existing owner DCO sign-off. The
[asset inventory](AAIF_ASSET_INVENTORY.md) distinguishes project assets from
the company and personal accounts and links the actual foundation charter PDF.
Proposed scope boundaries are not agreed exceptions to foundation requirements.

This approval is recorded in the asset inventory; it is an owner declaration,
not independent rights or registry verification. Actual LF agreements and the
project technical charter still need separate
review and signature. The foundation's TC/GB decisions and onboarding are external
steps. No form has been submitted, agreement signed, transfer performed or
foundation vote obtained. See [remaining gates](RELEASE_CHECKLIST.md).
