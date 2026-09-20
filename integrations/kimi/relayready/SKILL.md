---
name: relayready
description: Use RelayReady to resume unfinished work from HANDOFF.md only after a checked readback, and write a validated handoff before leaving unfinished work. Use for cross-session or cross-agent task transfer.
---

# RelayReady

When `HANDOFF.md` exists at session start, read it before acting. Produce
`READBACK.yaml`, echoing invariants verbatim and in order, indexing every rejected
approach, rechecking stale facts, and surfacing human-only questions. Run
`relayready readback check HANDOFF.md READBACK.yaml` if available. Show the readback
and wait for human approval before continuing.

Before ending unfinished work, create or update `HANDOFF.md`, retain inherited
invariants and rejected approaches, then run
`relayready lint HANDOFF.md --check-pointers` if available. Never invent check output.
