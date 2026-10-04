# Does Sybil-resistant accuracy depend on repeated knowledge? Cross-model replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/pipeline-scarcity-qwen; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **0/4** — On packets byte-identical to sybil-scarcity-opus, a synthesizer other than Opus 5.5 (qwen3.7-flash without reasoning; gpt-6-sol at reasoning effort low) also loses specialist accuracy when each rare fact has one truthful carrier instead of 81. Basis: Unrun. The package is prepared and tested offline only; no stage has run on a server and no model call has been made. Each model is a separate chain; results will never be pooled.
- **sample_size_summary:** Observed: none. Planned per model: 24 paired synthetic world roots x 60 conditions = 1,440 S1 calls on the parent's identical packets, after P0 (1 call) and Q0 (48 calls); roots are the independent units; calls, identities and skills are not.
<!-- experiment-evidence:end -->

**Nothing has run.** This directory is a launch-ready package for the first of two pre-registered models (`qwen/qwen3.7-flash`). No stage has been executed on a server and no model call has been made. Exploratory; owner dmarz; built by dmarz/pipeline-scarcity-qwen on 2026-10-04.

Review status and authority: dmarz did not name this study. As relayed to this builder by dmarz/fleet-monitor on 2026-10-04, dmarz told the fleet monitor to keep experiments running and to ship tonight; at 12:00Z he added "we have no experiments running! fix that and or use opus 5 or an oai model". The fleet monitor chose this study under that instruction (the Anthropic organization had reached its monthly usage threshold at 11:44Z, so only OpenRouter and OpenAI routes can run) and set the design below. Cross-researcher review is waived by dmarz for these exploratory runs. dmarz/fleet-monitor's check of this package is a same-researcher check and nothing more. The run is not independently reviewed. It is not an accepted hypothesis and makes no novelty claim.

## TLDR

[sybil-scarcity-opus](../sybil-scarcity-opus/RESULTS.md) cut the number of honest identities that report each rare fact from 81 to 1 while keeping a 972-identity world, its graph, audits, admission and attacker reports fixed. With one truthful carrier per rare fact, `claude-opus-5-5` answered 4.2% of rare facts correctly, against 100% at 81 carriers (primary −95.8 percentage points, 24 roots); it gave the attacker's repeated value 94% of the time. This study asks whether other models show the same dependence on repetition **on the identical packets**. Every one of the parent's 1,489 inputs (1 probe, 48 qualification packets, 1,440 comparison packets on roots 7800 to 7823) is rebuilt here byte for byte, and the scripted stage proves it. Two models are pre-registered, each as its own complete chain: `qwen/qwen3.7-flash` with reasoning disabled (a cheap model, this package) and `gpt-6-sol` with reasoning effort low (a strong model; its adapter is added in a later code commit before its own launch). Results are reported per model and compared with Opus root by root, cell by cell; they are never pooled. The 972 identities are simulated, not model agents; only the synthesis of each admitted packet is a model call.

## Question and prediction

On byte-identical packets, does a different synthesizer lose specialist accuracy as truthful carriers become scarce, as Opus 5.5 did?

Primary contrast, for each model: specialist accuracy (rare facts answered exactly right, divided by 3; null and wrong both count as incorrect) at **1** truthful carrier per rare fact minus the same at **81**, under random auditing, 108 checks and attacker check-pass probability 0.1, paired by world root over 24 roots. This is the parent's primary on a different model.

No numerical prediction is made. The parent's reading was that its synthesizer behaves close to a count of agreeing reports; same-packet plurality scored 3% in the primary cell at one carrier. A model that counts reports would show a contrast near the parent's; a model that weighs the verification badges or treats repetition as one source could show a smaller drop. A model that fails the clean qualification gives no comparison: a Q0 stop is the result for that model and is reported, never retuned.

## Setup

