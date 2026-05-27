---
id: vc.document.file_naming_source_index_sop
title: File Naming And Source Index SOP
documentType: sop
supportedProjectTypes:
  - vc_deal_room
  - vc_origination_pipeline
  - vc_investment_management
summary: Operating convention for naming files and maintaining source indexes.
---

# File Naming And Source Index SOP

## Purpose

Use this SOP to keep Deal Pipeline and Origination artifacts traceable across task outputs, uploaded files, CRM references, and document workspaces.

## Naming Pattern

Use `YYYY-MM-DD_company-or-pipeline_document-purpose_source-or-owner_vNN`.

Examples:

| Artifact | Example Name |
| --- | --- |
| Initial call brief | `2026-05-18_acme-ai_initial-call-brief_task_v01` |
| Diligence report | `2026-05-18_acme-ai_financial-dd-report_team_v02` |
| Sourcing digest | `2026-05-18_ai-infra-pipeline_sourcing-digest_apify_v01` |

Keep names plain and stable. Avoid personal local paths, private nicknames, or source-system IDs as the only human-readable identifier.

## Source Index Fields

| Field | Guidance |
| --- | --- |
| Source title | Human-readable title, not only a system ID |
| Source type | Pitch deck, transcript, CRM note, model, filing, call note, source run |
| Source owner | Founder, firm, task, external provider, public source |
| Source date | Publication, meeting, retrieval, or task-run date |
| Artifact ID or URL | Durable reference for retrieval |
| Related task | Task that created or consumed the source |
| Evidence quality | High, medium, low, stale, partial, or unverified |
| Reuse restrictions | Confidential, founder-provided, counsel-only, internal-only |
| Notes and open questions | Gaps, contradictions, and follow-up needed |

## Maintenance Rule

Update the source index when a task creates or consumes a durable file artifact. If a file is superseded, link the replacement instead of deleting the earlier reference.
