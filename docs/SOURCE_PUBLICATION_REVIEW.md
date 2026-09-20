# Source-publication review

Recorded after GitHub organization setup, 20 September 2026 UTC
(21 September in the owner's local time).

## Account state at the initial review

- `pawelworks` exists on GitHub's Free plan under `pavelpxp500`.
- The organization contact matches the owner-approved address.
- `pawelworks/relayready` is public, empty, has issues enabled, and grants the
  authenticated account administrative access.
- Private vulnerability reporting is enabled on this intended repository.
- No source has been pushed and no foundation application has been submitted.

The account bullets above record the pre-publication checkpoint. Publication
superseding that empty-repository state is recorded below.

## Read-only source audit

A second agent inspected 295 candidate files, 258 reachable historical blobs
and commit messages. It reported no apparent live credential or private-asset
leak. Matches were intentional test values, parser constants and documentation.
This pattern-based review is not a comprehensive security audit or legal clearance.

Contribution packaging excludes temporary/build/site directories and hosting
configuration. The Git-tracked `.openai/hosting.json` contains a project identifier
and static-directory setting, not a credential. The live website is unchanged.

## Corrections verified locally

- Replaced `jsonschema[format-nongpl]` with plain jsonschema and the specifically
  required MIT-licensed rfc3339-validator. Explicit per-instance date-time
  registration uses jsonschema's public customization API and preserves the
  continuation gate's independent timestamp checks.
- A fresh runtime-only installed wheel resolved nine dependencies, all declaring
  MIT or PSF-2.0 licenses, with no `fqdn`. See `THIRD_PARTY_LICENSES.md`.
- Removed obsolete tracked root `PKG-INFO` reporting version 0.1.0; the build
  generates current metadata. The removed file is recoverable in Git history.
- The corrected candidate passed 223 Python tests, 97.38% stafeta.rules coverage,
  Ruff, strict Mypy (53 files), 23 browser vectors, five reproduced fixtures and
  all 150 deterministic mock runs. Clean wheel checks cover both CLI names, four
  schemas and rejection of invalid S001/RB001 timestamps without global format
  registration. See `docs/VERIFICATION.md` for scope and limitations.
- Frozen schema files and `out/` are unchanged; the public website was not redeployed.

## Owner attestation and publication authorization

The five local website-era commits use a deployment identity and have no DCO
sign-offs. Account creation, contact approval and GitHub Terms consent do not
attest contribution rights. The separate attestation below applies to the new
reviewed import; it does not rewrite or retroactively sign the deployment history.

On 20 September 2026 UTC, the owner replied "i authorize everything" to a specific
request to certify the right to contribute RelayReady under Apache-2.0 and
authorize the permanent public [DCO 1.1](https://developercertificate.org/) sign-off
below. The question explicitly limited that approval to GitHub source publication,
not foundation submission or donation agreements. The reviewed contribution ZIP
at that decision had SHA-256
`e4af6350594fda5d818a58a1c33ca175a0a94c2d25eab9ab04fb07e1d507c61c`.

The authorized publication path retains local deployment history intact and
imports the reviewed current source to the intended empty public repository,
with applicable third-party notices and this authorized sign-off:

```text
Signed-off-by: Pavel Mihai Lucian <lucian.pavel@pawelworks.com>
```

This attests the reviewed import, not earlier commits, and does not erase their
provenance. The name, email and sign-off remain public in Git history and may be
redistributed. The import discloses its AI-assisted preparation. This record is
an owner declaration, not an independent intellectual-property audit.

For publication, verify the source tree against the reviewed candidate, commit
with the authorized identity/sign-off, run the DCO check on the import, push only
to `pawelworks/relayready` and inspect actual hosted CI results. Any material
changes to the reviewed contribution require renewed review. No release tag or
package-registry publication is authorized by this preparation step.

Foundation submission and contribution/transfer agreements remain separate
decisions requiring their actual final contents and terms to be reviewed. No
such submission or agreement has been executed here.

## Public source import

The initial public source commit is
[`d058b5f984347bb147bf98a5810c7a337ffbea54`](https://github.com/pawelworks/relayready/commit/d058b5f984347bb147bf98a5810c7a337ffbea54).
GitHub's remote commit matches the local parentless import and includes the
authorized author-matching DCO trailer. The local DCO checker passes on the entire
public history at that checkpoint. A byte comparison confirmed 149 implementation,
test, specification, app and integration files plus the checked project metadata
scope were unchanged from the reviewed candidate; publication-status documents and
successor handoffs record the new authorization.

The local `main` branch still points to deployed commit
`c4066a3f2215c4ff5192b7a9c4b950ef357f222d`, retaining all five deployment commits.
The separate `public-source` branch tracks GitHub's `main`. No original commit was
rewritten, no personal-placeholder source was pushed, and the Site was not redeployed.

Main branch protection requires the 12 observed CI matrix checks and the DCO
`check` job from GitHub Actions, strict up-to-date checks, resolved conversations
and linear history. Administrators are subject to these rules; force pushes and
deletion are disabled. Pull requests are required, with zero mandatory independent
approvals because only one maintainer is confirmed. Private vulnerability reporting
remains enabled. These controls are not a security audit or independent review.

All 12 jobs in [hosted CI run 35540740611](https://github.com/pawelworks/relayready/actions/runs/35540740611)
passed for the import: Python 3.11-3.14 across Linux, macOS and Windows. No hosted
success was claimed before the terminal run result. Publication-status documentation
is submitted through a protected pull request, which also exercises the hosted
DCO check. Its current status is visible in GitHub; this paragraph does not claim
that a subsequent PR or release has already passed or merged.
