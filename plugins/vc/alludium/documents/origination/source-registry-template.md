---
id: vc.document.source_registry_template
title: Source Registry Template
documentType: template
supportedProjectTypes:
  - vc_origination_pipeline
  - vc_sourcing_line
summary: Shared catalog of reusable origination source connections and approved scopes.
---

# Source Registry Template

This is the shared connection catalog for an Origination Pipeline. It records reusable providers and approved connection scopes. It does not define sourcing lines. A sourcing line references one or more registered sources and separately owns its query, screen, cadence, review policy, outreach policy, and performance history.

## Registry

| Source Key | Provider / Surface | Source Type | Owner | Connection State | Approved Connection Scope | Capabilities | Shared Cost Policy | Last Validation | Known Issues | Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | CRM / database / public source / paid source / manual |  | Ready / Missing / Expired / Blocked | Accounts, actors, endpoints, regions, or collections the connection may access | Discovery / enrichment / relationship / write-gated | Free / budget ceiling / per-run approval / disabled |  |  | Available / degraded / blocked / retired |

## Source Setup Notes

| Source Key | Setup Artifact | Dry Run Result | Approval Status |
| --- | --- | --- | --- |
|  |  | Pass / Issue / Blocked | Approved / Pending / Rejected |

## Usage

Keep this registry compact and operational. Credentials remain in the platform connection store, never in this artifact. Provider setup details can live in linked setup notes. Query filters, cadence, result limits, Inbox thresholds, outreach rules, cursors, and run history belong to Sourcing Line projects.
