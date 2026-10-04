# Q-A5 scientific post-mortem

2026-10-04 UTC, vishesh/codex-idea-scores. Completed author assessment from a PI perspective, not independent review. Decision: **diagnostic successor**, Q-A6. [Prospective plan](q-a5-evidence-audit-plan.md); frozen source 9b11abb7db4cbf689a1f64827c28274e0e9ae761, native Haiku schema interface, evidence-audit-config.json plus private admitted runtime. Previous [Q-A4 critique](q-a4-pi-review.md) read before execution.

Evidence confidence: **1, exploratory** for localizing observed failures to worker outputs. Four reused development roots crossed with two structures; 8/8 assigned, started, terminal, graded and analyzed episodes, 128 work items, 144 model calls. Items and repeat executions are not independent samples. No optimal-size evidence yet.

## Reconcile recorded facts

Parallel success was 3/4, chain success 0/4. No runtime, schema, repair or missing-prerequisite failures. All eight episodes finished within 22.30–43.77 seconds, below the 600-second cap. Every per-item worker/final correctness comparison was unchanged: zero correct-to-wrong and zero wrong-to-correct transitions across 128 items. This does not assert byte-identical artifacts.

| Root | Structure | Worker and final wrong values / 16 | Worker and final wrong proofs / 16 | First wrong value |
|---|---|---:|---:|---|
| 0 | parallel | 0 | 0 | none |
| 1 | parallel | 1 | 0 | item_02 |
| 2 | parallel | 0 | 0 | none |
| 3 | parallel | 0 | 0 | none |
| 0 | chain | 6 | 0 | item_10 |
| 1 | chain | 11 | 16 | item_05 |
| 2 | chain | 4 | 0 | item_12 |
| 3 | chain | 15 | 16 | item_01 |

New settled cost $0.428632. Original canonical ledger: 487 cumulative calls, $1.386154 settled plus $0.220480 unresolved historical reservation = $1.606634 total exposure, leaving $18.393366 of the original $20. No new unresolved charge in this attempt; no ledger reset. Token details remain in original sanitized call records; this assessment does not estimate them from dollars.

Execution complete; response validity passed; diagnostic instrumentation complete; full-width all-success qualification still failed; no size-effect conclusion. Exact public plan/source and per-condition TLDRs were verified prospectively. All 32 public artifacts (assignment, trace, outcome, replay for each episode) were downloaded and hash-matched, with matching public TLDRs and done statuses. The remote qa5-verification.json is the readback receipt. Done denotes execution, not task success. No exclusions, replacements or unstarted episodes. The exact Q-A5 worker has exited. Existing exclusive allocation retained for this authorized study cycle, not shared with another experiment.

## PI interpretation and quality

The diagnostic discriminates worker-stage errors from integration-induced errors: the former explain every observed incorrect item in this cohort. It does not distinguish numerical reasoning weakness, serial propagation, long context or an upstream task ambiguity. Repeating the same roots reproduces the failure pattern but supplies no new independent task coverage. Increasing integration budget or timeout has no supporting evidence here.

| Dimension | Assessment | Evidence and next acceptance check |
|---|---|---|
| question | pass | Stage-localization question answered by paired worker/final records |
| scenarios | gap | Synthetic evidence only, reused roots; Q-A6 uses fresh development roots, not transfer claims |
| controls | pass for diagnostic | Same N=1 protocol, no actor feedback; worker assembly is a derived audit, not a separately executed arm |
| capability | gap | Chain 0/4; preserve genuine failures as outcomes, do not claim prior qualification passed |
| measurement | pass for scoped diagnostic | Deterministic value/provenance evaluator and transition fixtures; no independent arithmetic audit claimed |
| sample_size | gap | Four reused roots, dependent items; Q-A6 feasibility only, no powered population estimate |
| agent_context | pass scoped | Public task and prior actor messages only; diagnostic truth computed after execution, no oracle feedback |
| data_integrity | pass | 8/8 reconciliation, 32 artifact hashes and exact public TLDRs verified |
| resources | pass | Original ledger, settled/held split, exclusive admitted machine; no new machine cost |
| reproducibility | pass scoped | Frozen source/config/task hashes and retained traces; hosted responses need not reproduce |
| visualization | gap | Measured service replay and static interval tables retained/readback verified; no new visual inspection of every frame claimed. Q-A6 should show final quality/cost beside the timeline |

## Resolve prior suggestions

Accepted: preserve worker outputs and test the integration hypothesis; verified zero correctness transitions. Rejected for now: spending more on integration or deadlines, since all errors predate integration and timing is far below caps. Accepted: enforce supplied prerequisite edges before comparing N. All Q-A4/Q-A5 plans happened to include them, so the loophole is a prospective integrity repair, not a retrospective cause. Revised: requiring perfect N=1 answers before any exploratory comparison would hide the performance outcome of interest. Q-A4 remains failed under its original criterion; a new exploratory matched-roster instrument gets a separate plan and criteria.

## Next iteration

[Q-A6 prospective plan](q-a6-matched-roster-plan.md): N=1/N=2 on two fresh development roots, both structures, mandatory dependencies in both arms, eight episodes, $4 attempt sublimit within remaining original authority. No larger-N sweep or confirmatory claim. The owner's active request explicitly delegates deciding, implementing and running successive design improvements, then post-mortems; this is the scope authority, not a fabricated reviewer approval. Researcher review is now optional by standing owner direction; historical Dmarz review remains historical evidence. Required runtime/public/claim/budget gates still apply.
