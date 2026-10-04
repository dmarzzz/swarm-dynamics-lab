# Q-A3 canary post-mortem

2026-10-04 UTC. Retrospective closeout of source c2655e66d1fba970035c558f68a37ee771f30fbb and q-a3-canary-plan.md. The exact immutable public plan/source receipt and each condition TLDR were verified before paid dispatch. Exclusive allocation: vishesh-swarm-size-canary-q3, agentops PR207. Dedicated Swarm Lab credential policy followed; no secret in public records.

## Outcomes

All four assigned cases started, reached planning/work/integration, completed both work items, passed the deterministic evaluator and finished on time. No repair calls: 16 model calls total. All four outcomes and terminal statuses were acknowledged; all 16 uploaded artifact files were downloaded and matched local SHA256 hashes. Public per-run TLDRs matched and all four public states were done.

| Family / structure | Public run suffix | Quality / success | Elapsed seconds | Settled USD |
|---|---|---|---:|---:|
| Evidence / parallel | 4d77f67b46fc9f9b | 1.0 / pass | 9.582 | 0.003389 |
| Repository / chain | 7bd7f127497eeca5 | 1.0 / pass | 7.864 | 0.003596 |
| Evidence / chain | 7c860223a1f1eec7 | 1.0 / pass | 5.246 | 0.003627 |
| Repository / parallel | bb5c6e654d04f8ea | 1.0 / pass | 5.759 | 0.003426 |

Run IDs have prefix optimal-swarm-size-q1/. All are width=2, N=1, development root0 with separate width-aware identities and fresh histories. Independent task-performance evidence is limited to these four tiny fixtures; no size-effect or production reliability inference is justified.

## Cost and accounting

Added settled usage: $0.014038 for 16 calls. The same canonical ledger now contains 55 historical/current calls, $0.122548 settled and the original $0.220480 unresolved reservation: cumulative exposure $0.343028 against the original $20. Remaining authority $19.656972. The canary's atomic $5 attempt and $1.25 episode sublimits were recorded in that ledger; no separate authority, reset, refund or replenishment.

## Interpretation and limitations

The repaired native schema contract now has live end-to-end evidence across both task families and both structures, unlike the earlier trivial transport probe. Qualification, task correctness, budget accounting, exact public registration and artifact readback all passed for this canary. Historical Q-A1/Q-A2 failures remain unchanged. This is development requalification, not a randomized estimate of the repair's causal benefit.

Known display limitation: the legacy live progress reporter still labels work completion with total=16, although these assignments and outcomes correctly record width=2 and completed_items=2. This does not affect dispatch, evaluator results, terminal metrics or replay service intervals, but the transient progress fraction is misleading. Correct width propagation before further deployment; preserve the original trace/publication evidence rather than silently rewriting it.

Next eligible step: prepare a separately admitted full-width N=1 qualification using the repaired schema contract, original ledger and fresh allocation/public receipt. Do not infer width-16 feasibility from width-2 success or automatically advance to Q-B. Resolve mandatory dependency-edge validation and keep roster-versus-slot distinctions explicit before any scientific size comparison, as recorded in next-run-design.md. No additional stage was launched.
