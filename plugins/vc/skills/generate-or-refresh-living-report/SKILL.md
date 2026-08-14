---
id: generate-or-refresh-living-report
name: Generate or Refresh Living Report
description: >
  Create or refresh one durable project report from the complete current readable
  project evidence corpus. Use this skill for living VC reports that must discover
  newly linked evidence, preserve artifact identity, record their evidence basis,
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
      note: Requires project/task-chat artifact discovery, artifact reads with revision or hash metadata, and create/update text-artifact tools.
      gracefulDegradation: Stop and identify the unavailable discovery, read, create, or update capability; do not claim the report was generated or refreshed.
  routingHints:
    preferredSurface: skill
    notes:
      - Report-specific methodology, templates, output fields, and decision boundaries remain in the calling task definition.
---

# Generate or Refresh Living Report

Maintain one logical project report while its evidence corpus changes.

## Evidence Corpus

1. Enumerate all artifacts linked to the current project and task chat that are readable in the current authorization context. Do not depend on Deal Manager-supplied inventory fields.
2. Exclude methodology and output templates, configuration or setup artifacts, and the report artifact currently being regenerated.
3. Add every readable upstream report or specially identified document declared by the task, even if it was not returned by the first general listing.
4. Add every readable artifact named by `focus_artifact_ids`. Focus IDs increase attention; they are never a whitelist and must not hide other project-linked evidence.
5. Deduplicate by stable artifact ID. For each included source, read and retain its observed revision and content hash before synthesis. If a named source is unreadable, report that gap truthfully rather than inventing its contents.

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
  ]
}
```

Sort sources by artifact ID for deterministic comparison. Do not include template, configuration, or current-report artifacts in the manifest.

On refresh, read the prior manifest from the supplied existing report and compare it with the current corpus by stable artifact ID:

- `added`: present now but absent previously;
- `changed`: present in both with a different observed revision or content hash;
- `removed`: present previously but no longer linked or readable;
- `unchanged`: present in both with the same observed revision and content hash.

Use the comparison to write a short visible “Changes since previous report” section when appropriate. Keep normal visible citations near material claims; the hidden manifest supplements rather than replaces them.
If a readable pre-existing report has no valid manifest, state that the prior evidence baseline is unavailable, add the first manifest during this refresh, and do not invent added/changed/removed classifications.

## Artifact Lifecycle

- First generation: create exactly one project-shared standalone safe static HTML report and return its artifact ID through the task-specific output field.
- Refresh: read the supplied existing report and its source metadata, then update that exact artifact in place using its observed revision and content hash. Return the same artifact ID.
- If the existing report cannot be read or the in-place update fails because of revision, hash, authorization, or tool errors, stop truthfully. Never create a duplicate fallback.

Apply the calling task's methodology, template, output field, and decision boundaries after establishing this shared lifecycle contract.
