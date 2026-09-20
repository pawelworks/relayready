# RelayReady

RelayReady is a vendor-neutral contract for handing an unfinished task from one AI agent harness to another. A structured `HANDOFF.md` records critical state, and a checked readback makes the receiver acknowledge invariants, stale facts, dead ends, and open questions before acting. Relay Bench measures whether that process improves completion rather than merely producing well-formed files.

RelayReady is deterministic: its checking path makes no LLM calls, reads no private session stores, and requires no hosted service.

The public name changed from **Stafeta** to **RelayReady** before release. The
accepted 0.1 wire keys (`stafeta`, `stafeta_readback`), Python module, legacy CLI,
and benchmark arm remain unchanged for compatibility. New usage should prefer
the `relayready` command and `relayready` Python package.

## Status

Early. The project has one maintainer and no production adopters yet. Milestones M0 through M5 implement the version 0.1 contracts, deterministic CLI, checked readbacks, invariant chains, portable agent integrations, and Relay Bench. The M4 owner-run cross-vendor exercise and M5 real-runner comparison remain explicit external gates.

Project owner and lead maintainer: **Pavel Mihai Lucian**,
[@pavelpxp500](https://github.com/pavelpxp500), affiliated with PAWELWORKS, Romania.
Contact: [lucian.pavel@pawelworks.com](mailto:lucian.pavel@pawelworks.com).
Try the [public demonstration](https://relayready.org/).
Source: [pawelworks/relayready](https://github.com/pawelworks/relayready).
The reviewed, AI-assisted source import is public with the owner's authorized DCO
sign-off. See [GitHub Actions](https://github.com/pawelworks/relayready/actions)
and the [source-publication record](docs/SOURCE_PUBLICATION_REVIEW.md).

See the [roadmap](docs/ROADMAP.md), [AAIF application draft](docs/AAIF_APPLICATION_DRAFT.md),
[Sandbox thesis](docs/AAIF_SANDBOX_THESIS.md) and
[release checklist](docs/RELEASE_CHECKLIST.md). Sandbox is the proposed entry
stage, not a status already held. [AAIF proposal #44](https://github.com/aaif/project-proposals/issues/44)
has been submitted; no acceptance, endorsement or completed donation has occurred.
See the [submission record](docs/AAIF_SUBMISSION_RECORD.md).

## Interactive workbench

Serve `out/` locally and open `workbench.html`. Edit simulated observations,
compare up to 20 in-tab runs, run ten regression cases, and export exact-byte
evidence bundles. The browser checks the supplied example contracts; the Python
CLI independently validates exported artifacts:

```console
relayready gate bundle experiment.json --replay --json
```

Omit `--replay` to check against the current clock. Neither mode authorizes
execution. See [Workbench](docs/WORKBENCH.md) for scope, privacy and reproduction,
and [Product research](docs/PRODUCT_RESEARCH.md) for the feature rationale.

## The 60-second flow

Write a handoff:

```markdown
---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PG"
created: "2026-09-20T16:00:00+03:00"
task: "Finish the import fix"
status: in_progress
profile: code
parent: null
sender:
  agent: "example-cli"
  vendor: "example"
  model: null
lang: "en"
---

## Goal

Finish the import fix without changing the database schema.

## Done means

- [ ] The import test passes.

## Invariants

- Never run deploy scripts.

## State

- The failing case is in `tests/test_import.py`. [verified 2026-09-20: reproduced locally]

## Done so far

- Added a regression test in `tests/test_import.py`.

## Do not redo

- Do not retry CSV dialect sniffing; it broke quoted newlines.

## Next steps

1. Fix the row parser.

## Open questions

- None.

## Pointers

- `tests/test_import.py`

## Environment

- Branch: `fix/import`
- Run: `pytest tests/test_import.py`
```

The receiver emits a readback before touching the task:

```yaml
stafeta_readback: "0.1"
handoff_id: "01K5M85YQ6E6XM1YSE7YB7A9PG"
created: "2026-09-20T16:05:00+03:00"
receiver:
  agent: "other-cli"
  vendor: "other"
  model: null
goal_restated: "Repair the row parser while preserving the current schema."
invariants_hash: "sha256:f3ef86e95eb441cb51d2f99602ab322f6accb1c6e875e934457851518e552527"
invariants_echo:
  - "Never run deploy scripts."
will_not_redo: [1]
rechecked: []
conflicts: []
questions_for_human: []
first_action: "Inspect the failing regression test and row parser."
```

`relayready lint HANDOFF.md` rejects an unsafe or malformed handoff. `relayready readback check HANDOFF.md READBACK.yaml` rejects a readback that omits an invariant, a rejected approach, a required recheck, or a human-only question. `relayready chain check handoffs/` detects missing parents, cycles, and silently dropped invariants.

The M2 commands are documented in [`docs/CLI.md`](docs/CLI.md).

## Experimental continuation checkpoint

The optional [Continuation Gate](docs/CONTINUATION_GATE.md) adds a draft checkpoint
and observation pair without changing the accepted 0.1 wire format. It binds the
exact handoff/readback bytes, checks declared resource revisions and pinned input
digests, and emits `resume`, `recheck`, or `escalate`. Unknown or already-applied
effects prevent a blind retry. A passing receipt checks supplied records; the
executor remains responsible for current authorization and conditional writes.

```console
relayready gate check HANDOFF.md READBACK.yaml CHECKPOINT.json OBSERVATION.json --json
python tools/generate_continuation_fixtures.py --check
```

Five simulated scenarios and their real local validator receipts are in
[`examples/continuation/`](examples/continuation/). The static presentation app
under `out/` replays those receipts. The [contribution proposal](docs/CONTRIBUTION_PROPOSAL.md)
and [integration profile](docs/INTEGRATION_PROFILE.md) explain how this draft can
be reviewed alongside A2A, MCP, resource systems and identity brokers. No live
adapter, standards acceptance, institutional endorsement or unique invention is claimed.

## Agent integrations

Portable project instructions, native Codex/Claude Code/Kimi skills, a goose
recipe, and no-filesystem chat prompts live under [`integrations/`](integrations/).
Each package states what was verified and what remains an external runtime or
owner acceptance check.

## Relay Bench

Five deterministic fixtures cover three code tasks and two knowledge tasks.
`relayready bench verify-mock` runs 150 zero-cost combinations and proves that the
perfect mock is clean while dead-end repetition, invariant breakage, ignored
stale facts, and guessed questions each move their matching metric. Mock results
are never rendered in the public matrix; real-runner execution is owner-only.

## Conformance

- **L1 Writer:** produces handoffs that pass `relayready lint` with no errors.
- **L2 Reader:** produces readbacks that pass `relayready readback check`.
- **L3 Relay:** a sender and receiver pair with published Relay Bench results.

## Related work

RelayReady is designed to complement existing handoff tools, not displace them. [`chentaymane/handOff`](https://github.com/chentaymane/handOff) generates structured handoffs across coding tools. [`czri23333/agenthandoff`](https://github.com/czri23333/agenthandoff) extracts session state into deterministic bundles. [`homeofe/AAHP`](https://github.com/homeofe/AAHP) defines a git-oriented directory protocol, [`open-grove/handoff`](https://github.com/open-grove/handoff) supports redacted sharing, and [`StoneReaper/openhandoff`](https://github.com/StoneReaper/openhandoff) explores an MCP-backed context format. RelayReady focuses on receiver readback and measured relay outcomes while keeping compatibility with pre-existing `HANDOFF.md` files.

## Relay matrix

See [`docs/matrix.md`](docs/matrix.md). Until real result files exist, every cell is reported as `not run`.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Contributions require a Developer Certificate of Origin sign-off.

## License

Apache-2.0.
