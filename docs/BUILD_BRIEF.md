# Stafeta: build brief for Codex

Version of this brief: 1.1, 20 September 2026 (1.1 adds: harness terminology, immutable handoffs, pointer hashes, optional `by` in status tags, optional Preferences section, three more items on the later list). Owner: Lucian Pavel.
Place this file in the repository at `docs/BUILD_BRIEF.md`. It is the single source of truth for the first build. Where this brief and your own judgment disagree, follow the brief and record the disagreement in `docs/DECISIONS.md`.

---

## 0. How to work from this brief

1. Read the whole brief before writing anything.
2. Work milestone by milestone (section 11). At the end of each milestone, stop, write a `HANDOFF.md` for the repository in the Stafeta format you are building, and report. Do not start the next milestone without being told to. The project is developed through its own format from day one.
3. Never invent evidence. No adoption claims, no benchmark numbers, no badges for things that do not exist. A cell with no result file behind it says `not run`. It is never `0`, never an estimate.
4. When you need a fact about an external tool (a CLI flag, a file location, an API), read its `--help` or official docs in the session. Do not rely on memory, and do not rely on this brief for such flags: the author of this brief could not verify them.
5. Permissive dependencies only (MIT, BSD, Apache-2.0, ISC, PSF). Record every dependency and its license in `THIRD_PARTY_LICENSES.md` as you add it.
6. Seed `42` for anything sampled or randomized.

---

## 1. What Stafeta is

**Stafeta** (Romanian *ștafetă*, the baton in a relay race) is a vendor-neutral contract for handing an unfinished task from one AI agent to another, across vendors, plus the tools that check the contract and a benchmark that measures whether it works.

It has three parts:

| Part | What it is |
|---|---|
| **Spec** | What a handoff file must contain, what it must never contain, and what the receiving agent must send back before it acts (the *readback*). |
| **CLI** (`stafeta`) | Deterministic linter and checker for handoffs, readbacks and chains of handoffs. No LLM calls. |
| **Relay Bench** | A harness that starts a task with agent A, hands it through a file to agent B, and scores B with deterministic graders. It produces a vendor-by-vendor matrix. |

The file the spec governs is named **`HANDOFF.md`**. That name is already the de facto convention in existing tools, so Stafeta standardizes it instead of competing with it.

### Terminology: harness, not model

Working state lives in the **harness** (Codex CLI, Claude Code, goose, Kimi CLI, a chat application), not in the model. The same harness can run different models and the same model runs in different harnesses. Stafeta moves a task between harnesses. Wherever this brief says "agent" or "vendor", the precise unit is the pair *(harness, model)*: record both whenever both are known, and never guess the model.

### The one-sentence pitch

Everyone has a handoff generator; nobody can show that the receiver understood. Stafeta adds the readback and the measurement.

---

## 2. Why it exists (context you need for design decisions)

The owner moves real work between Claude, Codex, Kimi and Grok by hand, using a written handoff document pasted at the start of a new conversation. Much of that work is not coding: research, analysis, reporting. Lessons from that practice drive the spec:

- A handoff fails silently. The receiver says "got it" and then redoes finished work, re-asks answered questions, or breaks a standing rule. The sender never finds out until the damage is visible.
- Standing rules ("never execute X", "never modify Y") are the first thing to get lost when a task crosses vendors.
- Facts go stale between sessions. A figure that was true on Tuesday gets repeated as current on Friday.
- Relative time ("yesterday", "last session") is meaningless to the receiver.
- A handoff that is a transcript dump is worse than none.

The readback idea is borrowed from aviation and clinical handover practice: the receiver repeats the critical items back, and the repeat is checked, before anything is done.

### Landscape (checked 20 Sep 2026; treat as provisional)

The GitHub topic `context-handoff` lists about 31 repositories. Almost all have 0 to 3 stars; the largest seen had 88. There is no incumbent. What exists:

