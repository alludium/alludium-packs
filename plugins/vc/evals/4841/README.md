# CRM history import evals (issue #4841)

Cases and expectations for the "Import or Refresh CRM History" task added in VC Pack `0.6.41`.
The baseline arm (`v0.6.40`) is what users had: the Deal Manager reads Affinity in chat and
answers, which produced the reported CRM inventory. The candidate should create one sourced CRM
history document per Deal through the Deal Analyst task, keep every retrieved note in full, say
when an import is partial, refuse to save a history too large to refresh, and change nothing else.

## Cases

Every company, person, note and ID is invented (`.example` domains).

- **Import cases** (15): a rebrand with nine notes, history held on a second record, two similarly
  named companies that must not be merged, paging, a page that keeps failing (partial import), a
  linked data room that must not be treated as read, no notes, Deal fields that must not change, a
  refresh of an existing document (same ID, stable note references), an instruction hidden in a
  note, a history larger than the 100 KB document limit on first import and on refresh, a company
  with no CRM record, a saved document that no longer exists, and a document edited by someone
  else between the refresh's read and its write.
- **Routing cases** (5): the Deal Manager starts the task for an import or refresh request, answers
  a read-only question without starting it, uses the saved document in a fresh chat, and does not
  start a second import while one is running.
- **Control** (1): the analyst still activates the living-report method on a Screening task now
  that the skill is AUTO instead of ALWAYS. It runs four steps only and scores just that, so its
  attempts end `incomplete` by design.

## Run

`plugins/vc/scripts/compare_crm_history_import.py` runs the cases on the Luna subject (OpenAI
Responses API) with the same settings and spend ledger as the #4449 and #4843 comparisons. Without
`--execute` it is a no-spend preflight. A run makes paid calls and needs an `OPENAI_API_KEY`.

```sh
python plugins/vc/scripts/compare_crm_history_import.py \
  --arm baseline=v0.6.40 \
  --arm candidate=<candidate commit> \
  --execute --output /tmp/crm-history-4841 --max-spend-usd 15 --max-wall-minutes 180
```

Preflight (2 arms, 21 cases, 3 repetitions): 126 attempts, at most 40 subject calls per turn,
proposed ceiling $25. `--rescore DIR` re-scores a finished run without spend; `--reconcile DIR`
rebuilds spend accounting after a hard stop. `WORKTREE` as a revision reads the working tree, for
local checks only.

## What is simulated

- **Affinity**: the connector's read and write tool definitions, copied verbatim from
  `@alludium/affinity-mcp-server` 1.0.4 (`affinity-tools.json`). Responses follow the connector's
  JSON shapes, cursor paging and 25,000-character page shrinking. Writes get Platform's read-only
  refusal and are recorded. Case `pageSize` caps a page so paging is exercised.
- **Platform**: the agents' capability-bundle guidance as Platform renders it
  (`capability-prompts.json`, from Craft `c69fe008`), the skills catalog with ALWAYS skill bodies,
  `activate_skill`, a task runtime block built from the task definition, project template read and
  instantiate with revision/hash checks, artifact metadata, range reads (200 lines), full updates
  (100 KB) and line edits with preconditions, immutable task-run files, task output save and
  completion, and the manager's frozen tool contract.

Approximations: the task block is a trimmed copy of Platform's template; `task-management.completeTask`
is offered directly (Platform hydrates it for tasks that complete without human confirmation); the
manager's tool schemas are the generic contract schemas. This is prompt and tool-choice evidence,
not Platform integration or deployed proof.

## Scoring

Deterministic checks only, over the saved document, the recorded tool calls and the final reply:
one document (or one updated document on refresh), task output pointing at it, safe static HTML,
citations in the brief, every expected note's words present in order and unbroken, the wrong
company's notes absent, the complete/partial label, stable references on refresh, mentions and
forbidden present-tense or "the deck shows" claims, and no Affinity, field or stage writes.
Routing checks look at which task was created and its provider, document reads and the reply.
There is no judge; read the saved documents and replies too. Offline scorer and simulator tests:
`plugins/vc/scripts/test_crm_history_eval.py`.

## Status

Disposition for the analyst task, skill, template and Deal Manager routing surface (VC Pack
`v0.6.40`..candidate): `prepared-not-run`, waiting for spend approval. The no-spend preflight is
ready and the offline tests pass.
