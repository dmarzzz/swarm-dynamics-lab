# Reference code for ready-chain studies

Maintained by dmarz/pipeline. Code here is copied into a study's `src/` (so it is covered by that study's
source hash); studies never import it from this folder.

- `openrouter_provider.py`: OpenRouter chat-completions adapter and study ledger for research program v5
  (`qwen/qwen3.7-flash`, provider pinned to Alibaba, no fallback, reasoning disabled, JSON-object mode with
  local validation). Request body exactly the frozen template plus `messages`; usage and cost from the
  response; model and provider checked; distinct failure categories; transport retry on 429 and overload
  statuses only; billing-outage pause and stop category `provider_credit_balance_low`; HTTP status and
  response body kept on every failure; byte-based reservation (there is no token-counting endpoint).
- `test_openrouter_provider.py`: 32 offline tests (`python3 test_openrouter_provider.py`), no network and
  no model call. Copy the ones that apply into the study's selftest.

Use: `ledger = Ledger(path, design['budget'])`, `api = OpenRouter(ledger, config)` with `config` holding
`model`, `canonical_model`, `provider`, `request_template` and `budget` (see `CONFIG` in the test file for
every key), then `answer, accounting = api.call(system, user, call_id, validate)`; `call_id` is
`<batch>:<unit id>`. One adapter instance is shared by all threads of a stage. `INTEGRITY` lists the
categories that stop dispatch at once; `BILLING_STOP` is the category after which unfinished units are
recorded as not started and may be resumed. The credential is read from `SWARM_OPENROUTER_API_KEY` in the
process environment and is never written anywhere.

Revision of 2026-10-04 11:20Z (after the fleet monitor's standby pre-reviews and a builder's report): a response
must name its provider and it must be the pinned one (`provider_missing` otherwise); the reservation is 10 times
the snapshot-price bound (`budget.reservation_margin`); a call left unanswered by a billing stop has its reservation
voided so a continuation batch can run it within the exact call caps; duplicate keys in the answer are rejected.
Studies that copied the first version (main f2d7517e) take this one.

Billing detector widened at 11:25Z at the fleet monitor's request: HTTP 402, or a 400/403/429 whose body names
credit, balance, billing, a usage or spend limit, an exceeded limit or insufficient funds; such a refusal pauses and
re-sends instead of failing the call. 32 tests. Per-stage call caps are counted per batch family (`s1-001` with its continuations `-r1`...; a repair
attempt `q0-002` has its own allowance); `max_attempted_calls` counts every attempt in the ledger, so a study that
pre-registers one repair attempt sets it to one attempt's total plus the repair's qualification calls.

Not verified against the live service (no call was made while writing it): the exact wording of
OpenRouter's credit error, whether `usage.cost` is present without asking for it, and the `provider`
field's spelling. The adapter accepts either form in each case, and each study's one-call probe (P0)
is where these are first seen for real.

## OpenAI (`openai_provider.py`, added 2026-10-04 by dmarz/openai-route)

Third provider for ready-chain studies while the Anthropic organisation is at its monthly limit. Same ledger,
reservation, failure-category, billing-pause, voided-reservation and duplicate-key rules as the OpenRouter
adapter; endpoint `https://api.openai.com/v1/chat/completions`, `Authorization: Bearer`, credential from
`SWARM_OPENAI_API_KEY` in the process environment.

- `openai_provider.py`: request body exactly `model`, `reasoning_effort`, `max_completion_tokens`,
  `response_format` (`json_object`, or `json_schema` with `name`, `schema`, `strict: true`), optional
  `temperature`/`top_p` (only with `reasoning_effort: none` on gpt-6-sol or gpt-6-luna), `messages`. No provider
  object, no provider check; the response `model` must be the requested id, `canonical_model` or `<id>-YYYY-MM-DD`.
  `check_config` refuses a template the adapter cannot send or price exactly (wrong keys, an effort the model
  page does not list, sampling parameters with reasoning on, `max_input_tokens` over 272,000, prices that differ
  from `PRICES`). Billing stop category is `provider_billing_stopped` (OpenRouter's is
  `provider_credit_balance_low`); a 429 whose code or message names `insufficient_quota`, quota, billing,
  credit, balance, insufficient, a usage, spend or hard limit is a billing outage, not a rate limit.
  Re-sent statuses: 429 (rate limit), 500, 502, 503, 504. The numeric `x-ratelimit-*` limit and remaining values
  of each successful response are kept (LESSONS item 10).
- `test_openai_provider.py`: 28 offline tests (`python3 test_openai_provider.py`), with a stub opener and a
  real stub HTTP server on 127.0.0.1; no model call.

Usage: `ledger = Ledger(path, design['budget'])`, `api = OpenAI(ledger, config)`, then
`answer, accounting = api.call(system, user, call_id, validate)`. In JSON-object mode the prompt must contain the
word "json" (the API rejects it otherwise; the adapter refuses before reserving, `json_mode_prompt_lacks_json`).

### Prices (USD per million tokens, Standard tier, prompts up to 272K tokens)

Source: https://developers.openai.com/api/docs/pricing (platform.openai.com/docs/pricing redirects there) and
the model pages https://developers.openai.com/api/docs/models/<id>; retrieved 2026-10-04 12:10Z. Copy the
model's row into `budget.prices` of the hashed design; the adapter refuses a row that differs from `PRICES`.

