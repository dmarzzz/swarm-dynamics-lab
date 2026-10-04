# Identity splitting at fixed attacker resources, replicated on two other models

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-split-qwen; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — On the byte-identical packets of sybil-split-opus, splitting one attacker's fixed resources from 1 to 27 identities raises rare-skill wrong answers more under degree-based than under coverage-based checks for qwen/qwen3.7-flash (reasoning disabled) and gpt-6-sol (reasoning effort low, and none as the one pre-registered follow-up), each reported separately. Basis: No evidence for the claim: none of the three configurations passed the parent's clean-packet qualification (gpt-6-sol effort low 3 of 6 shapes, effort none 3 of 6, Qwen 5 of 6), so no S1 contrast exists; the study is closed. Observed: all three abstain on some unanimous present facts (25, 28 and 3 of 320 fields), 0 wrong values. Builder's own assessment; not independently reviewed.
- **sample_size_summary:** Observed: qualification only, per configuration 60 clean packets on 10 roots (5 ring, 5 community) plus a 1-call probe; all 180 Q0 answers structurally valid; shapes passed 3, 3 and 5 of 6. S1 (planned 48 roots x 56 conditions = 2,688 calls per configuration) not run. Roots are the independent units, not calls.
<!-- experiment-evidence:end -->

**Status 2026-10-04: closed. Three configurations (gpt-6-sol at effort low and at effort none, Qwen3.7 Flash) each stopped at the Q0 gate; no S1 exists. See [RESULTS.md](RESULTS.md).** It is exploratory. The owner is dmarz, and dmarz/pipeline-split-qwen built it on 2026-10-04.

**Authority and review status.** dmarz did not name this study. On 2026-10-04 his instruction was to keep experiments running and to ship tonight; after the Anthropic organization reached its monthly usage threshold at 11:44Z he added: "we have no experiments running! fix that and or use opus 5 or an oai model". The fleet monitor (dmarz/fleet-monitor) chose this study under that instruction and set the two models. dmarz waived cross-researcher review for these exploratory runs. dmarz/fleet-monitor's check of this package is a same-researcher check and nothing more. **The run is not independently reviewed.** This is a hunch-level study in researcher notes, not an accepted hypothesis. It makes no novelty claim. S2 is disabled.

Parent: [sybil-split-opus](../sybil-split-opus/README.md). It finished on 2026-10-04 with 2,749 of 2,749 calls valid and a cost of USD 45.39. According to its hub run summaries and [post-run review](../sybil-split-opus/reviews/chain-001-post.md), its primary contrast was **+0.410** (descriptive 95% interval +0.278 to +0.549; ring +0.500, community +0.319). That result was for `claude-opus-5-5` at effort low.

## TLDR

The parent study gave one attacker a fixed budget of 27 report rows, 27 attachment edges and 27 verification attempts. The attacker held that budget with 1, 3, 9 or 27 identities. The parent found that splitting from 1 to 27 identities raised Opus 5.5's rare-skill wrong answers much more when checks were placed by `degree` than when they were placed by `coverage`. This study asks whether two other models show the same contrast when they read **the identical packets**:

- `qwen/qwen3.7-flash` through OpenRouter (Alibaba only, reasoning disabled);
- `gpt-6-sol` through the OpenAI API (reasoning effort low).

The simulator, graph families, attacker overlay, policies, check budgets, packet construction, roots, qualification packets, thresholds and primary contrast are the parent's. The scripted stage proves that every packet is byte-identical to the parent's. Each model runs its own complete chain: S0 with 0 calls, P0 with 1, Q0 with 60 and S1 with 2,688, for 2,749 calls per model. Each chain has its own batches, ledger, dollar cap and results. The two models are never pooled.

## Question and prediction

Question: does a cheaper model, with reasoning disabled or at low effort, show the parent's identity-splitting contrast on the same packets?

