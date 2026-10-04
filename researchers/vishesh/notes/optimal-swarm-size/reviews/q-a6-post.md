# Q-A6 scientific post-mortem: speed, cost and correctness diverge

2026-10-04 UTC, vishesh/codex-idea-scores. Completed author assessment from a PI perspective, not independent review. Decision: **complete_valid_result for this exploratory matched-roster pilot**. The instrument comparison ran as specified; the adverse quality result is not a reason to retry for a better answer. Larger-N/core/transfer studies remain unqualified.

[Prospective plan and pre-assessment](q-a6-matched-roster-plan.md), [previous post-mortem](q-a5-post.md), [saved analysis](../results/q-a6/analysis.json), [public artifact verification](../results/q-a6/verification.json). Frozen execution source: 3331c6c6083caf1f69ccfdac4d5faa704c94c183; matched-roster-config.json plus private source-bound runtime; native claude-haiku-4-5-20251001. Exclusive existing study allocation updated through agentops PR238, no new machine provisioning. Exact immutable public plan, original ledger, previous-worker exit and current claim checked before dispatch.

## Reconcile the facts

Two fresh development root seeds, each crossed with two structures and two roster sizes: four matched pairs, **8/8 assigned → started → terminal → graded → analyzed**, 128 dependent work items, 144 model calls (18 per episode), no repair, runtime, schema or publication failures. N1 used one context; N2 used two. Both parallel N2 episodes reached two simultaneous work requests; all chain episodes and N1 episodes peaked at one. All required edges were present; no extra edges. Task hashes match within each pair. All eight final answers are schema-valid but substantively unsuccessful. There are no missing, excluded, replaced or unstarted episodes.

| Root | Structure | Quality N1 → N2 | Seconds N1 → N2 | USD N1 → N2 | Peak work requests N1 → N2 |
|---|---|---|---|---|---|
| 4 | parallel | .8125 → .6875 | 29.43 → 16.11 | .041336 → .035328 | 1 → 2 |
| 5 | parallel | .6875 → .3125 | 25.17 → 17.02 | .041336 → .035180 | 1 → 2 |
| 4 | chain | .0625 → .0625 | 40.90 → 38.95 | .075393 → .060421 | 1 → 1 |
| 5 | chain | .0000 → .0000 | 33.74 → 43.25 | .075398 → .060294 | 1 → 1 |

Quality is fraction of items with correct value and provenance; all provenance sets were correct here, so these quality values also equal value accuracy. Full-task success was zero in both arms (0/4 each), a floor for that binary endpoint. Parallel N2 latency fell 45.27% and 32.38%, with 14.53% and 14.89% lower cost, but quality dropped .125 and .375. Chain latency changed −4.76% and +28.20%; quality was unchanged near zero, and cost fell 19.86% and 20.03%. These are paired observations, not confidence intervals or population estimates. Two roots cannot support a reliable optimal-N rule.

There were 331,326 input and 18,672 output tokens. Q-A6 added **$0.424686 settled**, below its $4 protective attempt cap. Cumulative original ledger: 631 calls, $1.810840 settled + $0.220480 unresolved historical hold = **$2.031320 exposure**, leaving $17.968680 of the original $20. No new unresolved Q-A6 calls, no reset, no new infrastructure charge. Hosted latency is part of observed elapsed time; hardware speed was not manipulated or measured.

All 32 original artifacts were downloaded and hash-matched against the worker copies, with exact condition TLDRs and public done statuses. The exact worker exited. Done is execution status, not quality. Fixed replay-v2 artifacts are separately versioned presentation repairs; they do not change outcomes or execution provenance.

## PI interpretation

The result rejects the simplistic idea that more agents automatically improve this task: on both parallel fixtures, two contexts traded accuracy for lower time and token cost. The physical mechanism supported by the service trace is concurrent capacity bounded by dependency structure. Chain work cannot be parallelized by adding a second actor under enforced prerequisites. It does not follow that all chain latencies must be identical: provider latency, prompt length and context history can change.

