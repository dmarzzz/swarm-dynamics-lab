# Pre-run assessment: chain-002 (S0, P0, Q0, S1 on gpt-6-sol)

Written 2026-10-04 evening by dmarz/pipeline-alarm-oai, before any run of this study. No stage has run and no model call has been made.

- **Code commit:** `73ff27519ab0b4546c41303b561fd55380164389` (the commit "[dmarz/pipeline-alarm-oai] false-alarm-cascade: gpt-6-sol rung").
- **Source hash:** `0947408b186386656be794d9dc9d65246461c88aa3c598bde063fe349296e4fd`.
- **Launch commit:** the commit named in the run request, the first commit on main that contains this review and has this source hash. No launch hash is written into any file.
- **Pre-registration:** [amendment A2](../preregistration.md), committed before the code commit.
- **What this review covers:** the change from the Opus package reviewed in [chain-001-pre.md](chain-001-pre.md) (code `af115c44`, source `7803e3b8…`) to a ladder whose first rung is `gpt-6-sol`. The instrument, worlds, conditions, scripted controls, evaluator, gates, call caps and analysis are unchanged; chain-001's design assessment, scripted-policy table and frozen execution plan (stage digests) still hold and are not repeated here. The manifest digest is unchanged (`6f126bb5…`).

## Authority and review status

dmarz did not name this study. He told the fleet monitor to keep five experiments running and, when Opus ran out, "use another odel like opus 5, and if that runs out use open router or whatever u need to keep shi[[ing thesewhile im asleep" and later "use opus 5 or an oai model". The fleet monitor (dmarz/fleet-monitor) chose this study from his backlog (honeypot-vigilance hunch V4) under that delegation. Cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check, and the run is not independently reviewed. This builder launches nothing.

## Why the model changes

The Anthropic API organisation is at its monthly limit. Error recorded at 11:44 UTC: "You have reached your API usage limits: your organization has crossed its monthly API usage threshold ... You will regain access on 2026-11-01 at 00:00 UTC". No rung of the A1 ladder can run before then.

## In one line each

- **Model ladder:** `[gpt-6-sol, claude-opus-5-5, claude-opus-5]`, providers `{gpt-6-sol: openai, claude-opus-5-5: anthropic, claude-opus-5: anthropic}`; default (no `--model`) gpt-6-sol; one model per attempt; batches `p0-001-gpt-6-sol`, `q0-001-gpt-6-sol`, `s1-001-gpt-6-sol`; Opus batch names unchanged; nothing pooled across models.
- **Failure handling, part 1 (evidence):** every failed request keeps HTTP status, the first 2,000 characters of the body and the request id (`x-request-id` on OpenAI); never the key or a request header.
- **Failure handling, part 2 (token count):** there is no count request on OpenAI; the reservation is the request's byte length at the higher input price (USD 2.50) plus the full 16,000-token output allowance at USD 10.00, times 10 (reference adapter), so no call can fail on counting.
- **Failure handling, part 3 (which failures stop):** P0 and Q0 strict; in S1 a failed call ends its episode and dispatch continues; integrity failures (ledger refusals, `reservation_bound_breached`, `model_mismatch`, `output_ceiling_exceeded`, deadline, missing credential) stop at once.
- **Failure handling, part 4 (billing):** HTTP 402, or 400/403/429 naming quota, billing, credit, balance, insufficient, a usage, spend or hard limit, pauses every call; the same call is re-sent every 60 s for up to 1,200 s; then the stage stops as `provider_billing_stopped`, which the study treats exactly as `provider_credit_balance_low` (rows not started, no failed unit, `chain.py resume` for S1 only).
- **`max_failed`:** 3 failed S1 episodes (the larger of 3 and 1% of 120), unchanged.
- **Billing schedule:** 60 s between re-sends, 1,200 s at most, unchanged.
- **Load:** at most 10 requests in flight (2 episodes × 5 agents; 5 in Q0), unchanged.
- **Cap:** USD 120 on the gpt-6-sol ledger; expected about USD 57.
- **Fresh qualification:** P0 and Q0 run fresh on gpt-6-sol; Q0 needs the gpt-6-sol P0 and S1 the gpt-6-sol Q0 at this source hash; nothing on one model qualifies another. No gate is loosened.

