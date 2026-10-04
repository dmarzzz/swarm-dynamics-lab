# Antsy repair v3 specification

Version frozen before S1; exploratory engineering only. Owner vishesh/codex-methods.

## Assignment and deterministic environment

`task % 4` selects target A/B/C/NONE. Task-seeded prices vary order. On an eligible task, target costs 1, another eligible provider costs 3, and a 0.5 provider violates one of scanned support, retention or accuracy. Across three groups of four tasks, the violated field cycles. NONE tasks have one distinct violating field per provider. No equal cheapest eligible prices occur; a future tie uses stable provider-name order. Environment truth constructs source reports and scores results; it is not passed to the actor adapter.

Sources 0–3 each publish a complete table as three separately delivered rows, with revision equal to source index. A source root is an explicit fixture annotation, not discovered provenance. The `late` schedule is [1,2,4,5]; `stalled` is [1,2,99,99], so sources at 99 never arrive before either cutoff. Provider row order is shuffled with task/seed. Row slot modulo scout count determines private recipient. At tick t, each scout sees every row with arrival<t and its own rows arriving at t. Communications are lossless, synchronous and free in logical ticks; the model has no extra private memory. Changing agent count changes early private allocation, not the global evidence supply. This is not a clean estimate of independent model diversity.

Clean: all rows truthful. Copies: nine extra copies of root 0, with ancestry unchanged. Early-wrong: roots 0/1 falsely make the cheapest provider fully eligible. Late-wrong: roots 2/3 do that. A later revision wins per provider among visible rows. These are designed adversarial stress cases, not estimated real-world corruption rates. Copies may change private coverage timing; provenance-floor invariance is specifically about counting, not every aspect of delivery.

## Decision and provenance contract

The three-provider candidate catalogue is known. Any scout missing a candidate must WAIT and does not invoke the model. Complete rows enter `adapter.Hybrid`: exact concise state, three binary Laya questions, then observed-row hard-constraint guard and price comparison. No tool calls, open-ended text actions, autonomous research, retraining or shared conversation. Exactly the same pinned model is used for every role. Deterministic memoization is by exact state/question, and every reuse points to the original physical receipt. Repeated agents are not independent model samples.

A root supports candidate k only if that root's own complete observed table would select k under the declared symbolic constraints/price rule. NONE requires a complete table with no eligible provider. Union supporting roots across the candidate's majority voters; duplicates cannot create extra roots. This host-side source-support check uses observed facts and a deterministic rule, not model-generated citations. It can reject a model's false acceptance when source tables do not corroborate it. Source truth itself is not checked.

## Policies and fair comparisons

All five decentralized policies consume the same potential ballot history, avoiding model noise between arms. Strict majority is more than n/2 scouts voting the same non-WAIT action.

| Policy | Commitment rule |
|---|---|
| Majority | First strict majority, no root floor |
| Fixed-two | First strict majority plus two supporting roots |
| Fixed-three | First strict majority plus three supporting roots |
| Adaptive | Fixed-three until final tick; then two roots |
| Deadline-vote | Majority at final tick only |
| Central-deadline | One hybrid decision on the union of all rows delivered by cutoff |
| Symbolic-deadline | Deterministic selection on that same centralized board |

No commitment means abstain at deadline. An execution fault invalidates policies still consuming that tick, not ones already committed. Central controls have full aggregation at cutoff, including current private deliveries. They are an information ceiling, not a compute-matched decentralized topology. Central does not receive hidden truth. A paired fully symbolic execution of every policy also checks the incremental effect of model extraction; report all policy disagreements.

## Metrics and estimand

Primary exploratory contrast: adaptive minus fixed-three all-assigned loss, separately by world/schedule/deadline at nine scouts. Fixed-two is the essential lower-threshold comparator. Report correct, violated, abstained and false-NONE counts alongside loss. An improvement that depends entirely on comparing to an overconservative fixed-three rule is not general superiority. No post-hoc winner selection or pooled significance test.

Twelve tasks are the cluster units. Factorial cells and policies are repeated on each task. Report exact descriptive counts and paired per-task differences; do not bootstrap ballots or claim real-world confidence intervals from the engineered fixture set. Clean long-deadline cells are manipulation/competence checks, not discovery evidence. Deliberately wrong evidence may correctly produce a negative policy result. It is not a runtime failure.

Logical ticks measure evidence release and sharing, not service time. Physical receipt counts, actual encoder tokens and CPU inference seconds are reported across the executed shared tape. Logical model-call costs for an arm stop at commitment. Model caching changes physical cost but not the declared deterministic choices; it prevents interpreting our measured batch latency as production latency. There are no terminal verification probes in v3. Historical v2 post-deadline probes retain their old interpretation.

## Splits, gates and failure policy

D0 uses old development fixtures 7400–7407. Q1 uses 8000–8015 and six boundaries (failed). Q2 uses 8100–8115 plus six changed boundaries. S1 uses 8200–8211, seed1. IDs10000+ are untouched S2; no launch entry point is provided. All fixtures share a narrow generator, so disjoint IDs do not establish external validity.

Each attempt writes assignments and source/runtime manifest before calls, then incremental outcomes, receipts and compressed invocation/guard audit. No outcome retries. A runtime/schema fault stops after preserving its block; unexecuted assignments remain in the manifest denominator. Reporting failures must be fixed without re-executing scientific outcomes. A fresh run uses a new directory and run ID. Completed negative outcomes remain completed outcomes.
