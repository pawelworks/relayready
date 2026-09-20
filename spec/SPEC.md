# RelayReady Specification 0.1

## 1. Scope

RelayReady defines a portable, deterministic contract for transferring one unfinished task between agent harnesses. The accepted 0.1 serialization retains the `stafeta` and `stafeta_readback` keys; these are compatibility identifiers, not the current product brand. The contract consists of an immutable Markdown handoff, a receiver readback, and rules for chained handoffs. This specification does not define private session extraction, long-term memory, hosted transport, or agent orchestration.

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in BCP 14 when, and only when, they appear in all capitals.

## 2. Terminology

- **Handoff:** one `HANDOFF.md` describing one task at one moment.
- **Sender:** the harness that issues a handoff.
- **Receiver:** the harness that must acknowledge the handoff before acting.
- **Readback:** the receiver's structured acknowledgment.
- **Harness:** the application or CLI that holds working state and invokes a model.
- **Issued:** a handoff referenced by a readback.
- **Chain:** handoffs linked by their `parent` fields.

Harness and model are separate identities. A producer MUST record the harness when known and MUST NOT guess a model name.

## 3. Handoff container

A conforming handoff MUST be one UTF-8 Markdown file named `HANDOFF.md`, contain one task, begin with YAML front matter, and continue with H2 sections. Its front matter MUST conform to `handoff.schema.json`.

Content under the fixed English headings MAY use any language. The `lang` field SHOULD identify that content using a BCP 47 language tag.

The body SHOULD contain fewer than 1,500 words and MUST contain fewer than 4,000 words. Implementations MUST count body words independently of YAML front matter and SHOULD document their tokenizer.

### 3.1 Immutability and successors

Once a readback references a handoff's `id`, that handoff MUST NOT be edited. New state MUST be represented by a new handoff with a new `id` and `parent` set to the prior id. `HANDOFF.md` SHOULD name the latest handoff; earlier handoffs SHOULD be archived as `handoffs/<id>.md`.

A successor created from another handoff MUST carry forward every invariant unless section 8 permits a waiver. It MUST also carry forward unresolved human questions.

## 4. Front matter

The YAML front matter object has these fields:

| Field | Requirement | Meaning |
|---|---|---|
| `stafeta` | REQUIRED | Exact specification version `"0.1"`. |
| `id` | REQUIRED | A 26-character canonical Crockford Base32 ULID. |
| `created` | REQUIRED | RFC 3339 date-time with an explicit numeric offset or `Z`. |
| `task` | REQUIRED | Short, non-empty task title. |
| `status` | REQUIRED | `in_progress`, `blocked`, `ready_for_review`, or `done`. |
| `profile` | REQUIRED | `code` or `knowledge`. |
| `parent` | REQUIRED | Prior handoff ULID or `null`. |
| `sender` | REQUIRED | Sender object described below. |
| `recheck_after` | OPTIONAL | RFC 3339 full-date after which every State fact is treated as `[recheck]`. |
| `lang` | REQUIRED | BCP 47 language tag for body content. |

The sender object MUST contain non-empty `agent` and `vendor` strings. It MAY contain `model` and `operator`. `model` MAY be `null`; a sender MUST omit it or use `null` when the model is unknown. Unknown front-matter properties MUST be rejected so misspelled contract fields cannot pass silently.

## 5. Handoff sections

The following sections are REQUIRED in this exact order:

1. `## Goal`
2. `## Done means`
3. `## Invariants`
4. `## State`
5. `## Done so far`
6. `## Do not redo`
7. `## Next steps`
8. `## Open questions`
9. `## Pointers`

Unknown extra sections MAY appear only after the required sections and MUST otherwise be ignored by conforming readers. The known optional sections are `## Preferences`, `## Decisions`, `## Environment`, `## Glossary`, and `## Waived invariants`.

### 5.1 Goal

`Goal` MUST be one paragraph describing what the task is for.

### 5.2 Done means

`Done means` MUST be a Markdown task-list checklist of acceptance criteria. Criteria SHOULD be observable and tell the receiver when to stop.

### 5.3 Invariants

`Invariants` MUST be a Markdown list. Each item MUST be imperative, self-contained, and state one standing rule the receiver must not break. When there are no invariants, the section MUST contain exactly `- None.`

### 5.4 State

