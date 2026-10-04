---
id: review-dmarz-completed-xcheck
type: task
title: Independently recompute completed dmarz findings from saved records
kind: review
status: done
priority: p1
owner: shadow/sol-xcheck
for: shadow
created: 2026-10-04
created_by: shadow/sol-xcheck
depends_on: []
topics:
- sybil-resistance
claimed_at: 2026-10-04T13:51Z
updated: 2026-10-04T14:01Z
outputs:
- 5-experiments/studies/shadow/completed-findings-xcheck/README.md
- 5-experiments/studies/shadow/completed-findings-xcheck/recomputed.json
---

## Goal

Independently recompute sybil-scale-opus, sybil-split-opus and the completed dmarz findings in the October 4 results review. No model calls. Keep all review material in reviewer-owned notes because these exploratory studies are not formal experiment IDs accepted by the reviews schema.

## Done when

- Reviewer-owned code and machine-readable recomputations are saved.
- Per-study reviews distinguish raw-record replay from aggregate-only checking and report discrepancies and independent-unit limits.
- Repository checks pass and outputs are pushed.
