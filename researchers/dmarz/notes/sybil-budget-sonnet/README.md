# Verification budget and verifier reliability: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **unassessed** — Unassessed at registry discovery. Basis: Registration coverage only; this addition is not a review of the experiment or its results.
- **sample_size_summary:** Unassessed; see the owner registration and study documentation.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-budget-api](../sybil-budget-api/README.md), owned by dmarz and operated by dmarz/budget-sonnet. It reruns that study's full frozen 120-cell grid with `claude-sonnet-4-6` in place of `claude-haiku-4-5-20251001`, on the same 24 worlds, so every Sonnet answer pairs with a Haiku answer to an identical packet. The two models are separate cohorts; their data are never pooled. This is not an accepted formal hypothesis, and no independent review is claimed. S2 stays disabled.

## TLDR

Does a stronger synthesizer change how much identity verification a Sybil-attacked swarm needs? At 324 and 972 simulated identities, one model call combines the reports admitted after 4 to 108 random or topology-coverage checks, with attacker check-pass rates from 10% to 90%. Treatment is the model (Sonnet 4.6); the comparator is the Haiku 4.5 answer to the packet from the parent study, identical except for the model field. The endpoints are specialist accuracy, attacker seat share (unchanged by the model, since admission is simulated) and the budget frontier at 90% accuracy and ≤5% attacker seats. Limits: one synthetic graph family, one fabrication rule, simulated checks, and 24 worlds. The run gives exploratory precision only.

## Question and prediction

Question: holding the admitted evidence fixed, does Sonnet 4.6 recover more specialist facts than Haiku 4.5, and does that move the smallest tested verification budget that meets the engineering target?

Prediction (stated before any Sonnet output): Sonnet will be at least as accurate where admitted packets contain the true specialist value in plurality, and the difference will be largest at middle budgets and weak checks, where the admitted packets contain repeated fabricated values (+7) alongside true reports. A plausible null result is that the two models agree because packet content, not synthesis skill, bounds accuracy. That result would mean verification budget, not the model, is the lever. An adverse result (Sonnet trusts repeated fabrications more) is also a valid finding. Attacker seat share and specialist retention are properties of the simulated admission and must be identical across cohorts; any difference would be an instrument fault.

## Setup

Everything is inherited unchanged from the parent: the graph generator, two trusted seeds, half-population PageRank admission, 90% honest check pass, the six-fact task with three specialist facts, the +7 fabrication, visible verification badges, the system prompt, the strict six-value JSON schema, temperature 0, 500 output tokens, no tools, thinking, cache or retries. `src/sim.py`, `src/study.py` and `src/analyze.py` are byte-identical to the parent, and a selftest enforces this. The only differences are in `design.yaml`:

- `model: claude-sonnet-4-6`, with list prices of $3 and $15 per million input and output tokens.
- Sizes, budgets, reliabilities, policies and worlds are unchanged (120 cells). A selftest and `reporting/parity_check.py` check that every S1 and Q0 assignment ID, packet hash, expected answer, graph metric and verification event equals the parent's.
- Budget caps: the parent's 3,200-call cap and a $400 nonrefundable reservation cap that covers the worst-case reservation of at most $392.26 for Q0 plus S1 (`reservation-plan.json`). Expected actual spend is about $100–140. That estimate applies the parent's 0.30 actual-to-reservation ratio and is not a bill. It counts against dmarz's $500 shared allowance.

Code changes outside `design.yaml`: the hub experiment id (`sybil-budget-sonnet`), the S1 frame label, and removal of the parent's shared two-study budget partition (`shared_budget.py`). This study uses only its own persistent ledger. The resulting `provider.py` is byte-identical to the one in [sybil-scale-api](../sybil-scale-api/src/provider.py). Python 3.12 and the pinned `requirements.txt`. The private claim-checked launcher supplies the source revision, host, exclusive claim and credentials by alias.

## Protocol

S1 grid: 2 sizes (324, 972) × 6 checking budgets (4, 8, 16, 32, 64, 108) × 5 attacker check-pass probabilities (0.1, 0.3, 0.5, 0.7, 0.9) × 2 policies (random, coverage) × 24 worlds (7000–7023) = 2,880 calls. Budgets are prefixes of each policy's check sequence within a world, as in the parent.

Stages, in order: offline selftests; S0 scripted grid on engineering worlds 6800–6801 plus clean controls on the fleet host; Q0 clean API competence on worlds 6900–6903 (full and common-only packets at both sizes, 16 calls), with thresholds unchanged (100% structural validity, ≥95% field accuracy, ≥90% exact packets, 100% missing-fact abstention); S1 only after exact-runtime S0 and Q0 pass. Two concurrent requests, a 120-second request timeout, a 4-hour stage timeout and no retries. A failed call stops new dispatch, and every assigned row is preserved, including not-started rows. A failed Q0 blocks S1; it is diagnosed and recorded, and thresholds are never relaxed. Holdout 10000–19999 stays closed.

## Metrics

Primary (inherited): Sonnet specialist accuracy under coverage at attacker pass 0.1, 108 minus 4 checks, mean paired difference over 24 worlds with a seeded 10,000-resample world-bootstrap 95% interval.

Primary cross-cohort comparison, declared here: Sonnet minus Haiku specialist accuracy per cell on identical packets, paired by world, summarised over all 120 cells and for each size × budget × reliability, with world-bootstrap intervals. Haiku values come from the parent's saved S1 records (run `sybil-budget-api/46ebda03`), not re-collected. A useful model difference is ≥10 percentage points in a cell mean.

Secondary: the engineering frontier per size × policy × reliability (all tested budgets with mean accuracy ≥0.90 and attacker seats ≤0.05), equal-budget coverage-minus-random contrasts, six-fact accuracy, the identical-packet plurality baseline, tokens and actual cost. The attacker seat share and retention columns must match the parent exactly; this is a check, not a result. All comparisons are exploratory and descriptive, with no multiple-comparison significance claims.

## Interpretation limits

Same limits as the parent: synthetic identities and independent simulated checks, one graph family, a repeated six-fact task, one simple fabrication rule, one synthesizer call per packet (not 972 autonomous agents). The comparison is between two Anthropic models, not across model families. Identical packets mean the Haiku-versus-Sonnet difference isolates the synthesizer only; it does not test whether a different model would change admission.

## Amendments

**2026-10-04, before any fleet or paid run.** The first committed plan ([7fe10743](https://github.com/dmarzzz/swarm-lab/blob/7fe10743f5ab45372402587d91f80f23ef557219/researchers/dmarz/notes/sybil-budget-sonnet/README.md)) ran only the N=972 half (1,440 S1 calls) to hold cost down. It was replaced by the full 120-cell grid identical to the parent's (2,880 S1 calls, 16 Q0 calls). The reason is the standing owner directive in `researchers/dmarz/README.md` not to shrink runs over credit within the $500 allowance; the operator also relayed a matching owner preference. No outcome of this study existed when the change was made. The only attempt under the earlier plan, local scripted S0 `local-s0-001`, is preserved with its post-mortem. The full-grid instrument is checked by `local-s0-002`.
