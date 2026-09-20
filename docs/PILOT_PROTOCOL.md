# Live relay pilot protocol

**Proposed; not executed.** Version 1, 20 September 2026. Coordinator: Pavel
Mihai Lucian, <lucian.pavel@pawelworks.com>. No participant, company or external
maintainer is represented as having agreed to this pilot.

## Question and design

Does a checked receiver readback reduce lost constraints and repeated work when
an unfinished task moves between agent harnesses? Evaluate continuation-gate
failure handling separately from task-completion benefit.

Use the five existing Relay Bench tasks in clean, isolated workspaces. Freeze
the repository revision, task inputs, scoring tests, model identifiers, tool
permissions, prompts and budgets before any run. Use the benchmark's documented
`relay` mode and three arms (`none`, `freeform`, `stafeta`) without relabelling
synthetic runs as live runs. Pair results by task, sender/receiver direction and
repetition index; run each arm from the same clean starting task state.
Run two sender/receiver directions across distinct real harnesses, three arms
and five repetitions per task: 150 planned runs. Counterbalance arm order and
retain failed or timed-out attempts. This small pilot is exploratory, not a
powered claim about all models or production workflows.

The current benchmark executes deterministic mocks only. A real-runner adapter
and trustworthy measurement collection must be implemented and reviewed before
this plan can be executed. Integration instruction files alone are not evidence
of an exercised runtime integration.

## Safety and authorization gate

- Obtain explicit authorization for provider accounts, credentials, spending
  limits and each allowed tool before starting live execution.
- Use disposable fixtures, test accounts and isolated directories; no private
  production data, real payments, deployments or third-party messages.
- Do not expose API keys or session stores in handoffs, logs or result bundles.
- Model output, imported artifacts and tool responses are untrusted data.
- The executor must independently check current authorization and use conditional
  or idempotent writes; a `resume` receipt is not execution permission.
- Stop and preserve evidence on an invariant breach or unintended side effect.

No provider calls or live pilot costs are authorized merely by this document.

## Measurements and evidence

Record task completion against frozen tests, invariant violations, repeated
rejected approaches, ignored stale facts, guessed human answers, elapsed time,
tool failures, token/cost data when actually supplied by the provider, and
recheck/escalation frequency. Unknown cost or model-version data stays unknown.

For each run retain a unique ID, source and input hashes, UTC timestamps,
sender/receiver versions, effective permissions, sanitized transcripts,
workspace diff, handoff/readback artifacts, validator outputs, scoring outputs
and termination reason. An external harness must collect these measurements;
do not trust the agent to assert its own success or write the scoring markers.
Publish redacted artifacts with a manifest. Record redactions and distinguish
recomputed validation from an original observation.

Separately inject resource drift, changed input bytes, an unknown prior effect
and a pending owner decision. Check the expected `recheck`/`escalate` behavior
without permitting an actual unsafe mutation. Include clean cases to measure
unnecessary blocking. Have an independent reviewer inspect all safety failures
and a preselected sample of other runs; no such reviewer is yet appointed.

## Reporting and exit criteria

Report per-task paired outcomes, all run counts and exclusions, missing data,
costs, variability and uncertainty. Do not collapse mock and real results into
one matrix or claim statistical significance from a small exploratory sample.

Exit requires reproducible artifacts, reviewed scoring, no unresolved safety
failure and transparent reporting of negative results. Benefit is a finding to
be measured, not an acceptance condition to engineer into the report. A
successful pilot is not production adoption or foundation acceptance. Preserve
the original product decision gate: if RelayReady fails to outperform freeform
handoffs on the predeclared primary outcomes, pause feature expansion and
reassess the specification and approach. A valid negative experiment is evidence
for that reassessment, not a result to hide or relabel as success.
