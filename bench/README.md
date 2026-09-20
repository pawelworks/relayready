# Relay Bench

Relay Bench measures whether a fresh receiver completes a task without repeating
dead ends, breaking invariants, trusting stale facts, or guessing human-only
answers. Five fixtures (three code, two knowledge) run in `golden` and `relay`
modes with `none`, `freeform`, and `stafeta` arms.

The zero-cost mock suite exercises five scripted behaviors:

```console
relayready bench verify-mock
relayready bench run-mock --output bench/results/mock-local
```

Mock JSON is useful for CI acceptance but is always excluded from the public
matrix. Generate that matrix only from committed real-runner JSON files:

```console
relayready bench report
```

All external runners are disabled by default. Codex and Claude command flags are
recorded only because their local `--help` was inspected. goose and Kimi have no
command template because their binaries were absent; enable them only after
recording version-specific help evidence. The owner, not this build, runs and
commits real-runner results.
