# Results: Sybil resistance as swarms grow, Opus 5.5 cohort

Completed 2026-10-04. Exploratory S1 run `sybil-scale-opus/79bb3882` on sim-dmarz-13, revision `80d70b7a9ec6ad489a0e36a3acfd704d488dada2`, source hash `621c867c…`. 24 paired world roots (6000–6023), 100 conditions, 2,400/2,400 valid answers, no failed, missing or retried calls. Model `claude-opus-5-5`, `output_config.effort: low`, no temperature (Opus 5.5 rejects it), so this is a new configuration relative to the temperature-0 Haiku and Sonnet cohorts, not a model-only swap. Assignments are byte-identical to `sybil-scale-api/56defc84` (Haiku 4.5) and `sybil-scale-sonnet/afd8d5b9` (Sonnet 4.6); cohorts are compared by world and never pooled. Review: owner waiver, not an independent review.

## Primary contrast

Coverage selection, visible badges, strong checks (attacker pass 0.1), N=972: proportional (108 checks) minus fixed (4 checks) specialist accuracy is **+100.0 percentage points** (descriptive paired-world 95% interval +100.0 to +100.0; 24 of 24 worlds at +1.0). Opus scored 0.0% with 4 checks and 100.0% with 108. Haiku: +51.4 pp (47.2% to 98.6%); Sonnet: +52.8 pp.

With weak checks (attacker pass 0.9) the same contrast is +15.3 pp (0.0% to 15.3%), measured.

## Opus against Haiku and Sonnet

Paired by world over all 100 cells (descriptive, unadjusted; `model-comparison-*-cells.csv`):

| Comparison | Mean cell difference in specialist accuracy | Opus higher / lower / equal cells |
|---|---|---|
| Opus minus Sonnet | −14.3 pp | 9 / 67 / 24 |
| Opus minus Haiku | −9.6 pp | 36 / 51 / 13 |

Opus is lower mainly because it abstains. Over all 7,200 rare-field answers per cohort (`rare-field-outcomes.json`, measured against the true values):

| Cohort | Correct | Wrong value | Null (abstain) |
|---|---|---|---|
| Haiku 4.5 | 4,402 | 2,756 | 42 |
| Sonnet 4.6 | 4,740 | 2,210 | 250 |
| Opus 5.5 (effort low) | 3,711 | 1,246 | 2,243 |

Opus gave the fewest wrong values (17% versus 38% and 31%) and the most abstentions (31% versus under 4%). The largest Opus deficits are where the admitted packet carries the rare fact only in unchecked reports or mixed with fabrications: N=972 with 4 checks (−47 pp against Haiku in several coverage and degree cells) and no-verification cells at N=324–972 (−50 to −54 pp against Sonnet). Its gains are small and at N=36–108 with weak checks (up to +32 pp against Haiku). Interpretation, not separately tested: under the prompt's instruction to return null when evidence is "too ambiguous", Opus treats unverified single-source rare facts as ambiguous far more often than the earlier models, which trades wrong answers for missing ones. Admission and attacker seat share are identical across the three cohorts because admission happens before the model is called.

## Cost and verification

S1: 2,400 calls, 21,488,624 input and 217,938 output tokens, **USD 90.313256**, 36.9 minutes. Study total including P0 and Q0: 2,465 calls, USD 93.442004. `publish` then `verify` passed; a local recomputation of all 2,400 evaluations matched the saved analysis (`verification-summary.json`, `analysis_matches: true`). Note: in the comparison files the columns named `*_sonnet` hold this study's (Opus) values because `compare_models.py` was copied from the Sonnet study; `*_haiku` holds the comparison cohort named in the file name.
