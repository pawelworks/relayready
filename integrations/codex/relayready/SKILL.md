---
name: relayready
description: Uses RelayReady to resume unfinished work from HANDOFF.md with a checked readback and writes a validated handoff before leaving unfinished work. Use when HANDOFF.md exists or when transferring work to another agent.
---

# RelayReady

## Resume as an L2 Reader

1. If `HANDOFF.md` exists at session start, read it before acting.
2. Run `relayready readback new HANDOFF.md > READBACK.yaml` when the CLI is available; otherwise author the same 0.1 fields manually.
3. Restate the goal, echo every invariant verbatim and in order, identify all `Do not redo` items by one-based index, recheck stale facts, and surface every human-only question.
4. Run `relayready readback check HANDOFF.md READBACK.yaml` when available.
5. Show the readback and wait for the human to say to proceed. Do not begin task work first.

## Pause as an L1 Writer

Before ending with unfinished work, create or update `HANDOFF.md`. Preserve
inherited invariants and rejected approaches, use evidence markers for state, and
run `relayready lint HANDOFF.md --check-pointers` when available. State honestly when
a check could not run.
