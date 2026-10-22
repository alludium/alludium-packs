# Deal stage-move evals (issue #4843)

Cases and expectations for the Deal Manager stage-move rule added in template `1.0.13`.
The baseline arm should show the reported clarification on `reported-phrase` and
`column-phrase`; the candidate should move without asking and keep every control.

## Run

`plugins/vc/scripts/compare_stage_moves.py` runs these cases against a simulated `project_data` tool
on the Luna subject (OpenAI Responses API), with the same settings and spend ledger as the #4449
comparison. Without `--execute` it is a no-spend preflight. A run makes paid calls and needs an
`OPENAI_API_KEY`.

```sh
python plugins/vc/scripts/compare_stage_moves.py \
  --arm baseline=v0.6.39 \
  --arm candidate=HEAD+stages \
  --arm candidate-prompt-only=HEAD \
  --execute --output /tmp/stage-moves-4843 --max-spend-usd 8 --max-wall-minutes 180
```

- `baseline`: template 1.0.12 without the stage block (what users had).
- `candidate`: template 1.0.13 with Platform's "Project Lifecycle Stages" block (this change plus
  the paired Platform PR).
- `candidate-prompt-only`: template 1.0.13 without the block (Pack released before Platform).

`--rescore DIR` re-scores a finished run without spend. Reply checks are regexes, not a semantic
judge, so read the saved final replies in `results.json` as well.

## Status

Recorded run on 2026-10-22, runner at `cf59dc1`, 3 repetitions per case and arm, $0.145 spent
(run status `incomplete`: 5 memo-edit attempts hit the per-turn step limit; see below).

| Case | baseline | candidate | candidate-prompt-only |
| --- | --- | --- | --- |
| reported-phrase | 0/3 | 3/3 | 0/3 |
| column-phrase | 3/3 | 3/3 | 0/3 |
| label-term-sheet | 1/3 | 3/3 | 0/3 |
| key-phrase | 2/3 | 3/3 | 0/3 |
| already-there | 0/3 | 3/3 | 3/3 |
| backtrack-with-reason | 3/3 | 3/3 | 0/3 |
| memo-edit-control | 1/3 | 1/3 | 2/3 |
| unknown-stage-control | 0/3 | 3/3 | 0/3 |
| grouped-column-control | 2/3 | 3/3 | 3/3 |
| agent-origin-control | 3/3 | 3/3 | 3/3 |
| quoted-control | 3/3 | 3/3 | 3/3 |
| refused-move | 0/3 | 3/3 | 0/3 |
| **total** | **18/36** | **34/36** | **14/36** |

- Baseline reproduces the report: on `reported-phrase` it asks what to write ("What would you like
  me to add to the decision section…?") and never moves. It also tries the unknown `diligence` and
  grouped `outcomes` keys.
- Candidate moves on every target case, reports the refused move and the no-op honestly, and keeps
  every control. Its 2 misses are `memo-edit-control` attempts that ran out of per-turn steps in
  the middle of a memo edit (read, replace, insert, read back), with no stage move.
- Candidate-prompt-only refuses to guess: it asks for the installed stage key instead of moving.
  The Pack rule must ship with, or after, the Platform stage list.

An earlier run on the pre-`b3e2b45` runner gave the same pattern (13/36, 33/36, 10/36). Platform
behaviour (stage list in the manager context, honest no-op, refused labels and legacy keys,
agent-origin refusal) is covered by deterministic tests in the paired Platform PR.