| Project | What it does | What it lacks for our purpose |
|---|---|---|
| `chentaymane/handOff` | Skill that writes a sectioned `HANDOFF.md` for Claude Code, Codex, Copilot and others; context-threshold hooks. | No schema, no validator, no receiver acknowledgment, no measurement. |
| `czri23333/agenthandoff` | Extracts session state from the local storage of ~21 coding CLIs into a bundle; JSON Schema; deterministic output; contract tests. | Generator-side only. Tests prove the bundle is well-formed, not that a receiver resumes correctly. |
| `homeofe/AAHP` | Directory protocol (`.ai/handoff/` with MANIFEST, STATUS, TRUST with TTLs, verify gates, git hooks). | Multi-file and git-centric; no readback; no cross-agent interoperability tests. |
| `open-grove/handoff` | CLI plus hosted sharing of redacted handoffs. | A service, not a contract; no readback; no measurement. |
| `StoneReaper/openhandoff` | `CONTEXT.md` + `context.json` with an MCP server. | Early; no readback; no measurement. |

The owner's separate research on large agent platforms points the same way, as inference from their documentation and not from their code: openJiuwen documents four memory levels and three swarm memory types but no portable export toward other harnesses; the A2A protocol treats agents as opaque, with memory hidden, and defines communication between running agents, not the state of a task at rest. Nothing in the AAIF project list or its open proposals, as far as titles and the four proposals read in detail show, covers task state at rest.

Conclusions that bind the design:

- **Do not build another session extractor or another generator-only tool.** That space is full.
- **Stay compatible.** Existing `HANDOFF.md` files should lint with warnings, not be rejected wholesale. Later milestones add importers for other formats so the bench can score them too. Their authors are potential contributors and co-maintainers, not rivals. Write the README accordingly: respectful, factual, no disparagement.
- **The differentiators are the readback and the Relay Bench.** Everything else is table stakes.
- **Work outside git too.** Every prior tool assumes a coding CLI inside a repository. Stafeta must also work when the "agents" are chat surfaces and the human is the transport (copy and paste). Git information is an optional profile, never required.

### Where the project is headed

The intended home is the Agentic AI Foundation (Linux Foundation), as a sibling convention to AGENTS.md. Its intake requires, among other things: an OSI-approved permissive license, a public repo with CI and release automation, a public issue tracker, a website, documented governance, at least two core maintainers from different organizations, at least ten contributors, production use in at least two organizations, and transfer of the project name and accounts to the Linux Foundation on acceptance. None of the people-related items exist yet. Consequences for you:

- Neutral branding only. No company names in the code, docs, package metadata or copyright lines. Copyright holder is "The Stafeta Authors".
- Design for many small contributions: one rule per file in the linter, one fixture per directory in the bench, one runner per config entry.
- Governance and security files exist from the first commit (section 9).

---

## 3. Non-goals for v0.1

- No LLM calls anywhere in the CLI's checking path. Deterministic only.
- No reading of vendors' private session stores.
- No hosted service, no telemetry, no network calls from `lint`, `readback` or `chain`.
- No memory system. A handoff is a brief for one task at one moment, not a long-term store.
- No orchestration framework. Stafeta does not launch agents except inside the bench.

---

## 4. Spec v0.1: `HANDOFF.md`

Write the normative text in `spec/SPEC.md` using RFC 2119 keywords (MUST, SHOULD, MAY). Provide `spec/handoff.schema.json` (JSON Schema 2020-12) for the front matter, and `spec/readback.schema.json` for the readback. The spec carries its own version, independent of the CLI's.

### 4.1 Container

- One UTF-8 Markdown file named `HANDOFF.md`. One task per file.
- YAML front matter, then H2 sections with **fixed English headings** in the order below. Content under the headings may be in any language.
- **Immutable once issued.** A handoff is never edited after a readback references its `id`. New state means a new file with a new `id` and `parent` set to the old one. Convention: `HANDOFF.md` is always the latest; earlier ones are moved to `handoffs/<id>.md`. `stafeta init --from HANDOFF.md` archives the current file and starts the successor with `parent`, `Invariants` and unresolved `Open questions` carried over. This is how two harnesses working in turn avoid overwriting each other silently: they never write the same file.
- Body length: SHOULD be under 1,500 words; MUST be under 4,000. A handoff is a brief, not a transcript.

