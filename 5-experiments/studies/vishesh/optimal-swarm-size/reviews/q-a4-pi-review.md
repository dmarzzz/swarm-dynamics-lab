# Q-A4 post-mortem and PI-perspective critique

2026-10-04 UTC. Author self-review from a PI perspective, not an independent researcher review. Retrospective saved-data audit; no scores changed.

## Result

16 assigned/started/terminal, all schema-valid, all 256 work items completed; 11/16 on-time substantive successes. Repository: 8/8. Evidence parallel: 3/4. Evidence chain: 0/4. No runtime failures or plan repairs; 288 calls. Q-A4 added $0.834974. Canonical exposure now $1.178002 ($0.957522 settled plus the retained $0.220480 hold), leaving $18.821998 of the original $20. Publication acknowledgments complete; full artifact readback separately recorded on host as qa4-verification.json.

Evidence parallel root1 missed the arithmetic value for item02, with correct provenance. Chain root0 missed values for items10–15; root2 missed items12–15, both with correct provenance. Chain root1 missed values for items05–15 and all provenance sets; root3 missed values for items01–15 and all provenance sets. None contained duplicate provenance entries. This audit uses the unchanged evaluator and per-field comparisons, not a revised headline score.

All observed Q-A4 plans contained the supplied prerequisite edges. The validator still permits omissions in future, but omitted edges do not explain these observed failures. All outcomes were well within the existing 600-second deadline. Raising the time budget or increasing N has no demonstrated causal justification yet.

## PI assessment

The infrastructure qualification succeeded; the full-width task-competence criterion failed. The 11/16 aggregate hides a complete chain-evidence failure and a ceiling effect in code repair. Pooling them would obscure mechanisms. Eight agents are not eight independent samples; roots and repeated development attempts are the experimental units/lineage, and there are only four roots per cell.

The protocol currently conflates worker computation with final integration: the final model can recompute or rewrite all worker answers. Only the final artifact was saved. Consequently error propagation in worker arithmetic, evidence accumulation, and damage during integration are competing explanations, not established mechanisms. The fact that wrong chain values form suffixes suggests propagation, but this is an inference needing intermediate data.

Q-A4 is development qualification, not a randomized estimate of an N effect, a realistic software benchmark, or a hardware law. Full task visibility permits actors to recompute prerequisite results. Four service slots distinguish roster size from physical concurrency. Schema constraints improve structural validity, not truth. Future dependency-integrity enforcement and matched resource profiles are necessary before size claims.

## Decision

Do not proceed to Q-B or larger N. Add intermediate artifact observability and run the eight evidence fixtures under the same N=1 protocol, model, schema and caps. Evaluate worker and final artifacts after termination, with no evaluator feedback to actors. This is a diagnostic repeat on development roots; it is not an independent replication. Preserve code-repair results and avoid spending on another ceiling-effect batch.

The next post-mortem must quantify worker-correct/final-wrong regressions, worker-wrong/final-correct rescues, arithmetic versus provenance errors, first chain divergence, and extra/missing prerequisite edges. Only then choose an integration or worker intervention. Keep failures visible; do not iteratively alter endpoints until a preferred result appears.
