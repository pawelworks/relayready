# AAIF application working draft

Prepared 20 September 2026. **Not submitted; not an accepted donation.**
This document is for owner review and an early-stage eligibility discussion,
not a statement that RelayReady satisfies foundation admission requirements.

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
remain compatible. The current local development candidate is `0.1.3.dev0`;
the published presentation app is the earlier `0.1.2.dev0` workbench snapshot.

The intended contribution is the specification, schemas, implementation, CLI,
portable integration instructions, negative tests, reproducible fixtures,
benchmark harness and demonstration app. Third-party conference slides are not
included. See [the technical proposal](CONTRIBUTION_PROPOSAL.md).

## Ecosystem fit

The project aims to make cross-harness continuation inspectable and testable,
without requiring a particular model vendor or a hosted service. An A2A task
could carry these artifacts; MCP could expose the underlying resources; project
instructions can teach a receiver to emit a readback. These are complementary
integration designs, not accepted extensions or verified live adapters. See
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
- Repository: <https://github.com/pawelworks/relayready> (created, currently empty).
- Issue tracker location: <https://github.com/pawelworks/relayready/issues>.

The earlier namespace-access blocker is resolved. The Pawelworks organization
exists on GitHub's Free plan under `pavelpxp500`; the intended public repository
has administrative access, issues and private vulnerability reporting enabled.
It is still empty. Dependency-policy corrections and contribution-provenance
review remain before publishing source and running hosted CI. No code has been
pushed to the personal placeholder repository.

## People, governance and contributions

Pavel Mihai Lucian is the sole confirmed maintainer, project owner, security
lead and application contact. Email: <lucian.pavel@pawelworks.com>.
His public GitHub handle and organizational affiliation for this proposal
remain unconfirmed; a requested repository namespace does not establish a
legal entity or affiliation. AI assistants are not counted as independent
maintainers or community contributors.

The repository's `GOVERNANCE.md` records maintainer-led decisions, a seven-day
normal review window, and at least two weeks for normative specification
changes. `CONTRIBUTING.md` describes DCO sign-offs and review; issue templates
cover bugs, rule proposals, fixtures and specification changes. Public operation
of this process still depends on publishing the intended repository. Historical
commits lack DCO sign-offs and require rights/provenance review; no retroactive
personal signature has been fabricated.

## Engineering, security and roadmap

The proposed CI matrix covers Python 3.11 through 3.14 on Linux, macOS and
Windows, plus Node 24 browser checks. Tagged artifact builds must pass that
matrix and match package metadata. Workflows are prepared locally, not yet
verified on the intended GitHub repository. Release artifacts are not
automatically uploaded to PyPI. There is no established release cadence.

Runtime dependencies are jsonschema, PyYAML and rfc3339-validator. The corrected
candidate uses explicit date-time registration instead of broad format extras;
the clean installed wheel's nine resolved runtime dependencies declare MIT or
PSF-2.0 licenses. `THIRD_PARTY_LICENSES.md` records that dated inventory, not a
cross-platform lock or legal clearance. No completed independent security audit
or OpenSSF Best Practices badge is claimed. Private security and conduct reports
go to Pavel Mihai Lucian at the email above; no independent conduct appeal
channel is yet staffed.

The [12-month roadmap](ROADMAP.md) prioritizes provenance, independent review,
two separately implemented adapters, live pilots and broader governance.

## Foundation discussion and owner-only decisions

The current [proposal form](https://github.com/aaif/project-proposals/blob/main/.github/ISSUE_TEMPLATE/project-proposal.yml)
mentions Sandbox, Growth and Impact, whereas the linked
[lifecycle policy](https://github.com/aaif/project-proposals/blob/main/governance/project-lifecycle-policy.md)
describes Growth/Impact entry. Ask AAIF which early-stage route applies before
selecting one. No technical committee sponsor has been identified. The project
does not meet the stated Growth/Impact community and adoption expectations.

Proposed individual signatory: **Pavel Mihai Lucian**,
**lucian.pavel@pawelworks.com**. Country has not been supplied. If contribution
is through an organization, its legal name, address, entity type and signing
authority must instead be confirmed. Existing sponsorship and project social
accounts have not been inventoried. Infrastructure needs are currently modest:
public Git hosting, CI and static hosting; no grant or funding request is made.

The trademark/account transfer commitment is **not checked or agreed on the
owner's behalf**. Rights review, scope of transferred assets and any contribution
agreement require the owner's explicit review. No form has been submitted,
agreement signed, or foundation vote obtained. See the
[release and submission gates](RELEASE_CHECKLIST.md).
