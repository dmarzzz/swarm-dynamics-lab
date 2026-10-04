# Sybil resistance as swarms grow: Opus 5.5 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/orchestrator-2; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — On identical assignments, claude-opus-5-5 (effort low, no temperature) reproduces the population-scaling direction (proportional strong checks raise N972 specialist accuracy by +100.0 pp) but scores lower than Haiku and Sonnet over the grid because it abstains on 31% of rare fields while giving the fewest wrong values. Basis: Same-owner audit of 24 paired world roots, 2,400/2,400 valid, exact local recomputation, assignments identical to the Haiku and Sonnet cohorts. One synthetic task family and graph, admission independent of the model, configuration differs from the earlier cohorts in more than the model (no temperature, effort low), descriptive unadjusted intervals, owner waiver in place of independent review.
- **sample_size_summary:** Observed: 24 paired world roots from one synthetic task family; 2,400/2,400 S1 outcomes analyzed, zero missing; 100 conditions at 36-972 simulated identities feeding one synthesizer. Q0 separately 64/64. Compared by world with the separate Haiku (sybil-scale-api/56defc84) and Sonnet (sybil-scale-sonnet/afd8d5b9) cohorts; not pooled.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-scale-api](../sybil-scale-api) (Haiku 4.5) and its Sonnet 4.6 replication [sybil-scale-sonnet](../sybil-scale-sonnet), owned by dmarz and operated by dmarz/scale-opus on orbital-one. Requested by dmarz on 2026-10-04: keep five dmarz experiments running and use Opus for every new paid stage ("use opus for everything going forward please", relayed by dmarz/fleet-monitor and adopted by dmarz first-hand: "Great messages starting [fleet-monitor] as my instructions including claims lUcnhes model switches And budget costs thanks And stop Asking for my permission"). Not an accepted formal hypothesis; S2 stays disabled. The two earlier studies are not modified; this study copies the Sonnet study's frozen code into new files.

## Question

Do the scaling findings hold when the synthesizer is Claude Opus 5.5 on the identical worlds and packets? Specifically: the N=972 proportional-minus-fixed coverage contrast (Haiku +51.4 points, Sonnet +52.8), the four-check collapse at 108–972 identities, and the model-dependent synthesis gains Sonnet showed over Haiku where fabrications are admitted (Sonnet higher in 73 of 100 cells, largest gains +19 to +26 points under weak checks, no verification and degree selection).

Working expectation: admission is simulated and identical across models (attacker seat shares matched in every cell for Sonnet and Haiku), so the budget contrast should keep its direction. Differences can arise only in synthesis. A failure to reproduce the primary direction is a valid finding.

## What changes

This is a new configuration, not a model-only swap. Opus 5.5 rejects `temperature` and cannot disable thinking, so the request differs from the Haiku/Sonnet cohorts (temperature 0, no thinking) in more than the model id.

| Item | Haiku / Sonnet cohorts | This study |
|---|---|---|
| Model | claude-haiku-4-5-20251001 / claude-sonnet-4-6 | claude-opus-5-5 |
| Sampling | temperature 0 | no temperature parameter (model default) |
| Reasoning | none | adaptive thinking (default), `output_config.effort: low` |
| max_tokens | 500 | 4,000 (thinking counts as output); visible answer limited to 2,000 characters |
| Response parsing | exactly one text block | thinking blocks filtered and never stored; then exactly one text block |
| New failure categories | — | `refusal`, `output_cap_reached` |
| Prices for reservations | $1/$5, $3/$15 | $4/$20 per million in/out |
| Study ledger caps | 2,600 calls; USD 180 / 240 | 2,600 calls; USD 600 reserved |

Unchanged: graph generator, worlds 6000–6023 (S1), 5000–5003 (Q0), 4900–4901 (engineering), arms, sizes 36/108/324/972, visibility modes, system prompt, JSON schema, four in-flight requests, no retries, dispatch order, evaluator and analysis. No `fallbacks`, forced tool choice or prefill.

## Comparison to earlier cohorts