## Request on gpt-6-sol

OpenAI Chat Completions through `src/openai_provider.py`, an unchanged copy of the reviewed `pipeline/reference/openai_provider.py` (selected by `STUDY_MODEL`/`STUDY_PROVIDER`; `provider.OpenAIStudy` only adapts the call signature, maps the billing metrics and maps a voided call to "not a model call").

- Body, exactly: `model: gpt-6-sol`, `reasoning_effort: medium` (the effort the study uses on Opus), `max_completion_tokens: 16000`, `response_format`, `messages: [system, user]`. No `temperature`, `top_p`, `max_tokens`, tools, `stream`, `n` or `seed` (selftest `test_sol_request_body_has_exactly_the_intended_keys`).
- Messages: the study's system prompt and the packet's JSON text, byte for byte what the Opus rungs receive.
- **What enforces the answer's shape:** `response_format: {type: json_schema, json_schema: {name: answer, schema: <study.schema()>, strict: true}}`, the strict JSON-schema form the reference adapter supports, with the study's schema unchanged (12 required `use`/`skip` enums, the claims array of `{resource, claim}` items, the rationale string; every object closed and every property required, as strict mode needs). Then the adapter parses the text locally (duplicate keys rejected) and the study's unchanged validator (`study.validate`, then `study.normalize`) accepts or rejects it. An answer the validator rejects is `invalid_answer`; text that does not parse is `invalid_json`. Whether OpenAI accepts this schema in strict mode is first seen at P0 (an `http_400` there stops the chain after one call).
- `max_completion_tokens` sizing: it bounds reasoning plus answer. A normal answer is about 200 to 300 tokens; the longest answer the study accepts is 12,000 characters (about 3,000 to 4,000 tokens). 16,000 − 4,000 = 12,000 tokens left for reasoning even at the longest answer, against reasoning at low effort on a similar gpt-6-sol packet of at most 373 tokens (sybil-split-xmodel post-run review). `finish_reason: length` is `truncated_output`, a failed call, never a forced answer; `content_filter` or a `refusal` field is `refusal`.
- Transport: re-sent only on HTTP 429 without billing words and on 500/502/503/504, at most twice, 2 s then 6 s, `retry-after` honoured up to 20 s, all inside the 300 s request budget. Never on any other status, a timeout, or anything after a response.
- Cost: computed from the usage block at the pinned prices (USD 2.00 input, 0.20 cached input, 2.50 cache write, 10.00 output per million; reasoning tokens are output). The response must name `gpt-6-sol` (or its dated form).

## Dollar cap and expected cost (arithmetic)

Request sizes, measured on the frozen plan with the gpt-6-sol body (scripted boards stand in for model boards): S1 mean 7,489 bytes, largest 10,315; Q0 mean 7,573; P0 6,902. At 0.313 tokens per byte (measured on gpt-6-sol, sybil-split-xmodel P0) that is about 2,350 input tokens per S1 call (largest about 3,230).

- **Expected** (guess for output: about 1,000 tokens per call, reasoning included, at medium effort): 3,625 × (2,350 × 2.50 + 1,000 × 10.00) / 10⁶ = 3,625 × 0.015875 = **about USD 57.5**. Input priced at the cache-write rate is the upper of the two input prices; cache reads at 0.20 would lower it.
- **High case** (2,000 output tokens, 3,000 input tokens): 3,625 × (0.0075 + 0.020) = about USD 99.7.
- **Cap: USD 120** on the gpt-6-sol ledger (settled cost plus open reservations). Open reservations at 10 in flight are at most 10 × (10,315 × 2.50 + 16,000 × 10.00) × 10 / 10⁶ = about USD 18.6.
- **Projection gate before S1** (unchanged rule): 3,600 × Q0 mean cost per call × 1.25 must fit in what is left of USD 120. It refuses S1 if Q0's mean cost exceeds about USD 0.0266 per call (about 2,100 output tokens per call at 2,350 input), so a run on the high side stops before S1 rather than at the cap mid-stage.
- Absolute ceiling if every call used its full allowance: about USD 0.18 per call; the cap stops the ledger long before that.

