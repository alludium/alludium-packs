# Fund persistence eval results (issue #4449)

Simulated prompt and tool-choice evidence for Platform issue #4449, produced by
`plugins/vc/scripts/compare_fund_persistence.py` on the Luna subject (`gpt-5.6-luna`, OpenAI Responses API)
against a simulated `project_data` tool. Recorded 2026-09-29. This is **not** Platform integration or
deployed proof; see [What this does and does not prove](#what-this-does-and-does-not-prove).

## Arms

| Arm | Prompt | Kickoff guard |
|---|---|---|
| `live` | `vc_deal_pipeline_manager` at tag `v0.6.29` (commit `9c6385713`), the version running on Dev during the #4449 QA | current Platform wording |
| `main` | `origin/main` at `c49c0f4` (includes #100 and #101) | current Platform wording |
| `candidate` | template `1.0.8` from this PR (prompt sha256 `1efeb81b9b18`) | proposed wording (paired Craft PR) |
| `candidate-prompt-only` | same template `1.0.8` | current Platform wording, unchanged |

The kickoff guard is the runtime instruction Platform attaches to the server-authored creation kickoff:
"...It authorizes Deal orientation only. Do not create or mutate tasks until the human user explicitly instructs you in this manager chat."
The proposed wording adds "plus saving the Fund the user explicitly named in the initial request when it resolves to exactly one active Fund".

## Results (10 cases x 3 repetitions per arm, scorer v2)

| Case | live | main | candidate | candidate-prompt-only |
|---|---|---|---|---|
| named-explicit | 0/3 | 0/3 | 3/3 | 3/3 |
| named-informal | 0/3 | 1/3 | 3/3 | 2/3 |
| named-with-screening-ask | 0/3 | 0/3 | 3/3 | 3/3 |
| ordinal-trap | 0/3 | 3/3 | 3/3 | 3/3 |
| no-fund-named | 3/3 | 3/3 | 3/3 | 3/3 |
| unknown-fund | 2/3 | 3/3 | 3/3 | 3/3 |
| ambiguous-fund | 3/3 | 3/3 | 3/3 | 3/3 |
| inactive-fund | 2/2 | 2/3 | 3/3 | 3/3 |
| manager-suggests | 3/3 | 2/2 | 3/3 | 3/3 |
| confirm-after-suggestion | 3/3 | 3/3 | 3/3 | 2/3 |
| **total** | **16/29** | **20/29** | **30/30** | **28/30** |
| Correct Fund written (4 creation-time must-save cases, 12 attempts each) | 2/12 | 5/12 | 12/12 | 12/12 |
| Fully passed (right write **and** a reply that says it was saved) on those 4 cases | 0/12 | 4/12 | 12/12 | 11/12 |

Cells are passed/scored attempts. `live` and `main` score 29 rather than 30 because one attempt in each hit a
provider error (unscored) and one more ended without a final reply (scored as a failure). Two `candidate-prompt-only`
attempts also ended at the 8-step limit without a final reply; no wrong Fund was saved in any attempt of any arm.

What each case requires (`evals/4449/expectations.yaml`):
- The four creation-time must-save cases need exactly one successful `fund_id` write of the correct stable id, in the
  first turn, and a reply that says that same Fund was saved and does not claim any other Fund was saved, confirmed, resolved,
  matched or selected. `confirm-after-suggestion` needs that write in the confirming second turn.
- The five must-not-write cases (`no-fund-named`, `unknown-fund`, `ambiguous-fund`, `inactive-fund`, `manager-suggests`)
  must not attempt any `fund_id` write, and the reply must not present any Fund as saved, confirmed, resolved, matched or
  selected (unknown, ambiguous and inactive Funds must also say it was not saved or is unresolved).
- Every case also requires no task creation, no lifecycle change, no invalid tool calls, and no Deal mutation other than
  saving `fund_id` (`noOtherMutations`: any other `update_state` field, `update_project`, attach/detach documents,
  `project.update`, `project.instantiateTemplate`, or an edit to the pre-existing deck; rejected attempts count). Creating
  and editing the evidence artifact the kickoff asks for is allowed.

## What works and what does not

- **The defect reproduces.** On the live prompt the correct Fund is written in only 2 of 12 creation-time must-save
  attempts, and none of the 12 fully pass: both writes were in the ordinal trap and neither reply said it was saved.
  That matches the Dev QA (0 of 3 Deals saved). Otherwise the manager resolves the Fund but does not save it, because the
  kickoff turn is recommendation-only. `main` writes it in 5 of 12 and fully passes 4 of 12; the one write that failed was
  a reply that did not say it was saved. Neither prompt is reliable.
- **The change fixes it.** `candidate` writes the correct Fund in 12 of 12, all fully passing, and refuses correctly in all
  five must-not-write cases, including the #4290 ordinal trap (it never picks a Fund by list position) and the ambiguous,
  unknown and inactive cases, with honest "saved" or "not saved (reason)" replies.
- **The prompt does most of the work.** `candidate-prompt-only` also writes 12 of 12 and fully passes 11 of 12; its lost
  point was a run that hit the step limit without a final reply. Across all cases it scores 28/30 to the candidate's 30/30.
  That difference is not statistically meaningful at this sample size. The guard wording is included so the two
  instructions do not contradict each other.
- **Unchanged flows still work.** `confirm-after-suggestion` (Deal B: the manager suggests, the human confirms, then it
  saves) passes in every arm except one `candidate-prompt-only` attempt that hit the step limit, so the change does not break the path that worked before.
- **What did not work first time** (kept so reviewers can see the iteration):
  - First candidate round, 27/30: two misses were the model sending a flat `data.fieldKey` instead of
    `data.fieldOptions.fieldKey`, then wrongly reporting the Fund lookup as unavailable. Template 1.0.8 now shows the exact
    call shape; this is the only change between that candidate and the one scored above.
  - One more miss in that round and one in the guard-only ablation were scorer false positives ("none was saved" and
    "could not be resolved" were not matched). The patterns were fixed and covered by tests, then every arm was re-run.
  - A guard-only ablation (old prompt, proposed guard) scored 18/20 on the first scorer. One miss was that false positive;
    the other was genuine: the model saved the Fund but its reply said "Fund 3 confirmed" instead of "saved", so it failed
    the honesty check. The reply wording comes from the prompt, not the guard.
  - The first smoke runs of the harness had a bug where artifacts the model created could not be read back; fixed before
    any scored run.

## What this does and does not prove

Proves, for this model and these frozen inputs: with the real kickoff message and guard, the current prompts do not save
a Fund the human named, and template 1.0.8 does, safely, and says so honestly.

Does not prove:
- **Live behaviour.** The tools, project state and Fund options are simulated. The `project_data` schema is a bounded copy
  of Platform's (`project-data-tool.json` records its source and omissions). A Dev browser check is still required: create
  a Deal with "The Fund for this Deal is Fund 2" and confirm the Deal header, the Pipeline Fund filter and the manager's
  reply agree after a reload. The #4449 QA also pre-dated Platform #4465 (`strict: false` on OpenAI tools), which this
  harness already sends.
- **Statistical certainty.** Three repetitions per case per arm on one model.
- **Independence.** Candidate wording and scorer patterns were refined after seeing the first round's failures; the ten
  cases and expectations were not changed. After independent review the scorer gained `noOtherMutations` and a reply check
  against the Fund actually saved (past-tense assertions, each verb judged in its own clause so a negated first claim cannot hide a second one; conditional, modal or negated phrasing is not a claim),
  and every saved run was re-scored (`--rescore`, no spend). The re-score moved two `live` results from fail to pass (replies
  the earlier regex missed, such as "The Fund cannot yet be confirmed or recorded"); no other verdict changed.
- **The reply check is still heuristic.** It is a set of patterns, not a judge. To make the results auditable,
  `results/final-attempts.json` includes each attempt's final reply (bounded to 4,000 characters, so nearly all are complete), and all 30 `candidate`
  replies were read by hand: each says "saved" for the correct Fund, or "not saved" with the reason where nothing should be saved.
- **Other models or providers.**

## Run identity and cost

- Runner `compare_fund_persistence.py` sha256 `e6fddab2fd07`, cases `e1e6da90e6c5`, expectations `e1869258f6db`.
- Spend at Platform-billable rates: live $0.35, main $0.36, candidate $0.11, candidate-prompt-only $0.13. Each run had its own ceiling and a wall-clock cap.
- `results/final-attempts.json` lists every attempt (arm, case, repetition, status, assertions, Fund writes attempted).
  Raw provider requests and responses are not committed.

## Reproduce

```sh
python plugins/vc/scripts/compare_fund_persistence.py --arm live=v0.6.29 --arm main=origin/main \
  --arm candidate=origin/fix/4449-record-named-fund+guard=proposed \
  --arm candidate-prompt-only=origin/fix/4449-record-named-fund \
  --execute --output /tmp/fund-persistence --max-spend-usd 2 --max-wall-minutes 45
```

Needs `OPENAI_API_KEY`. Arms accept a git revision or `file:PATH`; `+guard=proposed` selects the proposed kickoff guard.
