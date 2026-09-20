# Proposed continuation integration profile

This is an implementation guide for a draft extension. No live integration with
A2A, MCP, an identity broker or a skill registry is claimed.

## Responsibilities

| Component | Responsibility |
|---|---|
| Sender | Write the task contract and references; disclose interrupted operations |
| Receiver | Produce the checked readback and request observations |
| Adapter/orchestrator | Pin the accepted pair, resolve revisions and reconcile effects |
| RelayReady gate | Compare explicit local inputs and emit a deterministic receipt |
| Policy/executor | Verify authority, prevent conflicting writes and record actual effects |

## Integration sequence

1. Store the sender's handoff and receiver's readback as immutable artifacts.
2. Build a checkpoint with exact file hashes, scoped resource identities, expected
   provider revisions, operation IDs/idempotency keys and pinned input digests.
3. Fetch the relevant current state through existing provider clients. Observe all
   declared resources, run inputs and prior operations. Bind the observation file
   to the exact checkpoint digest. Record a real reconciliation reference.
4. Call `relayready gate check` and retain the receipt with its four input files.
5. On `recheck`, obtain new evidence and re-evaluate or issue a successor. On
   `escalate`, reconcile prior effects, resolve the task conflict or obtain the
   human decision; then issue a successor. Do not translate either into permission.
6. On `resume`, the executor still verifies current authority and enforces the
   appropriate revision condition at the write boundary. Record the observed
   result before the next handoff.

## A2A artifact experiment

Carry the files or references in an A2A artifact using existing protocol mechanisms.
Keep RelayReady's handoff ULID distinct from the orchestrator's A2A task ID. The
adapter stores their mapping. A RelayReady receipt does not complete an A2A task
or alter A2A state by itself. No extension URI is registered or fabricated here.

## MCP resource experiment

Use existing resource URIs for the artifacts. For business resources, obtain the
revision through a provider-specific response or hash the relevant fetched content.
Document the namespace and meaning of each revision. MCP resource notifications
may trigger recollection, but notification delivery is not proof of freshness.
RelayReady does not invent a standard MCP revision method or filesystem API.

## Skills and reproducible inputs

Resolve a skill with the installation mechanism already in use. Hash the exact
installed artifact or an adapter-defined deterministic bundle of its files. Pin
the same byte representation at observation time. Also pin prompt templates,
tool schemas, policy documents and evidence manifests when relevant. Do not put
credentials in the bundle. A package label can identify a release but cannot
substitute for a digest, and neither proves the quality of model behavior.

## Identity and policy

An identity broker can receive an opaque receipt reference and application-selected
task context as policy inputs. The draft does not exchange tokens, approve grants,
verify identity assertions or implement ID-JAG. A receipt is not a bearer capability.
Avoid accepting policy inputs from an untrusted sender without independent checks.

## Acceptance criteria for a future adapter

- Reproduces the local fixture decisions at the published evaluation time.
- Demonstrates resource scope isolation and provider-defined revision comparisons.
- Shows that both resource changes and revoked authority prevent a mutation.
- Reconciles an interrupted operation before a retry and records its actual outcome.
- Documents observation provenance, clock assumptions and undeclared-state limits.
- Publishes live evidence separately from simulated fixtures.