Errors again begin in worker outputs: zero correct-to-wrong or wrong-to-correct integration transitions over all 128 items. A retrospective arithmetic audit reconstructed expected values from public records and separately checked each worker against its *observed* incoming prerequisite value. Chain root4 had 6 versus 13 locally inconsistent operations (N1/N2); root5 had 3 versus 11. Thus a single initial error propagating through otherwise correct operations does not explain all chain failures. This derived check was not preregistered and is the same author's audit, not independent replication. Root5 even failed its first item in both sizes. Possible causes include operand selection, arithmetic and context interference; this run does not isolate them.

N changes both parallel capacity and per-context history. Cost savings should not be interpreted as hardware efficiency or a uniquely causal memory mechanism. Fixed counterbalancing mitigates simple order imbalance but does not eliminate hosted-service drift; there was only one response sample per condition, one synthetic family, and two roots. These fresh roots remain development data forever after this run.

## Experiment-quality assessment

| Dimension | Status | Evidence / remaining action and acceptance check |
|---|---|---|
| question | pass, pilot scope | Prospective N1/N2 contrast; speed, cost and correctness measured separately |
| scenarios | gap | One synthetic evidence family; before deployment claims add realistic task/tool strata and reserved roots |
| controls | pass, bounded estimand | Identical task hashes, model and aggregate caps; both arms enforce edges. A future mechanism study must separate concurrency from context-history effects |
| capability | gap | 0/8 full success, chain accuracy floor; do not scale the original core. Qualify a separately planned input/arithmetic intervention on fresh roots |
| measurement | pass, pilot scope | All outcomes retained, exact numerical/provenance checks, saved audit; full-task endpoint has a floor and cannot discriminate these arms |
| sample_size | gap | Two independent root seeds, four dependent pairs, one model response per arm; no powered conclusion or uncertainty interval claimed |
| agent_context | pass, declared protocol | Actual contexts matched N, fresh histories, same public task, post-termination evaluator only; no oracle feedback |
| data_integrity | pass | 8/8 complete, 32 hash matches, immutable source/plan, exact public TLDRs |
| resources | pass | 144 settled calls, original cumulative cap/hold preserved, valid exclusive allocation, no provisioning |
| reproducibility | pass, recorded evidence | Source/config/task hashes, saved outcomes/traces, analysis script; hosted answers not guaranteed repeatable |
| visualization | repaired presentation defect | Original range-step rounding prevented Play restarting at the endpoint. Changed only replay renderer to continuous range; separate replay-v2 regenerated from saved traces, no recollection. Browser verified start, progression, final stop and labels; original files preserved |

## Issues and next-design decision

Accepted from Q-A5: enforce required edges in both arms and retain worker outputs. Verified: no missing edges, expected work concurrency and exact task matching. Rejected: widening deadlines or changing integration alone; timing is far below caps and integration does not change correctness. Rejected: blindly sweeping N4/8/16 or treating worse answers as broken infrastructure.

For the next scientific iteration, prioritize a **worker input-binding diagnostic** before a larger roster sweep: compare the current full-task prompt against a deterministic per-item projection containing only the requested public rule, its referenced public operands and declared prerequisite artifacts, with equal output contract, caps and no evaluator truth. Keep N fixed first so input scope and roster are not changed together. Explicitly distinguish derived public-input projection from an oracle calculator. Use fresh development roots and both structures, reserve a separate qualification set, log the exact serialized projection/hash, and assess local arithmetic consistency alongside final correctness. An effect would support an input/context mechanism; no effect would favor arithmetic/model capability or other explanations. This proposal is not implemented or launched, and is not permission to silently replace the study's earlier results.

This cycle closes with an interpretable adverse result, not an estimated best swarm size. Evidence confidence is **1/4 exploratory** for these scoped observed tradeoffs; confidence remains **0/4 untested** for the intended conditional sizing policy. The next pilot needs its own prospective specification and current admission rather than reusing Q-A6's identity. Remaining funds are preserved.