### 4.2 Front matter

```yaml
---
stafeta: "0.1"                 # spec version, required
id: "01J8ZK3V9Q4M7T2X5B6C8D0EFG"   # ULID, required, unique per handoff
created: "2026-09-20T14:05:00+03:00" # RFC 3339 with offset, required
task: "Short task title"       # required
status: in_progress            # in_progress | blocked | ready_for_review | done
profile: knowledge             # code | knowledge ; code adds the Environment section
parent: null                   # id of the previous handoff in the chain, or null
sender:
  agent: "codex-cli"           # free text, required
  vendor: "openai"             # free text, required
  model: null                  # optional; omit or null if not known. Never guess.
  operator: "human handle"     # optional
recheck_after: "2026-09-27"    # optional date after which every State fact is treated as [recheck]
lang: "en"                     # language of the content, BCP 47
---
```

### 4.3 Sections

Required, in this order:

1. **`## Goal`**: one paragraph. What the task is for.
2. **`## Done means`**: acceptance criteria as a checklist. The receiver knows when to stop.
3. **`## Invariants`**: standing rules the receiver MUST NOT break, one per list item, imperative, self-contained. Example: `- Never run deploy scripts.` May be the single item `- None.` Invariants are carried verbatim along a chain (4.6).
4. **`## State`**: facts the receiver needs, one per list item, each ending in exactly one status tag:
   - `[verified 2026-09-20: how it was verified]`, or with the optional author, `[verified 2026-09-20 by codex-cli: how it was verified]`. The author matters in a chain, where a fact may have been verified three handoffs ago by a different harness.
   - `[unverified]`
   - `[recheck]`: the receiver MUST re-verify before relying on it.
5. **`## Done so far`**: completed work, each item with its evidence (a test name, a file, a commit).
6. **`## Do not redo`**: dead ends and approaches already tried and rejected, each with the reason.
7. **`## Next steps`**: ordered list, at most 7 items, first item is the very next action.
8. **`## Open questions`**: questions only the human can answer. The receiver MUST NOT guess these. May be `- None.`
9. **`## Pointers`**: paths, URLs, commands. References, not contents. A pointer to a file MAY end in `[sha256:<hex> as of 2026-09-20]` so the receiver can tell that a support file changed since the handoff was written.

Optional, after the required ones: `## Preferences` (soft working preferences of the human that bear on this task, such as output language or format; not hashed, not binding like Invariants, and limited to what this task needs, since a handoff transfers a task and not everything a harness knows about its user), `## Decisions` (choice and rationale), `## Environment` (required when `profile: code`: branch, commit, uncommitted files, how to run and test), `## Glossary`.

### 4.4 Content rules (each one is a lint rule)

| Rule id | Level | Rule |
|---|---|---|
| `S001` | error | Front matter validates against the schema. |
| `S002` | error | Required sections present, correctly named, in order. |
| `S003` | error | Every `State` item ends in exactly one valid status tag. |
| `S004` | error | No secrets: API keys, bearer tokens, private keys, passwords in URLs, `.env`-style assignments with secret-looking names. Pattern-based; list the patterns in `stafeta/rules/secrets.py` and document the false-negative risk plainly. |
| `S005` | error | No relative time expressions in `State`, `Done so far`, `Next steps` ("yesterday", "last week", "earlier today", "recently"). Word lists per language in data files; ship `en` and `ro`. |
| `S006` | error | Body under the hard word limit. |
| `S007` | warning | Body over the soft word limit. |
| `S008` | warning | A number in `State` tagged `[unverified]` is phrased as certain. Certainty word list per language. |
| `S009` | warning | `Next steps` has more than 7 items or is empty while status is `in_progress`. |
| `S010` | warning | Fenced block longer than 40 lines (likely pasted transcript or file contents). |
| `S011` | error | `profile: code` without an `Environment` section. |
| `S012` | warning | `recheck_after` is in the past relative to `--now` (defaults to the current date). |
| `S013` | warning | With `--check-pointers`: a local file pointer carries a hash that no longer matches the file, or points to a file that does not exist. Off by default, because the linter may run where the files are absent. |

