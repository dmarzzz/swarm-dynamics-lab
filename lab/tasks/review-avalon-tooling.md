---
id: review-avalon-tooling
type: task
title: Review imported Avalon Swarm tooling for possible reuse
kind: build
status: open
priority: p2
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: vishesh/codex-avalon
depends_on: []
topics: [llm-agent-swarms, sync-consensus]
---

## Goal

Assess [the imported offline Avalon Swarm prototype](../../5-experiments/toolkit/avalon-swarm/README.md) as a reusable development resource for the existing Avalon research lane. The source, protocol, thirteen tests, and compact scripted validation results are available; no provider adapter or real-model results exist. This task does not authorize research promotion or replace the existing design-only task.

Check [integration boundaries](../../5-experiments/toolkit/avalon-swarm/INTEGRATION.md), threshold calibration, oracle and uninformed controls, and information isolation before recommending reuse. Follow the survey and hypothesis gates before an actual experiment.

## Done when

- Evaluate consensus quorum, coverage, confidence, patience, and stability defaults against suitable control policies.
- Inspect whether bounded council communication answers the intended swarm question and document omitted Sybil and fork/merge capabilities.
- Record a reuse recommendation and remaining work without marking the separate Avalon design task complete.
- Re-run the offline tests, report validation, and repository check.
