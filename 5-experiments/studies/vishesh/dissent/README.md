# Dissent: The Right Dissenter

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-decision-models; source `ad0dbb81` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — On this fixed synthetic cohort, evidence-gated dissent saved nine checks but produced six fewer correct decisions than always-check, including two missed favorable recovery events. Basis: Scripted votes, repeated scenario grammar, shared saved responses and 52 fixed roots limit generalization. All outcomes and three rejected calls are retained; clean qualification passed after a prospective wording amendment. This is an owner assessment, not independent review.
- **sample_size_summary:** Observed S1: 52 fixed roots with reused grammar; 420/420 decisions across 7 policies; 129/132 unique calls valid. Separate screens: Q0 12/18 correct; Q1 clarified 18/18 plus 6/6 uncertainty controls; D1 9/9 valid. No independent replication.
<!-- experiment-evidence:end -->

Research area connecting minority evidence, collective correction and typed decision models. Canonical question **DM-03**, jointly tagged **dissent** and **decision-models**. DM-14 is a related question. Tags are many-to-many; each idea keeps one ID and one assessment history.

The practical rule: a dissenter can earn a bounded independent check. Evidence determines whether the group changes its decision. A challenge must also be able to withdraw and reopen when facts change.

## Current result

**Latest separate iteration: [RD4, the right to resume](rd4/REPORT.md).** All 576 decisions are accounted for. Alias identity and persistent closure are repaired, but symmetric wording ties the original gate at 87/96; always-check reaches 88/96 with fewer model calls. Transport sensitivity prevents an accuracy ranking. The report isolates the more useful open problem: unresolved repeated judgments can spend the check needed for later recovery. Prior results below remain their own cohort.

The exploratory cycle is complete. Q1 qualified the clarified model; in S1 the evidence gate scored **24/60**, versus **30/60** for always-check, with **31 versus 40 checks**. It missed both favorable recovery events after correctly withdrawing earlier false alarms. [Read the result and limitations](REPORT.md) or [watch the measured replay](https://swarm-live.pages.dev/api/a/right-dissenter/s1-a1/measured_replay.gif).

The evidence metadata above reflects the completed exploratory cohort and is assessed by the study owner. Native results do not support deploying the current gate. The initial allocation error was corrected and remains documented; the borrowed Dmarz fleet host is released.

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

Exploratory Q0/Q1/S1/D1 cycle completed. The current evidence does not establish a benefit for the gate. Original idea ratings remain historical; the evidence block now reflects this cohort. Formal research review and confirmatory S2 remain closed; a redesigned protocol needs a new prospective assessment.

## Next design

[RD5 implementation and next-run package](rd5/README.md) reconciles the observed accuracy gap and proposes explicit uncertainty memory, separate acquisition/inference accounting and a test of protected future verification. Status: implemented with offline checks; native qualification and current operational admission pending. No new native outcomes or machine allocation.

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
