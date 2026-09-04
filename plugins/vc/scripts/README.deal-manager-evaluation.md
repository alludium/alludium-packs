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
  --revision 915267b3e701a8be71ea788714e231fddd1b4c7d \
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
