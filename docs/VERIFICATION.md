# Workbench candidate verification

Local checks on 20 September 2026 for RelayReady `0.1.2.dev0` and experimental
Continuation Gate `0.1-draft`. These are local candidate checks, not independent
certification, live integrations or evidence of real-runner advantage.

| Check | Observed result |
|---|---|
| Python regression suite | 191 tests passed on Python 3.12.14 |
| Existing lint-rule coverage | 97.38% of `stafeta.rules`, not the whole product |
| Browser/Python agreement | 23 vectors matched decisions, reason codes, exact-byte bindings and clock instants |
| Interactive regression studio | 10 / 10 simulated cases matched expected decisions in the browser |
| Deterministic Relay Bench | All 150 mock runs matched expected outcomes |
| Ruff / strict Mypy | Passed; Mypy checked 51 source files |
| JavaScript | Syntax and dependency-free engine/UI checks passed |
| Static links | Both HTML pages' local assets and fragment links checked |
| Browser inspection | Resume, edited revision/recheck, unknown effect/escalate, run comparison and local suite inspected |
| Responsive check | Desktop, 390px and 320px; narrow clock overflow fixed and no document horizontal overflow remained |
| Browser console | No warnings or errors observed during the inspected workbench run |
| Brand asset | Transparent PNG loaded in the app; both page favicons and website marks use it |
| Frozen core contract | Accepted spec and handoff/readback schemas unchanged |
| Python artifacts | Updated wheel and source distribution built successfully |

The input tests reject malformed JSON, duplicate keys, oversized bundles, invalid
timestamps, unsupported fields and tampered browser assessments. Python ignores
claimed browser decisions and independently evaluates exact artifacts. Imported
scope that cannot be represented by the editor is rejected, not silently dropped.

This is targeted functional, keyboard and responsive verification, not a complete
accessibility or security audit. All observations and benchmark runs above are
simulated. The browser is not a model runner or an authorization service.

## Reproduction

```console
python -m pytest
ruff check src tests tools
python -m mypy --strict
python -m mkdocs build --strict
python -m stafeta bench verify-mock --json
python tools/generate_continuation_fixtures.py --check
node --check out/app.js
node --check out/workbench.js
node --check out/workbench-engine.mjs
node tools/test_site.mjs
node tools/test_workbench.mjs
python -m build --no-isolation
python tools/package_contribution.py
```

The contribution packager verifies a per-file SHA-256 manifest and exact bytes.
It excludes Git metadata, hosting configuration, temporary research and conference
decks. The website is served directly from `out/`; it needs no frontend build or
backend service.

## Publication and contribution boundary

This source snapshot was prepared before the publishing step. The registered
private Site is reused. Supported Sites helpers and an authenticated source
connection are now available; the earlier networking/helper blocker is resolved.
Use the native deployment status to determine publication success and its URL,
rather than interpreting a local archive as a deployment.

No adoption, institutional endorsement, exclusive novelty or accepted donation is
claimed. Formal contribution still needs provenance and maintainer/security
details reviewed with the receiving organization.

## Submission-readiness update, 20 September 2026

The website deployment succeeded and public access was subsequently enabled at
<https://relayready.pavel752770.chatgpt.site/>. It serves commit
`c4066a3f2215c4ff5192b7a9c4b950ef357f222d`. The earlier pre-publication section
above is historical, not the current hosting status. The local readiness changes
do not alter `out/` and have not been deployed or pushed to public GitHub.

For the local `0.1.3.dev0` candidate, a fresh Windows/Python 3.12.14 environment
passed **205 tests**, with **97.38% coverage of stafeta.rules only**, Ruff and
strict Mypy (52 files). The 23 browser/Python vectors, static link checks, all five
byte-reproduced fixtures and all 150 deterministic mock runs passed. MkDocs strict
build, wheel and source distribution builds passed. An isolated installed wheel
loaded all four schemas, rejected impossible date-times and ran both CLI names.

The fresh environment exposed and now tests the required JSON Schema format
extra. The S013 evidence source and issued handoff archives explicitly retain LF
bytes on Windows. The DCO checker now examines final author-matching trailers,
not arbitrary body text. Its audit of HEAD intentionally fails on all five
unsigned historical commits; this is an unresolved provenance gate, not a test
failure to conceal.

The successor handoff records the preceding 203-test checkpoint. Final review
added two more DCO regressions for Unicode pseudo-newlines and folded trailers;
the 205-test rerun and the successor handoff/readback checks both passed.

The owner confirmed Pavel Mihai Lucian and lucian.pavel@pawelworks.com for the
project's contact roles. The requested `pawelworks/relayready` destination is now
created and accessible but still empty. Hosted CI, public source release, independent security review,
live pilots and foundation submission remain incomplete. See the
[application draft](AAIF_APPLICATION_DRAFT.md) and [release gates](RELEASE_CHECKLIST.md).

## Dependency-policy correction, 20 September 2026 UTC

A new clean Windows/Python 3.12.14 development environment passed **223 tests**
with **97.38% coverage of stafeta.rules only**, Ruff and strict Mypy over 53
files. This supersedes the earlier candidate's 205-test count. The 23 browser
vectors, static site checks, five exact fixture reproductions and all 150
deterministic mock runs also passed again. None is a live-provider benchmark.

The runtime now requires plain jsonschema, PyYAML and rfc3339-validator, without
the broad format extra that introduced the policy conflict. Explicit per-instance
registration keeps date-time checking active even when global optional format
registration is removed. Regressions also reject trailing-newline timestamps.
Frozen schemas, wire identifiers, the legacy CLI and `out/` remain unchanged.

The wheel built from the source distribution installs in a separate runtime-only
environment with no `fqdn`; its nine resolved dependencies declare MIT or
PSF-2.0 licenses. Both CLI names run, all four packaged schemas load, and S001/RB001
reject impossible timestamps with global date-time registration removed.
`pip check`, MkDocs strict, successor handoff/readback checks, source/wheel builds
and contribution-ZIP manifest verification pass. The stale tracked
root `PKG-INFO` was removed and ignored; current package metadata is generated
by the build backend. The old copy remains recoverable in Git history.

The corrected inventory is in `THIRD_PARTY_LICENSES.md`. This is local verification,
not a hosted matrix result, security audit, legal opinion or foundation approval.
At this verification checkpoint, the public repository was empty pending the
owner's contribution-rights attestation. The owner subsequently authorized the
reviewed import and public DCO sign-off; see the source-publication record.
No historical sign-off has been invented or history rewritten.

## Public source and hosted verification, 20 September 2026 UTC

The reviewed source is public at <https://github.com/pawelworks/relayready>.
The initial import is `d058b5f984347bb147bf98a5810c7a337ffbea54`; GitHub's
remote SHA matches the local signed-off commit. All 12 jobs in
[CI run 35540740611](https://github.com/pawelworks/relayready/actions/runs/35540740611)
completed successfully: Python 3.11, 3.12, 3.13 and 3.14 on Linux, macOS and Windows.
Each job includes Python tests, lint/types, browser checks, fixture reproduction,
mock bench, documentation and package builds. This supersedes the prior
hosted-CI/public-source blockers, not the independent-review or live-pilot gates.

Main's protection requires these 12 checks plus DCO, with administrator enforcement,
up-to-date branches, resolved conversations, and no force pushes or branch deletion.
The source-publication record distinguishes the owner-attested initial import from
unsigned local deployment history. No PyPI release, foundation application,
foundation acceptance or legal transfer occurred. The public website is unchanged.