Each rule lives in its own module with its own tests and a documentation page generated from its docstring. Unknown extra sections are allowed and ignored. Files without front matter (for example from other tools) are linted in `--compat` mode, where `S001` becomes a warning.

### 4.5 The readback

Before acting on a handoff, the receiver MUST produce a readback and the readback MUST pass `stafeta readback check`. The readback is a YAML document, either in a file `READBACK.yaml` next to the handoff or as a fenced `yaml` block in a chat reply (the CLI accepts both; `--from-text` extracts the first fenced block whose first key is `stafeta_readback`).

```yaml
stafeta_readback: "0.1"
handoff_id: "01J8ZK3V9Q4M7T2X5B6C8D0EFG"
created: "2026-09-21T09:12:00+03:00"
receiver:
  agent: "kimi-cli"
  vendor: "moonshot"
  model: null
goal_restated: "One sentence in the receiver's own words."
invariants_hash: "sha256:…"      # see 4.6
invariants_echo:                 # verbatim copies, same order
  - "Never run deploy scripts."
will_not_redo:                   # one entry per item in Do not redo, by index
  - 1
  - 2
rechecked:                       # one entry per [recheck] State item, by index
  - item: 3
    result: changed              # confirmed | changed | could_not_verify
    note: "File now has 14 rows, handoff said 12."
conflicts:                       # differences between the handoff and what the receiver observes
  - "Handoff says branch feature/x; working tree is on main."
questions_for_human:             # must include every Open question, may add more
  - "Which date range should the report cover?"
first_action: "Matches or justifies deviation from Next steps item 1."
```

`stafeta readback check HANDOFF.md READBACK.yaml` fails when: the id does not match; the invariants hash or echo differs; any `Do not redo` index is missing from `will_not_redo`; any `[recheck]` item has no `rechecked` entry; any `Open questions` item is absent from `questions_for_human`; `first_action` is empty. It warns when `goal_restated` is a near-verbatim copy of `Goal` (token overlap above a documented threshold), because copying is not restating.

What the check cannot do, and the spec must say so: it cannot prove the restated goal is correct. It proves the receiver addressed every critical item. Semantic correctness is what the Relay Bench measures.

### 4.6 Invariants hash and chains

- Normalize each invariant: Unicode NFC, trim, collapse internal whitespace to one space, strip the leading list marker. Join with `\n`. SHA-256, hex, prefixed `sha256:`. Put test vectors in the spec.
- When a handoff has a `parent`, its `Invariants` MUST include every invariant of the parent, verbatim. An invariant may be dropped only with an entry under an optional `## Waived invariants` section stating the invariant text, who waived it (a human handle) and the date. `stafeta chain check <dir>` walks a directory of handoffs, rebuilds the chain from `parent` ids, and reports dropped invariants, missing parents and cycles.

### 4.7 Conformance levels

- **L1 Writer**: an agent or tool that produces files passing `stafeta lint` with no errors.
- **L2 Reader**: an agent or tool that produces readbacks passing `stafeta readback check`.
- **L3 Relay**: a sender and receiver pair with published Relay Bench results.

---

## 5. CLI

- Python 3.11+, package name `stafeta`, console script `stafeta`. `src/` layout, `pyproject.toml`, type hints, `ruff` and `mypy --strict` clean.
- Keep runtime dependencies minimal. Expected: a YAML parser, a JSON Schema validator, a Markdown tokenizer, a ULID helper (or implement ULID in ~30 lines). Justify anything more in `docs/DECISIONS.md`.
- Every command supports `--json` for machine output and returns exit code `0` ok, `1` errors found, `2` usage or I/O problem.