| Model | Input | Cached input | Cache write | Output | reasoning_effort allowed |
|---|---|---|---|---|---|
| gpt-6-luna | 0.10 | 0.01 | 0.125 | 0.50 | none, low, medium (default), high, xhigh, max |
| gpt-6-sol | 2.00 | 0.20 | 2.50 | 10.00 | none, low, medium (default), high, xhigh, max |
| gpt-6.1-sol | 2.00 | 0.10 | 2.50 | 10.00 | low, medium (default), high, xhigh, max |
| gpt-6-astra | 10.00 | 1.00 | 12.50 | 50.00 | low, medium (default), high, xhigh, max |

Prompts over 272K tokens cost about twice as much (gpt-6-sol 4.00 / 0.40 / 15.00); the adapter does not
support them. Batch and Flex are half price; not used here. All four models: 1,050,000-token context,
128,000 max output tokens, Chat Completions supported, Structured Outputs supported.

Cost is computed, never provider-reported (Chat Completions usage has no cost field): uncached input at the
input price, `prompt_tokens_details.cached_tokens` at the cached price, `completion_tokens` (which include
reasoning tokens) at the output price. GPT-6 models bill cache writes automatically; when usage does not
report `cache_write_tokens`, uncached tokens of a prompt of 1,024 tokens or more are priced at the cache-write
price (an upper bound, `input_pricing: cache_write_upper_bound`).

### Verified against the documentation on 2026-10-04, and not

Verified (WebFetch of developers.openai.com): the prices above; `max_completion_tokens` bounds visible plus
reasoning tokens and `max_tokens` is deprecated; `reasoning_effort` values per model page (`minimal` appears in
the generic reference but on no GPT-6 model page; gpt-6.1-sol's page says `none` and `minimal` are unsupported);
`temperature`, `top_p`, `logprobs` must be removed unless `reasoning_effort` is `none`, which only gpt-6-sol and
gpt-6-luna accept ("latest model" guide); `response_format` `json_object` / `json_schema` (`name`, `schema`,
`strict`); usage fields `completion_tokens_details.reasoning_tokens`, `prompt_tokens_details.cached_tokens`
and no cost field; `message.refusal`; finish reasons stop, length, tool_calls, content_filter, function_call;
model pages list only the undated snapshot id for each model.

Not verified (no page fetched said it, and no call was made): the exact 429 `insufficient_quota` body (the
adapter matches code or message words); the Chat Completions spelling of a cache-write usage field (the caching
guide names `input_tokens_details.cache_write_tokens` for the Responses API); the `x-ratelimit-*` header names;
the JSON-mode "must contain json" rule (long-standing API behaviour, not re-read today); whether a `strict`
schema accepts every JSON-Schema keyword a study uses (OpenAI's strict mode needs `additionalProperties: false`
and every property in `required`). Each study's one-call probe (P0) is where these are first seen for real.

### Observed live, 2026-10-04 (trust-credit-qwen attempt 002, 528 gpt-6-luna calls)

Correcting the "not verified" list above with what the live responses showed:

- Usage in Chat Completions carries `prompt_tokens_details.cache_write_tokens` (2,569 of 2,572 prompt tokens on 523 calls, 0 on 5) beside `cached_tokens` (2,569 on the 5 calls that repeated an identical packet). The adapter reads it, so input is priced from reported writes (`input_pricing: cache_write_reported`), not from the upper bound. A prompt of about 2,600 tokens is written to the cache on first use at USD 0.125 per million (gpt-6-luna) instead of 0.10.
- `completion_tokens_details.reasoning_tokens` is present. At `reasoning_effort: low` gpt-6-luna used 0 reasoning tokens on 358 of 528 calls, at most 840 (mean 120); total output at most 885, so a 1,500 allowance was ample for a short JSON answer.
- The response `model` was the undated id (`gpt-6-luna`) on every call; no dated form was seen. `system_fingerprint` was null.
- The `x-ratelimit-limit-requests`, `x-ratelimit-remaining-requests`, `x-ratelimit-limit-tokens` and `x-ratelimit-remaining-tokens` headers are present with these names (10,000 requests and 10,000,000 tokens per minute for gpt-6-luna), and the adapter records them.
- `prompt_tokens` was exactly 2,572 on every call although the requests ranged from 5,818 to 5,875 bytes; the cause is not known. Do not rely on input tokens to differ between packets of nearly the same size.
- One call of 528 took 97 s (median 1.1 s); keep the request timeout at 120 s or more.
- Still not seen live: a 429 `insufficient_quota` body, a rate-limit 429, a 5xx, a refusal or a `length` stop. The flagship study's gpt-6-sol run through the same adapter and launcher path (8,118 calls, as reported by the fleet monitor) had no billing pause either.

### Switching an OpenRouter ready-chain package to OpenAI

1. Copy `openai_provider.py` into `src/` and call `OpenAI(...)` where the study calls `OpenRouter(...)` (same
   `Ledger`, same `call()` signature); treat `provider_billing_stopped` as the billing-stop category.
2. In `design.yaml`, per model: a `request_template` with `model`, `reasoning_effort`, `max_completion_tokens`
   (= `budget.max_output_tokens`, leaving room for reasoning), `response_format`; `budget.prices` = the
   model's `PRICES` row; `retryable_http_status: [429, 500, 502, 503, 504]`; drop `provider`/`reasoning`.
3. Make sure the system or user prompt contains the word "json" (JSON-object mode) or supply a strict schema.
4. In `READY.yaml`: `model_ladder: [qwen/qwen3.7-flash, gpt-6-sol]` with `providers: {qwen/qwen3.7-flash:
   openrouter, gpt-6-sol: openai}`; the launcher's `--model gpt-6-sol` sends only the OpenAI credential.
5. Re-run selftests, refresh `selftests`/`source_hash`, new pre-run review; gpt-6-sol gets its own P0/Q0.
