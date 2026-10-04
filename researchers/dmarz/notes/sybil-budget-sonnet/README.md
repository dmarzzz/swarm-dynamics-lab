# Verification budget and verifier reliability: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/budget-sonnet at planning time ([rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4**: planned only. No qualification or scientific outcome exists for this cohort at this revision.
- **sample_size_summary:** Planned: Q0 4 worlds × 2 packet types × 1 size = 8 calls; S1 24 paired worlds × 60 cells = 1,440 assigned answers at N=972. Independent unit is the world (24), not the call, cell or identity. Observed: none.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-budget-api](../sybil-budget-api/README.md), owned by dmarz and operated by dmarz/budget-sonnet. It reruns the N=972 half of that study's frozen grid with `claude-sonnet-4-6` in place of `claude-haiku-4-5-20251001`, on the same 24 worlds, so every Sonnet answer pairs with a Haiku answer to an identical packet. The two models are separate cohorts; their data are never pooled. This is not an accepted formal hypothesis, and no independent review is claimed. S2 stays disabled.

## TLDR

Does a stronger synthesizer change how much identity verification a Sybil-attacked swarm needs? At 972 simulated identities, one model call combines the reports admitted after 4 to 108 random or topology-coverage checks, with attacker check-pass rates from 10% to 90%. Treatment is the model (Sonnet 4.6); the comparator is the Haiku 4.5 answer to the byte-identical packet from the parent study. The endpoints are specialist accuracy, attacker seat share (unchanged by the model, since admission is simulated) and the budget frontier at 90% accuracy and ≤5% attacker seats. Limits: one synthetic graph family, one fabrication rule, simulated checks, and 24 worlds. The run gives exploratory precision only.

## Question and prediction

Question: holding the admitted evidence fixed, does Sonnet 4.6 recover more specialist facts than Haiku 4.5, and does that move the smallest tested verification budget that meets the engineering target?

Prediction (stated before any Sonnet output): Sonnet will be at least as accurate where admitted packets contain the true specialist value in plurality, and the difference will be largest at middle budgets and weak checks, where the admitted packets contain repeated fabricated values (+7) alongside true reports. A plausible null result is that the two models agree because packet content, not synthesis skill, bounds accuracy. That result would mean verification budget, not the model, is the lever. An adverse result (Sonnet trusts repeated fabrications more) is also a valid finding. Attacker seat share and specialist retention are properties of the simulated admission and must be identical across cohorts; any difference would be an instrument fault.

## Setup

Everything is inherited unchanged from the parent: the graph generator, two trusted seeds, half-population PageRank admission, 90% honest check pass, the six-fact task with three specialist facts, the +7 fabrication, visible verification badges, the system prompt, the strict six-value JSON schema, temperature 0, 500 output tokens, no tools, thinking, cache or retries. `src/sim.py`, `src/study.py` and `src/analyze.py` are byte-identical to the parent, and a selftest enforces this. The only differences are in `design.yaml`:

- `model: claude-sonnet-4-6`, with list prices of $3 and $15 per million input and output tokens.
- `sizes: [972]`. The N=324 half of the parent grid is dropped, a choice pre-specified here before any run to hold Sonnet cost near the parent's. The parent's primary contrast is at N=972. The world generator depends only on the task root, size, rate and configuration, so the N=972 assignments are identical. A selftest checks that every S1 and Q0 assignment ID, packet hash and expected answer equals the parent's N=972 rows.
- Budget caps: a 1,600-call cap and a $290 nonrefundable reservation cap that covers the exact worst-case reservation of $277.24 for Q0 plus S1 (`reservation-plan.json`). Expected actual spend is about $75–100. That estimate applies the parent's 0.30 actual-to-reservation ratio and is not a bill. It counts against dmarz's $500 shared allowance.

Code changes outside `design.yaml`: the hub experiment id (`sybil-budget-sonnet`), the S1 frame label, and removal of the parent's shared two-study budget partition (`shared_budget.py`). This study uses only its own persistent ledger. The resulting `provider.py` is byte-identical to the one in [sybil-scale-api](../sybil-scale-api/src/provider.py). Python 3.12 and the pinned `requirements.txt`. The private claim-checked launcher supplies the source revision, host, exclusive claim and credentials by alias.

## Protocol

S1 grid: N=972 × 6 checking budgets (4, 8, 16, 32, 64, 108) × 5 attacker check-pass probabilities (0.1, 0.3, 0.5, 0.7, 0.9) × 2 policies (random, coverage) × 24 worlds (7000–7023) = 1,440 calls. Budgets are prefixes of each policy's check sequence within a world, as in the parent.

Stages, in order: offline selftests; S0 scripted grid on engineering worlds 6800–6801 plus clean controls on the fleet host; Q0 clean API competence on worlds 6900–6903 (full and common-only packets at N=972, 8 calls), with thresholds unchanged (100% structural validity, ≥95% field accuracy, ≥90% exact packets, 100% missing-fact abstention); S1 only after exact-runtime S0 and Q0 pass. Two concurrent requests, a 120-second request timeout, a 4-hour stage timeout and no retries. A failed call stops new dispatch, and every assigned row is preserved, including not-started rows. A failed Q0 blocks S1; it is diagnosed and recorded, and thresholds are never relaxed. Holdout 10000–19999 stays closed.

## Metrics

Primary (inherited, with N=972 the parent's primary cell): Sonnet specialist accuracy under coverage at attacker pass 0.1, 108 minus 4 checks, mean paired difference over 24 worlds with a seeded 10,000-resample world-bootstrap 95% interval.

Primary cross-cohort comparison, declared here: Sonnet minus Haiku specialist accuracy per cell on identical packets, paired by world, summarised over all 60 cells and for each budget × reliability, with world-bootstrap intervals. Haiku values come from the parent's saved S1 records (run `sybil-budget-api/46ebda03`), not re-collected. A useful model difference is ≥10 percentage points in a cell mean.

Secondary: the engineering frontier per policy × reliability (all tested budgets with mean accuracy ≥0.90 and attacker seats ≤0.05), equal-budget coverage-minus-random contrasts, six-fact accuracy, the identical-packet plurality baseline, tokens and actual cost. The attacker seat share and retention columns must match the parent exactly; this is a check, not a result. All comparisons are exploratory and descriptive, with no multiple-comparison significance claims.

## Interpretation limits

Same limits as the parent: synthetic identities and independent simulated checks, one graph family, a repeated six-fact task, one simple fabrication rule, one synthesizer call per packet (not 972 autonomous agents). The comparison is between two Anthropic models, not across model families. Identical packets mean the Haiku-versus-Sonnet difference isolates the synthesizer only; it does not test whether a different model would change admission.
