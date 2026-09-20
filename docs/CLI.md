# CLI core

M2 provides deterministic local commands and makes no network calls.

`relayready` is the primary command. `stafeta` remains an equivalent 0.1
compatibility alias.

## Exit codes

| Code | Meaning |
|---|---|
| `0` | The command succeeded; lint may contain warnings only. |
| `1` | A check failed, or the continuation gate requires recheck/escalation. |
| `2` | Usage, input, or filesystem failure. |

Every command accepts `--json`. For `schema`, the normal result is already JSON.

## Create a handoff

```console
relayready init --profile code
relayready init --from HANDOFF.md
```

A fresh code handoff records available Git facts and strips credentials, query strings, and fragments from remote URLs. A successor archives its source as `handoffs/<id>.md`, generates a new ULID, sets `parent`, and carries Invariants plus unresolved Open questions forward.

## Lint

```console
relayready lint HANDOFF.md
relayready lint HANDOFF.md --now 2026-09-20 --check-pointers
relayready lint legacy.md --compat --json
```

Human output is grouped by rule id and includes source lines when available. `--check-pointers` enables S013 filesystem and hash checks; it is off by default because receiver environments may not contain the referenced files.

## Hash invariants

```console
relayready hash HANDOFF.md
```

The output follows specification section 8.1 exactly.

## Print schemas

```console
relayready schema handoff
relayready schema readback
```

The bundled schemas are JSON equivalents of the normative copies under `spec/`.

## Create and check a readback

```console
relayready readback new HANDOFF.md > READBACK.yaml
relayready readback check HANDOFF.md READBACK.yaml
relayready readback check HANDOFF.md --from-text reply.md
```

`new` pre-fills the handoff id, invariant echo and hash, rejected-work indices, required rechecks, human questions, and first action. `check` enforces every mechanical acknowledgment from specification section 7. `--from-text` extracts the first fenced YAML block whose first key is `stafeta_readback`.

Goal restatements receive a warning when their case-folded word-token Jaccard overlap with Goal exceeds `0.80`. The check cannot prove semantic understanding.

## Check a handoff chain

```console
relayready chain check handoffs/
```

The command reports duplicate ids, missing parents, cycles, and invariants dropped without a human waiver. Waivers use the form `<invariant> [waived by <human handle> on <YYYY-MM-DD>]`.

## Evaluate a continuation checkpoint

```console
relayready gate check HANDOFF.md READBACK.yaml CHECKPOINT.json OBSERVATION.json --json
relayready schema checkpoint
relayready schema observation
```

This optional experimental command emits a receipt bound to all four input files.
It exits `0` for `resume`, `1` for `recheck` or `escalate`, and `2` for malformed
input. `--now 2026-09-20T12:05:00Z` supports deterministic fixture replay; normal
operation uses current UTC. See [the draft profile](CONTINUATION_GATE.md) for
decision rules and the trust boundary. The `stafeta` alias supports the same command.

## Validate an exported workbench bundle

```console
relayready gate bundle experiment.json --json
relayready gate bundle experiment.json --replay --json
```

The default uses current UTC. Historical replay explicitly uses the exported clock,
not current readiness. The full validator ignores claimed browser assessments and
checks the four exact artifact strings independently. `--now` and `--replay` are
mutually exclusive. The legacy `stafeta` command supports the same options.

## Run Relay Bench

```console
relayready bench verify-mock
relayready bench run-mock --output bench/results/mock-local
relayready bench report
```

`verify-mock` runs all five fixtures, two modes, three arms, and five scripted
behaviors in a temporary directory. It succeeds only when the perfect behavior
is clean and each failure changes its matching deterministic metric.

`run-mock` writes one JSON result per run for inspection. `report` reads result
JSON files and regenerates `docs/matrix.md`; it excludes every result whose
runner is `mock`. External runner commands are disabled by default in
`bench/runners.toml`, and real runs are reserved for the owner gate.