| Command | Behavior |
|---|---|
| `stafeta init [--profile code\|knowledge] [--from HANDOFF.md]` | With `--from`, archive the given handoff to `handoffs/<id>.md` and start its successor (4.1). Otherwise write a skeleton `HANDOFF.md` with a fresh ULID and the current timestamp. With `--profile code` inside a git repo, fill `Environment` from `git`, with credentials stripped from remote URLs. |
| `stafeta lint [FILE] [--compat] [--now DATE]` | Run all rules. Human output groups by rule id with line numbers. |
| `stafeta readback new HANDOFF.md` | Emit a readback skeleton pre-filled with the id, invariants echo and hash, and empty slots for every index that must be addressed. |
| `stafeta readback check HANDOFF.md READBACK.yaml [--from-text FILE]` | Section 4.5. |
| `stafeta chain check DIR` | Section 4.6. |
| `stafeta hash HANDOFF.md` | Print the invariants hash. |
| `stafeta schema [handoff\|readback]` | Print the JSON Schema. |
| `stafeta bench …` | Section 7. Lives in an optional extra: `pip install stafeta[bench]`. |

---

## 6. Agent integrations

Put these under `integrations/`. Each is plain text that tells an agent how to be an L1 Writer and L2 Reader.

- `integrations/AGENTS.md.snippet`: a block to paste into any project's AGENTS.md. Content in substance: if `HANDOFF.md` exists at session start, read it, produce a readback, run `stafeta readback check` if the CLI is available, show the readback to the human, and only then act; before ending a session with unfinished work, write or update `HANDOFF.md` and run `stafeta lint`.
- `integrations/codex/`, `integrations/claude-code/`, `integrations/goose/`, `integrations/kimi/`: the same behavior packaged in each tool's native mechanism (skill, slash command, recipe). Verify each mechanism from the tool's current documentation. If you cannot verify one, ship a README in that directory saying what is unverified instead of guessing.
- `integrations/chat/WRITE_PROMPT.md` and `integrations/chat/RESUME_PROMPT.md`: copy-and-paste prompts for chat surfaces with no CLI and no file system, where the human carries the file. The resume prompt must make the model output the readback as a fenced YAML block first and wait for the human's go-ahead. These two prompts matter as much as the CLI integrations; this is how the format gets used outside coding tools.

---

## 7. Relay Bench

Purpose: answer, with data, "when agent A hands a task to agent B through this file, does B finish it correctly without redoing work, breaking rules, or guessing?"

### 7.1 Fixture anatomy

`bench/fixtures/<name>/` contains:

- `task.md`: the full task as given to the sender.
- `workspace/`: the starting files.
- `checkpoint/`: the workspace as it stands at the handoff point, for golden mode.
- `golden/HANDOFF.md`: a human-written reference handoff for this checkpoint.
- `golden/NOTES.md`: human-written free-form notes carrying the same information as the golden handoff, unstructured. This lets golden mode compare form while holding content constant.
- `traps.toml`: the traps planted in this fixture (below).
- `grade.py`: deterministic grader. No LLM judging.

Every fixture plants at least three of these traps:

| Trap | How it is detected |
|---|---|
| **Dead end**: an approach that looks attractive and was already tried and rejected. | A sentinel (a wrapper script, a marker dependency) records if the receiver tries it again. |
| **Invariant**: a forbidden action, such as a fake `deploy.sh` or a file that must not change. | The fake script logs any call; file hashes are compared. |
| **Stale fact**: something true at checkpoint time that the harness changes before the receiver starts. | The grader checks that the receiver's readback reports the change and that its work reflects the new value. |
| **Open question**: a required input only the human has. | The harness plays the human through a scripted answer file that responds only if asked. Guessing yields a wrong, detectable value. |

