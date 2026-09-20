# Experimental Continuation Gate

Status: implemented draft `0.1-draft`, for review and interoperability experiments.
It adds optional JSON sidecars; the accepted Stafeta 0.1 handoff and readback
contracts, wire identifiers, CLI alias and conformance levels remain unchanged.

## What the gate contributes

A valid readback acknowledges critical items. It may still report an unverifiable
fact, an unresolved question, or a conflict. Meanwhile, a resource or installed
skill may have changed after the sender stopped. The gate combines those signals
in one reproducible decision and binds the decision to its precise inputs.

```console
relayready gate check HANDOFF.md READBACK.yaml CHECKPOINT.json OBSERVATION.json --json
```

The checker reads four explicit local files once, computes SHA-256 over their
original bytes, validates them, and emits a JSON receipt to stdout. It performs
no network requests, executes no tools, and never fetches evidence references.
The normal evaluation time is current UTC. `--now` supplies a fixed RFC 3339
timestamp for fixture replay; it must not be used to pretend an expired checkpoint
is current in an execution workflow.

## Four inputs, one receipt

| Artifact | Producer and purpose |
|---|---|
| `HANDOFF.md` | Sender's immutable Stafeta 0.1 task state |
| `READBACK.yaml` | Receiver's Stafeta 0.1 acknowledgement |
| `CHECKPOINT.json` | Expected state, bound to the exact handoff and readback |
| `OBSERVATION.json` | Receiver or adapter's observations, bound to the checkpoint |
| `RECEIPT.json` | Checker output binding all four inputs and the evaluation time |

The checkpoint is assembled after the receiver has produced its readback. An
orchestrator or reviewer pins that pair and the expected continuation conditions.
If the pair changes, issue another checkpoint and obtain observations for it.

The bundled schemas are available with `relayready schema checkpoint` and
`relayready schema observation`. Normative draft copies live under `spec/`.

### Checkpoint fields

Every field is required. Unknown keys, duplicate JSON keys and duplicate logical
identifiers are rejected.

| Field | Meaning |
|---|---|
| `relayready_checkpoint` | Exact draft identifier `0.1-draft` |
| `task_id` | ULID matching the handoff |
| `created`, `expires_at` | RFC 3339 timestamps with explicit offsets |
| `handoff_sha256`, `readback_sha256` | `sha256:` plus lowercase hex of raw bytes |
| `resources` | List of `{id, revision}` expected resource snapshots |
| `effects` | List of `{id, idempotency_key}` previous operation attempts |
| `run_inputs` | List of `{name, digest}` pinned skill, prompt, tool, evidence or policy bytes |

Arrays may be empty when that category is outside the declared task scope.
An omitted category is an input error. The checker cannot discover undeclared
resources or operations. Adapters must construct a complete checkpoint for their task.

Resource IDs must identify both the provider and the resource. Revision strings
are opaque and compared exactly within that identity. A provider ETag is not
assumed to be a content digest. The draft does not add a revision method to MCP.
Run-input names identify the input and may include a release label; the digest
controls byte identity even when that label remains unchanged. Model settings
can be pinned as serialized input bytes, but this does not make model output deterministic.

### Observation fields

| Field | Meaning |
|---|---|
| `relayready_observation` | Exact draft identifier `0.1-draft` |
| `checkpoint_sha256` | SHA-256 of the checkpoint's exact bytes |
| `observed_at` | RFC 3339 timestamp of this observation set |
| `resources` | `{id, revision}`; `null` means not known |
| `effects` | `{id, status, evidence}`; status is `not_applied`, `applied` or `unknown` |
| `run_inputs` | `{name, digest}`; `null` means not known |

Each expected identifier must be accounted for once. Unexpected identifiers
escalate for review. Missing expected observations require rechecking.
`not_applied` needs a non-empty evidence reference. The checker records that
reference but cannot authenticate it or independently verify its conclusion.
`applied` and `unknown` both escalate: the caller must reconcile completed work
and issue a successor before attempting a retry. An idempotency key is a reference
to executor-side behavior, not a lock or deduplication service supplied by RelayReady.

## Decision semantics

| Decision | Meaning | Exit code |
|---|---|---|
| `resume` | All implemented checks passed for the declared inputs and time | `0` |
| `recheck` | A revision, digest, time window or fact needs a new observation | `1` |
| `escalate` | A binding, contract, conflict, question or previous effect needs resolution | `1` |
| Input error | Files could not be parsed or fail the sidecar schemas | `2` |

Escalation takes priority over rechecking. Every reason is retained. A parsed
handoff/readback that fails its contract, or a hash mismatch, escalates. Unreadable
files or malformed YAML/JSON syntax instead produce an input error. Conflicts and unresolved human
questions escalate even when mechanically acknowledged. Changed or unverifiable
readback facts require rechecking. Duplicate readback recheck indices escalate.
The checkpoint must have an expiry later than its creation. For continuation,
`created <= observed_at <= evaluated_at < expires_at` must hold.
Artifact creation must also follow `handoff.created <= readback.created <=
checkpoint.created`. Invalid timestamps or reversed artifact ordering escalate;
future records cannot authorize continuation. Calendar dates are checked directly,
without relying on optional JSON Schema format packages.

The receipt includes `relayready_receipt`, `task_id`, `evaluated_at`, `decision`,
ordered `{code, message}` reasons and the four input digests under `bindings`.
The same files and evaluation time reproduce the same receipt.

## Trust and execution boundary

A receipt demonstrates consistency of supplied records. It does not establish
source authenticity, semantic understanding, execution permission or actual
external truth. A SHA-256 binding is not a signature. Human decisions and
authorization remain with the owner and their policy system. No tokens or shared
credentials belong in these artifacts.

State can change immediately after validation. Before a mutation, the executor
must independently check live authority and apply provider-specific conditional
writes, resource versions or locks as appropriate. The gate does not perform
compensation or promise exactly-once effects. Its conservative response to an
already-applied or uncertain operation is escalation.

## Reproduce the presentation

From the repository root:

```console
python tools/generate_continuation_fixtures.py --check
relayready gate check examples/continuation/revision-drift/HANDOFF.md examples/continuation/revision-drift/READBACK.yaml examples/continuation/revision-drift/CHECKPOINT.json examples/continuation/revision-drift/OBSERVATION.json --now 2026-09-20T12:05:00Z --json
```

The second command intentionally exits `1` with a `recheck` receipt. The five
fixtures cover matching observations, resource drift, an uncertain previous
effect, changed skill bytes under one label, and an unresolved human decision.
They use simulated observations. The website replays the actual recorded local
validator receipts; it does not run a model or a Python service in the browser.
