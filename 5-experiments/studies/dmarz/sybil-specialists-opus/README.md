# Sybil resistance with a model synthesizer: Opus 5.5 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/fleet-monitor; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — Untested: with claude-opus-5-5 as the synthesizer on the Haiku pilot's identical S1 packets, coverage auditing still beats degree auditing on rare-skill accuracy. Basis: Prepared model replication only. The scripted S0 stage ran (216 of 216 valid, zero model calls); no qualification or S1 model call exists. Admission is simulated identically to the Haiku pilot, so only synthesis can differ.
- **sample_size_summary:** Observed: scripted S0 only, 216 rows, no model outcome. Planned: Q0 on fresh worlds 3100-3105; S1 on the Haiku pilot's 12 worlds (4000-4011), 192 packets; ledger cap 300 calls. Worlds are the independent units.
<!-- experiment-evidence:end -->

Exploratory model replication of [sybil-specialists-api](../sybil-specialists-api) (Haiku 4.5) with `claude-opus-5-5` as the report synthesizer. dmarz owns it; dmarz/orbital-orchestrator operates it on orbital-one. It replaces the [Sonnet 4.6 version](../sybil-specialists-sonnet), which ran only its scripted S0. dmarz asked on 2026-10-04 to "use opus for everything going forward"; the change is recorded as [Amendment A1](preregistration.md). This is not an accepted formal hypothesis, and S2 stays disabled.

## Question

Do the Haiku findings hold with a much stronger synthesizer on identical S1 packets?

1. Does coverage still beat degree on rare-skill accuracy (attacker pass .10, visible badges, four checks)? Haiku: 34/36 against 3/36, a paired difference of +.861 with an interval of [.722, .972] over 12 worlds.
2. With uninformative checks (attacker pass .90), does Opus recover more from contaminated packets? Haiku scored 9/36 masked and 12/36 visible, below scripted plurality when masked.
3. Does the badge effect stay uncertain?

Attacker admission is simulated identically, so the admission side must match the Haiku study exactly. Model differences can only enter through synthesis. Failing to reproduce the Haiku direction is a valid result.

## What changes

| Item | Haiku pilot | This study |
|---|---|---|
| Model | claude-haiku-4-5-20251001, temperature 0, no thinking | claude-opus-5-5, adaptive thinking at effort low (cannot be disabled), no sampling parameters |
| Output cap | 500 | 3,000 (thinking counts against it) |
| Prices (in / out per million) | $1 / $5 | $4 / $20 |
| Ledger cap | 300 calls, USD 5 | 300 calls, USD 40 |
| Q0 worlds | 3000–3005 | 3100–3105 (fresh) |
| S1 worlds and packets | 4000–4011, 192 rows | identical (ordered hash `7eaff47f…`) |
| Hub experiment | sybil-specialists-api | sybil-specialists-opus |

Everything else is unchanged:

- the simulator and the dispatch seed;
- the system prompt and the six-field JSON schema;
- one worker and no retries;
- the evaluator, the thresholds and the analysis.

Offline selftests pass: 15 study tests, including new tests for the Opus request shape, ignored thinking blocks and refusal handling, plus the 15 parent tests.

## Review status

There is no cross-researcher review. Under dmarz's standing rules only dmarz can waive one, per experiment. Q0 and S1 wait for that decision. S0 makes no model calls. Nothing here may be described as independently reviewed.

## Budget

The expected spend is USD 1.6–5.7 for Q0 plus S1; [Amendment A1](preregistration.md) gives the basis. The worst-case reservation is about USD 27, under the USD 40 study cap. This draws on dmarz's shared USD 500 allowance, of which the hub reported about USD 160 spent on 2026-10-04. Q0's measured usage replaces the estimate before S1 launches.

## Protocol and records

[Pre-registration](preregistration.md), [design](design.yaml), [runbook](RUN.md), [visual mapping](VISUALIZATION.md), [reviews](reviews/).

The stages run in this order:

1. Fleet S0: scripted, 0 calls.
2. Q0: 24 calls on fresh worlds; it must pass the unchanged thresholds.
3. S1: 192 calls.

## Limits

This study inherits every limit of the Haiku pilot: synthetic identities and checks, one graph family and 12 toy worlds. Opus thinks before answering and Haiku did not, so a model difference mixes model capability with the presence of reasoning.

## Results

Not yet collected.
