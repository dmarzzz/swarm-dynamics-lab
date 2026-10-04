# Pre-run assessment: diagnostic-04

- Healing Helping Hands / vishesh/codex-regrowth-docs / S0 diagnostic.
- Parent and review: diagnostic-03-post.md. Status diagnostic-only.
- Question: does the asserted claim contaminate a report-outcome classification, particularly absent evidence? Decision: qualify a report-only adapter or report the requested models as unsuitable under this scope.

## Design and assessment

Use the same 18 development reports as diagnostic-03. One Qwen thinking configuration and one Laya configuration receive REPORT only. Options describe measured improvement, measured no improvement/worse, and no measurement/result. The mapping to SUPPORT/REFUTE/UNCERTAIN is fixed because all corpus claims assert improved accuracy. No labels or hidden fixture metadata reach models. This changes both framing and removes the claim, so a gain cannot uniquely identify claim anchoring as the cause. Earlier interfaces are development comparators, not new independent randomizations.

Acceptance remains >=16/18 and >=5/6 per class, no provider/schema errors. Development success only permits a fresh qualification with new language fixtures, not a scientific sweep. Units are reports; tokens/time/counts and confusion matrices are primary diagnostic outputs. No pilot outcome tuning, no held-out corpus execution.

## Changes and unresolved issues

Q3/L3: evidence absence is confused with claim falsehood. Predicted correction: classify observation availability before direction in explicit instructions. Acceptance is the unchanged development threshold followed by untouched qualification. Owner vishesh/codex-regrowth-docs. S3 scenario weakness is deferred to a prospective pilot revision, not altered here.

## Frozen execution plan

Source and registered plan must be the same immutable commit at launch; model pins unchanged. `src/diagnose.py --variant-set report-only --out <diagnostic-04> --run-tldr <purpose>`. Eighteen Qwen plus eighteen Laya calls maximum, 90 seconds each, 15 minutes overall. No retries or paid API. One active provider at a time, <=4 CPU threads. Exclusive sim-vishesh allocation retained under vishesh-healing-helping-hands; verify exclusivity/expiry again before launch. Every cell ends completed/failed/not-run with append-only call events. Regression tests must pass before source freeze.

## Visualization mapping

Reuse mapping D1 from diagnostic-03-pre.md, bound to diagnostic-04 and report-only Qwen/Laya configurations. Confusion matrices and 0–18 completion counters, not swarm frames; raw counts and missing states retained. Expected-label rows are evaluator-only. Validate record totals and class counts. Public image fallback and private full journal; no sensitive endpoints or credentials.