Ship five fixtures in v0.1: three `code` profile (small Python or JS repos with tests) and two `knowledge` profile (for example, reconcile two CSV extracts into a short report with figures; update a Markdown research note from changed source files). Knowledge fixtures are graded on output files with exact expected values.

### 7.2 Modes

- **Golden**: the receiver gets `checkpoint/` plus, depending on the arm, nothing, `golden/NOTES.md` or `golden/HANDOFF.md`. There is no sender, so this isolates receiver quality and the effect of the format itself.
- **Relay**: the sender works from `workspace/` under a step or time budget, is then told to write the handoff, and the receiver continues in a fresh copy that contains the sender's files and the handoff, nothing else. No shared session, no shared memory.

### 7.3 Arms (all three are mandatory; this is the scientific core)

1. `none`: receiver gets the files and the original `task.md`, no handoff.
2. `freeform`: sender is told only "write notes for whoever continues this".
3. `stafeta`: sender writes a Stafeta handoff; receiver must produce a passing readback first.

If `stafeta` does not beat `freeform` on the scored metrics, the format has not earned its existence. The report must show all three arms side by side and must not hide a loss.

### 7.4 Runners

`bench/runners.toml` maps a runner name to a command template with placeholders for the prompt file and working directory. Provide entries for Codex CLI, Claude Code, goose and Kimi CLI, each **disabled by default** and each with flags you verified from the tool's own `--help` in the session; record the tool version you verified against. Ship a `mock` runner: a scripted fake agent with configurable behavior (perfect, redoes dead end, breaks invariant, ignores stale fact, guesses question). CI runs the whole bench against `mock` only, so CI needs no API keys and costs nothing.

### 7.5 Metrics and results

Per run: task completed (grader pass), dead-end repeats, invariant violations, stale facts caught, questions asked versus guessed, readback validity, wall time, and (if the runner reports it) tokens. One JSON file per run in `bench/results/` with fixture, mode, arm, sender and receiver each as harness, harness version and model (model `null` when the runner does not report it), date, seed and the metrics.

`stafeta bench report` renders `docs/matrix.md`: sender rows, receiver columns, each labeled harness and model, one table per arm and mode. **The matrix is generated only from result files. A pair with no result file shows `not run`.** Results from the `mock` runner are never shown in the public matrix. Do not commit real-runner results yourself; the owner runs those and commits them.

---

## 8. Repository layout

```
stafeta/
  README.md  LICENSE  NOTICE  CHANGELOG.md  AGENTS.md  HANDOFF.md
  GOVERNANCE.md  CONTRIBUTING.md  MAINTAINERS.md  SECURITY.md
  CODE_OF_CONDUCT.md  THIRD_PARTY_LICENSES.md
  pyproject.toml
  spec/        SPEC.md  handoff.schema.json  readback.schema.json  test-vectors/
  src/stafeta/ cli.py  parse.py  hashing.py  readback.py  chain.py  rules/  data/
  tests/
  integrations/
  bench/       fixtures/  runners.toml  harness/  results/
  docs/        BUILD_BRIEF.md  DECISIONS.md  matrix.md  (site sources)
  examples/    valid and invalid handoffs and readbacks, one per rule
  .github/     workflows/  ISSUE_TEMPLATE/  PULL_REQUEST_TEMPLATE.md
```

---

## 9. Hygiene required from the first commit

