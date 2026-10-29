---
id: generate-or-refresh-living-report
name: Generate or Refresh Living Report
description: >
  Create or refresh one durable project report from the complete current readable
  project evidence corpus. Use this skill for living VC reports that must discover
  newly linked evidence, keep each refresh as a new complete report, record their evidence basis,
  and explain source changes without relying on a manually maintained source list.
tags:
  - vc
  - reporting
  - evidence
  - living-document
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: required
      required: true
      note: Requires project/task-chat artifact discovery, artifact reads with revision or hash metadata, and a create text-artifact tool.
      gracefulDegradation: Stop and identify the unavailable discovery, read, or create capability; do not claim the report was generated or refreshed.
  routingHints:
    preferredSurface: skill
    notes:
      - Report-specific methodology, templates, output fields, and decision boundaries remain in the calling task definition.
---

# Generate or Refresh Living Report

Maintain one logical project report while its evidence corpus changes.

This lifecycle applies to living reports, not to a per-meeting brief or summary.
For meeting work, follow `meeting-prep-and-summary` and the calling task's output
contract instead; do not apply the corpus-wide manifest or report refresh
steps below. Preserve earlier meeting files and the living reports.

## Evidence Corpus

1. Enumerate the stable identities of all artifacts linked to the current project and task chat, then determine which are readable in the current authorization context. Retain the linked-but-unreadable set separately. Do not depend on Deal Manager-supplied inventory fields.
2. Exclude methodology and output templates, configuration or setup artifacts, the report artifact currently being regenerated, and earlier versions of that same report. On refresh, the supplied existing report is read only as the comparison baseline.
3. Add every readable upstream report or specially identified document declared by the task, even if it was not returned by the first general listing.
4. Add every readable artifact named by `focus_artifact_ids`. Focus IDs increase attention; they are never a whitelist and must not hide other project-linked evidence.
5. Deduplicate by stable artifact ID. For each readable included source, retain its observed revision and content hash before synthesis. If a linked or named source is unreadable, record it as unavailable and report that gap truthfully rather than inventing its contents or treating it as removed.

## Evidence-Basis Manifest

Embed this machine-readable JSON in the generated HTML inside an inert hidden element such as `<section hidden data-evidence-basis-manifest="v1"><pre>...</pre></section>`:

```json
{
  "schemaVersion": 1,
  "sources": [
    {
      "artifactId": "stable artifact ID",
      "observedRevision": "observed revision",
      "contentHash": "observed content hash",
      "role": "project evidence, upstream report, focus source, or task-identified document"
    }
  ],
  "unavailableSources": [
    {
      "artifactId": "stable linked or task-identified artifact ID",
      "role": "project evidence, upstream report, focus source, or task-identified document",
      "reason": "unreadable in the current authorization context"
    }
  ]
}
```

Sort both arrays by artifact ID for deterministic comparison. Keep `sources` limited to evidence actually read at the observed revision/hash. Use `unavailableSources` only for evidence that is still linked or specially identified but could not be read. Do not include template, configuration, or current-report artifacts in either array.

On refresh, read the prior manifest from the supplied existing report and compare it with the current corpus by stable artifact ID:

- `added`: linked and readable now but absent from both prior arrays;
- `changed`: present in both with a different observed revision or content hash;
- `removed`: present previously but no longer linked and no longer specially identified by the task;
- `unavailable`: still linked or specially identified now but unreadable in the current authorization context;
- `unchanged`: present in both with the same observed revision and content hash.

If a previously unavailable source becomes readable, classify the restored readability explicitly and compare against its last readable revision/hash when one exists. Never infer removal from an authorization, provider, indexing, or transient read failure.

Use the comparison to write a short visible “Changes since previous report” section when appropriate. Keep normal visible citations near material claims; the hidden manifest supplements rather than replaces them.
If a readable pre-existing report has no valid manifest, state that the prior evidence baseline is unavailable, add the first manifest during this refresh, and do not invent added/changed/removed classifications.

## Artifact Lifecycle

- First generation: create exactly one project-shared standalone safe static HTML report and return its artifact ID through the task-specific output field.
- Refresh: read the supplied existing report, its observed revision and content hash, and its prior manifest as the comparison baseline. Then create exactly one new project-shared standalone safe static HTML report containing the complete refreshed content, and return the new artifact ID through the same task-specific output field. The Deal then points at the new report; the earlier report stays unchanged as history.
- Earlier reports are immutable task evidence. Never edit, overwrite, or replace the supplied existing report, and never call a text-artifact update tool on it. This overrides any older or more general instruction to update a living report in place. Prepare the complete refreshed content before creating the new report; do not create a scaffold to edit later.
- If the existing report cannot be read, stop truthfully and create nothing. If the new report cannot be created, stop truthfully. Never create more than one new report in a run, and on a retry reuse a new report this run already created rather than creating another.

Apply the calling task's methodology, template, output field, and decision boundaries after establishing this shared lifecycle contract.