Primary (one per model, exploratory; the parent's primary unchanged): attacker pass rate 0.1 and 12 checks. For each root, compute (rare-skill wrong-answer rate at k = 27 minus k = 1 under `degree`) minus (the same difference under `coverage`). Take the mean over the 24 roots of each family, then the mean of the two family means. The useful size is 10 percentage points. No direction is predicted for either model, beyond noting that the parent found +0.41 on Opus 5.5 and +0.41 under the scripted plurality rule on the engineering roots.

What the comparison can and cannot show:

- **Same packets, different reader.** The model and its configuration both differ from the parent: no reasoning for Qwen, low reasoning effort for GPT-6 Sol, against Opus 5.5 at effort low. A difference therefore belongs to the model-plus-configuration and cannot be attributed to either part alone.
- **The parent's stated limit carries over.** A change in k changes both the partition of the fixed resources and the attacker's internal links (0, 3, 18 and 54 links at k = 1, 3, 9, 27).
- **Qualification is part of the result.** A Q0 stop on either model is that model's result. Thresholds are not changed and nothing is retuned.

## Setup

Everything about the world and the packets is the parent's. The parent's Setup section gives the full description: 108 honest simulated identities in two graph families, an attacker that partitions 27 fixed resource units into k identities, and `coverage`, `degree` and `random` admission checks at 4 or 12 checks plus a no-check baseline. Each check pass rate is either 0.1 (informative) or 0.9 (unreliable).

- **Byte identity, proven before any call.** `src/sim.py` is the parent's file byte for byte. The parent's `src/sim.py`, `src/study.py`, `design.yaml` and `records/s1-episodes.jsonl.gz` are pinned by SHA-256 in [design.yaml](design.yaml). S0 runs the parent's own code, unmodified, in its own process and directory. It requires the parent's code to give the same assignment ids and the same packet hashes as this study's code for all four stages (S0 1,853, P0 1, Q0 60, S1 2,688). It also requires the parent's recorded S1 run to hold exactly these 2,688 packet hashes. The user message is the parent's (`json.dumps(packet, sort_keys=True)`), so its SHA-256 is the recorded packet hash.
- **System prompt.** The prompt is the parent's text byte for byte (S0 checks it against the parent's `src/provider.py`), followed by one paragraph giving the answer shape: `{"values":{"0":<integer or null>, ... "5":<integer or null>}}`. The parent's route enforced that shape with a JSON schema in the request. Both routes here have JSON-object mode only, so the shape is stated in words and checked locally. This paragraph is the only change to what the model reads.
- **Answer validation.** The parent's schema is enforced locally. Before pinning, the validator was checked against harmless variants of a correct answer:
  - accepted, as the parent's JSON schema accepts them: any key order, surrounding whitespace, and an integral number written with a fraction (12.0);
  - rejected, as the parent's schema rejects them: a string such as "12", a missing or extra key, a boolean, a non-integral number, a code fence.
  
  The selftests drive each of these through the real adapter with a stubbed endpoint. The rehearsal runs a whole chain whose stub answers only with such variants.
- **Models (pre-registered set of two).**
  - `qwen/qwen3.7-flash`: request body exactly the program v5 template (`provider {only: [alibaba], allow_fallbacks: false, require_parameters: true}`, `reasoning {enabled: false}`, `max_tokens` 1,000, `response_format {type: json_object}`) plus the two messages.
  - `gpt-6-sol`: OpenAI Chat Completions, request body exactly `model`, `reasoning_effort` low, `max_completion_tokens` 2,000 (visible plus reasoning tokens) and `response_format {type: json_object}`, plus the two messages. It uses the reference OpenAI adapter (`src/openai_provider.py`, copied unchanged from main 8290d7ad). Cost is computed from that adapter's pinned price row (USD 2.00 input, 0.20 cached input, 2.50 cache write, 10.00 output per million tokens, retrieved 2026-10-04 12:10Z), because the API reports no cost.
  
  The model of a chain comes from `STUDY_MODEL` (launcher `--model`). Batches carry the model tag (`s0-001-qwen` ... `s1-001-sol`) and every row records its model.
- **Each model is launched separately.** The launcher passes the model with `--model` (`STUDY_MODEL`) and gives each model its own ledger and results directory. Each gate looks only at runs of its own model. The two chains may run at the same time on different servers. Because the hub hands out the next planned run of an experiment, a stage is not queued while a planned run of either model is waiting.

## Protocol

Per model, one chain on one server. A stage is queued only when exactly one run of the previous stage, for the same model and at the same source hash, is `done` with no invalid row and with its gate passed.

