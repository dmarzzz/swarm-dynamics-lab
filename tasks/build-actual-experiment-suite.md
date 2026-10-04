---
id: build-actual-experiment-suite
type: task
title: Implement and deploy developed exploratory experiment designs
kind: build
status: claimed
priority: p1
owner: vishesh/codex-experiments
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-experiments
depends_on: []
topics: []
claimed_at: 2026-10-03T23:41Z
updated: 2026-10-03T23:41Z
---

## Goal

Implement the developed external-influence and immune-response designs, plus Avalon if confirmed, using the latest worker template. Deploy bounded exploratory S0/S1 runs to the existing hub. Total new spend capped at USD 50. Preserve review gates for S2.

## Done when

- [x] Freeze concrete plans and executable configurations.
- [x] Validate paired fixtures, scoring, state isolation, failures and budgets.
- [x] Publish source and deploy workers with recorded hub outcomes.
- [x] Report scope, results, costs and remaining research gates.

## Remaining work

Live model qualification is blocked on authorized access to the encrypted per-launch model credential store. No paid runs were queued and no API spend occurred. Avalon deployment is not included pending clarification of the intended third design. See researchers/vishesh/notes/actual-experiments/DEPLOYMENT.md.
