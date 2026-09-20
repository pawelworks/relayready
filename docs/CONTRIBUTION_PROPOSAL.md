# RelayReady contribution proposal

Prepared for technical discussion with the Agentic AI Foundation community.
Status: submitted for [AAIF Sandbox consideration](https://github.com/aaif/project-proposals/issues/44);
no AAIF affiliation, acceptance, endorsement, ownership transfer or production
adoption is claimed.

## Offer

Contribute a small Apache-2.0 implementation of a portable continuation checkpoint:
an immutable handoff, receiver readback, expected state, observations and a
deterministic receipt. The package includes schemas, a local CLI, negative tests,
reproducible fixtures, a presentation website and documented integration boundaries.
The [verification record](VERIFICATION.md) separates observed local results from
hosted CI results and external checks that have not been completed.

The practical question is: after a task crosses an agent boundary, do the supplied
records still justify continuing, or must the next actor recheck or escalate?

## Where it fits

| Work discussed at AGNTCon/MCPCon | RelayReady contribution | Status |
|---|---|---|
| Orange: typed task contracts and recoverable A2A handoffs | Executable checks over a specific handoff/readback pair and unresolved effects | Implemented locally as a draft profile |
| Bloomberg: filesystem-shaped resources and shared artifact lifecycles | Expected versus observed resource revision records | Local comparison implemented; provider adapter proposed |
| Supabase: version, digest and evaluation as separate signals | Pin input bytes; changed bytes trigger recheck even under the same label | Implemented locally; registry resolution outside scope |
| Zalando: delegated identity, consent and policy enforcement | Receipt and task context as possible policy inputs | Integration design only; no broker connection |
| GitHub: deterministic checks within a broader evaluation stack | Reproducible failure fixtures and matching receipts | Local conformance evidence; behavioral benefit not established |

The supplied talks already contain many of these architectural ideas. We have
not established that any company lacks an internal equivalent. The contribution
is a compact, inspectable implementation and shared test surface, not a claim
to have invented handoffs, checkpoints or recovery.

## Public source cross-check, 20 September 2026

- [A2A specification](https://a2a-protocol.org/latest/specification/): tasks and
  artifacts provide transport and lifecycle concepts. RelayReady could travel as
  an artifact profile without replacing those operations.
- [MCP resource specification, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/resources):
  resource identity and read/update facilities support artifact access. A generic
  resource revision token is not defined there; RelayReady uses adapter-supplied
  opaque revision values or explicit content digests.
- [Agent Skills specification](https://agentskills.io/specification): metadata can
  record a release label. [Discovery PR #254](https://github.com/agentskills/agentskills/pull/254)
  proposes digest-based discovery and was open when reviewed; it is not an
  accepted requirement of this contribution.
- [Zalando engineering account](https://engineering.zalando.com/posts/2026/08/agentic-engineering-at-zalando-a-snapshot.html):
  the platform separates delegation, OAuth brokering and token custody. RelayReady
  leaves current authorization with that infrastructure.

These are narrow documentation comparisons. They do not prove absence of features
in any repository or private system. The conference archive is supporting research;
third-party slide files are not included in the distributable contribution.

## Demonstration and proposed pilot

The demonstration follows a staging review interrupted between agents. Matching
observations produce `resume`; revision drift and changed skill bytes produce
`recheck`; an unknown previous effect or unresolved owner decision produces
`escalate`. The application labels its observations as simulated and exposes the
real input artifacts and recorded validator receipts.

A useful next pilot is two independently implemented adapters, each resolving
resource revisions and reconciling prior operations in its own environment. Both
should emit the same decisions for the shared fixtures. Then run paired live tasks
with and without the gate, holding prompts, skills, tool schemas and model settings
as stable as possible. Measure repeated operations, missed changes, task completion,
latency and unnecessary escalations. Publish actual result files, including failures.
This work is proposed; no live adapter or efficacy result is claimed yet.

## Donation readiness

The public [repository](https://github.com/pawelworks/relayready) and
[issue tracker](https://github.com/pawelworks/relayready/issues) are available.
[Publication PR #1](https://github.com/pawelworks/relayready/pull/1) merged at
`c3c91545f6c7584a7f093e8904a7e8d26fc22d1a`, with all twelve hosted platform
jobs passing in [CI run 35541220709](https://github.com/pawelworks/relayready/actions/runs/35541220709).
The public import records the owner's authorized Apache-2.0 contribution-rights
attestation and DCO sign-off. Earlier unsigned website-era commits remain in
separate local deployment history; no retroactive signatures were fabricated.
Publication, private vulnerability reporting and protected CI checks are
established, not pending source-release blockers. They are not an independent
IP audit or permission to transfer project assets.

The owner has confirmed **Pavel Mihai Lucian**, **@pavelpxp500**, affiliation
**PAWELWORKS**, country **Romania**, and **lucian.pavel@pawelworks.com** as the
public contact. He reports being PAWELWORKS's sole owner and worker and supplied
PAWELWORKS S.R.L., a Romanian SRL, represented by Mihai-Lucian Pavel,
Administrator, as the contributor. Those details are owner-supplied, not
independently registry-verified. He explicitly confirmed company authority and
authorized the public application and its conditional project-transfer commitment. The
[application working draft](AAIF_APPLICATION_DRAFT.md),
[asset inventory](AAIF_ASSET_INVENTORY.md) and
[release checklist](RELEASE_CHECKLIST.md) record the remaining decisions.

The technical offer is a draft for community review, and the existing governance
requires review before changing accepted conformance. The frozen 0.1 schema stays
unchanged. The new sidecar identifier remains `0.1-draft` until that process concludes.

The proposed route is **Sandbox consideration**, supported by the
[Sandbox thesis](AAIF_SANDBOX_THESIS.md) and current
[TC lifecycle policy](https://github.com/aaif/technical-committee/blob/main/governance/project-lifecycle-policy.md).
The policy allows a working, permissively licensed implementation with one
active maintainer, documented intent to grow contributors, and a credible
pre-adoption thesis. RelayReady currently has one confirmed human maintainer
and no substantiated production adopters. Production use by two unaffiliated
organizations and multi-organization contribution evidence are future Growth
goals, not claims about the present project or immediate Sandbox intake gates.
The [roadmap](ROADMAP.md) records conditional six- and twelve-month Sandbox
checkpoints. Requested consideration is not acceptance or endorsement.

Under the current [proposal process](https://github.com/aaif/technical-committee/blob/main/project_proposal_process.md),
review is asynchronous by default; a live TC presentation is arranged if a TC
member requests one. Final shared-account and asset-transfer arrangements must
be settled with LF; owner submission approval is not an executed legal agreement.
The [foundation charter](https://github.com/aaif/foundation/blob/main/foundation-charter.pdf),
including section 8 on project trademarks, is part of that review. Any
contribution agreement and LF technical charter must be reviewed in their
actual supplied form. The application is submitted; no agreement has been signed,
account transferred or foundation approval obtained. The
[submission record](AAIF_SUBMISSION_RECORD.md) captures the exact public evidence.

Suggested review request: assess whether this small profile should live as an
independent reference implementation, an A2A extension experiment, or shared
conformance fixtures for existing resource and agent tooling.
