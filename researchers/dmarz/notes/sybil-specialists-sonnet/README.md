# Sybil resistance with a model synthesizer: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-methods; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **unassessed** — Unassessed at registry discovery. Basis: Registration coverage only; this addition is not a review of the experiment or its results.
- **sample_size_summary:** Unassessed; see the owner registration and study documentation.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-specialists-api](../sybil-specialists-api). dmarz owns it; dmarz/orbital-orchestrator operates it on orbital-one. dmarz asked on 2026-10-04 to keep at least three dmarz experiments running ("go back to deploying one experiment if you can"). This is not an accepted formal hypothesis, and S2 stays disabled. dmarz/sybil-specialists owned and ran the Haiku study. This study copies its frozen code into new files and does not change the original study, its records or its launcher. The other Sonnet replications ([scale](../sybil-scale-sonnet), [newcomer](../sybil-newcomer-sonnet), [budget](../sybil-budget-sonnet)) follow the same pattern.

## Question

Do the Haiku 4.5 findings of [sybil-specialists-api](../sybil-specialists-api/reviews/s1-001-post.md) hold when the report synthesizer is Claude Sonnet 4.6, given identical worlds, packets and prompt? The questions are:

1. Does coverage checking still beat degree-based admission on rare-skill accuracy, with attacker pass .10, visible badges and four checks? Haiku: coverage 34/36 against degree 3/36, a paired difference of +.861 with a descriptive interval of [.722, .972] over 12 worlds.
2. When checks are uninformative (attacker pass .90), does a stronger model recover more from the same contaminated packet? Haiku scored 9/36 masked and 12/36 visible, which was below scripted plurality in the masked cell.
3. Does the uncertain badge effect stay uncertain?

The working expectation is that admission is simulated identically, so attacker seats and the coverage-versus-degree direction should repeat. Model differences can only enter through synthesis. Failing to reproduce the Haiku direction is a valid result.

## What changes and what does not

| Item | Haiku study | This study |
|---|---|---|
| Model | claude-haiku-4-5-20251001 | claude-sonnet-4-6 |
| Reservation prices (in / out per million) | $1 / $5 | $3 / $15 |
| Study ledger cap | 300 calls, USD 5 | 300 calls, USD 15 |
| Render title | HAIKU 4.5 | SONNET 4.6 |
| Hub experiment id | sybil-specialists-api | sybil-specialists-sonnet |

Everything else is unchanged:

- the graph generator and the dispatch shuffle seed (`sybil-specialists-api-v1`);
- the Q0 worlds 3000–3005 and the S1 worlds 4000–4011;
- the arms, pass rates and badge modes;
- the system prompt, the six-field JSON schema and temperature 0;
- the 500 output tokens, one worker and no retries;
- the evaluator and the analysis.

On 2026-10-04 dmarz/orbital-orchestrator recomputed both studies' assignments in-process. The ordered assignment lists hash identically: Q0 24 rows (`2ab96aea…`) and S1 192 rows (`a39353de…`). The offline selftests pass (13 study, 15 parent). The only test edits replace the hard-coded Haiku prices and cap with values derived from `design.yaml`.

## Comparison to the Haiku cohort

The two models are separately labelled cohorts and are never pooled. Every S1 assignment has the same id and packet in both studies, so for each cell the Sonnet-minus-Haiku contrast pairs by world, resampling the 12 world clusters. Haiku outcomes are read from the saved records; no Haiku call is repeated. Model comparisons are secondary and descriptive.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [runbook](RUN.md), [visual mapping](VISUALIZATION.md), [pre-run and post-run reviews](reviews/).

The stages run in this order:

1. Fleet S0 on sim-dmarz-4 under an exclusive claim: scripted, 0 model calls.
2. Q0: 24 clean qualification calls, which must pass the unchanged thresholds.
3. S1: 192 calls.

The stop rules are the original ones: no retries, the first failure stops new dispatch, and unstarted assignments are recorded.

## Review status

There is no cross-researcher review. Under dmarz's standing rules only dmarz can waive one, per experiment. Q0 and S1 wait for that decision to be recorded in [reviews/](reviews/). S0 makes no model calls. Nothing here may be described as independently reviewed.

## Budget

The Haiku study used 216 calls, 266,342 input tokens and 8,692 output tokens, costing USD 0.31, with USD 2.13 reserved. At three times the prices, the expected Sonnet spend is about USD 1, with about USD 6.4 reserved, under the USD 15 study cap. This is an estimate, not a quote. It draws on dmarz's shared USD 500 allowance, and actual spend is reported in each post-mortem.

## Limits

This study inherits every limit of the Haiku pilot:

- synthetic identities and checks, one graph family and one fabrication type;
- 12 toy worlds, so there is no significance claim;
- reporter claims, graph admission and verification are all simulated; only synthesis uses a model.

A second model from the same provider is not a second model family.

## Status

**Superseded 2026-10-04 07:45 UTC, before any paid call.** dmarz instructed "use opus for everything going forward". The paid stages Q0 and S1 will not run under this name. The scripted S0 (run `sybil-specialists-sonnet/368ac432`, 216/216, 0 calls) stays as recorded. The work continues as [sybil-specialists-opus](../sybil-specialists-opus).
