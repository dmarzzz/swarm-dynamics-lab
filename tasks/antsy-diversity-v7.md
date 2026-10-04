---
id: antsy-diversity-v7
type: task
title: Measure worker diversity and correlated errors in Antsy
kind: build
status: done
priority: p1
owner: vishesh/codex-methods
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-methods
depends_on: []
topics: []
claimed_at: 2026-10-04T05:58Z
updated: 2026-10-04T06:29Z
outputs:
- researchers/vishesh/notes/antsy-diversity-v7/RESULTS.md
- tooling/agent-experiments/WORKER-DIVERSITY.md
---

## Goal

Implement declared and behavioral worker-diversity profiles, qualify a second OCR engine, compare evidence and aggregation factors on untouched receipts, and publish audited results.

## Done when

- [x] Prospective plan and setup evidence published.
- [x] Instrument and controls tested; native qualification executed and assessed without relaxing its gates.
- [x] Bounded native qualification rerun, assessed, and pushed; failures preserved. S1 correctly not run after failed per-family competence.

## Disposition

Delivered design, shared diversity guide,24 tests,100-call repaired qualification, charts/replay and audited results. The original aspiration of a held-out efficacy comparison remains unachieved because the competence gate failed; closing this iteration does not assert that gate passed. See researchers/vishesh/notes/antsy-diversity-v7/RESULTS.md for the next design requirements.
