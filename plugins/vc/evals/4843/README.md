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

Cases, expectations and runner only. No subject-model run has been recorded yet. Platform-side
behaviour (stage list in the manager context, honest no-op, refused labels and legacy keys,
agent-origin refusal) is covered by deterministic tests in the paired Platform PR.
