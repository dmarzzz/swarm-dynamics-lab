# Pre-registration: sybil-split-xmodel v1

Frozen on 2026-10-04 by dmarz/pipeline-split-qwen, before any stage of this study ran and before any model call. Exploratory; in researcher notes; not an accepted hypothesis; no novelty claim; S2 disabled. [design.yaml](design.yaml) is the machine-readable form. Items not restated here are the parent's [preregistration](../sybil-split-opus/preregistration.md) items 2 to 9 and 14 to 15, which apply unchanged. The parent's study ran at commit `75d51695`, source hash `95889bea…`.

Authority and review status. dmarz did not name this study. The fleet monitor (dmarz/fleet-monitor) chose it under two instructions from dmarz on 2026-10-04: to keep experiments running and ship tonight, and, after the Anthropic organization reached its monthly usage threshold, "we have no experiments running! fix that and or use opus 5 or an oai model". dmarz waived cross-researcher review for these exploratory runs. dmarz/fleet-monitor's check is a same-researcher check and nothing more. The run is not independently reviewed.

1. **Question.** Do two other models show the parent's identity-splitting contrast when they read byte-identical packets? The two models are pre-registered as a set: `qwen/qwen3.7-flash` (OpenRouter, Alibaba only, reasoning disabled) and `gpt-6-sol` (OpenAI, reasoning effort low). The parent's question and its stated limit carry over. In particular, k changes both the partition of the fixed resources and the attacker's internal links.

2. **Inputs identical to the parent's.** The following are the parent's: simulator (`src/sim.py`, byte-identical, SHA-256 pinned), graph families, attacker overlay, policies, check budgets, roots, packet construction, qualification fixtures, the probe fixture, assignment ids, user messages and the system prompt text. The S1 roots are ring 8233-8256 and community 8351-8374. No new root is drawn, so no seed scan is needed: every root is the parent's. S0 refuses unless all of the following hold:
   - the pinned parent files have their recorded SHA-256;
   - the parent's own code, run unmodified in its own process, gives the same id-to-packet-hash map as this study's code for S0, P0, Q0 and S1;
   - the parent's recorded S1 rows hold exactly the S1 packet hashes;
   - the system prompt begins with the parent's prompt byte for byte.

3. **The one change to what a model reads.** The system prompt is the parent's text, a blank line, and one paragraph stating the answer shape: "The specified JSON object has exactly this shape, with an integer or null for each skill:" followed by `{"values":{"0":<integer or null>, … ,"5":<integer or null>}}`. The parent's route sent that shape as a JSON schema. Both routes here use JSON-object mode, so it is stated in words. The paragraph mentions nothing about the manipulation, truth or ownership.

4. **Answer validation.** The parent's schema is enforced locally: exactly `{"values": {"0".."5": integer or null}}`.
   - An integral number written with a fraction (12.0) is accepted as the integer, as JSON Schema `integer` accepts it.
   - Key order and whitespace do not matter.
   - A string value, a boolean, a non-integral number, a missing or extra key at either level, a code fence, or duplicate keys make the call invalid.
   - There is no repair call and no answer retry.

5. **Model settings, frozen.**
   - **Qwen:** request body exactly the program v5 template (`model`, `provider {only: [alibaba], allow_fallbacks: false, require_parameters: true}`, `reasoning {enabled: false}`, `max_tokens: 1000`, `response_format {type: json_object}`) plus `messages`. The response must name the model (or its dated slug) and provider Alibaba, report usage, finish `stop` and report no reasoning tokens. Prices are USD 0.03 / 0.13 per million (program snapshot).
   - **GPT-6 Sol:** request body exactly `model: gpt-6-sol`, `reasoning_effort: low`, `max_completion_tokens: 2000`, `response_format {type: json_object}` plus `messages`, through the reference OpenAI adapter (main 8290d7ad). Cost is computed from its pinned price row: USD 2.00 input, 0.20 cached, 2.50 cache write, 10.00 output per million.
   - **Both:** 4 requests in flight, 120 s per request, input ceiling 31,000 tokens.

6. **Per-model chains, never pooled.** Each model runs its own chain: S0 (0 calls), P0 (1), Q0 (60), S1 (2,688), for 2,749 calls per model.
   - Batches are suffixed by the model tag (`s0-001-qwen` … `s1-001-sol`), and every row records its model.
   - Each model has its own ledger, dollar cap and results directory. The gates look only at the model's own runs.
   - Results of the two models are reported side by side and never pooled with each other or with the parent.

7. **Primary contrast, one per model.** This is the parent's primary, unchanged, on each model's answers. Use attacker pass 0.1 and 12 checks. For each root, compute (rare-skill wrong-answer fraction at k = 27 minus at k = 1 under `degree`) minus (the same under `coverage`). Take the mean over the 24 roots of each family, then the mean of the two family means. The interval is a 95% percentile interval from 10,000 bootstrap draws (seed 20261004), with roots resampled within family. The useful size is 10 percentage points. No direction is predicted.

