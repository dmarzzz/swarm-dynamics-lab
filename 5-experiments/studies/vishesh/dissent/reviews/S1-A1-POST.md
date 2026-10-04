# S1-A1 post-mortem

Execution completed all 364 assigned trajectories and 420 decisions. Native calls: 132 unique / 170 logical, 129 valid and three rejected with generic ValueError. These three saved failures affected six policy decisions through the prospective shared-response cache. None was retried or excluded. Settled S1 API cost $0.005615064; three uncertain charges retain $0.004032 in reservations. Worker elapsed 80.29 seconds.

| Policy | Correct / 60 | Checks | Harmful reversals / 24 initially correct | DEFER | Failed decisions |
|---|---:|---:|---:|---:|---:|
| Majority | 24 | 0 | 0 | 0 | 0 |
| Blind veto | 28 | 0 | 20 | 0 | 0 |
| Always check | 30 | 40 | 4 | 10 | 2 |
| Evidence gate | 24 | 31 | 4 | 10 | 2 |
| Fixed 50% random allocation | 28 | 19 | 2 | 5 | 1 |
| Pooled | 32 | 0 | 15 | 2 | 1 |
| Exact grammar reference | 32 | 40 | 4 | 8 | 0 |

All 420 saved records exactly match replay with the saved native actions and failures. This reconciliation made no provider calls. [Detailed analysis](../results/s1-a1/analysis.json) retains scenario/condition tables, paired changes, logical costs, temporal closures and illustrative loss sensitivities.

## Scientific interpretation

Evidence gating saved nine checks but lost six correct decisions relative to always-check. It never improved a paired outcome against that comparator. Both policies share the same two failed checked requests on the same cases, so their paired six-decision gap is invariant to assigning any common replacement decision to those two failures. This does not recover their absolute accuracy or explain the original validation failures.

Four of the six lost decisions occur when cited evidence agrees with the majority even though evaluator truth differs: refusing that incoherent objection prevents an always-check policy's lucky rescue. Two occur after a fresh favorable alarm observation: evidence-gate chose KEEP and remained on HOLD, whereas always-check reopened correctly. Evidence-gate did withdraw all four initial false alarms and suppress all four unchanged repeats, but reopened correctly in only two of four changed epochs. These are valid adverse observations for the published policy, not a reason to retune and rerun the score.

The gate uses 63 logical model calls versus 32 for always-check. Saved-response counterfactual settled API costs are $0.002682792 and $0.001383732 respectively, excluding uncertain charges. Thus fewer physical checks did not imply fewer model calls. Pooled's higher accuracy accompanies 15 harmful reversals; blind veto has 20. The deterministic reference demonstrates that the grammar can be handled without model adjudication. No policy is recommended for operational use from this small synthetic study.

## Quality and process

Q1 qualified the clarified clean task before S1. Q1's public plan includes the prospective S1 amendment; the source remained b21ce280760d0c91e2ba500002aae087b4df62d9. Fresh source, Q1 summary hash, public plan, actual hostname and exclusive claim checks passed. Votes were scripted and evidence ancestry fixed. Root cases, not frames or policy rows, are the experimental units; repeated templates limit generalization. S2 and independent research review remain closed. The earlier Q0 allocation violation stays documented separately.

All assignments are retained, including unavailable, late, noisy and missing-evidence conditions. DEFER is not correct completion. Harmful-reversal counts exclude abstentions, which remain in the primary denominator and DEFER column. Illustrative losses use the published weights and vary wrong-PROCEED weight over 1, 5 and 10; they are preferences rather than empirically established utilities.

The final PNG and fixed-selection measured GIF were uploaded. Numerical and public playback/readback verification are required at closeout. An unknown response-validation subtype is a reporting defect: the relay discarded which fixed validation predicate rejected the reply. Preserve the original generic errors and uncertain reservations.

## Next action: bounded validation diagnostic, then close

Do not rerun S1 for a better outcome. Publish D1 before implementation: expose fixed validation codes and retain only safe numeric response-contract metadata, repeat the three rejected requests as explicitly labelled bug reproductions, and include six fresh clean controls. No D1 answer replaces S1. A failure to reproduce leaves the original subtype unknown; do not claim it repaired retrospectively. Close the observed policy comparison with its limitations and release the borrowed machine after verified artifacts.
