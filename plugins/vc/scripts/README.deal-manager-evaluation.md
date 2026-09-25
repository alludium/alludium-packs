# Deal Manager behavioral regression

`evaluate_deal_manager.py` sends the actual Deal Manager prompt text to Bedrock
Converse and observes model-generated tool calls and final responses. It consumes
the six issue #4010 scenarios in `alludium/fixtures/deal-pipeline-management.yaml`.
Scenarios naming both manager templates run against both, producing eight cases
per repetition. Expected values are used only by the scorer; they are never sent
to the subject model.

## Run

Use Python with `plugins/vc/requirements.txt` installed and an authenticated AWS
CLI profile with Bedrock Converse access. Each run makes paid model calls.

```sh
python plugins/vc/scripts/evaluate_deal_manager.py \
  --revision HEAD \
  --output /tmp/deal-manager-evaluation \
  --repetitions 3
```

The output directory must not already exist. The default model is
`global.anthropic.claude-sonnet-4-6` in `eu-west-1`, with the Platform catalog's
1,024-token thinking budget. Temperature is 1 for extended thinking; each model
step has a 4,096-token output cap. Cases stop after eight steps. No second human
message is supplied: continuation messages contain simulated tool results only.

`--scenario` selects diagnostic subsets; omit it for complete coverage.
`--thinking-budget 0` is a diagnostic configuration, not the Platform catalog
default. `--candidate-templates` freezes local template edits and labels evidence
as a candidate snapshot rather than evidence for the Git head. Neither option
should be hidden when reporting results.

## Evidence and assertions

Every request, provider response, final response, tool-call ledger, token count,
prompt hash, fixture hash, runner hash, and selected source revision is recorded.
`summary.json` includes `aggregateUsage`, summed across every case and repetition;
each result also retains its own usage. The last result is not the run total.
The manifest also records the Platform revision from which the handoff guard was
copied. A failed case makes the process exit nonzero; failed and rejected tool
attempts remain in the evidence.

The scorer checks:

- Clear human requests create exactly one task with the expected discovered
  definition and read it back, without another confirmation question.
- Ambiguous requests create no task and ask one question; missing-Fund
  clarification identifies the Fund rather than requiring a task-creation phrase.
- Existing tasks are read back and no duplicate is created.
- Agent-origin input requests human approval without creating or assigning work.
- Invalid calls, unsupported calls, incomplete turns, and false claims of execution
  fail rather than being counted as successful abstention.

Open tasks are already included in the synthetic project context. The scorer does
not require a redundant task-list call. Review the saved final responses alongside
the deterministic checks; string checks are not a semantic judge.

Run the failure-injection tests without model spend:

```sh
python -m unittest discover -s plugins/vc/scripts -p test_deal_manager_evaluation.py
```

## Proof boundary

This is a prompt/tool-choice evaluation, not a Platform integration test. The
source templates, fixture cases, and task definitions are read from the specified
Git revision. Company evidence, project/member IDs, and tool results are synthetic.
Tool input schemas are bounded evaluation approximations, not generated repository
schemas; the simulator validates required coordination identifiers but does not
prove every input-field or persistence contract. Runtime skills and project-manager
overlays are not installed or executed.

For agent-origin cases, the harness supplies Platform's verbatim project-handoff
system guard and synthetic trusted attribution. It deliberately records attempted
creation as a failure even though real Platform authorization guards may reject
that call. Simulated tool receipts do not demonstrate a real task was started.
No customer workspace, task, CRM record, or database is modified.

Passing results apply only to the recorded model configuration and source hashes.
They do not establish deployed correctness, universal model reliability, or the
reviewer's acceptance. Failed runs must not be described as passing evidence.

## Paired prompt comparison (issue #4308)

`compare_deal_manager_prompts.py` compares two revisions of the Deal Pipeline
Manager prompt against one frozen case set. By default it compares Packs PR #98
base and head; fetch them first with `git fetch origin pull/98/head`.

- `fixtures/deal-manager-4308-cases.yaml` holds subject inputs and run settings:
  a fictional Deal, six cases (including two live human turns and one labelled
  frozen-reconstructed prefix), subject/judge models, limits, prices and the
  proposed spend ceiling.
- `fixtures/deal-manager-4308-expectations.yaml` holds deterministic assertions
  and the judge rubric. It is never sent to the subject model.
- `fixtures/deal-manager-tool-contract.json` freezes the Platform tools granted
  by the manager's capability bundles, with the source Platform revision.
  Manager templates no longer declare `mcpServers`; `evaluate_deal_manager.py`
  now uses this contract and refuses templates with other bundles.

The default mode is a no-spend preflight. It resolves both prompts, checks that
only the prompt differs (template capabilities, task definitions and every
first request), and reports counts, limits, the attempt plan and a cost estimate:

```sh
python plugins/vc/scripts/compare_deal_manager_prompts.py \
  --preflight-out /tmp/preflight.json --preview-dir /tmp/first-requests
```

The subject is `gpt-5.6-luna` through the OpenAI Responses API, confirmed on
2026-09-23 as the evaluated model and system default. Its settings mirror
Platform: reasoning scale 5 gives medium effort, detailed summaries and medium
verbosity; no temperature is sent; the output cap is the catalogue's 128,000
tokens. The runner is stateless (`store: false`): encrypted reasoning items and
function calls are sent back unchanged each step, and each tool result is
linked by its `call_id`. The optional judge stays on Bedrock Opus 4.8.

