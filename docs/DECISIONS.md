# Decisions and first-session report

## Decisions

### M0/M1 only

This first build stops after M1. The executable CLI, individual rule modules, generated rule pages, integrations, and Relay Bench implementation belong to later milestones even where the hygiene section describes their eventual CI use.

### No repository URL yet

Project URLs are omitted from package metadata because the owner must confirm the GitHub organization and repository URL. The planned location in the brief is not treated as approved.

### Security contact placeholder

`SECURITY.md` contains the required explicit placeholder. No person, company, email address, or private reporting service was invented.

### Dependency boundary

M1 had no runtime dependencies. M2 adds only PyYAML and jsonschema at runtime; both are permissively licensed. The handoff parser recognizes only YAML front matter, H2 sections, list items, and fenced blocks needed by the contract, so a general Markdown tokenizer would add dependency weight without improving the fixed grammar. ULID generation is implemented locally in fewer than 30 lines. Build, test, coverage, type-check, lint, and documentation tools are recorded in `THIRD_PARTY_LICENSES.md`.

### Public name and compatibility

The public project name is RelayReady. Exact-name web searches performed before
release found no obvious package or AI-handoff collision, but they are not legal
or trademark clearance. Because M1 already accepted the 0.1 serialization, the
`stafeta` and `stafeta_readback` wire keys remain frozen. The `stafeta` Python
module, CLI command, and benchmark arm also remain compatibility identifiers;
new documentation and integrations use `relayready`.

### CI milestone boundary

The initial CI ran only checks implemented at M1 and named later milestone deferrals rather than simulating success. M2 replaced the draft audit with the installed `stafeta lint` command. The mock Relay Bench remains deferred until M5.

### Readback overlap and waiver syntax

M3 defines the previously unspecified near-copy threshold as Jaccard overlap above 0.80 over case-folded word tokens. It also defines the interoperable waiver item form as `<invariant> [waived by <human handle> on <YYYY-MM-DD>]`. These clarify algorithms and section content without changing a frozen section name or readback field.

### Documentation source layout

`spec/SPEC.md` remains the sole normative specification. The MkDocs site links to it rather than duplicating normative text under `docs/`.

### Integration evidence boundary

M4 uses native filesystem skills for Codex, Claude Code, and Kimi Code, and a
YAML recipe for goose, based on each project's current official documentation.
Installed `--help` and version checks were possible only for Codex and Claude
Code. goose and Kimi runtime behavior is labeled unverified. The required manual
two-vendor chat relay remains an owner acceptance exercise; no synthetic result
is substituted for it.

### Relay Bench evidence boundary

The mock runner is a deterministic fault injector, not evidence of model
quality. Its graders inspect sentinels, protected files, task output, and
question markers without an LLM judge. Mock JSON is excluded from the public
matrix. External runners remain disabled, and goose/Kimi command templates are
intentionally absent until their installed binaries' own `--help` output can be
recorded. The owner must run real sender/receiver pairs and apply the stated
stafeta-versus-freeform stop gate.

## Ambiguities

1. Section 9 says the first commit's CI runs the mock benchmark and `stafeta lint`, while milestones place those implementations in M5 and M2. This build follows milestone ordering.
2. M0 acceptance requires CI green on three operating systems, but a local build cannot prove hosted CI. The workflow matrix is present and local checks are reported separately; live status remains unverified.
3. M1 asks for one valid and one invalid file per rule before the linter rules exist. The examples include explicit `EXPECT` comments for the future rule tests, and M2 must make findings exact.
4. “Documentation page generated from its docstring” does not identify a generator or target layout. It is deferred with rule modules to M2.
5. The brief requires the owner's real-world conversion for M1 acceptance but supplies no source handoff. That gate remains an open question and is not guessed.
6. A `profile: code` handoff requires an `Environment` section, but the initial delivery directory may not itself be a Git repository. The repository handoff records that fact explicitly.

## Deviations

1. M0 and M1 were built together before writing the final handoff, rather than pausing for owner approval between them. The user's request supplied the full first-session brief as a single build request, and no externally visible or destructive action was taken.
2. No git commit was created. DCO requires the human contributor identity, and inventing a sign-off would violate the evidence rule.
3. The documentation site is built but not deployed, as required.
