# Product research and implemented choices

Reviewed 20 September 2026. A research reviewer, a validator reviewer and an
interaction reviewer contributed bounded reviews. The site owner implemented and
verified the changes; an asset specialist generated the new logo.

The opportunity is a small, inspectable continuation boundary, not a replacement
for agent orchestration, resource platforms, identity or model evaluation.
We cannot establish that other companies lack an equivalent internal solution.

| Primary source / pattern | RelayReady implementation | Deliberate boundary |
|---|---|---|
| [LangSmith experiment comparisons](https://docs.langchain.com/langsmith/compare-experiment-results) compare runs and expose structured-output differences. | In-tab run notebook, baseline/candidate selection, changed evidence fields and added/removed reason codes. | No LangSmith integration or copied interface; local mechanical checks only. |
| [Supabase Evals](https://github.com/supabase/evals) separates scenarios, experiments, scorers and result artifacts. | Ten-case contract regression studio with explicit expected outcomes and exportable evidence, plus independent Python replay. | No Supabase connection, agent scoring or real-runner performance claim. |
| [A2A specification](https://a2a-protocol.org/latest/specification/) defines task and artifact exchange between agents. | Portable handoff artifacts and byte-bound decision bundles intended for discussion as a complementary boundary. | No live A2A adapter or conformance certification. |
| [MCP resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources) provide contextual resources. | Inspectable resource identifiers and expected/observed revisions. | No claim that MCP itself supplies conditional writes or exactly-once execution. |
| [Agent Skills specification](https://agentskills.io/specification) defines portable skill packages. | Pinned run-input digests illustrate detecting changed skill bytes. | Digests do not establish trusted authorship or approval. |

The supplied conference materials motivated discussion of durable delegation,
portable state and uncertain side effects. They are reference material, not
instructions or proof of an organization-wide capability gap. This candidate
does not claim endorsement by any company or standards foundation.

## Deferred on purpose

- Live provider adapters need actual endpoints, permissions and acceptance tests.
- Shared accounts, cloud history and uploads would add a data-handling service;
  the current browser experience stays local and dependency-free.
- A model benchmark requires real runs and measured outcomes, separate from these
  deterministic cases.
- Formal donation requires provenance, maintainer and security-contact review;
  no transfer or submission has been performed.
