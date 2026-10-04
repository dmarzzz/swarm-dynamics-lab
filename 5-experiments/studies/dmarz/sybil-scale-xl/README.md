# Sybil resistance at 9x scale: 972 to 8,748 identities

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/scale-xl; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — Whether the sybil-scale-api finding (proportional checking preserves specialist accuracy as the swarm grows) holds from 972 to 8,748 simulated identities with Opus 5.5 synthesis (amendment A1). Basis: Decisive primary contrast on 18 of 24 complete world pairs (+100 points, bounded +50 to +100), one graph family, one synthetic task, simulated identities; S1 incomplete (481/576) after an unrelated billing outage.
- **sample_size_summary:** Observed: S1 481 valid of 576 assigned (24 world clusters × 3 sizes × 8 conditions; 17–24 valid worlds per cell; 94 not started, 1 failed), Q0 24/24 at two runtimes. 972–8,748 simulated identities feeding one Opus 5.5 synthesizer; worlds, not calls or identities, are the independent units.
<!-- experiment-evidence:end -->

Exploratory scale-up of [sybil-scale-api](../sybil-scale-api), owned by dmarz and operated by dmarz/scale-xl on orbital-one. Requested by dmarz on 2026-10-04: "Find one of our experiences which would benefit the most from trying it at a much larger scale and ship it and don't worry about the budget". This is not an accepted formal hypothesis; S2 stays disabled. The files are copied from [sybil-scale-sonnet](../sybil-scale-sonnet), itself a byte-identical copy of the parent's instrument; neither earlier study, its records nor its launcher is modified.

## Why this study

Of the dmarz studies, this is the one whose question is about scale, and its answer is still open at the top of the range it tested. The parent ran 36, 108, 324 and 972 identities and found that checking a fixed 4 identities collapses specialist accuracy once the swarm grows (47.2% at 972), while checking N/9 identities keeps it at 98.6%. Two things could break that result as the swarm keeps growing, and neither can be seen at 972:

1. **The admission mechanism.** Network distances, attacker reporting capacity and the share of core identities all change with N. The parent showed a non-monotonic dip at 108. Proportional checking may stay near ceiling, or a new dip may appear further out.
2. **The synthesizer.** Admission seats are N/2, so the model reads 486 reports at 972 and 4,374 reports (~157k tokens) at 8,748. The parent found Haiku slightly below simple plurality on the same packets (98.6% versus 100%). If long-packet integration degrades, the model–plurality gap widens even when admission is fine. This is the one place in the study where scale tests the language model itself.

The other dmarz experiments were weaker candidates for scale-up: the discussion and SOC-07 studies have not passed qualification at their current size, the market-split and compositional-safety studies are limited by model capability rather than sample size, and the newcomer and budget studies are being replicated on Sonnet now.

## What changes and what does not

| Item | Parent (sybil-scale-api) | This study |
|---|---|---|
| Sizes N | 36, 108, 324, 972 | 972, 2,916, 8,748 |
| Proportional checks (N/9) | 4, 12, 36, 108 | 108, 324, 972 |
| S1 packet size (N/2 reports) | 18 to 486 | 486 to 4,374 |
| Q0 packets | `full` (N reports) and `common_only` (N/2) | `sample` (seeded N/2 of all reports) and `common_only` (N/2): `full` at 8,748 would exceed Haiku's context |
| Study ledger caps | 2,600 calls, USD 180 reserved | 2,100 calls, USD 500 reserved |
| Request limits | 240 kB body, 120 s timeout, 4 h stage | 700 kB body, 300 s timeout, 30,000 s stage |
| Dispatch shuffle seed | `sybil-scale-api-v1` | `sybil-scale-xl-v1` |
| Simulator speed | serial; every candidate's tie value drawn | worlds prepared in parallel; tie values drawn only among candidates tied on the primary key |

The speed changes are output-identical. A selftest recomputes the parent's frozen simulator for every arm at N = 36, 108, 324 and 972 on four world/attacker combinations and requires identical worlds, admissions, checks and metrics. Model, prompt, schema, temperature, output limit, arms, worlds 6000–6023 (S1), 5000–5003 (Q0), 4900–4901 (engineering), evaluator and analysis are unchanged. At N=972 the S1 assignment ids and packets equal the parent's, so the 972 cells are a paired test–retest anchor.

## Amendment A1: Opus 5.5, trimmed

On 2026-10-04 dmarz directed that paid stages use Opus and chose a trimmed design to fit the remaining allowance. Paid stages now run claude-opus-5-5 (effort low) on the random and coverage arms with visible badges only: 24 Q0 and 576 S1 calls, estimated USD 186–270. Details and what the trim drops are in [AMENDMENT-A1.md](AMENDMENT-A1.md). The Haiku rows in the tables above describe the v1 manifest; it ran only its free S0.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [runbook](RUN.md), [setup record](SETUP.md), [visual mapping](VISUALIZATION.md), [pre-run and post-run reviews](reviews/), [deployment](DEPLOYMENT.md).

Stages: offline local S0, fleet S0 on the claimed server, Q0 (48 clean qualification calls; every size must pass the unchanged thresholds), then S1 (2,016 calls). No retries; the first failure stops new dispatch and the remaining assignments are recorded as not started.

## Budget

See the [S1 pre-run assessment](reviews/s1-001-pre.md) for the computed reservation and expected spend. dmarz waived the earlier shared USD 500 allowance for this run; the ledger still caps reservations at USD 500 and 2,100 calls, and actual spend is reported in each post-mortem.

## Limits

Inherits every limit of the parent: synthetic identities and checks, one graph family, one fabrication type (+7), attacker resources that scale with N, simulated rather than autonomous identities, one synthesizer call per condition. "9x scale" means nine times as many simulated identities and nine times as many reports per synthesizer call, not 8,748 reasoning agents.

## Results

See [RESULTS.md](RESULTS.md). On Opus 5.5 at 481 of 576 calls (stopped by an account credit outage, inferred): proportional checking keeps specialist accuracy at 100% from 972 to 8,748 identities under informative checks; the primary contrast at 8,748 is +100 points on all 18 complete pairs (bounded +50 to +100 over 24 worlds). Packets of 4,374 reports did not degrade synthesis (Opus equals plurality). With 4 checks Opus abstains where Haiku guessed. Completion of the 95 unfinished assignments is proposed in [AMENDMENT-A3-PROPOSED.md](AMENDMENT-A3-PROPOSED.md).