`State` MUST be a Markdown list. Every item MUST end in exactly one of:

- `[verified YYYY-MM-DD: METHOD]`
- `[verified YYYY-MM-DD by AUTHOR: METHOD]`
- `[unverified]`
- `[recheck]`

`METHOD` and `AUTHOR` MUST be non-empty. A receiver MUST verify a `[recheck]` item before relying on it. Once `recheck_after` is earlier than the receiver's effective date, the receiver MUST treat every State item as requiring recheck regardless of its written tag.

### 5.5 Done so far

`Done so far` MUST list completed work. Every substantive completion claim MUST cite inspectable evidence such as a test, file, result, or commit. The section MUST NOT claim evidence that does not exist.

### 5.6 Do not redo

`Do not redo` MUST list tried and rejected approaches with their reasons. When there are none, it MUST contain exactly `- None.`

### 5.7 Next steps

`Next steps` MUST be an ordered list. When `status` is `in_progress`, it SHOULD contain between one and seven items. Its first item MUST be the next intended action. Other statuses MAY use `1. None.` when no action remains.

### 5.8 Open questions

`Open questions` MUST list only questions that require a human answer. A receiver MUST NOT guess their answers. When there are none, it MUST contain exactly `- None.`

### 5.9 Pointers

`Pointers` MUST contain references rather than copied contents. A local file pointer MAY end with `[sha256:HEX as of YYYY-MM-DD]`, where `HEX` is a lowercase 64-character SHA-256 digest. Pointer checking is OPTIONAL because files may be absent in the receiver environment.

### 5.10 Optional sections

`Preferences` MAY record task-specific, non-binding working preferences. It MUST NOT be used to transfer unrelated personal information.

`Decisions` MAY record choices and rationales.

`Environment` MUST exist when `profile` is `code`. It SHOULD record branch, commit, uncommitted files, and exact run or test commands when those facts apply. It MUST distinguish absent information from unverified information.

`Glossary` MAY define project-specific terms.

`Waived invariants` is governed by section 8.2.

## 6. Content rules

Conforming L1 validators MUST implement the following findings. An error prevents L1 conformance; a warning does not.

| Rule | Level | Requirement |
|---|---|---|
| S001 | error | Front matter MUST validate against `handoff.schema.json`. In compatibility mode only, absent front matter produces a warning. |
| S002 | error | Required sections MUST be present, correctly named, and correctly ordered. |
| S003 | error | Every State item MUST end in exactly one valid status tag. |
| S004 | error | Handoffs MUST NOT contain detected secrets. |
| S005 | error | State, Done so far, and Next steps MUST NOT use prohibited relative-time expressions. |
| S006 | error | Body word count MUST be below 4,000. |
| S007 | warning | Body word count at or above 1,500 SHOULD be reduced. |
| S008 | warning | A numeric claim tagged `[unverified]` SHOULD NOT be phrased as certain. |
| S009 | warning | Next steps SHOULD contain one to seven items when status is `in_progress`. |
| S010 | warning | A fenced block SHOULD NOT exceed 40 lines. |
| S011 | error | A `code` profile MUST include Environment. |
| S012 | warning | `recheck_after` SHOULD NOT precede the validator's effective date without review. |
| S013 | warning | With pointer checking enabled, hashed local pointers SHOULD exist and match. |

### 6.1 Secret detection

S004 is pattern-based and cannot prove that a document is secret-free. The M2 implementation MUST enumerate its exact patterns in `src/stafeta/rules/secrets.py` and document both false-positive and false-negative risk. At minimum, patterns SHOULD cover private-key headers, bearer tokens, credential-bearing URLs, common API-key forms, and `.env`-style assignments whose names imply passwords, tokens, keys, or secrets. Detection MUST NOT transmit content over a network.

### 6.2 Relative-time and certainty data

S005 and S008 SHOULD use language-specific data files. Version 0.1 implementations MUST ship English and Romanian data. Relative-time matching MUST cover the examples “yesterday”, “last week”, “earlier today”, and “recently”, plus Romanian equivalents. Implementations SHOULD use word boundaries and document limitations for inflection and tokenization.

### 6.3 Compatibility mode

An implementation MAY offer `--compat` for handoff files without RelayReady's 0.1 front matter. In compatibility mode, absence of front matter changes S001 from error to warning; other rules SHOULD run when their required inputs can be inferred. Compatibility mode MUST NOT silently label the input conforming.

