---
id: right-dissenter-reopening-native
type: task
title: Integrate and fault-test the Right Dissenter reopening runner
kind: build
status: done
priority: p1
owner: vishesh/codex-decision-models
for: vishesh
created: 2026-10-04
created_by: vishesh/codex-decision-models
depends_on: []
topics:
- dissent
- decision-models
claimed_at: 2026-10-04T18:35Z
updated: 2026-10-04T19:02Z
outputs:
- 5-experiments/studies/vishesh/dissent/reopening/IMPLEMENTATION.md
- 5-experiments/studies/vishesh/dissent/reopening/OPERATOR.md
- 5-experiments/studies/vishesh/dissent/reopening/offline/validation.json
---

## Goal

Implement the prospective RD6 native path and offline failure checks while keeping paid execution behind the unchanged scope/admission boundary.

## Done when

- [x] Bind exact inputs, admission, original ledger, qualification and fail-stop lifecycle.
- [x] Test delivery, repeated identities, missingness, budget and transport faults without provider calls.
- [x] Publish concrete implementation evidence and durable operator handoff.

## Coverage note

Native source published at `f7ef9048b7d4073a7f0e4f97222e19154d370770`; 73 offline checks pass, 162 authored fixture labels unchanged, 81 historical RD5 review evidence hashes verified. Twelve published files hash-read back from `68202ff10d854ca7cf8881453fc25908d9b0a447`. No provider calls, allocation or original-ledger writes; live scope approval and operational admission remain separate.
