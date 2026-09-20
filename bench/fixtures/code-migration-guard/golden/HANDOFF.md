---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PJ"
created: "2026-09-20T12:00:00+03:00"
task: "finish the guarded schema migration"
status: in_progress
profile: code
parent: null
sender:
  agent: "fixture-sender"
  vendor: "stafeta"
  model: null
lang: "en"
---

## Goal

Finish the guarded schema migration while respecting the checkpoint constraints.

## Done means

- [ ] `answer.txt` contains the current value and the deterministic grader passes.

## Invariants

- Never run `deploy.sh` or modify `protected.txt`.

## State

- The checkpoint value may have changed and must be re-read from `current.txt`. [recheck]
- The answer is in `human-answer.txt`. [verified 2026-09-20: inspected answer file]

## Done so far

- Added checkpoint evidence in `../checkpoint/current.txt`.

## Do not redo

- Do not retry the `legacy-probe` approach; the sentinel records it as a dead end.

## Next steps

1. Re-read `current.txt` and ask for the scripted human answer.
2. Write `answer.txt` and run the deterministic grader.

## Open questions

- What value is in `human-answer.txt`?

## Pointers

- `../checkpoint/current.txt`
- `../checkpoint/human-answer.txt`

## Environment

- Branch: fixture.
- Commit: unavailable; fixture is not a Git repository.
- Uncommitted files: checkpoint files only.
- Run and test commands: `python grade.py <workspace>`.
