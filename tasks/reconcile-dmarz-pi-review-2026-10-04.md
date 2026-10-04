---
id: reconcile-dmarz-pi-review-2026-10-04
type: task
title: Incorporate and respond to Dmarz PI recommendations
kind: admin
status: done
priority: p1
owner: vishesh/codex-pi-review
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-pi-review
depends_on: []
topics: []
claimed_at: 2026-10-04T03:54Z
updated: 2026-10-04T04:05Z
outputs:
- researchers/vishesh/notes/pi-review-response-dmarz-2026-10-04/README.md
- researchers/vishesh/notes/pi-review-response-dmarz-2026-10-04/response.json
---

## Goal

At the user's request, reconcile the PI recommendations pinned at e0a3170 with current evidence and existing owner plans, incorporate defensible methods improvements, and publish an item-by-item response. Preserve historical reviews and running protocols; no new experiments or budget allocation.

## Done when

- [x] Reconcile each current-study item, successor, shared rule and retained direction.
- [x] Incorporate useful methods changes without duplicate implementation lanes.
- [x] Commit a sourced response and incorporate changes directly in relevant study documents.
- [x] Validate documents and repository, then push.

## Coverage note

All 27 portfolio items reconciled at evidence commit 4312d3cc, with 44 pinned source hashes. Substantive changes span 14 study documents and three shared methods documents. User requested direct document incorporation instead of an inbox response; no inbox message was sent. No model runs, resource allocation, frozen settings or historical outcomes changed. Validation: zero repository errors, five pre-existing citation warnings, 67 new local links/anchors valid and zero scoped secret-scan findings.

Published substantive changes at 1f51de2de42b5c7060d38bd094820fd07a06aeb0. Pre-publication Discussion refresh at d2fee7c8 is explicitly separated from the primary 4312d3cc evidence cutoff.
