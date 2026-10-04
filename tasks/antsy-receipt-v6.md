---
id: antsy-receipt-v6
type: task
title: Build and evaluate real receipt-total checking with fresh data
kind: build
status: done
priority: p1
owner: vishesh/codex-methods
for: vishesh
created: 2026-10-03
created_by: vishesh/codex-methods
depends_on: []
topics: []
claimed_at: 2026-10-04T04:09Z
updated: 2026-10-04T04:48Z
outputs:
- researchers/vishesh/notes/antsy-receipt-v6/RESULTS.md
---

## Goal

Replace ideal QA and regional recall with real OCR checker outputs, exact total decisions and measured latency; strengthen mutation/leakage/denominator tests; run frozen development and fresh exploratory evaluation with preserved failures.

## Done when

- [x] Plan, sources and evaluator contract frozen before implementation/run.
- [x] Regression and mutation tests pass.
- [x] Development measurement and post-mortem complete.
- [x] Fresh exploratory application evaluation audited and published, or precise blocking evidence recorded.

## Results

[Completed assessment](../researchers/vishesh/notes/antsy-receipt-v6/RESULTS.md): final50 assigned receipts,47 scorable,250 valid OCR calls,0 execution errors.46 tests and six mutation checks pass. Preserved three instrument defects and targeted repairs. Selective9 correct/1 wrong/37 refer;80 checks versus100 always. Zero model calls. Host released through agentops PR140; no active workers.
