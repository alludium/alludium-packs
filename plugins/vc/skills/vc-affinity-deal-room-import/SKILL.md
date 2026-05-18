---
id: vc-affinity-deal-room-import
name: "VC Affinity Deal Room Import"
description: >
  Import approved Affinity seed data into an already-created VC Deal Room project
  after Project Setup review and platform project creation.
tags:
  - vc
  - affinity
  - deal-room
  - import
capability:
  dependencies:
    - kind: skill-assignment
      importance: required
      required: true
    - kind: setup
      importance: required
      required: true
      owner: platform
      ownerPath: Create the target VC Deal Room project and pass the approved seed-deal import payload.
      confirmationRequired: true
      gracefulDegradation: Produce a blocked import receipt that names the missing approval or target project data.
  routingHints:
    preferredSurface: skill
    notes:
      - This task runs after project creation; setup tasks only collect seed selection and approval evidence.
---

# VC Affinity Deal Room Import

Use this skill only inside a created `vc_deal_room` project, after the user has reviewed and approved selected Affinity seed deals during Project Setup.

## Required Inputs

- Target Deal Room project ID from the platform-created project.
- Approved source scope from Affinity setup.
- Accepted stage mapping from Affinity setup.
- One approved seed deal for this project, including source object IDs, source URL, company identity, owner, and source stage when available.
- Approval metadata including approving user, approval time, and setup task or preview reference.

## Process

1. Confirm the task is project-scoped and the target project already exists.
2. Confirm the seed deal was selected from reviewed setup evidence or an approved preview.
3. Read only the approved Affinity records needed to complete the import receipt and project field map.
4. Map source fields to Deal Room fields such as company, domain, source system, source object, CRM URL, owner, source/referrer, and initial investment stage.
5. Produce an import receipt with provenance and unresolved gaps.

## Output Contract

Return:

- `import_status`: completed, partial, blocked, or failed.
- `import_summary`: concise summary of what was imported and what remained unresolved.
- `affinity_import_receipt_artifact_id`: durable receipt with source IDs, source links, field provenance, duplicate policy, approval evidence, and gaps.
- `imported_field_map`: compact field map in prose or table form.
- `source_index`: compact list of Affinity records read and how each was used.
- `next_task_recommendations`: compact list of suggested follow-up Deal Room tasks.

## Boundaries

- Do not create projects.
- Do not import unapproved Affinity records.
- Do not enable recurring sync.
- Do not write to Affinity, move stages, create notes, update external records, or send notifications.
- Do not create follow-up tasks unless a separate platform action explicitly approves them.