8. **Secondary, descriptive, no multiplicity correction.**
   - (a) Everything in the parent's item 7, on each model.
   - (b) This model minus the parent's Opus 5.5 on the same assignments, paired by root, per cell and for the primary, with the share of identical answers. The parent's answers come from its recorded rows (`records/s1-episodes.jsonl.gz`, SHA-256 pinned).
   - (c) Agreement of each model's answers within byte-identical packet groups of a root (1,901 distinct packets among 2,688 S1 assignments).
   
   The model and its configuration both differ from the parent, so a difference in (b) is not attributed to either part alone.

9. **Gates, the parent's, unchanged.**
   - P0: the response passes the adapter's checks and the answer equals the expected values exactly.
   - Q0: per shape over its 10 packets, all structurally valid, field accuracy ≥ 0.95, exact packets ≥ 0.90, and 100% null on the 40 withheld fields.
   - A Q0 stop is that model's result. Thresholds are not changed, nothing is retuned and there is no repair attempt.
   - Before Q0 and before S1, a chain stops with `input_ceiling_projection` if the measured input tokens per message byte times the stage's largest request exceeds 31,000.
   - Before S1, a chain stops with `projection_exceeds_cap` if 2,688 times Q0's measured cost per call does not fit in the remaining cap.

10. **Failure handling** (ready-chain rule of 2026-10-04, as in trust-credit-qwen):
    - Every failed request keeps its HTTP status, response body (2,000 characters) and request id. A request is re-sent at most twice, only when the provider rejected it before the model ran: OpenRouter 429/502/503/529; OpenAI 429 rate limit and 500/502/503/504.
    - A credit, balance or quota refusal (including OpenAI's 429 `insufficient_quota`) pauses the stage. The same call is re-sent every 60 s for up to 20 minutes, and then the stage stops with `provider_credit_balance_low` or `provider_billing_stopped`. The unanswered reservations are voided.
    - Pre-registered resume, dated 2026-10-04: after such a stop, `chain.py resume` runs exactly the units not started, at the same source hash, as `s1-001-<tag>-r1`, under the same ledger and caps. The analysis counts every unit once.
    - S1 continues past failed calls until more than 27 have failed (the larger of 3 and 1% of 2,688).
    - Integrity failures stop dispatch at once: a ledger refusal, a model or provider mismatch, a breached reservation, a deadline or an internal error.
    - S0, P0 and Q0 are strict. Missing outcomes stay in their denominators with bounds 0 and 1. Nothing is imputed or re-run.

11. **Budget per model.**

    | | Qwen | GPT-6 Sol |
    |---|---|---|
    | Call caps | P0 1, Q0 60, S1 2,688, study 2,749 | same |
    | Transport attempts | 3,300 | same |
    | Dollar cap (settled cost plus open reservations) | USD 3 | USD 90 |
    | Expected | about USD 0.35 | about USD 25 to 50 |

    Each reservation is 10 times the byte-based upper bound (request bytes as input tokens plus the full output limit). The Qwen expectation rests on the parent's 10.4 M input tokens at USD 0.03 per million plus output. The GPT-6 Sol expectation is 10 to 18 M input tokens at USD 2.00 to 2.50 per million plus output at USD 10 per million. The fleet monitor set the GPT-6 Sol cap. Stages time out after 3 h and a chain after 4 h.

12. **Stop rules.** No answer retries. No replacement runs. No change to sample, thresholds, prompt or models after outcomes are seen. Null and adverse results complete the study. The holdout 10000-19999 stays closed.

## Amendment A1, 2026-10-04 (written before its code; no outcome of this configuration exists)

13. **A third, follow-up configuration: `gpt-6-sol` with `reasoning_effort: none`.** It was added **after** the effort-low gpt-6-sol chain stopped at its Q0 gate ([post-mortem](reviews/chain-001-sol-post.md)). The reasons:
    - that chain's misses were nulls on unanimous present facts, and they came with about three times the reasoning tokens of exactly-right packets (mean 164 against 53);
    - effort none also matches the Qwen chain's no-reasoning setting.

    It is a follow-up on the same instrument, not a retune. The packets, system prompt, answer validation, fixtures and every threshold are unchanged. Only `reasoning_effort` differs. The request body has exactly `model`, `reasoning_effort: none`, `max_completion_tokens: 2000`, `response_format {type: json_object}` and `messages`. With effort none the adapter would accept `temperature` and `top_p`; **none is sent**.

    It is model-ladder entry `gpt-6-sol-none` (the API model is still `gpt-6-sol`). It has its own batches (`s0-001-solnone` … `s1-001-solnone`), ledger, results and cap (USD 90). It runs P0 and Q0 first, and S1 only if Q0 passes, under the gates of item 9. It is reported separately and never pooled with the effort-low chain, the Qwen chain or the parent.

    The effort-low Q0 stop stays reported as a result whatever this configuration does. **A second stop ends the gpt-6-sol route**: no other effort level, prompt or configuration follows. Decided by dmarz/fleet-monitor on the builder's proposal; dmarz did not name it. Not independently reviewed.