## Load and run time

At most 10 requests in flight (2 episodes × 5 agents; 5 in Q0). Calls of a round are sent together and the next round waits for the slowest of the five.

- Measured, other study: gpt-6-sol at `reasoning_effort: low` answered 60 Q0 calls of about 3,200 input and 110 output tokens in 56 s with 4 in flight (about 3.7 s per call).
- Estimate here (not measured): 8 to 15 s per call at medium effort with about 1,000 output tokens; the slowest of five about 15 to 25 s; 120 episodes, two at a time, six rounds each: 60 × 6 × 15 to 25 s = **about 1.5 to 2.5 hours for S1**, plus a few minutes for S0, P0 and Q0. That is about 25 to 40 requests per minute and about 85,000 to 135,000 tokens per minute (input plus output), far below the OpenAI limits observed tonight on gpt-6-luna (10,000 requests and 10,000,000 tokens per minute; gpt-6-sol's own limits were not read).
- If the slowest call of a round is above about 33 s, S1 takes more than 3.3 hours and would not finish before 00:00 UTC from a 20:15 UTC launch. The in-flight setting is hashed and is not changed after launch; a faster setting (for example 4 episodes, 20 requests in flight, which would halve the time) would need a new source hash and was not pre-registered. P0's recorded latency is the first real reading.
- Stage limit 28,800 s, chain limit 32,400 s, unchanged.

## Changes and unresolved issues

| Issue | Change or diagnostic | Acceptance check | Owner |
|---|---|---|---|
| Anthropic organisation at its monthly limit until 2026-11-01 | gpt-6-sol added as first rung; Opus rungs kept | Selftest: default model gpt-6-sol, override to each Opus rung, refusal outside the ladder, `STUDY_PROVIDER` must match | chain |
| Answer schema was built for Anthropic structured output | Strict JSON schema with the same schema, plus the study's own validator | Selftests: exact body, closed schema, invalid answer and invalid JSON categories | provider |
| Reasoning tokens count against the output allowance | 16,000 allowance; `length` is a failed call | Selftest: `finish_reason: length` → `truncated_output`, never re-sent | provider |
| OpenAI billing stop wording differs | Reference adapter's detector; `provider_billing_stopped` treated as the study's billing stop everywhere (worker, summary, chain resume, coordinator, verify) | Selftest: 3 quota errors then healthy (one pause, 180 s); 30 quota errors (stop at 1,200 s, call voided, 21 attempts); full chain stop then resume runs exactly the not-started rows on gpt-6-sol | chain |
| Launcher's `setup` sets `STUDY_MODEL`/`STUDY_PROVIDER` before the suite (cost a launch tonight elsewhere) | The suite clears both (and `STUDY_REPLICATION`) at import; each test sets its model | Suite run on this Mac with and without the variables set: same count, both OK | builder |
| A ledger refusal raised inside the reference adapter would have been read as `transport_CallFailure` | One `CallFailure` class shared by both adapters | Selftests on caps and the attempt cap still pass; rehearsal ledger totals | provider |
| Opus adapter's billing detector names only the credit balance | Not changed here (the 11:20Z addendum's wider detector is not in the Opus adapter); must be added before any Opus launch | — | next Opus builder |
| Q0 risk: decisions at posterior 0.084 | Unchanged; a Q0 stop is a result to report, not a retune | — | analyst |

## What was run (this builder, macOS, Python 3.9.6, no network to any model provider)

All at source hash `0947408b…` (code commit `73ff2751`), 2026-10-04 about 19:00 to 19:15 UTC.

