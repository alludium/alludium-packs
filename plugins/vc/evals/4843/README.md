# Deal stage-move evals (issue #4843)

Cases and expectations for the Deal Manager stage-move rule added in template `1.0.13`.
The baseline arm should show the reported clarification on `reported-phrase` and
`column-phrase`; the candidate should move without asking and keep every control.

Status: cases and expectations only. No subject-model run has been recorded yet, because a run
makes paid model calls and needs explicit approval. Platform-side behaviour (stage list in the
manager context, honest no-op, refused labels and legacy keys) is covered by deterministic tests in
the paired Platform PR.
