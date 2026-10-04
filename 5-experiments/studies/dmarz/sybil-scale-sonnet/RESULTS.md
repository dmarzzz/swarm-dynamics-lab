# Results: Sybil resistance as swarms grow, Sonnet 4.6 replication

Completed 2026-10-04. Exploratory S1, run `sybil-scale-sonnet/afd8d5b9`, 24 paired world clusters, 100 conditions and 2,400 valid model answers from `claude-sonnet-4-6`. All planned calls completed once; no failed, missing, duplicate or retried assignments. Scripted fleet S0 (264/264) and API Q0 (64/64, every size 1.0) passed before collection. Reported-usage cost: S1 **USD 56.271264**, Q0 USD 1.983438, study total **USD 58.254702** over 2,464 calls.

This study changes only the model of the completed Haiku study [sybil-scale-api](../sybil-scale-api/RESULTS.md) (run `sybil-scale-api/56defc84`). The 2,400 assignments are identical record for record (checked after collection on the decompressed files), so every cell pairs world by world with the Haiku cohort. The two cohorts are reported side by side and never pooled.

## Primary contrast (frozen)

Coverage selection, visible badges, strong checks (honest pass 90%, attacker pass 10%), 972 identities: proportional (108) minus fixed (4) checks.

| Cohort | Accuracy difference | Descriptive paired-world 95% interval |
|---|---:|---|
| Sonnet 4.6 (this study) | **+52.8 pp** | +38.9 to +66.7 |
| Haiku 4.5 (sybil-scale-api) | +51.4 pp | +38.9 to +62.5 |

Both exceed the predeclared 10-point practical threshold. The scaling result replicates with a stronger synthesizer: the effect comes from which identities are admitted, and admission is computed before the model call. Attacker seat shares are identical in every cell of both cohorts (asserted per assignment in `reporting/compare_models.py`).

## The scaling table, both models

Coverage selection, visible badges. Accuracy is correctness on the three specialist facts; attacker share is the percentage of admitted seats held by attacker identities. Each cell has 24 worlds. Format: Sonnet / Haiku.

| Identities | Checks fixed / proportional | Strong, fixed | Strong, proportional | Weak, fixed | Weak, proportional | Attacker share strong fixed / prop. | Attacker share weak fixed / prop. |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 36 | 4 / 4 | 81.9% / 76.4% | 81.9% / 76.4% | 56.9% / 40.3% | 56.9% / 40.3% | 8.3% / 8.3% | 36.1% / 36.1% |
| 108 | 4 / 12 | 6.9% / 5.6% | 95.8% / 83.3% | 6.9% / 5.6% | 54.2% / 44.4% | 0.7% / 3.5% | 0.7% / 26.3% |
| 324 | 4 / 36 | 43.1% / 33.3% | 97.2% / 94.4% | 44.4% / 37.5% | 55.6% / 50.0% | 7.7% / 3.0% | 7.7% / 22.0% |
| 972 | 4 / 108 | 47.2% / 47.2% | 100.0% / 98.6% | 52.8% / 45.8% | 45.8% / 52.8% | 11.5% / 3.6% | 11.5% / 21.5% |

Weak-check secondary at 972 (proportional minus fixed accuracy): Sonnet **−6.9 pp** (−22.2 to +6.9); Haiku +6.9 pp (−5.6 to +19.4). Neither interval excludes zero. With weak checks, more checking still raises attacker seat share by 10.0 points under both models, because admission does not depend on the model.

## Sonnet minus Haiku, paired by world

Across all 100 cells the mean cell difference in specialist accuracy is **+4.7 pp**; Sonnet is higher in 73 cells, Haiku in 14, and 13 are equal. Selected cells (full table: [model-comparison-cells.csv](model-comparison-cells.csv)):

| Identities | Arm | Checks | Attacker pass | Badges | Sonnet | Haiku | Difference (95% interval) |
|---:|---|---:|---:|---|---:|---:|---|
| 36 | coverage | 4 | 0.9 | masked | 47.2% | 20.8% | +26.4 pp (+12.5 to +41.7) |
| 36 | coverage | 4 | 0.9 | visible | 56.9% | 40.3% | +16.7 pp (+1.4 to +31.9) |
| 108 | coverage | 12 | 0.1 | visible | 95.8% | 83.3% | +12.5 pp (+5.6 to +20.8) |
| 324 | degree | 4 | 0.9 | visible | 59.7% | 37.5% | +22.2 pp (+8.3 to +37.5) |
| 324 | no_verification | 0 | 0.9 | visible | 50.0% | 29.2% | +20.8 pp (+6.9 to +36.1) |
| 972 | random | 4 | 0.1 | masked | 76.4% | 56.9% | +19.4 pp (+11.1 to +29.2) |
| 972 | coverage | 108 | 0.1 | visible | 100.0% | 98.6% | +1.4 pp (0.0 to +4.2) |
| 972 | coverage | 108 | 0.9 | visible | 45.8% | 52.8% | −6.9 pp (−19.4 to +6.9) |

Measured: Sonnet's gains are largest where admitted packets mix honest specialists with repeated fabrications (weak checks, no verification, degree selection), i.e. where synthesis judgement matters. Where proportional strong checks already admit almost no attackers, both models are near ceiling. Over all rare fields Sonnet gave 2,210 wrong non-null answers and 1,598 abstentions out of 7,200; Haiku gave 2,756 and 1,390. Inferred, not tested: Sonnet discounts repeated identical reports more often and abstains more when evidence conflicts. Intervals are descriptive paired-world bootstraps (seed 20261004); 100 cells were compared, so individual cell intervals are not corrected for multiplicity.

## Scope

The same limits as the Haiku study apply: one synthetic graph family, a single +7 fabrication, six repeated facts, two trusted seeds, attacker resources that grow with population, and synthetic identities rather than autonomous agents. A model change cannot alter which identities are admitted, so this replication tests synthesis robustness, not the admission policies themselves. Exploratory only; S2 stays disabled.

## Reproduction

Raw records were fetched from the study servers (sim-dmarz-3 for Sonnet, sim-dmarz-4 for Haiku) into git-ignored `data/`. `python3.12 reporting/build_report.py <sonnet-run-dir> <out>` recomputed all 2,400 evaluations and the frozen analysis exactly (`analysis_matches: true`, source hash `a1a619f7…`). The same script on the Haiku records reproduced the committed Haiku `results-cells.csv` byte for byte. `python3.12 reporting/compare_models.py <sonnet-run-dir> <haiku-run-dir> <out>` produces the cross-model tables. Pinned dependencies: requirements.txt.
