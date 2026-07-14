# Brain + Lean Workers POC3 — VC Pack Changes

This document describes the pack-side changes on `codex/bare-brain-lean-runtime-poc3`. The matching
platform implementation uses the same branch name in the internal platform repository; the shared
technical briefing links both review surfaces.

## Size and scope

Before this note, the pack POC changed 26 files relative to its main-branch base: approximately
1,248 insertions and 8 deletions.

The branch contains the complete POC evolution:

- POC1: delegated product-chat sourcing variant;
- POC2: smaller product-chat worker templates;
- POC3: bare decision brain, chatless lean workers and deterministic script comparison.

The change is intentionally additive. It does not rewrite the 92 production task definitions.

## New agent contracts

### `orchestrator_minimal`

The minimal brain:

- has no skills;
- uses `capabilityProfile.baseline: NONE`;
- declares only `orchestrate.delegate` and `orchestrate.finish`;
- is restricted to decision, retry, sufficiency, reconciliation and finalization;
- must exchange bounded references/counts/warnings rather than source or document bodies;
- cannot perform research, artifact creation, external writes or project/task mutation directly.

### `vc_lean_worker_minimal`

This records the intended zero-skill, one-role-at-a-time lean contract. It receives only explicitly
allowed capabilities, cannot delegate, cannot mutate external systems and returns bounded result
references.

Important implementation detail: the final eval harness did not instantiate this template. It
reused inline-created `vc_worker_minimal` deployments to resolve the exact connector configuration,
then bypassed their product-chat runtime and supplied the filtered tool directly to `LeanExecutor`.
The lean template is therefore a proposed pack contract, while the chatless platform path is the
part that was actually exercised.

### `vc_worker_minimal`

This is the POC2 product-chat comparison worker. Its eval-created deployments were also reused as
connector-configuration containers by POC3, but their chat execution path was bypassed. The
product-chat worker itself is not the recommended runtime.

## Five experimental task definitions

The branch adds five POC-only variants and registers them in the catalog/project-type metadata:

- `run-vc-sourcing-pipeline-delegated` — POC1/POC2 nested product-chat comparison;
- `run-vc-sourcing-pipeline-brain` — POC3 minimal brain;
- `run-vc-sourcing-pipeline-script` — deterministic sourcing ablation;
- `summarize-meeting-records-brain` — POC3 meeting decision brain;
- `summarize-meeting-records-script` — deterministic meeting ablation.

These variants let the eval harness compare architectures without changing production task behavior.
They should not become permanent duplicate product workflows. A production migration should add a
versioned execution contract to canonical definitions and remove the experimental variants.

## Were existing pack definitions extensively changed?

No. Existing production workflow bodies were not broadly rewritten. Besides plugin/catalog version
and inventory registration, the branch changes the VC deal-room and origination project-type JSON so
the POC definitions can be instantiated, and adds generated Markdown documentation for the new
templates/tasks.

The 92-workflow assessment was a static contract audit, not 92 runtime edits or executions.

## Pack-wide fit and the corrected count

The final audit classified:

- 62 analysis/document/artifact workflows as direct lean composition fits;
- 18 discovery/sync-read/write-proposal workflows as bounded connector/receipt fits;
- 1 sourcing parent pipeline as a direct brain-at-the-gates fit;
- 11 guided setup/project-creation workflows as hybrid control-plane fits.

There is no final 13-workflow exception list. The audited non-one-shot group is 11:

1. `affinity-setup`
2. `apify-setup`
3. `companies-house-setup`
4. `google-drive-setup`
5. `harmonic-setup`
6. `notion-setup`
7. `slack-setup`
8. `vc-pack-variable-discovery`
9. `configure-origination-pipeline`
10. `create-deal`
11. `capture-investment-management-handoff`

They deliberately run phased question/answer loops, persist user choices, pause/resume and hand an
approved payload to deterministic platform creation/finalization. A one-shot chatless worker would
regress that behavior.

They become safe fits when the platform supplies:

- a durable guided question and answer journal;
- explicit phase/defer/resume state;
- narrow read-only preview/validation workers;
- immutable approval evidence;
- deterministic idempotent finalizers/actuators.

## What the POC did not establish

- It did not execute the other 90 production definitions.
- It did not define a generic open-source contributor execution schema.
- It did not prove arbitrary tool metadata can be trusted to distinguish reads from mutations.
- It did not solve large-document reading, multi-artifact transactions or cross-process resume.
- It did not make external mutation a worker capability.

Those are productization concerns, not reasons to restore nested full-agent workers.
