# Third-party licenses

RelayReady's M1 contract had no third-party runtime dependencies. The current runtime dependencies are listed below.

Direct development, documentation and runtime dependencies:

| Dependency | Purpose | License |
|---|---|---|
| build | Build frontend | MIT |
| hatchling | Build backend | MIT |
| jsonschema | Runtime JSON Schema validation | MIT |
| rfc3339-validator | Explicit runtime date-time checking | MIT |
| MkDocs | Documentation build | BSD-2-Clause |
| mypy | Static type checking | MIT |
| pytest | Test runner | MIT |
| pytest-cov | Test coverage integration | MIT |
| coverage.py | Coverage measurement (via pytest-cov) | Apache-2.0 |
| PyYAML | Runtime YAML parsing | MIT |
| Ruff | Linting and formatting checks | MIT |
| types-jsonschema | Static typing stubs for schema tests | Apache-2.0 |
| types-PyYAML | Static typing stubs for YAML contract tests | Apache-2.0 |

Versions are constrained in `pyproject.toml`. Transitive dependencies are governed by the selected packages' lock or installation resolution and will be reviewed before a release artifact is published.

## Runtime resolution inspected on 20 September 2026

The following versions were installed from the built wheel in a fresh
runtime-only Windows/Python 3.12.14 environment for the corrected `0.1.3.dev0`
candidate. This is a dated inventory, not a cross-platform
lockfile, vulnerability scan or legal clearance. License labels come from the
installed distribution metadata and license files; upstream license texts govern.

| Package | Version | Declared license |
|---|---|---|
| jsonschema | 4.26.0 | MIT |
| PyYAML | 6.0.3 | MIT |
| attrs | 26.1.0 | MIT |
| jsonschema-specifications | 2025.9.1 | MIT |
| referencing | 0.37.0 | MIT |
| rpds-py | 2026.6.3 | MIT |
| typing_extensions | 4.16.0 | PSF-2.0 |
| rfc3339-validator | 0.1.4 | MIT |
| six | 1.17.0 | MIT |

This supersedes the earlier extra-based runtime inventory. The broad
`format-nongpl` extra pulled in `fqdn` (MPL-2.0), contrary to the project's
permissive-additions policy. The corrected candidate uses no format extra and
the clean wheel environment contains no `fqdn`. All nine resolved runtime
dependencies above declare MIT or PSF-2.0 licenses. Development/build tooling
is outside this runtime-only inventory; no vulnerability audit is implied.

The only schema formats used are `date` and `date-time`. Full-date checking uses
jsonschema's standard-library implementation. A local `FormatChecker.checks()`
registration explicitly uses the required RFC 3339 validator, so timestamps do
not silently pass when optional global registration is absent. Regressions cover
impossible dates, missing registration and surrounding whitespace. Leap seconds
remain unsupported by this validator; this is not a claim of complete RFC coverage.
See [jsonschema's format documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/#validating-formats).
