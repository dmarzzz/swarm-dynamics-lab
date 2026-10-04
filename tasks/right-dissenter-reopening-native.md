---
id: right-dissenter-reopening-native
type: task
title: Integrate and fault-test the Right Dissenter reopening runner
kind: build
status: open
priority: p1
owner: null
for: vishesh
created: 2026-10-04
created_by: vishesh/codex-decision-models
depends_on: []
topics: [dissent, decision-models]
---

## Goal

Implement the prospective RD6 native path and offline failure checks while keeping paid execution behind the unchanged scope/admission boundary.

## Done when

- [ ] Bind exact inputs, admission, original ledger, qualification and fail-stop lifecycle.
- [ ] Test delivery, repeated identities, missingness, budget and transport faults without provider calls.
- [ ] Publish concrete implementation evidence and durable operator handoff.
