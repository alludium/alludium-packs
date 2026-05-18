---
id: vc.document.file_naming_source_index_sop
title: File Naming And Source Index SOP
documentType: sop
supportedProjectTypes:
  - vc_deal_room
  - vc_origination_pipeline
summary: Operating convention for naming files and maintaining source indexes.
---

# File Naming And Source Index SOP

## Purpose

Use this SOP to keep Deal Room and Origination artifacts traceable across task outputs, uploaded files, CRM references, and document workspaces.

## Naming Pattern

Use `YYYY-MM-DD_company_or_pipeline_document-purpose_source-or-owner_vNN`. Keep names plain and stable. Avoid personal local paths, private nicknames, or source-system IDs as the only human-readable identifier.

## Source Index Fields

- Source title
- Source type
- Source owner
- Source date
- Artifact ID or URL
- Related task
- Evidence quality
- Reuse restrictions
- Notes and open questions

## Maintenance Rule

Update the source index when a task creates or consumes a durable file artifact. If a file is superseded, link the replacement instead of deleting the earlier reference.
