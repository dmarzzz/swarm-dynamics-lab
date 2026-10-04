# Reference code for ready-chain studies

Maintained by dmarz/pipeline. Code here is copied into a study's `src/` (so it is covered by that study's
source hash); studies never import it from this folder.

- `openrouter_provider.py`: OpenRouter chat-completions adapter and study ledger for research program v5
  (`qwen/qwen3.7-flash`, provider pinned to Alibaba, no fallback, reasoning disabled, JSON-object mode with
  local validation). Request body exactly the frozen template plus `messages`; usage and cost from the
  response; model and provider checked; distinct failure categories; transport retry on 429 and overload
  statuses only; billing-outage pause and stop category `provider_credit_balance_low`; HTTP status and
  response body kept on every failure; byte-based reservation (there is no token-counting endpoint).
- `test_openrouter_provider.py`: 30 offline tests (`python3 test_openrouter_provider.py`), no network and
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

Not verified against the live service (no call was made while writing it): the exact wording of
OpenRouter's credit error, whether `usage.cost` is present without asking for it, and the `provider`
field's spelling. The adapter accepts either form in each case, and each study's one-call probe (P0)
is where these are first seen for real.
