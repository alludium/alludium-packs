# VC agent prompt portability pilot (#4968)

Design frozen before model calls. This is a bounded diagnostic of **actual Packs prompt text
transplanted into subscription Codex/Claude with a common synthetic tool catalogue**. It does not
run the native Platform agents or change shipped Pack content. It cannot establish prompt
inferiority, native capability parity or a before/after product improvement.

## Question and controls

For each client, compare neutral fixture guidance with the rendered current Packs template,
holding its case, local state, operation schemas, tool catalogue, model request and client options
fixed. Actual prompt text is supplied as task instructions, not installed as the Platform system
prompt. Native runtime overlays, linked skills, provider credentials and task definitions are
absent. The supplied fixture names (`deal_create`, `task_read`, etc.) differ from native repository
names. Missing native methods/skills are **boundary mismatches**, not agent ability failures.

- Pipeline Manager: new Deal creation and recovery after a lost write acknowledgement (C01/C03).
- Deal Manager: screening delegation and refusal of an ineligible task assignee (C02/T03).
- Analyst: read a source claim and withstand source-content instructions (I01/I03).
- Two clients, neutral/Packs guidance, six cases: 24 cells, one repetition each. This is a small
  diagnostic, not a statistical ranking. A future candidate improvement needs its own paired
  old/new actual prompt evaluation with the same compatible runtime contract.

Before interpreting a failed task, classify it: unavailable native operation/skill, fixture target
or permission failure, model/tool misuse, truthful abstention, or infrastructure failure. Preserve
all attempts. State/trace scores and human inspection of final answers remain separate. Synthetic
state and receipts prove no real persistence. Inference about actual shipped behavior is prohibited.

## Frozen sources and safety

`plan.json` pins Packs and Craft source. `run.py` also freezes the actual templates, run adapter and
all imported catalogue fixture/runner files in the preflight manifest. No imported files are copied
or edited. The same runner exposes named tools throughout; catalogue selection is not varied.

The imported catalogue runner attests subscription authentication and strips API credentials and
provider routing from the child environment. It disables shell, files, external apps, skills,
hooks and web tools. Its local MCP server can mutate only synthetic JSON state.

The cumulative ledger reserves each attempt *before* launch and retains failed reservations. The
ceiling is 24 attempts × 120 seconds × 2 MB captured output, with 24 fixture tool calls per attempt.
These bounds are enforced by the runner. **They are not a provider token/dollar cap.** Claude requests
1,024 output tokens; Codex does not expose an independently verified output bound. Account extra-usage
settings and actual subscription charges are not attested. No paid API runner is invoked.

No-spend preflight is the default:

```sh
python experiments/4968/run.py --catalog-runner /path/to/Craft/tools/evals/mcp-catalog --out /tmp/vc-agent-pilot
python experiments/4968/run.py --catalog-runner /path/to/Craft/tools/evals/mcp-catalog --out /tmp/vc-agent-pilot --execute
```

Dependencies: Python plus the repository's `plugins/vc/requirements.txt`, installed subscription
CLI clients, and the exact compatible catalogue-runner checkout recorded in the manifest. Do not
run while changing its source files. Run directories stay outside the repository; durable summaries
are committed separately. Source drift refuses continuation; interrupted cells are not retried.

## Native field-write case (prepared, not run)

Target: direct human request to record one exact active Fund on the current Deal. Read current
value/definition revisions; write through the accepted dedicated field tool and read back before
claiming success. Controls: question-only/no write; existing populated value with evidence-only/no
replacement; stale revision/no overwrite; absent tool/truthful blocker; agent-origin/no mutation.

Current Packs teaches `project_data.update_state` with fields and broad `project.update` indexing.
Craft main refuses legacy field writes. #4687 owns correction; #4861 provides pending runtime skill
and exposure, with #4829/#4795 dependencies. No prompt-only substitution is made here. A real native
run needs the accepted installed Pack/runtime, isolated database, and per-call budget guard. Existing
Platform eval wrappers check cost between cells, so they remain prepare-only under the shared skill.

## Judge and scorer boundary

No model judge is used. Deterministic checks inspect operation records and complete final fixture
state; they do not establish natural-language truth. Each final answer must be manually inspected.
The existing catalogue scorer's tests exercise wrong-state, write-readback and failure paths;
this adapter adds tests for rendering and freeze enforcement. No product success is inferred from
these deterministic checks without an actual completed client turn and its final-answer review.

## Follow-up accounting and publication

The completed baseline and the diagnosed four-cell clarification are in [RESULTS.md](RESULTS.md).
The follow-up does not replace the original results or change Pack source. To prepare its independent
ledger, use `--plan experiments/4968/followup.json --prior-ledger /tmp/vc-agent-pilot/ledger.jsonl`
with a fresh output directory. It requires the completed 24-attempt predecessor and enforces a
28-attempt cumulative ceiling. Execute with the same plan and output directory. Ledger/source/input
drift refuses execution. A diagnosed infrastructure failure may continue remaining cells with
`--diagnosis`, but failed cells are retained and never automatically retried.

The baseline's exact adapter is retained as an evidence snapshot. The current adapter adds the
follow-up plan/ledger handling; the plan's issue URL is represented by its number for public-readiness.
Neither reporting edit changes the historical model inputs. `export.py` records raw hashes and
publishes only synthetic traces/state and subscription authentication type, omitting machine paths.

The current adapter also locks each run directory against simultaneous executors and refuses a reserved
cell without a result, including a crash before stdout capture. Historical run snapshots are evidence;
use the current adapter and a fresh preflight for reproduction, not to resume those frozen runs.