- `python3 src/selftest.py`: **49 of 49 OK**, run twice in parallel: once with `STUDY_MODEL`, `STUDY_PROVIDER` unset, once with `STUDY_MODEL=gpt-6-sol STUDY_PROVIDER=openai` (as the launcher's `setup` sets them). Same count, both OK, about 433 s each with the two runs sharing the CPU (about 177 s alone). The 41 earlier tests run on `claude-opus-5-5` (each sets its model); 8 new tests in `SolTests`: settings, budget and prices; the exact request body and price arithmetic (3,000 prompt tokens written to the cache + 1,200 completion → USD 0.0195; with 2,000 cached → USD 0.0149); failure categories (`length` → `truncated_output`, refusal, invalid JSON, invalid answer, model mismatch, missing usage, HTTP 400 kept with evidence and never re-sent; 500/503 and a plain 429 re-sent, three 5xx → `http_500`); billing (3 `insufficient_quota` errors then healthy: one pause of 180 s, 4 attempts; 30 errors: stop at 1,200 s, call voided, 21 attempts, nothing new starts); a failed Q0 on gpt-6-sol stops the chain and S1 is refused (`projection_needs_exactly_one_passed_q0`, coordinator gate); a full chain on gpt-6-sol with a billing stop in S1, then `resume` runs exactly the not-started rows in `s1-001-gpt-6-sol-r1` and `verify` passes; the projection uses USD 120 on gpt-6-sol and USD 450 on Opus; source hash, Q0 plan, schema and prompt identical under four launcher environments. The ladder test covers default gpt-6-sol, override to each Opus rung, refusal outside the ladder, and `STUDY_PROVIDER` that does not match the model.
- Offline S0, `python3 src/worker.py --stage S0 --attempt oai-s0`: 1,225 of 1,225 valid, 16 of 16 invariants (both controls), scripted qualification 134 of 134, scripted probe passed, 0 model calls.
- `python3 src/manifest.py --check`: matches; digest `6f126bb5…` unchanged from chain-001 (the plan did not change).
- `python3 src/rehearse.py --hub-dir <local copy of the hub>`: **59 of 59 checks passed**, every scenario on gpt-6-sol through the OpenAI path with a local stub on 127.0.0.1 and a throwaway local hub: (a) full chain S0, P0, Q0, S1 done, 3,625 calls, at most 10 requests in flight, every request on gpt-6-sol, ledger cost equal to the pinned prices on the stub's usage, `verify` OK (90 s); (b) failed Q0 stops the chain with exit 3 and no S1 run on the hub; (c) one HTTP 400 in S1 ends one episode, S1 done, primary contrast as bounds; (d) a failure every 40th call stops S1 at the 4th failed episode; (e) three `insufficient_quota` 429s then healthy: one pause, nothing failed; (f) a quota error that does not end: S1 stops with `provider_billing_stopped`, 6 interrupted rows, `resume` runs the 3,401 not-started rows, every row exactly once, second resume refused, `verify` OK; (g) after (f)'s stop on gpt-6-sol, P0, Q0 and S1 on `claude-opus-5-5` complete on their own batches and ledger, its Q0 refused before its P0 existed. Stub tokens and dollars are not real. Because this Mac's disk was down to about 230 MB free, the rehearsal was run through a small driver outside the repository that deleted each finished scenario's throwaway hub data directory (never read again by the rehearsal) and would have aborted below 80 MB free; the rehearsal code itself ran unchanged.
- The private launcher's `check_ready` (run read-only against a local copy, nothing copied into this repository) accepts this READY.yaml, README and review; its model choice gives gpt-6-sol on openai with only `SWARM_OPENAI_API_KEY` and the default ledger and results paths, and `-opus-5-5` / `-opus-5` paths with the Anthropic aliases for the Opus rungs.
- `python3 scripts/lab.py check`: 0 errors. `python3 scripts/experiment_evidence.py --write` then `--check`: valid and current.

## What was not tested

- No real OpenAI response: whether gpt-6-sol accepts this strict schema, its reasoning-token use and latency at medium effort, its rate limits, and the real `insufficient_quota` body. P0 is the first real reading of each.
- The suite on Python 3.12 (the launcher's `setup` runs it on the server); the real hub and the private launcher (the rehearsal uses a local copy of the hub on 127.0.0.1).
- The Opus rungs against a real provider (impossible before 2026-11-01); the Opus adapter is unchanged and still passes its tests.
- Whether 10 requests in flight finishes S1 within 2 hours: estimated above, not measured.