## 7. Readback

Before acting on a handoff, a receiver MUST produce a readback and the readback MUST conform to `readback.schema.json`. The readback MAY be a YAML file named `READBACK.yaml` beside the handoff or the first fenced `yaml` block in a chat message whose first mapping key is `stafeta_readback`.

The readback fields are:

| Field | Requirement |
|---|---|
| `stafeta_readback` | REQUIRED and exactly `"0.1"`. |
| `handoff_id` | REQUIRED and equal to the handoff id. |
| `created` | REQUIRED RFC 3339 date-time with offset. |
| `receiver` | REQUIRED identity object, with unknown models omitted or null. |
| `goal_restated` | REQUIRED non-empty sentence in the receiver's own words. |
| `invariants_hash` | REQUIRED hash from section 8.1. |
| `invariants_echo` | REQUIRED verbatim invariant strings, same order, without list markers. |
| `will_not_redo` | REQUIRED array containing every one-based Do not redo item index. |
| `rechecked` | REQUIRED array addressing every State item that requires recheck. |
| `conflicts` | REQUIRED array of observed differences, which MAY be empty. |
| `questions_for_human` | REQUIRED array containing every Open questions item, which MAY add questions. |
| `first_action` | REQUIRED non-empty action matching, or justifying deviation from, Next steps item 1. |

Each `rechecked` object MUST identify a one-based State item, set `result` to `confirmed`, `changed`, or `could_not_verify`, and include a non-empty note. The receiver MUST NOT silently treat `could_not_verify` as confirmation.

A readback checker MUST fail when the id differs; the invariant hash or echo differs; a Do not redo index is absent; a required recheck has no entry; an Open questions item is absent; or `first_action` is empty. It SHOULD warn when token overlap indicates that `goal_restated` is a near-verbatim copy of Goal. Version 0.1 uses case-folded word-token Jaccard overlap above 0.80 as that warning threshold.

A passing readback proves that the receiver addressed the mechanically checkable critical items. It cannot prove that the receiver understood or correctly restated the goal. Relay Bench measures semantic outcomes.

## 8. Invariant hashes and chains

### 8.1 Hash algorithm

For each invariant, in order, an implementation MUST:

1. Normalize Unicode to NFC.
2. Trim leading and trailing whitespace.
3. Strip one leading Markdown unordered-list marker (`-`, `*`, or `+`) and its following whitespace when present.
4. Collapse each remaining run of Unicode whitespace to one ASCII space.

It MUST join normalized invariants with a single LF (`U+000A`), encode the result as UTF-8, compute SHA-256, encode the digest as lowercase hexadecimal, and prefix it with `sha256:`. It MUST NOT add a final newline. Test vectors are in `test-vectors/invariants.json`.

### 8.2 Chain inheritance and waivers

When `parent` is non-null, the child's Invariants MUST contain every parent invariant verbatim and in the same relative order. Additional invariants MAY be inserted.

An invariant MAY be absent only when `Waived invariants` contains an entry with the exact invariant text, the human handle that waived it, and an absolute ISO date. The interoperable version 0.1 list-item form is `<invariant> [waived by <human handle> on <YYYY-MM-DD>]`. A tool MUST NOT infer a waiver from edits, omissions, task status, or model output.

A chain checker MUST rebuild parent relationships by id and report missing parents, cycles, and unwaived dropped invariants. It SHOULD report duplicate ids.

## 9. Conformance

- **L1 Writer:** produces handoffs that pass all error-level rules.
- **L2 Reader:** produces readbacks that pass the checks in section 7.
- **L3 Relay:** identifies a sender and receiver by harness and, when known, model, and publishes Relay Bench results backed by result files.

An implementation MUST NOT claim a conformance level without satisfying that level. A missing benchmark result MUST be displayed as `not run`, never as zero or an estimate.

## 10. Security and privacy

Validators MUST operate locally for lint, readback, and chain checks and MUST NOT make network calls. They MUST NOT read vendor-private session stores. A handoff SHOULD contain the minimum task state needed by the receiver and SHOULD prefer pointers over pasted content.

Secret scanning is defense in depth, not a guarantee. Humans remain responsible for reviewing a handoff before moving it across a trust boundary.
