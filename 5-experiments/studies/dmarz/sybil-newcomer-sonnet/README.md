# Knowledgeable newcomers versus a trusted Sybil coalition: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/newcomer-sonnet; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — In this synthetic newcomer task, replacing the Haiku 4.5 synthesizer with Sonnet 4.6 on identical assignments did not materially change outcomes: the sleeper attack still sharply reduced specialist accuracy, the policy ranking was unchanged, and renewal minus reputation stayed inconclusive (+11.1 pp, interval -0.0 to +22.2 pp; +2.8 pp more than Haiku, interval -2.8 to +8.3 pp). Basis: Same-owner assessment: twenty-four paired roots, passed qualification, 1,944/1,944 outcomes paired by assignment with the Haiku cohort and fully reconciled. One task family, two models from one provider, scripted actors and descriptive unadjusted intervals limit stronger conclusions. Independent review was waived by the owner.
- **sample_size_summary:** Observed: 24 paired roots from one synthetic task family; 1,944/1,944 S1 outcomes analyzed, zero missing, each paired by assignment ID with the separate Haiku cohort (not pooled); 24 honest + 1/4/16 controller identities, one synthesizer model. Q0 separately: 36/36 clean calls.
<!-- experiment-evidence:end -->

Model replication of [sybil-newcomer-api](../sybil-newcomer-api/README.md). Everything is held fixed except the synthesizing model, which changes from Haiku 4.5 to Sonnet 4.6. This is an exploratory S0/Q0/S1 study in `notes/`. It is not an accepted hypothesis, a completed novelty survey or a formal S2 experiment, and it has not been independently reviewed. See [SETUP.md](SETUP.md) for gate status.

## TLDR

The Haiku study found that after a coordinated sleeper attack, none of three equal-cost audit policies kept specialist accuracy high (round 8, sixteen controller identities: random 26.4%, renewal 20.8%, reputation 12.5%; renewal minus reputation +8.3 points, interval −2.8 to +19.4). Most lost accuracy traced to admission discarding the unique honest reports, not to synthesis. This replication sends the identical 1,944 packets to Sonnet 4.6. If Sonnet's accuracy and policy contrasts match Haiku's, the result is about admission. If Sonnet is much better on the same packets, part of the Haiku result was synthesizer weakness. Limits: one synthetic task family, scripted actors, the Haiku outcomes were known when this was written, and 24 worlds is a small exploratory sample.

## Question and prediction

Does the newcomer-study result depend on the synthesizing model? Primary contrast, unchanged from the original: renewal minus reputation specialist accuracy at sixteen controller identities, sleeper strategy, round eight, with a +10-point useful-effect marker. Prediction, written before any Sonnet call: the Haiku pattern replicates. All policies lose specialist accuracy under the sleeper attack, the primary contrast stays below +10 points, and accuracy stays bounded by the model-independent available-truth diagnostic. A Sonnet primary contrast of +10 points or more, or a sign reversal, would mean the Haiku conclusion is model-dependent. Null and adverse outcomes are valid results.

## Setup

Python 3.12 with pinned [requirements](requirements.txt); model `claude-sonnet-4-6`, temperature zero, native structured JSON, no tools, thinking or caching. The simulator, worlds 7100–7123, qualification worlds 7000–7005, engineering worlds 6900–6901, policies, system prompt, schema, evaluator and analysis are copied unchanged. Before launch, the Q0 and S1 assignment IDs, packet hashes, expected answers and dispatch order were checked equal to the Haiku study. Code changes are limited to the experiment identifier, the model id and token prices in [design.yaml](design.yaml), the run banner, and removal of the Haiku study's shared two-study budget partition: this study uses its own ledger. One dedicated fleet host under an exclusive claim; credentials reach the worker only as environment aliases from the private launcher.

## Protocol

Identical to the [original protocol](../sybil-newcomer-api/preregistration.md); the frozen copy for this study is [preregistration.md](preregistration.md). Each world runs eight simulated rounds with 18 honest veterans, six honest newcomers arriving in round 4 (three carry the only honest copy of a specialist fact), and one controller sending 16 messages per round over 1, 4 or 16 identities. Random, reputation and renewal policies each get four claim checks and admit twelve reports per round. Sonnet synthesizes the admitted packet at rounds 4, 5 and 8. Strategies are clean, sleeper (lies from round 4) and relapse (lies in rounds 4, 7, 8). S1 is 24 worlds × 3 identity counts × 3 policies × 3 strategies × 3 rounds = 1,944 calls. Q0 is 36 clean packets with the original thresholds (per shape ≥95% field accuracy, ≥90% exact packets, 100% abstention on absent fields); a failed Q0 blocks S1. S0 is the 198-observation scripted rehearsal on the fleet host. Any invalid call stops new dispatch; no retries.

## Metrics

Primary: specialist accuracy (exactly correct current skills 3–5, divided by three), renewal minus reputation, paired by world, with a 10,000-resample whole-world bootstrap (seed 20261004). Secondary, all reported: every cell of the 81-cell matrix, renewal minus random, wrong specialist outputs, harmful and controller seat share, newcomer retention, the available-truth diagnostic, and 16-minus-1 identity contrasts. Cross-model, descriptive: Sonnet minus Haiku accuracy on identical packets per policy at the primary cell, the difference between the two models' primary contrasts (paired-world bootstrap), and the share of identical packets answered identically. The world is the independent unit; identities, rounds and calls are not.

## Budget

2,050 attempted-call cap and a $75 nonrefundable conservative reservation ceiling in this study's own ledger. The computed nominal Q0+S1 reservation is $61.73. Expected actual cost is about $10 (the Haiku cohort cost $3.13 at one third of Sonnet's per-token price). This counts against the owner's $500 shared allowance.

## Documents

[Design](design.yaml) · [preregistration](preregistration.md) · [setup record](SETUP.md) · [visualization mapping](VISUALIZATION.md) · [run instructions](RUN.md) · [deployment record](DEPLOYMENT.md) · [reviews](reviews/)
