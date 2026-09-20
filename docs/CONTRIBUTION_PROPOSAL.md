# RelayReady contribution proposal

Prepared for technical discussion with the Agentic AI Foundation community.
Status: local donation candidate; no submission, affiliation, acceptance,
endorsement, ownership transfer or production adoption is claimed.

## Offer

Contribute a small Apache-2.0 implementation of a portable continuation checkpoint:
an immutable handoff, receiver readback, expected state, observations and a
deterministic receipt. The package includes schemas, a local CLI, negative tests,
reproducible fixtures, a presentation website and documented integration boundaries.
The [verification record](VERIFICATION.md) separates observed local results from
external checks that have not been completed.

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

The owner has now confirmed **Pavel Mihai Lucian** for project-side roles and
**lucian.pavel@pawelworks.com** as the public contact. The
[application working draft](AAIF_APPLICATION_DRAFT.md) and
[release checklist](RELEASE_CHECKLIST.md) record the remaining gates. This
updates the earlier placeholder status below; repository publication and
contribution rights are still unresolved.

The technical offer is a draft for community review, and the existing governance
requires review before changing accepted conformance. The frozen 0.1 schema stays
unchanged. The new sidecar identifier remains `0.1-draft` until that process concludes.

Before a formal transfer, the owner and receiving organization must establish
the public repository and issue tracker, maintainer identities, security reporting
route, contribution provenance and sign-offs, trademark/account control, and the
applicable current intake process. The project currently has one maintainer and
no substantiated production adopters. Source history contains unsigned commits
created during the earlier website work; they require provenance review rather
than fabricated personal sign-offs. No signatures, contributor counts or legal
commitments have been invented to fill those gaps.

Suggested review request: assess whether this small profile should live as an
independent reference implementation, an A2A extension experiment, or shared
conformance fixtures for existing resource and agent tooling.
