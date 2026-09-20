# Changelog

All notable changes will be recorded here.

## Unreleased

### 0.1.3.dev0 submission-readiness candidate

- Record owner-confirmed project roles and the approved security/conduct contact.
- Add a 12-month roadmap, unsubmitted AAIF application draft, live-pilot protocol
  and release/provenance checklist with explicit outstanding gates.
- Require only the permissively licensed RFC 3339 format dependency; explicitly
  register timestamp checking and regress impossible dates, missing optional
  registration and surrounding whitespace.
- Remove stale generated root package metadata; builds generate current metadata.
- Preserve the S013 evidence file's LF bytes across Windows checkouts.
- Provision Node in CI and gate release artifacts on the reusable test matrix
  and an exact version/tag match; keep publication owner-controlled.
- Make contribution packaging independent of an installed RelayReady runtime.
- Check actual author-matching DCO trailers for new commits, with regression tests;
  historical unsigned commits remain an explicit provenance gate.

### 0.1.2.dev0 workbench candidate

- Add an editable, local-only continuation workbench with explicit stale results,
  expected/observed evidence rows and actionable reasons.
- Add a 20-run in-tab notebook, decision and field comparisons, exact-byte bundle
  export/import, and a ten-case deterministic regression studio.
- Add independent Python bundle validation with explicit historical replay.
- Add a RelayReady logo and favicon, plus responsive and keyboard-friendly controls.
- Keep browser assessments distinct from full Python validation and preserve the
  frozen 0.1 wire identifiers and legacy CLI.

### 0.1.1.dev0 contribution candidate

- Add an experimental continuation gate with exact input-byte bindings, opaque
  resource revision checks, pinned run inputs and prior-effect reconciliation gates.
- Add checkpoint and observation schemas, deterministic receipts, negative tests
  and five reproducible simulated scenarios without changing the accepted 0.1 contracts.
- Replace the presentation's illustrative artifacts with real schema-valid fixtures
  and recorded local validator receipts; show resume, recheck and escalation outcomes.
- Document a proposed community contribution and integration boundaries derived
  from the conference material and primary protocol documentation.

### Initial 0.1 work

- Adopt RelayReady as the public name while retaining the `stafeta` wire fields,
  Python module, command, and benchmark arm as 0.1 compatibility identifiers.
- Establish the M0 repository skeleton.
- Define the version 0.1 handoff and readback contracts for M1.
- Add the deterministic M2 CLI core with `init`, `lint`, `hash`, and `schema`.
- Implement S001 through S013 as isolated, documented rule modules.
- Add M3 readback generation and checking, fenced-YAML extraction, and chain validation.
- Package M4 reader/writer behavior for Codex, Claude Code, goose, Kimi Code, portable project instructions, and plain chat.
- Add the M5 five-fixture Relay Bench, deterministic mock behaviors, result JSON, and mock-excluding matrix generation.
