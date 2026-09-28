# RelayReady: Sandbox thesis

Thesis for AAIF review, 21 September 2026. Requested stage: **Sandbox**.
Submitted in [proposal #44](https://github.com/aaif/project-proposals/issues/44);
not admitted, endorsed or donated. This short thesis accompanies the
[application context](AAIF_APPLICATION_DRAFT.md); it makes no adoption claim.

## Intended users and problem

RelayReady is for developers and platform teams that move unfinished work between
agent harnesses, models or sessions. The first target is an interrupted repository
task: one agent has identified a failing test, ruled out an approach and learned
which files must not change. A receiver needs those constraints, not just a fluent
summary. The same pattern can apply to a document or research task with unresolved
human decisions and facts that must be checked again.

The proposed contribution is a portable, inspectable checkpoint rather than a new
agent runtime. A sender writes an immutable handoff; a receiver returns a readback;
a local checker detects missing invariants, omitted questions and required
rechecks. The experimental Continuation Gate additionally compares declared
resource revisions, pinned input bytes and records of prior effects. Its receipt
requests continuation, rechecking or escalation. It neither grants tool permission
nor establishes that a supplied observation is truthful or still current.

## Why investigate this before adoption?

Our hypothesis is that an explicit receiver acknowledgment, combined with small
deterministic checks, can make continuation failures easier to detect and compare
across harnesses. No causal benefit, time saving or failure-rate reduction has been
demonstrated. A shared negative-fixture set is useful even if evaluation eventually
shows that the format is unnecessary or that a simpler approach performs better.

This is the proposed pre-adoption rationale, not documented external demand. The
project has no substantiated production users, independent pilot or external
maintainer. Conference research informed its design but does not imply interest
or endorsement from the speakers or their employers. We have not established
that another company lacks an equivalent.

RelayReady should complement existing tools. An A2A integration could transport
the artifacts, an MCP integration could supply observations, and project
instructions such as AGENTS.md can describe the readback convention. A goose
recipe and other portable integration instructions are present. These are
integration designs or instruction packages, not verified live adapters or
accepted changes to another project's standard. Frozen `stafeta` and
`stafeta_readback` wire identifiers and the legacy command remain supported.

## Working implementation and evidence

The Apache-2.0 [public source](https://github.com/pawelworks/relayready) includes
the specification, schemas, Python CLI, tests, fixtures and static demonstration
app. The current source baseline is
`c3c91545f6c7584a7f093e8904a7e8d26fc22d1a`, version `0.1.3.dev0`.
[Hosted CI](https://github.com/pawelworks/relayready/actions/runs/35541220709)
passed all 12 platform/Python matrix jobs for that revision. The recorded checks
include 223 Python tests, 23 browser validation vectors, five reproducible gate
fixtures and 150 deterministic mock relay runs. Coverage of 97.38% refers only
to `stafeta.rules`, not the whole product. Mock runs establish checker behavior,
not production safety or model performance. See [verification](VERIFICATION.md).

The [public workbench](https://relayready.org/workbench.html)
labels its simulated observations and supports exporting evidence for local
Python validation. It remains the earlier `0.1.2.dev0` presentation snapshot;
the source revision above contains subsequent validator and packaging fixes.
There is no tagged package release or completed independent security audit.

## Stewardship and proposed experiment

Pavel Mihai Lucian ([pavelpxp500](https://github.com/pavelpxp500)), affiliated
with PAWELWORKS in Romania, is the sole confirmed human maintainer. AI-assisted
implementation is disclosed and is not counted as independent participation.
The [roadmap](ROADMAP.md) proposes recruiting external fixture authors,
reviewers and an additional maintainer through public issues and documented
governance, without appointing people who have not agreed to participate.

The next experiment is two separately implemented adapters, tested against the
same failure fixtures, followed by the [predeclared live pilot](PILOT_PROTOCOL.md).
That pilot compares continuation with and without the gate and reports all
attempted runs, failures, unnecessary escalations, task completion and costs.
Disconfirming results will be published after privacy review rather than replaced
with mock scores. Provider credentials and execution authority remain outside
portable artifacts.

## What would justify Growth?

We would seek Growth on actual, permissioned evidence of production use by two
unaffiliated organizations, sustained contributions spanning two organizations,
named committers and an accepted growth plan. These are future targets, not
current achievements. We plan a six-month checkpoint and aim to apply for Growth
within twelve months of any eventual Sandbox admission. If the evidence does not
support progression, we expect an archival discussion rather than claiming
maturity. Our eventual Impact objective is self-sustaining,
multi-organization stewardship and useful interoperability without fragmenting
existing standards.

The requested initial support is standard project infrastructure, not assumed
funding, marketing, mentorship or security services. The owner authorized the
application and conditional project transfer; actual LF paperwork and shared-account
arrangements remain outstanding in the [asset inventory](AAIF_ASSET_INVENTORY.md).
The applicable
[TC lifecycle policy](https://github.com/aaif/technical-committee/blob/main/governance/project-lifecycle-policy.md)
provides the Sandbox route; only the foundation can decide admission.