| Stage | Batch (Qwen; Sol uses `-sol`) | Calls | What it does | Passes when |
|---|---|---|---|---|
| S0 | `s0-001-qwen` | 0 | Parent's scripted stage (1,853 rows: plurality rule on 32 engineering roots, 60 qualification fixtures, probe fixture), parent's invariants, plus byte identity with the parent's code and records | every row valid, no invariant violated, scripted qualification passes, grid not degenerate, packets identical to the parent's |
| P0 | `p0-001-qwen` | 1 | The parent's probe: the `multirow1` fixture of engineering root 4919. Raw response metadata recorded | parsed, model id matches, usage reported, finish `stop`, answer equals the expected values; Qwen also: provider named and Alibaba, no reasoning tokens; Sol: output plus reasoning tokens within 2,000 |
| Q0 | `q0-001-qwen` | 60 | The parent's 60 clean fixtures and thresholds, unchanged | per shape over its 10 packets: all valid, field accuracy ≥ 0.95, exact packets ≥ 0.90, 100% null on withheld facts |
| S1 | `s1-001-qwen` | 2,688 | 24 roots × 2 families × 2 check strengths × 4 identity counts × 7 policy cells | no gate of its own; failed calls within the limit |

Before Q0 and before S1, each chain stops with `input_ceiling_projection` if the measured input tokens per message byte times the stage's largest request exceeds 31,000 tokens. The largest request is 13,515 bytes; at Qwen's measured rate on comparable JSON, about 0.5 tokens per byte, that is about 7,000 tokens. Before S1 the chain also stops with `projection_exceeds_cap` if 2,688 times Q0's measured cost per call does not fit in the remaining cap.

Failure handling, as in trust-credit-qwen and the reference adapter:

- Every failed request keeps its HTTP status, response body (2,000 characters) and request id.
- A request the provider rejected before the model ran is re-sent at most twice (2 s, then 6 s, `retry-after` up to 20 s), inside one 120 s request budget. On OpenRouter that means HTTP 429/502/503/529; on OpenAI it means 429 (rate limit)/500/502/503/504. No answer is ever retried.
- A credit, balance or quota refusal pauses the stage. On OpenAI that includes a 429 `insufficient_quota`. The same call is re-sent every 60 s for up to 20 minutes, and then the stage stops with `provider_credit_balance_low` (OpenRouter) or `provider_billing_stopped` (OpenAI). The pre-registered `chain.py resume` then runs exactly the units not started, at the same source hash, as `s1-001-<tag>-r1`.
- S1 continues past failed calls until more than 27 have failed (the larger of 3 and 1% of 2,688).
- Integrity failures stop dispatch at once: a ledger refusal, a model or provider mismatch, a breached reservation, or a deadline.
- S0, P0 and Q0 are strict.
- Missing outcomes stay in their denominators, bounded at 0 and 1.

Caps per model: P0 1, Q0 60, S1 2,688, study 2,749 calls, 3,300 transport attempts.

| Model | Dollar cap | Expected cost | Basis |
|---|---|---|---|
| Qwen | USD 3 (settled cost plus open reservations) | about USD 0.35 | about 10.4 M input tokens at USD 0.03 per million, plus output at USD 0.13 per million |
| GPT-6 Sol | USD 90 | about USD 25 to 50 | 2,749 calls × about 3,700 to 6,500 input tokens = 10 to 18 M tokens; USD 20 to 45 at the cache-write bound of USD 2.50 per million, plus output at USD 10 per million |

Four requests are in flight. There are 3 hours per stage and 4 hours per chain.

## Metrics

Everything the parent reported, on each model's answers, from the parent's analysis code:

- the primary contrast and its percentile interval (10,000 root draws within family, seed 20261004);
- the primary under unreliable checks and at 4 checks;
- `random` against the other policies;
- raw multiplicity effects;
- model minus same-packet plurality;
- cell tables with rare-skill correct, wrong and abstained answers, attacker seat and row share, specialist retention, checks, tokens and dollars;
- bounds for missing outcomes.

Secondary and descriptive only, new here:

- `versus_parent`: this model minus the parent's Opus 5.5 answers on the same assignments, paired by root, per cell and for the primary contrast, with the share of identical answers. It is never pooled.
- `test_retest`: agreement of this model's answers within the groups of byte-identical packets in a root. The parent's S1 has 1,901 distinct packets among its 2,688 assignments.

## Limits

All of the parent's limits apply:

- no published Sybil defense is included as a comparator;
- one population size, one fabrication type and one attachment rule;
- the verification-attempt budget never binds;
- attacker-internal links are free and vary with k;
- 24 roots per family is a development-sized sample.

Further limits of this study:

- The model and its configuration change together.
- The system prompt gains one paragraph stating the answer shape.
- The parent's model saw a JSON schema; these models do not.
- OpenRouter and OpenAI prices and model behaviour are snapshots.

## Results

See [RESULTS.md](RESULTS.md): none of the three configurations passed the parent's clean-packet qualification on byte-identical packets; no S1 comparison exists.
