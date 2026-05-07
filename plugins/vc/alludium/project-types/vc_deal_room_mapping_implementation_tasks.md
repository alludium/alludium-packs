# VC Deal Room Schema And Mapping Implementation Tasks

Status: active implementation checklist

This checklist turns `vc_deal_room_task_io_audit.md` into implementation slices. Keep each slice reviewable on its own: the goal is a compact project control plane plus explicit artifact-first task I/O, not a copied dossier of every task field.

## Slice 1: Project Type Shape

- [x] Collapse lifecycle states to `intake`, `assessment`, `diligence`, `review`, `term_sheet`, `closing`, plus terminal outcomes `invested`, `passed`, and `archived`.
- [x] Update lifecycle transitions to support the collapsed flow and terminal outcomes.
- [x] Reshape `fieldsSchema` into ordered Data-tab sections using current flat-field ordering:
  1. Deal identity and source
  2. Source materials and working links
  3. Stage and decision state
  4. Assessment inputs
  5. Diligence inputs
  6. Review, term sheet, and closing state
  7. Artifact index
- [x] Prefer artifact ID/source-reference fields over URLs where task inputs should use uploaded files.
- [x] Update command-view stage groups to the collapsed lifecycle.

## Slice 2: Task Template I/O Rewrite

- [x] Move task `definitionJson.stage` values onto the collapsed stage model.
- [x] Replace `pitch_deck_url` with `pitch_deck_artifact_id` in assessment tasks.
- [ ] Replace transcript/material/document free-text inputs with artifact-reference inputs where the task needs platform files. Initial pass covers meeting transcript and term sheet; diligence and closing source materials remain.
- [ ] Remove `prior_task_outputs` from inputs and context.
- [ ] Remove broad context fields unless a task has a specific runtime-only reason to receive them.
- [ ] Fold detailed structured outputs into the primary file artifact where a required file output exists.
- [ ] Decide whether `run-follow-up-evaluation`, `prepare-lead-gen-packet`, and `prepare-deal-flow-agenda` remain Deal Room mapped tasks or move to optional/pipeline-only use.

## Slice 3: Project Task Mappings

- [ ] Add `projectTaskMappings` to `vc_deal_room.json` after task field shapes are updated.
- [ ] Map required task inputs from durable project fields or explicit artifact fields only.
- [ ] Map required file outputs back to artifact-index project fields.
- [ ] Promote only compact reviewed state outputs, such as decision outcome, closing status, readiness, and terminal outcome.
- [ ] Use manual-review activation and keep auto-start disabled.

## Slice 4: Validation

- [ ] Validate task mappings reference real project fields and real task fields.
- [ ] Enforce manual-review activation for public pack mappings.
- [x] Reject unknown lifecycle stages in task templates and command-view stage groups.
- [ ] Add guardrails against `prior_task_outputs` and broad context mappings returning in VC Deal Room templates.
- [x] Keep existing artifact file-field validation passing.

## Slice 5: Review And Handoff

- [x] Run `python3 plugins/vc/scripts/validate_pack.py`.
- [x] Run `git diff --check`.
- [ ] Review the diff against the audit before opening the PR.
- [ ] Document what is declarative only versus what is enforced by the pack validator.
