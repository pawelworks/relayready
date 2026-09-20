# Continuation Workbench

The workbench adds editable experiments to the recorded two-agent demonstration.
Open `out/workbench.html` through an HTTP server. It needs no account, model key,
backend service or JavaScript dependencies.

## What works

1. Choose one of five prevalidated example contracts.
2. Change resource revisions, pinned-input digests, previous-operation status,
   evidence references and UTC evaluation times. Remove observations to test gaps.
3. Evaluate a fresh browser assessment with reasons and expected/observed rows.
4. Compare two evaluated runs. Up to 20 immutable snapshots live in the current tab.
5. Export a bundle or run the ten-case regression suite and export its evidence.
6. Import a supported bundle. The browser recomputes the assessment and rejects
   modified claims, different contract bytes, ambiguous JSON or unsupported scope.

Editing invalidates the displayed result and disables its export until evaluated
again. Earlier notebook runs keep their original bytes. Reloading or closing the
page clears the notebook; export anything you need to keep.

## Independent reproduction

```console
relayready gate bundle experiment.json --replay --json
relayready gate bundle experiment.json --json
stafeta gate bundle experiment.json --replay --json
```

The first and third commands explicitly reproduce the historical evaluation clock.
The second uses current UTC, so an old checkpoint can correctly require a recheck.
An explicit `--now` is also supported, mutually exclusive with `--replay`.

The CLI ignores the bundle's claimed browser assessment and validates all four
artifact strings with the full Python validator. Inputs are written only to fixed
filenames in a temporary directory; they are never executed, fetched or followed.
Exit codes are 0 for resume, 1 for recheck/escalate and 2 for invalid input.

## Scope and trust boundary

Browser assessments use `relayready_browser_assessment`, not the Python receipt
identifier. The static browser engine supports only the five supplied contracts;
handoff/readback findings are generated from the full validator and immutable in
the editor. It does not parse or validate arbitrary Markdown/YAML contracts.
Use the CLI for those. The editor does not support arbitrary identifiers or
wrong checkpoint bindings; imports containing them are rejected without discarding
fields. The regression suite can exercise the latter condition independently.

SHA-256 bindings identify exact UTF-8 input bytes. They are not signatures.
Evidence references are declarations, not verified external records. A resume
assessment is mechanical consistency at the selected clock, not permission,
semantic understanding, a live lock, or an exactly-once guarantee. All example
observations are simulated; no agent or company integration is executed.

Only same-origin fixtures are fetched. Inputs are processed locally in the browser;
there is no upload endpoint, analytics or persistent browser storage. Exported
bundles include the full artifacts, so review them before sharing. Imports are
limited to 2 MB. Python accepts up to microsecond timestamps; this workbench
intentionally supports only millisecond precision.

## Verification

`node tools/test_workbench.mjs` covers 23 decision vectors, strict input checks,
tamper rejection and comparison semantics. `tests/test_bundle.py` independently
evaluates those vectors in Python and compares decisions, reason codes, exact
bindings and timestamp instants. This is targeted agreement for supported inputs,
not proof of complete equivalence or certification.