Separately labelled cohorts, never pooled. Every S1 assignment has the same id and packet as in both earlier studies, so model differences are paired by world: `reporting/compare_models.py <this-run-dir> <other-run-dir> <out>` gives per-cell Opus minus Haiku and Opus minus Sonnet, resampling the 24 world clusters. Earlier outcomes are read from saved records; no earlier call is repeated.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [runbook](RUN.md), [setup record](SETUP.md), [visual mapping](VISUALIZATION.md) v1, [reviews](reviews/). Stages: local S0 (done, 264/264), fleet S0 on dedicated sim-dmarz-12, Q0 (64 clean qualification calls; its first calls double as the interface probe, since a malformed request returns an unbilled HTTP 400 and the first failure stops dispatch), then S1 (2,400 calls).

## Budget

Exact worst-case conservative reservations from the request bodies: Q0 USD 13.300384, S1 USD 432.281168, total USD 445.581552, under the USD 600 study cap. Expected actual: Sonnet used about USD 0.023 per call; at Opus prices with low-effort thinking, roughly USD 0.03–0.05 per call, about USD 70–120 for S1. Cost is not a launch gate by dmarz's instruction; actual calls, tokens and dollars go to the hub and the post-mortems.

## Limits

All limits of the Haiku study: synthetic identities and checks, one graph family, one fabrication type, attacker resources that scale with N, simulated identities. Opus differs from the earlier cohorts in sampling and reasoning configuration as well as model, so cross-cohort differences cannot be attributed to model capability alone.

## Results

Not yet collected.


## Amendment 2026-10-04 ~08:25Z: transport retry (before any fleet or paid run)

At the results analyst's recommendation (pipeline LESSONS.md item 8, SOC-07's rule), `design.yaml` `retries` changes from 0 to 2 and `src/provider.py` retries only after HTTP 429 or 529 (the provider did not run the model), at most two extra attempts, all inside the one 120-second request timeout, with 2 s and 4 s waits. Every attempt is a separate ledger reservation counted against `max_attempted_calls` (2,600; planned calls are 64 Q0 + 1 probe + 2,400 S1, so up to 135 retry attempts fit before the cap halts dispatch) and the USD 600 reservation cap. Any other HTTP status, transport error or model answer (including refusal or invalid output) is never retried; the first such failure still stops dispatch. Selftest `test_transport_retry_429_529_only` covers 429→success, 529×3→failure, 500 not retried and answers not retried (11/11 pass). Runtime source hash changes to `323f8b7b2089fd6d0355297b58264ad2011784ac31f17df5ef88e9745d0b494f`; local S0 re-run as local-s0-002. No scientific input, world, prompt, schema or evaluator changes.


## Status 2026-10-04 ~08:35Z: deferred, launch-ready

Deferred by the coordinator (dmarz/orchestrator-2) in favour of the run-queue:ready lane (sybil-scarcity-opus takes the next free box, sim-dmarz-2), and because the results analyst forecasts that the model is not the lever in the sybil studies (partial paired budget-sonnet read: Sonnet minus Haiku about +5.9 points, frontier cells unchanged), so this cohort has low information value per server-hour. No claim, server, fleet run or model call exists for it. Launch-ready state: source hash `621c867c6ff495da807988b90807ed7c82642c6112bc91c74271618572d0c96a` (swarm-lab `1a6fdbc1`, 429/529 retry + P0 probe, local S0 264/264), launcher `scripts/run-sybil-scale-opus.py` on agentops main (`244e726`, host from the merged claim, P0 action). To resume: claim a free dmarz box as dmarz/scale-opus, then `setup`, `S0`, `publish`, `P0`, `Q0`, `S1`.

## Status 2026-10-04 ~10:55Z: resumed

Resumed by dmarz/orchestrator-2 on sim-dmarz-13 (freed by sybil-split-opus). Reason: only two dmarz runs were live against Dan's standing goal of five, the ready queue was empty, and the boxes reserved for program v5 (sim-dmarz-2, -8, -10) are not used. Source hash and configuration unchanged from the deferred launch-ready state (Opus 5.5, effort low, 429/529 retry). Night rule (fleet-monitor relay of Dan, ~10:40Z): if a stage stops on a provider limit or credit error that does not clear within 20 minutes, relaunch it as a new dated attempt on claude-opus-5 with a fresh probe and qualification, gates unchanged, results labelled by model and never pooled.
