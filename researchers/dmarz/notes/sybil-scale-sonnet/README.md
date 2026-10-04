# Sybil resistance as swarms grow: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/scale-sonnet; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Whether the Haiku sybil-scale-api budget-scaling findings hold with claude-sonnet-4-6 on identical worlds and packets. Basis: Unrun replication: only offline scripted S0 has executed. It does not inherit the Haiku study's score or sample count.
- **sample_size_summary:** Observed: none (offline scripted S0 264/264 only). Planned: 24 paired worlds × 100 conditions = 2,400 S1 calls plus 64 Q0 calls; 36–972 simulated identities feeding one synthesizer.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-scale-api](../sybil-scale-api), owned by dmarz and operated by dmarz/scale-sonnet on orbital-one. Requested by dmarz on 2026-10-04 as part of keeping at least three dmarz experiments running ("make sure at least 3 experiments are running at all time for swarm labs"). This is not an accepted formal hypothesis; S2 stays disabled. The Haiku study was owned and run by dmarz/sybil-specialists; this study copies its frozen code into new files and does not modify the original study, its records or its launcher.

## Question

Do the Haiku 4.5 scaling findings of [sybil-scale-api](../sybil-scale-api/RESULTS.md) hold when the report synthesizer is Claude Sonnet 4.6, on the identical worlds, packets and prompt? In particular: does proportional coverage checking still preserve specialist accuracy at 972 identities relative to four fixed checks (Haiku: +51.4 points, descriptive interval +38.9 to +62.5), does the four-check collapse at 108–972 identities persist, and how much does a stronger synthesizer change the model-minus-plurality gap and the weak-check result?

Working expectation: the graph-admission mechanism is model-independent (admission, checks and seats are simulated identically), so the budget contrast should persist in direction. The plausible differences are in synthesis: a stronger model may extract more rare facts from the same packet, or abstain more often where reports conflict. A replication that fails to reproduce the Haiku primary direction is a valid finding and will be reported as such.

## What changes and what does not

| Item | Haiku study | This study |
|---|---|---|
| Model | claude-haiku-4-5-20251001 | claude-sonnet-4-6 |
| Prices used for reservations | $1 / $5 per million in/out | $3 / $15 per million in/out |
| Study ledger caps | 2,600 calls, USD 180 reserved | 2,600 calls, USD 240 reserved |
| Render title label | HAIKU 4.5 | SONNET 4.6 |
| Hub experiment id | sybil-scale-api | sybil-scale-sonnet |

Everything else is byte-identical in effect: graph generator, worlds 6000–6023 (S1), 5000–5003 (Q0), 4900–4901 (engineering), arms, sizes 36/108/324/972, visibility modes, system prompt, JSON schema, temperature 0, 500 output tokens, 4 in-flight requests, no retries, the dispatch shuffle seed, the evaluator and the analysis. A pre-registration check (2026-10-04, dmarz/scale-sonnet) recomputed both studies' assignments in-process: the ordered list of (assignment id, packet hash) is identical for Q0 (64 rows, digest `2bc4840f…`) and S1 (2,400 rows, digest `8968bde3…`), and the prompt+schema digest is identical (`5458c494…`).

## Comparison to the Haiku cohort

The two models are separately labelled cohorts and are never pooled. Because every S1 assignment has the same id and packet in both studies, model differences are paired by world: for each cell, the descriptive contrast is Sonnet minus Haiku accuracy, resampling the 24 world clusters. The Haiku outcomes are read from the saved [sybil-scale-api](../sybil-scale-api) records; no Haiku call is repeated. Comparisons of the two models are secondary and descriptive.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [runbook](RUN.md), [setup record](SETUP.md), [visual mapping](VISUALIZATION.md), [pre-run and post-run reviews](reviews/).

Stages: offline local S0 (done, 264/264), fleet S0 on a dedicated claimed server (264 scripted rows), Q0 (64 clean qualification calls, every size must pass the unchanged thresholds), then S1 (2,400 calls). Same stop rules as the original: no retries, the first failure stops new dispatch, remaining assignments are recorded as not started.

## Budget

Worst-case conservative reservations computed from the exact request bodies: Q0 USD 6.615672, S1 USD 198.225276, total USD 204.840948, under the USD 240 study cap. Expected actual spend is about three times the Haiku study's USD 19.45, roughly USD 60, if Sonnet's token usage matches Haiku's; this is an estimate, not a quote. This draws on dmarz's shared USD 500 model-API allowance; actual spend is reported in each post-mortem.

## Limits

Inherits every limit of the Haiku study: synthetic identities and checks, one graph family, one fabrication type, attacker resources that scale with N (not fixed-resource identity splitting), simulated rather than autonomous identities. A second model from the same provider is not a second model family.

## Results

Not yet collected.
