# Q2 pre-run assessment

Antsy / vishesh/codex-methods / S0 qualification. Status: ready for bounded qualification only. Parent [Q1 post-mortem](Q1-post.md). Question: can the explicit model-extraction plus deterministic-constraint architecture correctly handle the declared clean synthetic provider-selection task? This is an architecture change, not an invisible replacement of v2 agents.

## Design and assessment

Fresh tasks 8100–8115, four each with best label A/B/C/NONE. Six additional cases cover accuracy 89/90/95, retention 0/2/7 and scanned support true/false. Each case is a complete three-provider board. The evaluator is `engine.symbolic` over fixture truth, while actors see only supplied row values. There are 22 assignments, not 22 independent draws from a real task population. Identical atomic inputs use deterministic memoization, with receipt references on every logical invocation; this is not independent agent sampling. Price comparison is explicit host code. Baseline is symbolic parsing of the same typed facts, which is expected to solve this synthetic task perfectly. Laya's added value may be zero.

Acceptance: all 4/4 in each core target stratum, all 6/6 boundary cases, zero invalid or truncated encodings. This strict narrow readiness gate is not a generalization guarantee. Any failure gets an atomic receipt diagnosis and a newly frozen attempt, never selective removal. No S2 holdout access (10000+ reserved). Neither timing nor quorum efficacy is tested by Q2.

## Changes and checks

R1 coverage guard, R2 candidate-specific provenance, R4 consumed-prefix faults, R5 exact state/options/head checks and R9 receipts are implemented. Deterministic regression checks cover missing evidence, copies, support versus availability, balanced labels, both agent populations, early commitment under later faults, and adaptation helping or hurting. Central baseline now receives the union of documents delivered by cutoff, an explicit information-aggregation ceiling rather than claiming equal per-agent access. Terminal tool arms are removed from the new stopping study; old attempts remain unchanged. Actual cost is physical calls/tokens/wall time; logical calls are separately counted.

## Frozen execution

Command: `python repair-v3/src/qualify.py --out <new-Q2-attempt-1-directory>` from this versioned source tree. Manifest records exact commit and runtime. Pinned Laya/checkpoint in `src/runtime.py`; model questions, state formatter and memoization in `src/adapter.py`. One worker/two CPU threads on exclusive `sim-vishesh`, claim `vishesh-antsy-repair`, expiration 2026-10-04T03:22:16Z. Same Antsy allocation across stages; refresh exclusivity before launch. Maximum 198 logical predicate calls, at most 198 physical calls, 20 minutes, zero hosted API spend. No outcome retries. Alarm termination preserves assignments and incremental results; missing assignments count as missing and fail readiness.

## Visualization mapping Q2-v1

Static qualification matrix: 16 core plus six boundary rows; target/choice/correct/error from saved outcomes, visible denominators. Progress is completed/22. Public PNG fallback on hub; raw synthetic records and receipts retained. No animation is appropriate for independent one-board competence tests. Temporal study has a separate mapping and launch gate. Verify plotted counts against summary; no missing case is rendered as a pass.

## Q2 amendment

The model-derived eligible set is intersected with `engine.eligible` on observed rows; every block/disagreement is logged. The original one-day retention case is a regression, not fresh qualification. This prevents typed observed violations but cannot prevent violations caused by false sources. Model usefulness is a separate question and remains unproven. Q2 adds no source verification.
