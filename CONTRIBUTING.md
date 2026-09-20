# Contributing

Thank you for helping build RelayReady. The project is deliberately organized so rules, language data, fixtures, and runner definitions can be contributed independently.

## Development

Use Python 3.11 or newer.

```console
python -m pip install -e .[dev]
ruff check .
mypy --strict
pytest
mkdocs build --strict
python -m build
```

Do not invent evidence. Benchmark claims must be backed by committed result files, and absent results must be shown as `not run`.

## Developer Certificate of Origin

Every commit must include a `Signed-off-by` trailer certifying the [Developer Certificate of Origin 1.1](https://developercertificate.org/):

```console
git commit -s -m "Describe the change"
```

By signing off, you certify that you have the right to submit the contribution under the project's license. CI checks the commits in each pull request.

## Pull requests

- Keep changes focused and include tests or fixtures when behavior changes.
- Update normative text, schemas, examples, and test vectors together when the contract changes.
- Add only permissively licensed dependencies and record each one in `THIRD_PARTY_LICENSES.md`.
- Never commit credentials, private handoffs, or real-runner benchmark results without the owner's explicit decision.