`--execute --output DIR --max-spend-usd N [--judge]` makes paid calls. It
requires `OPENAI_API_KEY` for the subject and an AWS profile for the judge. The
key is sent only as a request header and never written to evidence. Attempts
alternate old and new, and each attempt has its own folder. Human turns are
fixed. Simulated Platform state persists across turns, so a variant that
already started work is scored on not duplicating it.

Spend accounting:

- Before each call, the runner reserves a bounded worst case at
  Platform-billable prices. These are 1.3x the direct provider list price,
  which is also recorded.
- The output bound is the request's output cap. The input bound is the bytes of
  the indented request JSON (encrypted reasoning excluded), plus the output
  tokens already reported in this conversation (which bounds what replayed
  items can add), plus a fixed 4,096-token allowance. Both routes use
  byte-level tokenizers. The bound is still an assumption: every response is
  checked against it, and a violation halts the run.
- Cached input is priced as a subset of input tokens, and reasoning as a subset
  of output tokens, so neither is counted twice. Luna's long-context tier
  applies above 272,000 input tokens.
- A call is dispatched only while confirmed cost plus unreconciled exposure
  plus its reservation stays within the ceiling.
- A validated response settles at actual usage. A failed, timed-out or
  interrupted call keeps its full reservation as exposure; it is never treated
  as free. Missing or invalid usage does the same and also stops all later
  dispatch.
- Neither route retries: one reservation covers one submission. Platform
  itself allows two SDK retries.
- The ceiling is enforced by the runner, not by provider billing.

Durability and interruption:

- `run.json` is written before any spend.
- `ledger.jsonl` records every reservation, settlement and exposure, fsynced
  before dispatch. Attempts are checkpointed atomically after every step.
- SIGINT or SIGTERM marks the in-flight attempt and the run `interrupted`.
- After a hard kill, `--reconcile DIR` rebuilds accounting from the ledger
  alone. Unresolved in-flight calls stay charged at their reservation.

Exit status: `0` means execution completed (behavioural failures of either
prompt are valid results). `2` means execution was incomplete or interrupted:
a provider error, a step, token or time limit, a budget or accounting stop, an
unrun attempt, or a requested judge result that is missing. `1` means the
preflight or configuration refused the run. The report separates preparation,
execution completeness and behavioural results.

The optional judge sees a blinded transcript. The transcript has no variant
label, prompt text or deterministic verdict. Judge scores are reported
alongside deterministic results and never override a failure.

Run offline tests with `python plugins/vc/scripts/test_deal_manager_prompt_comparison.py`.
These tests use scripted providers and do not show a behavioural improvement.

## New issue-derived cases (`--suite-file`)

The built-in suite library also includes `pr97-4313-pipeline` and
`pr97-4313-legacy`, covering plain-language guidance for both manager templates.
Fetch `git fetch origin pull/97/head` before reproducing their pinned comparisons,
then select one with `--suite pr97-4313-pipeline` (or `pr97-4313-legacy`). These use
separate template-specific tool contracts. Each execution needs its own output
directory and approved ceiling; an earlier run's approval is not a new budget.
The guidance judge receives shared system facts and actual lookup results as
evidence. Skills, capability-bundle prompt text, connected apps and live runtime
behaviour remain outside these simulations.

A new case set that fits an existing suite kind needs no runner edit. Declare it
in a YAML suite file and pass `--suite-file PATH` instead of `--suite`:

```yaml
schemaVersion: "0.1"
id: my-issue-1234-case            # new, lowercase; built-in ids are refused
kind: guidance                    # or optional-context; a new kind needs runner code
issue: "1234"                     # namespaces simulated task-definition ids
templateId: vc_deal_manager       # template defaults to agent-templates/<templateId>.yaml
revisions: {old: <base sha>, new: <head sha>}
seed: 1234
cases: plugins/vc/evals/1234/cases.yaml               # repository-relative
expectations: plugins/vc/evals/1234/expectations.yaml
toolContract: plugins/vc/scripts/fixtures/deal-manager-legacy-tool-contract.json
```

The kind supplies the simulator, scorer and judge payload. `optional-context`
is the #4308 Deal Pipeline simulation (Fund-less Deal, deck, typed task
creation); `guidance` is the #4313 simulation (confirmed Fund, completed report,
advice-only turns). The preflight records the suite file's path and sha256 in
the run identity, prints an execute command that repeats `--suite-file`, and
`--judge-run` refuses a changed suite file. Built-in suites are unchanged.

`--judge-run` also refuses when any case fact, fixture or subject/run setting changed since
the subject phase (`casesExceptJudgeSha256`); only the `run.judge` block may be repaired for
a judge-only continuation. Runs recorded before that field existed resume only on
byte-identical cases (`casesSha256`).
The saved `summary.json` is trusted local evidence, not tamper-proof storage;
preserve it unchanged along with raw attempts and the spend ledger.

For a case where the agent must ask for a missing input, use
`requestsInput: {topic: <topic>}`. It passes on a question or a direct request
("Please upload the term sheet."). `asksAbout` keeps its original
question-only rule so frozen historical verdicts reproduce.

Offline tests: `python plugins/vc/scripts/test_deal_manager_suite_file.py`.
