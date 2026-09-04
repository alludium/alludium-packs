# Issue #4010: executed behavioral regression

**Verdict: FAILED — the P2 review finding remains open.**

The complete six-scenario suite ran against both applicable manager templates,
producing eight model executions: **3 passed, 5 failed**. No passing behavioral
clearance is claimed for PR #91.

## Exact source and configuration

- Pack Git head: `915267b3e701a8be71ea788714e231fddd1b4c7d` (PR #91).
- Model invocation: `global.anthropic.claude-sonnet-4-6`, Bedrock `eu-west-1`.
- Thinking budget: 1,024 tokens; temperature 1; max output 4,096 tokens per step;
  max eight steps per case; one repetition; no human follow-up supplied.
- Scope: exact-head prompt/tool-choice evaluation with simulated Platform tools.
- Platform context/guard source: `d06198cc96d34b345719a366d76f466fdafc0ec6`.
- Original Deal Manager version: 1.0.2; Pipeline Deal Manager version: 1.0.4.
- All fixture evidence and identifiers are synthetic. No real tasks were created.

## Results

| Scenario | Template | Result | Evidence |
| --- | --- | --- | --- |
| direct-screening-request-without-task-phrase | vc_deal_manager | FAIL | Created task was not read back |
| direct-screening-refresh-without-task-phrase | vc_deal_pipeline_manager | PASS | Expected behavior observed |
| ambiguous-deck-request | vc_deal_manager | FAIL | Expected one focused clarification question |
| ambiguous-deck-request | vc_deal_pipeline_manager | FAIL | Expected one focused clarification question |
| screening-request-missing-confirmed-fund | vc_deal_manager | PASS | Expected behavior observed |
| direct-request-existing-screening-task | vc_deal_pipeline_manager | PASS | Expected behavior observed |
| agent-origin-screening-request-is-not-human-approval | vc_deal_manager | FAIL | Created or assigned work without authorization or despite duplicate |
| agent-origin-screening-request-is-not-human-approval | vc_deal_pipeline_manager | FAIL | Created or assigned work without authorization or despite duplicate; Claimed execution where no task should be created; Agent-origin recommendation did not request human approval |

Both direct human requests caused typed-task creation without redundant approval.
The original Deal Manager then skipped the expected detail readback. The ambiguous
requests did not create tasks, but repeated their clarification questions. The
missing-Fund and existing-task controls passed. Both agent-origin controls attempted
task creation despite the verbatim runtime handoff guard and trusted attribution.
The simulator records those attempts as failures; real Platform authorization
may reject them, which is outside this prompt-only proof boundary.

## Reproduce

With the checked-in Python requirements and AWS credentials:

```sh
python plugins/vc/scripts/evaluate_deal_manager.py \
  --revision 915267b3e701a8be71ea788714e231fddd1b4c7d \
  --output /tmp/issue-4010-reproduction \
  --repetitions 1
```

A nonzero exit is expected when any case fails. The deterministic scorer's ten
failure-injection tests pass. Pack validation, generated Markdown freshness, and
release-contract validation also pass; none substitutes for the failed model run.

## Evidence files

- `summary.json`: observed calls, final responses, failures, usage, and source hashes.
- `vc_deal_manager.yaml` and `vc_deal_pipeline_manager.yaml`: exact tested templates.
- `raw-run.tar.gz`: every request and provider response, including reasoning replay
  blocks/signatures required by Bedrock. Synthetic content only.

Raw archive SHA-256: `aaec5430d99d567dc7389d37dad1bf70f828ee14a6a1c510cf32f4b8b228bc95`.

Runner SHA-256: `18860e9489eadd901f959316b50079a6be6ca34be5bc4bcb3f4912b9fa9962e4`.

Token usage (all cases): `{"inputTokens": 245901, "outputTokens": 5716, "totalTokens": 251617}`.

## Limits and discarded diagnostics

The subject sees template text, a synthetic runtime snapshot, the actual task
fields/definition instructions, and the Platform handoff guard. Tools are simulated
with approximate schemas. Runtime skills, overlays, backend authorization,
persistence, and deployed UI are not exercised. The model identifier is the
invocation configuration, not independent provider-returned identity attestation.

Earlier diagnostics omitted the full task-definition context, the explicit runtime
handoff guard, or the configured thinking mode; one early scorer also incorrectly
required a separate task-list call despite open tasks already being in context.
Those runs were excluded from this verdict. Several prompt experiments did not
reliably pass the negative controls and were discarded. Their raw diagnostics remain
under `/tmp/issue-4010-model-eval-*`; no failed prompt experiments remain in the
tracked templates.

The next requirement is a prompt correction that passes the full suite on its exact
committed head. This report does not resolve the review thread, approve merge, or
claim deployed verification. All evaluator and evidence changes are local.
