# Pre-run assessment: chain 003 (gpt-6-luna, the second pre-registered model: S0, P0, Q0, S1)

Follows [the review cycle](../../../../../tooling/agent-experiments/RUN-REVIEW.md). This is the owning builder's assessment. It is not an independent review and not permission to bypass a runtime gate.

- Study / owner / stages: verify-cost-qwen / dmarz / one chain of four stages on `gpt-6-luna` (provider OpenAI). Batches `s0-002-gpt-6-luna`, `p0-002-gpt-6-luna`, `q0-002-gpt-6-luna`, `s1-002-gpt-6-luna`; none exists on the hub. READY.yaml names `provider: openai`, `model: gpt-6-luna` alone, so the launcher sets `STUDY_MODEL=gpt-6-luna` and sends only the OpenAI credential. Written 2026-10-04 by the builder, dmarz/pipeline-verify. Operator: dmarz/fleet-monitor.
- Earlier attempts and their post-mortems (both read before this was built or pinned):
  - Attempt 001, Qwen, answer `{"inspect": "<cell>"}`, set a: stopped at the qualification gate, prose 10 of 12 and table 8 of 12 optimal, 24 of 24 valid ([post-mortem](chain-001-post.md)).
  - Attempt 002, Qwen, repaired answer (two written costs, then the choice), set b: stopped at the qualification gate, prose 6 of 12 and table 4 of 12 optimal, 24 of 24 valid ([post-mortem](chain-002-post.md), [pre-run review](chain-002-pre.md)). As pre-registered, that failed repeat ended the Qwen route of this line.
