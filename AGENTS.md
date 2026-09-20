# Agent instructions

## RelayReady protocol

If `HANDOFF.md` exists at session start, read it before acting. Produce a readback that follows `spec/SPEC.md`; if the CLI is available, run `relayready readback check HANDOFF.md READBACK.yaml`. Show the readback to the human and wait for acknowledgment before continuing the handed-off task.

Before ending a session with unfinished work, write or update `HANDOFF.md` and run `relayready lint HANDOFF.md` when the CLI is available. Once a readback references a handoff, never edit that issued handoff; archive it and create a successor.

Never invent evidence. Do not claim tests, adoption, benchmark results, or external verification without an inspectable source.

## Development commands

```console
ruff check .
mypy --strict
pytest
```
