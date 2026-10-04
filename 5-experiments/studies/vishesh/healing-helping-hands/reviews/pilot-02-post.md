# Post-mortem: pilot-02

- Experiment: Healing Helping Hands; owner vishesh/codex-regrowth-docs; exploratory S0; 2026-10-04 UTC.
- Parent: pilot-01, reviewed in ATTEMPT-01-REVIEW.md. Pre-run plan: README Repair 01. Frozen commit: 4518f40d6daad210502549eb28a6d9940e6a4075.
- Disposition: diagnostic. No model efficacy claim.

## What ran and what happened

144 assignments, 36 exact worlds started/completed/graded/analyzed, 108 model worlds not-run, all 144 terminal. No duplicate executions. Qualification: Qwen 40/60 (66.7%), class accuracy SUPPORT 100%, REFUTE 0%, UNCERTAIN 100%; Laya 51/60 (85%), class accuracy 100%, 100%, 55%. Both fail unchanged gates (overall >=85%, each class >=70%). All 120 provider calls returned valid schemas; no transport errors. Total 17.413 seconds on the local development runtime; no paid model API.

The concrete outcome interface worsened Qwen's negative-class performance. The exact cause is not established: overlapping output names, disabled reasoning and the prompt may contribute. Laya's new unevaluated-language cases exposed insufficient unknown-class coverage. An overall pass threshold alone would have hidden this failure.

## Visualization review

All completed worlds retain every measured round 0–23, state hashes and terminal state. Model worlds have explicit not-run records. Public animation was not delivered during execution; a retrospective renderer is being built from these recorded exact trajectories. No model animation can legitimately be shown for this attempt.

## Experiment-quality assessment

This attempt establishes that both current interfaces are unqualified, and that the deterministic control mechanism executes. It does not test model-backed recovery or superiority of heterogeneous heads. Three engineered corpus seeds are descriptive fixtures, not a population estimate. Qualification templates overlap development templates and cannot establish general language competence.

Two process gaps are retained: the pre-run assessment was embedded in README rather than the newly required per-attempt template; and the attempt used the existing local runtime without the new fleet allocation check. These are process failures, not retroactively valid allocations. No further inference launches locally. A fresh exclusive fleet allocation and explicit pre-run assessment precede diagnostics.

## Failure and repair ledger

| ID / kind | Evidence | Cause confidence | Repair / acceptance | Status |
|---|---|---|---|---|
| Q2 / capability | Qwen REFUTE 0/20 | Interface sensitivity suspected; no transport fault | Compare neutral output codes and bounded reasoning on development probes; then new disjoint qualification | Open |
| L2 / capability | Laya UNCERTAIN 11/20 | Unknown-description mismatch suspected | Test explicit report-outcome criteria on development probes, then disjoint qualification | Open |
| P2 / process | No fresh fleet claim before launch | Verified workflow omission | Exclusive merged claim + workload check before next call | Allocation created; verify again at launch |
| V2 / reporting | No embedded measured replay during run | Renderer absent | Replay retained frames, inspect event and final values, public GIF fallback | Open |

## Next run

Run bounded diagnostic-03 under its committed pre-run assessment; no pilot world launch. Preserve this attempt. Select adapters by a frozen development criterion, not pilot outcome. Qualification must use new language fixtures; the old probes can diagnose errors but are not fresh evidence. Held-out seeds 8301–8310 remain untouched.
