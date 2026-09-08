# Run attribution Pack companion — 6 September 2026

This is the Pack companion to Platform issue #4063
and PR #4073, Platform head
`89c148a334643659708bb97e4c895e383f8a49fc`. It is stacked on Pack #92 at
`855377c49b34fda783128337427a1c91391c2811`; the frozen #4072 validation pair is unchanged.

Source review found that Run VC Sourcing Pipeline still instructed the model to write Line status,
count and artifact summary fields. Platform now derives these from the exact attributed task and
committed finalization records. Removed that conflicting instruction, kept artifact IDs in the run
output and explicitly separated proposed candidates from created records. Registration carries the
exact originating sourcing run only when a run exists. Manual registration retains its existing
three required inputs and omits optional attribution. Invalid supplied attribution must be corrected,
not silently erased to evade validation.

Bumped the two changed task template versions and proposed Pack 0.6.27, including plugin/catalog/docs
references. This is an unreleased version: no tag, publish, deployment or installed runtime was changed.
Generated Markdown remains derived from the canonical YAML. Tests check the manual/run distinction,
exact-run handoff and the proposal-versus-created boundary; they do not prove native agent behavior.

Validation: full Pack validation passed (100 task templates), generated Markdown check passed
(123 files), release contract passed against the exact stacked base, and all 39 Python contract
tests passed. The new test is included in CI. Live paired/native/hosted validation remains pending;
these instructions require Platform #4073 and must not be presented as already deployed.

## 7 September — refresh after Pack #94 merged

Rebased onto main `380fc7ee1f49cbca67db8be117cf0d149cff6141`, which merged #94
and advances the Pack to 0.6.27. Resolved the README conflict by preserving the
0.6.26 Origination and 0.6.27 Deal Pipeline discovery history and adding a separate
0.6.28 run-attribution entry. Advanced both plugin manifests, Pack manifest,
inventory, ontology release provenance and derived package hashes to proposed
0.6.28. Component content, semantic versions and component hashes are unchanged.

Compared the incoming agent templates, generated agents/blueprints, generator and
connected-app tests directly with main: identical. Compared both Origination task
YAML files and their run-attribution regressions with previous head `e74458d`: identical.
The workflow and validator retain both incoming discovery checks and run-attribution checks.
No additional product-contract repair was required by this rebase.

Validation: full Pack validator passed (100 tasks); generated Markdown check passed
(123 files); release contract passed against main 0.6.27; all 43 Python contract tests
passed in 153.015 seconds; diff check passed. Accumulated author review against
main `380fc7e` passed for the Pack declaration/generated-contract scope, with no
remaining P1/P2 in that scope. These checks do not establish runtime acceptance.

Compatibility: inherited Pack #94 requires the role bundles in merged Platform
#4076 (`b3b082580144b95d216c858699a443562a9f7e6c`). The older local #4072 foundation
must be refreshed before ingesting the new Pack. Platform #4073 must update its
exact commit/archive/version and rerun the paired checks; its owner is coordinating
that separately. Draft and browser/native/hosted gates remain open. No tag,
deployment, workspace ingest or release publication was performed.

## 8 September — native promotion company-name repair

Fresh native execution on Platform `d7b7fff9ce1d445d025c1d82479a3eeb765f1e98`
with Pack `bd761f2803b70dd6a794d94a446b93893142b061` repaired the previous unsupported
Candidate-ID field but produced only `fieldValues.fund_id`. Platform correctly rejected review
with `Promotion requires a company name.` Reopening the same task and explicitly adding the
Candidate's canonical `company_name` produced one Deal, one canonical promotion relationship and
one promotion audit record; browser replay and API replay both reused that Deal. This is recovered
success, not fresh first-attempt acceptance.

The promotion template now requires the Candidate's canonical non-empty
`createRequest.fieldValues.company_name` in its instructions, missing-input policy, completion
criteria, required paths and JSON schema. The existing prohibition on
`fieldValues.origination_candidate_project_id` remains intact. The task template advances from
`0.1.16` to `0.1.17`; Pack version remains the unreleased proposed `0.6.28`.

Validation: all 47 Python contract tests passed, including the new company-name schema regression;
full Pack validation passed, generated Markdown is current across 123 files, the release contract
passed against main 0.6.27, and `git diff --check` passed. A fresh first-attempt native run on the
new exact Pack head remains required after the paired Platform fixture is repinned.
