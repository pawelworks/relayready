---
name: relayready
description: Uses RelayReady to resume unfinished work from HANDOFF.md with a checked readback and writes a validated handoff before leaving unfinished work. Use when HANDOFF.md exists or when transferring work to another agent.
---

# RelayReady

## Resume as an L2 Reader

1. Read `HANDOFF.md` before any task action when it exists at session start.
2. Create `READBACK.yaml` with `relayready readback new HANDOFF.md` when available, or manually follow the 0.1 readback schema.
3. Restate the goal, echo every invariant verbatim and in order, enumerate every rejected approach, recheck stale facts, and surface every human-only question.
4. Run `relayready readback check HANDOFF.md READBACK.yaml` when available.
5. Show the complete readback and wait for human approval before task work.

## Pause as an L1 Writer

Before ending unfinished work, create or update `HANDOFF.md`, preserving inherited
invariants and rejected approaches. Run `relayready lint HANDOFF.md --check-pointers`
when available and never claim an unperformed check.