- **Inputs: the parent's, unchanged.** Worlds (N = 972: 486 core, 243 honest outside, 243 attacker identities), carrier manipulation (seed `scarcity-carriers`), random and coverage auditing at 4, 64 and 108 checks, two check strengths, admission of 486 reports, packet construction and order, the 60 cells per root, roots (S1 7800 to 7823, Q0 7900 to 7907, probe 7790), the dispatch order and the qualification thresholds are read from the parent's frozen `design.yaml` and rebuilt by functions copied from the parent's `study.py`; `src/sim.py` is the parent's file. The parent's `design.yaml`, `src/sim.py`, `src/study.py`, `manifest.json` and `records/s1-episodes.jsonl.gz` are pinned by SHA-256 in this study's `design.yaml`.
- **Byte-identity proof (S0, and before every stage).** (1) The copied `sim.py` equals the parent's pinned file. (2) For S0, P0 and Q0, every packet text, expected answer and evaluator label equals what the parent's own code builds for the same assignment. (3) For every stage, the list of assignment ids and packet SHA-256 hashes in dispatch order equals the parent's committed manifest (S1: 1,440 lines, 1,207 distinct packets). A difference blocks every call of that stage.
- **Request.** The user message is the parent's exactly (`json.dumps(packet, sort_keys=True)`, about 48,000 characters). The system message is the parent's prompt byte for byte, followed by one block that states the exact JSON shape of the answer (`{"values": {"0".."5": integer or null}}`). The parent carried that shape as a JSON schema in `output_config`; this route has JSON-object mode only, so the shape is stated in words and checked locally. The added block says nothing about how to weigh reports.
- **Model 1, `qwen/qwen3.7-flash`.** OpenRouter, provider pinned to Alibaba, no fallback, `require_parameters`, reasoning disabled, JSON-object mode, `max_tokens` 1,000: the program's frozen template in [selected-model.json](../overnight-program-2026-10-04/selected-model.json) plus `messages`. Adapter: the pipeline's [reference OpenRouter adapter](../pipeline/reference/openrouter_provider.py), copied unchanged.
- **Model 2, `gpt-6-sol`.** OpenAI Chat Completions, `reasoning_effort: low`, `max_completion_tokens` 2,000, JSON-object mode, 2 requests in flight, dollar cap USD 150 (set by dmarz/fleet-monitor). Not runnable at this commit: the reference OpenAI adapter and the price row are added in a later code commit, which changes the source hash and gets its own pre-run review. Until then the code refuses this model (`model_not_ready`).
- **Answer validation.** Exactly six skill keys "0" to "5", each an integer or null. Harmless variants of a correct answer are accepted and recorded per row (`normalized`): extra top-level keys besides `values`, a value written as an integral number (42.0) or as integer text ("42"). A boolean, a fraction, other text or a missing or extra skill fails. Text around the JSON object (for example a code fence) fails as `invalid_json` in the unchanged adapter. Selftests push each variant through the real adapter.
- **Differences from the parent, all stated:** the model and its configuration (no reasoning for Qwen; Opus thinks before answering at effort low); the request format above; P0 checks the interface and records whether its answer is exact instead of requiring it (competence is Q0's 48 packets at the parent's thresholds); S1 continues past failed calls up to 15 (the parent stopped at the first), with billing-outage pause and resume; no repair attempt.

## Protocol

[Pre-registration](preregistration.md), [design](design.yaml), [setup record](SETUP.md), [runbook](RUN.md), [pre-run review](reviews/chain-001-pre.md).

Each model runs as its own chain on its own server: batches `s0-001-<tag>`, `p0-001-<tag>`, `q0-001-<tag>`, `s1-001-<tag>` (tags `qwen`, `sol`), hub experiment `sybil-scarcity-xmodel-<tag>`, ledger file and results directory suffixed by the tag, own dollar cap. Every row carries its model.

| Stage | Calls | What it does | Passes when |
|---|---|---|---|
| S0 | 0 | the parent's 168 scripted outputs (2 engineering roots × 60 cells, 48 clean packets) answered by same-packet plurality; byte-identity proof | every row valid, every check above holds, the clean gate passes under plurality, the primary cell is not constant |
| P0 | 1 | the parent's probe packet (root 7790, 81 carriers) | response parses, model and provider match, usage reported, finish `stop`, no reasoning tokens, valid structure; tokens per byte recorded |
| Q0 | 48 | the parent's 48 clean packets | the parent's gate: 48 of 48 valid; per carrier profile (16 packets) field accuracy ≥ 0.95, exact packets ≥ 0.90, null on every withheld fact |
| S1 | 1,440 | 24 roots × 60 cells | at most 15 failed calls and no integrity failure |

Before Q0 and S1 the chain stops (`input_ceiling_projection`) if the largest measured tokens per byte times the stage's largest request (57,085 bytes in Q0, 57,169 in S1) exceeds 31,000 tokens, which keeps Qwen inside its under-32,000-prompt-token price tier; before S1 it stops (`projection_exceeds_cap`) if 1,440 × Q0's cost per call exceeds what is left under the cap.

## Metrics

Per model, for every one of the 60 cells with its 24-root denominator: specialist accuracy, and the rare answers split into correct, the attacker's fabricated value (truth + 7), null, and other wrong; six-fact accuracy; same-packet plurality; the parent's evaluator diagnostics (truth available after admission, carrier survival, attacker seat share). Primary as above with a 10,000-draw root bootstrap (seed 20261004) and bounds in which each missing outcome is 0 or 1; carrier contrasts 3, 9 and 27 against 81. Secondary, descriptive: per cell, this model minus Opus 5.5 on the same root and packet (the parent's answers regraded by this study's grader), with the parent's primary recomputed from its pinned rows (−95.8 pp). Counts of normalized answers.

## Limits

- One synthetic task, one graph family, one attacker strategy (one repeated fabrication), simulated identities and checks; the parent's limits apply unchanged.
- Model and configuration differ together from the parent (Qwen: no reasoning, a different request format; gpt-6-sol: reasoning effort low). A difference from Opus is a difference between two model configurations on the same inputs, not an effect of any one factor.
- Two models are not a population of models; no claim about models in general.
- The parent's rows were produced once; its outcomes are a fixed comparison set, not a concurrent arm.

## Results

None. No stage has run.