- **The Qwen chain of attempt 002 was pinned at the earlier commit (code `35404c24`, source hash `ef40246d…`) and is not changed by this.** It has run. In the code reviewed here the Qwen configuration is identical to it (a selftest compares the Qwen manifest digest with attempt 002's, `a1543730…`), and its batch names `s0-002`, `p0-002` and `q0-002` exist on the hub, so the coordinator refuses to run it again.
- Status: **ready for dmarz/fleet-monitor's same-researcher check**. Still required before a call: that check, the run-queue request, and the launcher's `setup` passing on the server at the launch commit. The builder launches nothing.
- Authority and review status (as relayed to this builder by dmarz/pipeline): dmarz directed research program v5 himself; this package implements its line V. dmarz asked at 12:00Z on 2026-10-04 for experiments on an OpenAI model while the Anthropic account is at its monthly limit, and dmarz/fleet-monitor requires `gpt-6-luna` as a second pre-registered model for this study and decided at 12:38Z that its chain qualifies on set a. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check and nothing more; the run is not independently reviewed. This assessment is written by the agent that built the package.
- **Code commit (the pin of the code): `c74da5bc1f07c7bd765a7a066e4c8de86e1f2553`. Source hash: `b1b15d2573d295ee5560bdfbd3b2661b90c5a6cd435dd3a694ec3a9695dd5d48`** (`study.source_hash()` over `design.yaml`, `experiment.yaml`, `requirements.txt` and the thirteen `src/*.py` files; the same value is in [READY.yaml](../READY.yaml), which names this file as `review:`). The source hash does not depend on the model.
- **Launch commit:** the commit named in the run request: the first commit on main that contains this review and READY.yaml with this source hash.
- **Ledger:** READY.yaml declares `ledger: fresh`. The chain starts with a fresh ledger and a fresh results directory on a fresh server (READY.yaml is in the single-model form, so the launcher uses the untagged ledger and results paths; the batch names still carry the model tag). The hub holds the paid runs of attempts 001 and 002; none of them is on this model, and their calls do not belong in this chain's ledger, whose study cap of 600 assumes it starts empty.
- **Manifest:** [manifest.json](../manifest.json), section `ladder.gpt-6-luna`, digest `27d522674ab3cb4d0325f0ca6535f5ec16863157a91dc658ea5adc998089dd78`. That is exactly the digest of attempt 001's manifest: every request of this chain (144 scripted, 1 probe, 23 qualification, 576 main) has the same id and the same request hash as in attempt 001.

## Said up front, before any run on gpt-6-luna (preregistration, "Second pre-registered model" and its dated amendment)

1. `gpt-6-luna` gets the ORIGINAL instrument of attempt 001: system message, user message and answer `{"inspect": "<cell>"}`, byte for byte. It asks whether a more capable model passes the unrepaired instrument that Qwen failed.
2. It qualifies on set a, the 24 requests Qwen answered in attempt 001, so the two models are compared on identical requests. This was decided by dmarz/fleet-monitor after Qwen's attempt-002 result on set b was known (10 of 24 optimal under a different answer schema). That result played no part in the choice of fixtures for a different model and schema; `gpt-6-luna` has seen neither set, and no call to it has been made.
3. The chains differ in model, provider and reasoning setting at once (`reasoning_effort: low` here; reasoning disabled for Qwen). They are different actor configurations, compared descriptively and never pooled. Attempt 001, attempt 002 and chain 003 are three separate records.
4. Same gates and thresholds: 24 of 24 valid and at least 11 of 12 optimal in each representation, over P0's row and Q0's 23. A failed qualification ends this chain; there is no repair attempt for it. If it passes, S1 measures the table-versus-prose contrast for this model, which may be at ceiling; a contrast near zero is then the result.

## Question, design and precision

Unchanged from [chain-001-pre.md](chain-001-pre.md): 24 layouts (3000 to 3023) × 12 cases × 2 representations = 576 S1 calls; primary: per-layout mean table-minus-prose expected regret, 24 paired values, predicted negative, practical marker 0.03, bound ±0.3208; all twelve strata and the reliable-source regression flag reported; offline comparators always-check 0.1500 and always-explore 0.1708; units are layouts, not calls; missing units bounded in [0, |e − U|] and never dropped. Both representations hold the same facts (proved for every request, as before). The run is uninformative about the contrast if qualification fails (then that is the result for this model) or if both representations sit at regret 0 (reported as a ceiling).

Qualification: set a, 12 clear-dominance fixtures (margin at least 0.60, both actions legal) × 2 representations; every constant policy scores 6 of 12 and fails. Reference points on these same 24 requests: Qwen in attempt 001 scored 10 of 12 (prose) and 8 of 12 (table).

## What is new in this code, and what is not

| Item | Qwen chain (as attempt 002, already run) | gpt-6-luna chain (chain 003) |
|---|---|---|
| Model and provider | `qwen/qwen3.7-flash`, OpenRouter, Alibaba pinned | `gpt-6-luna`, OpenAI Chat Completions |
| Request body | `model`, `provider`, `reasoning {enabled: false}`, `max_tokens: 1000`, `response_format`, `messages` | `model`, `reasoning_effort: low`, `max_completion_tokens: 1500`, `response_format {type: json_object}`, `messages`; nothing else |
| Adapter | reference OpenRouter adapter, main `639e9501`, unchanged | reference OpenAI adapter, main `8290d7ad`, unchanged (SHA-256 `f48e8aa8…`, asserted by a selftest), with its 28 tests run by this selftest |
| Answer schema | two written costs, then `inspect` | `{"inspect": "<cell>"}` only, as in attempt 001 |
| Qualification set | b | a |
| Batches | `s0-002` … `s1-002` | `s0-002-gpt-6-luna` … `s1-002-gpt-6-luna` |
| Dollar cap, prices | USD 2; 0.03 / 0.13 per million | USD 5; 0.10 input, 0.01 cached input, 0.125 cache write, 0.50 output per million; cost computed from usage |
| Calls | 1 / 23 / 576, study cap 600 | 1 / 23 / 576, study cap 600, own ledger file |
| Transport re-sends | 429, 502, 503, 529 | 429 (rate limit), 500, 502, 503, 504 |
| Billing stop category | `provider_credit_balance_low` | `provider_billing_stopped` (HTTP 402, or 400/403/429 naming quota, billing, credit, balance or a usage, spend or hard limit); `chain.py resume` accepts each category for its own provider's chain |
| Scripted S0 | its own | its own, in its own answer schema (not shared; see deviations) |

Model selection: `STUDY_MODEL` (launcher `--model`), default the first entry of the frozen ladder `[qwen/qwen3.7-flash, gpt-6-luna]`, refused if not in the ladder; `STUDY_PROVIDER`, when set, must agree with the design. Hub runs carry `model`; the coordinator admits a stage only on a passed run of the previous stage with the same model and source hash, so a qualification on one model never admits the other.

## Validation for the original schema, decided in advance

Valid when the returned text parses as one JSON object and `inspect` is a string naming one of the two allowed cells after trimming whitespace and removing spaces around the comma. Tolerated and recorded: extra keys (including an unrequested cost object), an `inspect` that needed trimming, pretty-printed JSON. Invalid: text that is not JSON, JSON followed by text, JSON in a code fence, an array or a string, a missing `inspect`, `inspect` naming another cell, an action word, a non-string or null, a repeated key, output cut off at the limit (`truncated_output`: reasoning tokens count against the 1,500), more than 4,000 characters. This is more tolerant than attempt 001's validator (exactly one key, exact string); the request text is the same. A selftest sends all 5 tolerated forms and all 11 invalid forms through the OpenAI adapter and the validator.

## Frozen execution

- Gates and what happens at each failed gate:

| Stage | Assignments | Gate | On failure |
|---|---|---|---|
| S0 | 144 scripted rows in the original schema | every row valid; analytic policy passes both sets; 0 invariant violations | chain stops; nothing paid |
| P0 | 1 (`qa-2800-e90-u05-prose`, the probe request of attempt 001) | response parses; response model is `gpt-6-luna` or its dated form; usage reported; finish reason `stop`; output within 1,500 tokens; valid answer | chain stops after one call; its summary keeps the raw response metadata (model, id, system fingerprint, reasoning and visible output tokens, latency, rate-limit numbers) |
| Q0 | 23 (the rest of set a) | 24 of 24 valid and ≥ 11 of 12 optimal per representation, over P0's row and Q0's rows | chain stops with `gate_failed`; S1 never queued; this chain ends |
| before S1 | — | 576 × Q0's mean cost per call ≤ remaining cap; P0's tokens per content byte × 1,891 bytes ≤ 8,000 tokens | `projection_exceeds_cap` or `input_ceiling_projection`; no S1 call |
| S1 | 576 | ends `done` with at most 6 failed calls and no stop | `failed_units_over_limit`, `integrity_failure`, or `provider_billing_stopped` (resumable as `s1-002-gpt-6-luna-r1`) |

- Failure handling: part 1 adopted (status, body, request id kept; never a header or the key); part 2 not applicable (no token-counting request; the reservation is a byte bound); part 3 adopted, `max_failed` 6; part 4 adopted, 60 s re-sends for up to 1,200 s, then `provider_billing_stopped`, `chain.py resume`, voided reservations, standing S1 reservations never above 576.
- Hard caps: calls 1 / 23 / 576, `max_attempted_calls` 600, 760 transport attempts, USD 5 of settled cost plus open reservations, 4 requests in flight, request 120 s, stage 5,400 s, chain 7,200 s.
- Input: the largest request body is 2,129 bytes (1,891 bytes of content); attempt 001 measured 663 input tokens for the probe on Qwen's tokenizer; the 8,000-token ceiling is far away and the chain checks it with P0's measured ratio. Prompts are under 1,024 tokens, below the provider's caching minimum, so input is priced at the plain input price.
- Cost at the pinned prices: about 650 to 700 input tokens × 0.10 = 65 to 70 millionths of a dollar, plus output: about 8 visible tokens and an unknown number of reasoning tokens at `low` (say 50 to 400) × 0.50 = 30 to 200 millionths: about 100 to 270 millionths per call; 600 calls: **about USD 0.06 to 0.16**. Worst realistic, every call using its whole 1,500-token allowance: 600 × (70 + 750) millionths = USD 0.49. Reservation per call: 10 × (2,129 bytes × 0.125 + 1,500 × 0.50) = 10,161 millionths = USD 0.0102; four open at once USD 0.041. All far inside USD 5. Dollars are not the gate; the call caps are, and actual calls, tokens and dollars are reported to the hub.
- Wall time: unknown for this model; at 1 to 5 s per call S1 takes 576 ÷ 4 × 1 to 5 s = about 2.5 to 12 minutes and the chain about 3 to 14 minutes. The timeouts leave room for one full billing outage.
- Risk specific to this model: reasoning tokens count against `max_completion_tokens`. If reasoning used the whole 1,500 the call would end `truncated_output`; in P0 or Q0 that fails the gate (valid structure throughout). At `reasoning_effort: low` and a one-key answer this is unlikely; P0's summary shows the reasoning tokens of the first call.
- Stop rules: no answer retries, no replacement runs, no change of sample, thresholds or cases; no repair attempt for this chain; S2 disabled; task ids below 10000.
- Credential: alias `SWARM_OPENAI_API_KEY` only (the launcher sends only the chosen model's provider credential). No secret, server address or hub address is in the repository.

## Offline evidence (builder's own runs, 2026-10-04, local Python 3.9.6, no network beyond 127.0.0.1, no model call), at code commit `c74da5bc`

- `python3 src/selftest.py`: `Ran 123 tests`, `OK` (63 of this study, 32 of the OpenRouter reference adapter, 28 of the OpenAI reference adapter). The count does not depend on `STUDY_MODEL`: the selftest clears it at import and tests each model explicitly.
- Proofs in the selftest that matter for this chain: the `gpt-6-luna` system message, its 144 scripted, 1 probe, 23 qualification and 576 main requests have the hashes of attempt 001's committed manifest (stage digests and the manifest digest `27d52267…`); the Qwen manifest digest equals attempt 002's; model selection, batches, backends and budgets per model; the OpenAI configuration passes the adapter's own `check_config` (allowed effort, pinned prices, the word JSON in the prompt); gates do not cross models; a run queued for the other model or a provider that differs from the design is refused before any call; both chains on one in-memory hub with a billing stop each (`provider_credit_balance_low` and `provider_billing_stopped`), each resumed by `chain.py resume` from its own status and ledger, and a stop reason of the other provider refused.
- `STUDY_MODEL=gpt-6-luna python3 src/worker.py --stage S0 --attempt <name>`: planned 144, graded 144, invalid 0, model_calls 0, qualification_passed 1, invariant_violations []. The same for the default model.
- `python3 src/manifest.py --check`: current.
- `python3 src/rehearse.py --hub-dir <local hub copy>`: `ok true`, 41 of 41 checks, about 95 s, eight chains (run again after this review was written, same result). Six are the attempt-002 scenarios on the first model. The seventh and eighth run the two models one after the other on the same throwaway hub: the Qwen chain on an OpenRouter-shaped stub, then the `gpt-6-luna` chain on an OpenAI-shaped stub (no provider field, no cost, reasoning tokens inside `completion_tokens`, `system_fingerprint`) that cycles through the tolerated answer variants: eight runs on the hub with model-tagged batches, calls 0 / 1 / 23 / 576, 600 of 600 valid, its own ledger with cap USD 5, `chain verify` exit 0 for each.
- Not tested locally: Python 3.12 (no PyYAML or Pillow for it here; the launcher's `setup` runs the selftest on the server).
- Not verified against the live service by anyone in this lane: the OpenAI response for this model (the adapter's README lists what was checked against the documentation). P0 is the first look, at the cost of one call.

## Deviations and unresolved issues

| Issue | Choice | Reason | Blocks |
|---|---|---|---|
| The contract says one scripted S0 serves every model of a ladder | each model's chain has its own S0 (`s0-002-gpt-6-luna`) | S0 answers the fixtures in the chain's own answer schema, and the Qwen S0 on the hub is at another source hash, so it could not gate this chain | launch all four stages (the default) |
| The hub hands out queued runs per experiment | the two chains must not run at the same time against the same hub experiment | the Qwen chain cannot run again anyway (its batches exist) | none now |
| The hashed design keeps the ladder `[qwen/qwen3.7-flash, gpt-6-luna]` while READY.yaml names `gpt-6-luna` alone | READY.yaml: `provider: openai`, `model: gpt-6-luna`, `usd_cap: 5` (the form that ran two OpenAI chains through this launcher today, as dmarz/fleet-monitor reports); the ledger enforces the model's own cap from the hashed design | the Qwen route is closed, so the launcher only ever starts this chain | the chain depends on the launcher setting `STUDY_MODEL=gpt-6-luna`; if it were unset the code would select Qwen, whose batches exist, and the coordinator would refuse at S0 with `batch_exists_no_replay` before any call |
| Fenced or trailing-text JSON stays invalid | none | the reference adapter parses the whole text and is used unchanged | P0 would show it at the cost of one call |
| After a billing pause longer than the request timeout the owner call has no transport-retry budget left (both adapters) | none; reported earlier | tolerated in S1, fatal only in P0 or Q0 | reported |

## Visualization and closeout

- Mapping: [VISUALIZATION.md](../VISUALIZATION.md), v1; the frame's second line names the model and the answer schema. No written-cost line for this chain (the schema has no working field).
- Closeout: `status`, then `verify`; post-mortem per RUN-REVIEW.md with P0's raw metadata, the qualification table on set a next to Qwen's attempt-001 answers to the same 24 requests (descriptive, not pooled), and, if S1 runs, the per-stratum table, the primary with bounds and the regression flags.
- Admission decision: none by the builder. Assessor: dmarz/pipeline-verify, 2026-10-04.
