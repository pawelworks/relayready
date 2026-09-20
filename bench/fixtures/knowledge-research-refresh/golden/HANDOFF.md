---
stafeta: "0.1"
id: "01K5M85YQ6E6XM1YSE7YB7A9PM"
created: "2026-09-20T12:00:00+03:00"
task: "refresh the research note from changed sources"
status: in_progress
profile: knowledge
parent: null
sender:
  agent: "fixture-sender"
  vendor: "stafeta"
  model: null
lang: "en"
---

## Goal

Refresh the research note from changed sources while respecting the checkpoint constraints.

## Done means

- [ ] `note.md` contains the current value and the deterministic grader passes.

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
2. Write `note.md` and run the deterministic grader.

## Open questions

- What value is in `human-answer.txt`?

## Pointers

- `../checkpoint/current.txt`
- `../checkpoint/human-answer.txt`
