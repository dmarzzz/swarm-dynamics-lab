# Knowledgeable newcomers versus a trusted Sybil coalition: Opus 5.5 configuration

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/newcomer-opus; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — In this synthetic newcomer task, an Opus 5.5 synthesizer (effort low) on assignments identical to the Haiku 4.5 and Sonnet 4.6 cohorts did not materially change outcomes: the policy ranking (random > renewal > reputation) was unchanged, renewal minus reputation stayed inconclusive (+9.7 pp, interval -1.4 to +20.8 pp), and the difference from Haiku in that contrast was +1.4 pp (interval -4.2 to +6.9 pp). Accuracy never exceeded the share of truth present in admitted packets. Basis: Same-owner assessment: twenty-four paired roots, passed probe and qualification, 1,944/1,944 outcomes paired by assignment with both earlier cohorts and fully recomputed from frozen runtime. The Opus request configuration differs from the earlier cohorts (no temperature, adaptive thinking at effort low); one task family, scripted actors and descriptive unadjusted intervals limit stronger conclusions. Independent review was waived by the owner.
- **sample_size_summary:** Observed: 24 paired roots from one synthetic task family; 1,944/1,944 S1 outcomes analyzed, zero missing, each paired by assignment ID with the separate Haiku and Sonnet cohorts (not pooled); 24 honest + 1/4/16 controller identities, one synthesizer model. Q0 separately: 36/36 clean calls plus one probe call.
<!-- experiment-evidence:end -->

Third model cohort of [sybil-newcomer-api](../sybil-newcomer-api/README.md), after the [Sonnet 4.6 replication](../sybil-newcomer-sonnet/README.md). Same worlds, packets, prompt, schema, evaluator and analysis; the synthesizer is `claude-opus-5-5`. Opus 5.5 does not accept a temperature setting and cannot run with thinking disabled, so this is a new model configuration rather than a model-only swap (see Setup). Exploratory S0/Q0/S1 study in `notes/`; not an accepted hypothesis, a completed survey or a formal S2 experiment, and not independently reviewed. See [SETUP.md](SETUP.md).

## TLDR

On Haiku 4.5 and Sonnet 4.6, none of three equal-cost audit policies kept specialist accuracy high after a coordinated sleeper attack (round 8, sixteen controller identities; Haiku random/renewal/reputation 26.4/20.8/12.5%, Sonnet 25.0/19.4/8.3%), and the correct rare fact was present in only about a quarter to a third of admitted packets. This cohort sends the identical 1,944 packets to Opus 5.5 at effort low. If Opus also stays near the available-truth level, the newcomer result is about admission, not synthesis strength. Limits: one synthetic task family, scripted actors, earlier cohorts' outcomes known when this was written, 24 worlds.

## Question and prediction

Does the newcomer result change with a stronger synthesizer? Primary contrast unchanged: renewal minus reputation specialist accuracy at sixteen controller identities, sleeper strategy, round eight, +10-point useful-effect marker. Prediction, written before any Opus call: the pattern replicates. All policies lose specialist accuracy under the sleeper attack, the primary contrast stays below +10 points, and per-policy accuracy at the primary cell stays within 10 points of the Sonnet cohort. Opus exceeding the Sonnet cohort by 10 or more points at the primary cell, or a primary contrast of +10 or more, would mean the earlier conclusion is model-dependent. Null and adverse outcomes are valid results.

## Setup

Python 3.12 with pinned [requirements](requirements.txt). Request: `claude-opus-5-5`, `output_config.effort = low`, native JSON-schema output in `output_config.format`, no `temperature`/`top_p`/`top_k` (rejected by this model), no `thinking` field (model default; it cannot be disabled), no tools, forced tool choice, prefill, caching or fallbacks. `max_tokens` 4,000 because thinking tokens count as output; the visible JSON answer is limited to 2,000 characters on the text block. Thinking blocks are dropped before parsing and never stored as answers. `refusal` and `max_tokens` stops are their own failure categories. Prices $4/$20 per million tokens. Compared with the earlier cohorts, the changes are therefore: model, no temperature-0 setting, model-default thinking at effort low, and the larger output cap. The simulator, worlds 7100–7123, qualification worlds 7000–7005, engineering worlds 6900–6901, policies, system prompt, schema, evaluator and analysis are unchanged; Q0 and S1 assignment IDs and packet hashes were checked equal to the Haiku study before launch. One dedicated fleet host under an exclusive claim; credentials reach the worker only as environment aliases from the private launcher.

## Protocol

As the [original protocol](../sybil-newcomer-api/preregistration.md); frozen copy in [preregistration.md](preregistration.md). S1: 24 worlds × 3 identity counts × 3 policies × 3 strategies × 3 sampled rounds = 1,944 calls. Stages run one at a time on the dedicated host: fleet S0 (198 scripted observations) → P0, a one-call interface probe on an engineering packet → Q0 (36 clean packets; per shape ≥95% field accuracy, ≥90% exact packets, 100% abstention on absent fields) → S1. Each stage is launched only after the previous software gate passed; the coordinator also refuses Q0 without an exact-runtime S0 and S1 without an exact-runtime Q0. Any invalid call stops new dispatch; no retries.

## Metrics

Primary: specialist accuracy (exactly correct current skills 3–5, divided by three), renewal minus reputation, paired by world, 10,000-resample whole-world bootstrap (seed 20261004). Secondary: every cell of the 81-cell matrix, renewal minus random, wrong specialist outputs, harmful and controller seat share, newcomer retention, the available-truth diagnostic, 16-minus-1 identity contrasts. Cross-model, descriptive: Opus minus Haiku and Opus minus Sonnet on identical packets per cell, and the difference between primary contrasts (paired-world bootstrap). The world is the independent unit; identities, rounds and calls are not. Each cohort is reported separately and never pooled.

## Budget

Hard caps in this study's own ledger: 2,050 attempted calls and a USD 400 nonrefundable conservative reservation ceiling (worst case per call about USD 0.18 at 20,000 input bytes and 4,000 output tokens). Expected actual cost is estimated after the probe and Q0 from measured tokens per call. The owner has said cost is not a gate for Opus work and asked for running totals; every run reports `cost_usd` to the hub.

## Documents

[Design](design.yaml) · [preregistration](preregistration.md) · [setup record](SETUP.md) · [visualization mapping](VISUALIZATION.md) · [run instructions](RUN.md) · [deployment record](DEPLOYMENT.md) · [reviews](reviews/)