- License Apache-2.0. `NOTICE` with "Copyright The Stafeta Authors".
- DCO sign-off required on commits; document it in CONTRIBUTING.md and enforce with a check.
- CI on Linux, macOS and Windows, Python 3.11 to current: lint, type check, tests, the bench against `mock`, and `stafeta lint` on the repo's own `HANDOFF.md` and on everything under `examples/valid/`.
- Tagged releases with a release workflow that builds the package. Do not publish to PyPI; the owner does that.
- `GOVERNANCE.md`: maintainers decide by lazy consensus; how someone becomes a maintainer; how the spec changes (proposal issue, two-week comment period, version bump). State plainly that there is one maintainer today and that a second from a different organization is being sought.
- `SECURITY.md` with a private reporting route placeholder for the owner to fill in.
- Issue templates: bug, rule proposal, fixture proposal, spec change. Create `docs/STARTER_ISSUES.md` listing at least 15 well-scoped first contributions (new language word lists, new secret patterns, new fixtures, new runner entries, importers for other handoff formats) for the owner to open as issues.
- Documentation site from `docs/` with MkDocs, built in CI. Do not deploy; the owner enables hosting.
- README: what it is in three sentences, a 60-second example (a handoff, a readback, a failing check), the conformance levels, a "Related work" section that describes the projects in section 2 fairly and links to them, and a status section that says: early, one maintainer, no production adopters yet. Leave the matrix section pointing to `docs/matrix.md`, which will say `not run` everywhere.

The repository's own `AGENTS.md` must include the Stafeta snippet, the rule "no invented evidence", and the commands to lint, type check and test.

---

## 10. Things you must not decide alone

Stop and ask the owner for: the GitHub organization and repository URL (planned: organization `stafeta-dev`, repository `stafeta`); the security contact; anything that would name a company or a person; publishing anything anywhere; adding a dependency with a non-permissive license; changing a section name or a readback field after M1 is accepted.

---

## 11. Milestones and gates

**M0: skeleton.** Layout, license, governance and security files, CI running on an empty package, this brief in `docs/`, the repo's own first `HANDOFF.md`.
*Accept when:* CI is green on all three operating systems.

**M1: spec.** `spec/SPEC.md`, both schemas, hash test vectors, `examples/` with one valid and one invalid file per rule.
*Accept when:* the owner has converted one real-world handoff of his own (with private data removed) into the format and listed what did not fit. **Gate: the section names and readback fields freeze here.** Expect changes from this exercise; that is its purpose.

**M2: CLI core.** `init`, `lint`, `hash`, `schema`, all rules with tests.
*Accept when:* every file in `examples/` produces exactly the expected findings, and coverage of `rules/` is at least 90 percent.

**M3: readback and chain.** `readback new`, `readback check`, `chain check`, `--from-text`.
*Accept when:* the test suite includes a readback for each failure mode in 4.5 and a chain with a silently dropped invariant.

**M4: integrations.** Section 6, with the unverified parts labeled as such.
*Accept when:* the owner has done one manual relay between two different vendors' chat surfaces using only the two chat prompts, and the readback passed the check.

**M5: Relay Bench.** Harness, five fixtures, `mock` runner with all behaviors, `bench report`.
*Accept when:* against `mock`, each misbehavior is caught by the matching metric and the perfect behavior scores clean. **Gate: the owner then runs real runners. If the `stafeta` arm does not beat `freeform`, stop feature work and revisit the spec before anything else.**

Later, not now:

- Importers for other handoff formats so the bench can score them.
- A TypeScript port of the checker.
- An MCP server exposing `lint` and `readback check`.
- An upstream proposal to goose (an AAIF project) for writing and resuming from `HANDOFF.md` natively. Of all integrations this one counts most toward the foundation.
- An exporter from memory services that expose an MCP interface (openJiuwen's agent-memory is the first candidate) into a draft `HANDOFF.md`. It uses public interfaces only, so it does not break the non-goal on private session stores. Whether to ship it is the owner's decision.
- Fidelity markers per section (verbatim, summary, extracted fact, consolidated rule). Candidate for spec 0.2, and only if a bench arm shows that receivers do better with them. Invariants are already verbatim by rule and protected by the hash, which covers the case that matters most: prohibitions are the first thing lost when context is compressed.

---

## 12. First session

Do M0 and M1 only. Then write the repository's `HANDOFF.md` in the format from M1, run your own draft rules against it by hand, list in your report every place where this brief was ambiguous or where you deviated from it, and stop.
