# Origination Project Model Migration

## Scope

Pack `0.6.0` separates the legacy all-in-one `vc_origination_pipeline` into:

- `vc_origination_pipeline`: fund-level source registry, shared policy, budgets, cross-line Inbox, digest, and health.
- `vc_sourcing_line`: one repeatable experiment with a dedicated chat, source mix, screen, cadence, schedules, receipts, and metrics.
- `vc_origination_candidate`: one deduplicated pre-deal company with multi-line provenance, screening, relationship, outreach, and promotion state.

Existing project instances are not automatically rewritten. Historical tasks and artifacts remain evidence, but legacy schedules must stay disabled until a human reviews the proposed migration.

## Clean Install And Existing Instances

On a clean install, the hub guided-creation chat is the configuration step. Its default `draft` state intentionally has no mapped draft task, avoiding a duplicate Configure Origination Pipeline task after creation. A newly created line has exactly one draft task, Configure Sourcing Line; a newly registered candidate has exactly one identified-state task, Screen Identified Candidate.

For an existing workspace, installing the pack adds definitions but does not backfill project instances, relationships, or schedules. Operators must run the migration procedure below, create native relationships with reviewed IDs, and keep denormalized ID fields only for rollout provenance. The pack emits structured creation and relationship proposals; the platform creation finalizer remains responsible for atomic writes and returned project IDs.

## Relationship Contract

The native target relationships are:

- `vc.origination_pipeline_contains_sourcing_line`
- `vc.sourcing_line_originated_candidate`
- `vc.origination_candidate_promoted_to_deal`

The new project types retain denormalized compatibility ID fields during rollout for provenance, migration inspection, and older consumers. Native project relationships are authoritative; text IDs are not a substitute for referential integrity and must not be treated as proof that the target project exists.

## Migration Procedure

1. Keep the existing `vc_origination_pipeline` project as the fund-level hub.
2. Preserve its source registry as the shared provider/connection catalog. Remove query, cadence, and outreach experiment detail from source rows only after corresponding lines are created.
3. Inventory every enabled legacy schedule. Group schedules by coherent experiment: source mix, query/screen, cadence, review policy, and outreach policy.
4. Create one draft `vc_sourcing_line` for each coherent experiment and its canonical chat. Link it to the hub, review its configuration, cursor/window, spend guardrail, and historical receipts, then move it to paused without enabling schedules.
5. Do not create one line per provider unless the provider configuration is genuinely the whole experiment.
6. Deduplicate historical candidate batches by stable company/domain/source keys. Create one `vc_origination_candidate` per company and link all originating lines and source receipts.
7. Map legacy pipeline candidate states:
   - `identified` to `identified`
   - `enriched` or `initial_screen` to `enriched`
   - `prioritized` to `qualified`
   - `outreach_prep` to `outreach_ready`
   - `contact_attempts` to `contacted`
   - `engagement_screen` to `engaged`
   - `watchlist` to `watchlist`
   - `pass` or `no_response` to a human-reviewed `passed` or `watchlist`
   - `promoted_to_deal_pipeline` to `promoted` only when a real Deal Pipeline project is identified
8. Recreate schedules on their line projects in a disabled state. Run a dry-run comparison before approval.
9. Retire legacy pipeline-level discovery, screening, outreach, and candidate-promotion mappings. Keep only hub configuration, cross-line digest, and shared source-health work.
10. Record migration receipts with old project/task/artifact IDs, new project IDs, relationship proposals, unresolved duplicates, and the approving human.

## Safety

- Migration does not send outreach, spend on sources, write to CRM, or create Deal Pipeline projects.
- Preserve manual decisions, relationship owners, do-not-contact status, and opt-outs.
- If provenance or identity is ambiguous, keep the legacy record and create a review task instead of guessing.
- Do not enable line schedules until credentials, budgets, result limits, and dry-run output have been reviewed.
