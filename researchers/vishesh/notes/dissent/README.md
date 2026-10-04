# Dissent: The Right Dissenter

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Untested efficacy question: whether bounded evidence-backed challenge improves decisions against wrong majority reports without needless disruption. Basis: Votes are scripted; repeated native adjudications may share saved responses. Seven policies, five source/vote roles and temporal events do not multiply independent case count.
- **sample_size_summary:** No native results. Planned Q0: 18 clean decisions. S1: 52 roots × 7 policies = 364 trajectories containing 420 decision opportunities (48 static roots and 4 temporal roots with 3 steps each), across 3 scenarios.
<!-- experiment-evidence:end -->

Research area connecting minority evidence, collective correction and typed decision models. Canonical question **DM-03**, jointly tagged **dissent** and **decision-models**. DM-14 is a related question. Tags are many-to-many; each idea keeps one ID and one assessment history.

The practical rule: a dissenter can earn a bounded independent check. Evidence determines whether the group changes its decision. A challenge must also be able to withdraw and reopen when facts change.

## Current result

The exploratory cycle is complete. Q1 qualified the clarified model; in S1 the evidence gate scored **24/60**, versus **30/60** for always-check, with **31 versus 40 checks**. It missed both favorable recovery events after correctly withdrawing earlier false alarms. [Read the result and limitations](REPORT.md) or [watch the measured replay](https://swarm-live.pages.dev/api/a/right-dissenter/s1-a1/measured_replay.gif).

The evidence metadata above is a historical external assessment. Native results now exist, but they do not support deploying the current gate. The initial allocation error was corrected and remains documented; the borrowed Dmarz fleet host is released.

## Start here

- [Standalone live study plan RD-2](LIVE-PLAN.md) and [research and X source map](SOURCES.md).
- [Experimental design RD-1](PLAN.md), written before implementation.
- [Conditions and parameter ledger](PARAMETERS.md).
- [Implementation and validation](IMPLEMENTATION.md).
- [Readiness and research limits](READINESS.md).
- [Native results and limitations](REPORT.md).

## Three scenarios

1. **The Missing Bridge:** one fresh inspection confronts a majority repeating an old survey.
2. **The Passing Build:** one applicable failing test confronts a green summary; stale or wrong-platform counterexamples must not derail a sound release.
3. **The Alarm That Became True:** withdraw a false alarm, suppress repetitions, then respond to genuinely new evidence from the same source.

The design covers correct and incorrect dissent, correct and incorrect majorities, scope, freshness, source dependence, verification failure and cost, deadlines, repeated interruption, and changing facts. A dissenter is never given evaluator truth.

## Separate project handoffs

- [Phantom Coast context and starting prompt](../decision-models/handoffs/PHANTOM-COAST.md).
- [Quorum of Mirrors context and starting prompt](../decision-models/handoffs/QUORUM-OF-MIRRORS.md).

These briefs are ready for the owner to open in separate tasks. No new Codex tasks have been created on the owner's behalf. Dissent owns the bounded challenge mechanism; the other projects own exploration feedback and evidence-dependence respectively.

## Status

Exploratory Q0/Q1/S1/D1 cycle completed. The current evidence does not establish a benefit for the gate. Original idea ratings and the external evidence block are historical. Formal research review and confirmatory S2 remain closed; a redesigned protocol needs a new prospective assessment.
