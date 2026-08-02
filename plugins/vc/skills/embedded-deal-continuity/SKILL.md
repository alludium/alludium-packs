---
id: embedded-deal-continuity
name: Embedded Deal Continuity
description: >
  Produce one provisional, cited First Look, What Changed, and Next Decision
  bundle from adapter-supplied evidence, revisions, authorities, and S0/S1
  consequences. Use this skill for evidence-continuity updates that must retain
  explicit human investment authority and must not automate an invest/pass
  disposition.
tags:
  - vc
  - evidence-continuity
  - change-review
  - human-approval
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: tool
      importance: recommended
      required: false
      note: The method consumes evidence and change state supplied by the invoking task or Platform adapter; it does not require provider calls.
      gracefulDegradation: Stop with contract errors when required evidence, revision, citation, or authority identity is absent.
  routingHints:
    preferredSurface: skill
    notes:
      - Use the exact method identity and schema in references/method-run.schema.json.
      - The generated bundle is provisional until a human approves, edits, or rejects it outside this method.
---

# Embedded Deal Continuity

Use method `vc.embedded-deal-continuity` version `1.0.0` to produce three
coherent outputs from one cited input packet:

1. **First Look** — the useful current view, with claims, citations,
   uncertainty, evidence state, and authority status. It is not a final
   investment recommendation.
2. **What Changed** — an exhaustive account of adapter-supplied changes across
   `added`, `preserved`, `stale`, `superseded`, `conflicting`, and `unresolved`.
3. **Next Decision** — one consequential unresolved question, missing-evidence
   request, or explicitly human-owned judgment. It must never encode an
   automatic invest/pass disposition.

The machine-readable run contract is
[`references/method-run.schema.json`](references/method-run.schema.json). A
public-neutral complete run is in
[`references/examples/public-neutral-s1-run.json`](references/examples/public-neutral-s1-run.json).

## Ownership Boundary

- The Platform adapter owns the input identities and supplies cited evidence
  claims plus S0/S1 consequences. Preserve those identities; do not silently
  repair, reclassify, or infer them.
- The Fund or mandate method owner supplies a named method revision as context.
  Record that revision without inventing a universal Fund ontology.
- This method owns the three provisional output structures and their evaluation
  semantics.
- Humans own Fund-relative meaning, investment posture, IC export, and final
  judgment.

## Input Gate

Before composing output, validate the input against `$defs.input` in the
schema. Stop and report the exact contract error if any of these are absent or
invalid:

- method ID and version;
- Deal reference;
- Fund/mandate method revision and its citation;
- current authority context and required human approval owner;
- source revision registry;
- resolvable citations with source, revision, and locator;
- cited evidence claims with evidence state, authority, and uncertainty; or
- S0/S1 change consequences with one of the six allowed change categories.

Do not fetch private data, call providers, fill gaps with general knowledge, or
invent citations. A missing required identity is a failed input, not permission
to approximate.

## Composition Rules

### First Look

- Use only claims present in `evidenceClaims`.
- Keep the claim's citation IDs, evidence state, authority ID/status, and
  uncertainty explicit.
- A stale, superseded, conflicting, or unresolved claim may be mentioned only
  with that state visible. Never flatten it into current fact.
- Summarise what the evidence supports now and name material limitations.
- Do not emit a final screening recommendation, score, investment posture, or
  IC decision.

### What Changed

- Place every supplied change exactly once in its matching bucket:
  `added`, `preserved`, `stale`, `superseded`, `conflicting`, or `unresolved`.
- Preserve the adapter-supplied S0/S1 label; do not derive a new state model.
- Carry the linked claim IDs, citation IDs, authority statuses, consequence, and
  uncertainty into each item.
- Keep stale, superseded, conflict, and unresolved buckets visible even when
  empty. Never hide a non-current state by omission or by relabelling it
  `preserved`.

### Next Decision

- Choose exactly one `unresolved_question`, `missing_evidence`, or
  `human_judgment` item based on consequence, not convenience.
- State why it matters, what evidence would help, who owns the decision, which
  claims/citations support it, and the remaining uncertainty.
- The owner must be the input's human investment authority.
- Do not add `disposition`, `recommendation`, `score`, `invest`, `pass`, or any
  equivalent automatic posture field. Human decision options may be discussed
  only as a question that remains human-owned.

## Revision And Authority Rules

- A citation resolves only when its `(sourceId, revisionId)` exists in the
  source revision registry.
- A claim presented as `current` cannot rely on a stale or superseded source
  revision or on stale/revoked authority.
- Output claim state and authority status must match the input registries.
- Echo the exact Fund/mandate method revision into the revision receipt.
- List the exact source revisions and change IDs used. Do not substitute a newer
  or older revision silently.

## Approval Boundary

Every generated output must end with:

- `status: pending_human_review`;
- `postureAuthoritative: false`;
- `icExportAuthoritative: false`;
- the named human review owner; and
- allowed actions `approve`, `edit`, and `reject`.

Approval, editing, rejection, posture recording, and IC export happen outside
this generation method. Completing the task confirms that the provisional
bundle is ready for review; it does not make the content authoritative.

## Evaluation

Use
[`references/evaluation-rubric.v1.yaml`](references/evaluation-rubric.v1.yaml)
for regression and comparison. Critical citation, wrong-revision,
stale-authority, unsupported-claim, or automated-judgment failures fail the
method. Compare usefulness against strong same-source cited prose. A tie or
complexity without measured benefit favours cited prose.

## Related Skills

- `citation-enforcement` — citation and unsupported-claim review
- `investment-diligence-question-framework` — decision-relevant questions
- `investment-screening-framework` — existing Fund-relative screening method;
  do not import its disposition logic into this continuity method
- `ic-risk-checklist-and-decision-log` — downstream human-owned decision record
