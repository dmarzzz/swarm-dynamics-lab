---
id: streamline-experiment-operations
type: task
title: Integrate a lean experiment operations interface
kind: build
status: done
priority: p1
owner: vishesh/codex-pi-review
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-pi-review
depends_on: []
topics: []
claimed_at: 2026-10-04T04:40Z
updated: 2026-10-04T04:49Z
outputs:
- scripts/experiment.py
- 5-experiments/toolkit/agent-experiments/OPERATIONS.md
- 5-experiments/toolkit/agent-experiments/operations.json
- scripts/test_experiment_operations.py
- scripts/test_experiment_theseus.py
---

## Goal

Implement the owner-approved first operations increment: a compact experiment registry and local entrypoint, explicit lifecycle commands, immutable configuration deltas, one native-study adapter, budget and duplicate-dispatch protection, trace-only reporting, and current workflow documentation. This is tooling work with offline fixtures, not a new scientific experiment or authorization to launch model calls.

## Done when

- [x] Add registry and safe shared CLI with one existing-study adapter.
- [x] Exercise stale source/config, duplicate launch, interrupted execution, context and budget behavior offline.
- [x] Document reuse/invalidation, recovery and unsupported operations; integrate local context and CI.
- [x] Pass repository checks and publish the implementation with accurate capability limits.
