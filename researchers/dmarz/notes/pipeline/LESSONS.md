# Cross-lane lessons

Maintained by dmarz/results-analyst from tonight's runs. Not a review. Last updated 2026-10-04T10:47Z. Each item says what was observed, where, and what to do in the next plan.

## 1. Caps and timeouts are part of the hash that binds a stage to its qualification. Size them for the whole ladder before the qualifying run.

Observed in four studies: the dollar cap, call cap, output cap and stage timeout sit in a file that is hashed, and a later stage is admitted only when the earlier stage ran at the same hash.

| Study | Where the cap lives | What binds it |
|---|---|---|
| compositional-safety | `design.yaml` `budget:` | `src/common.py` line 13 hashes the file; `src/coordinator.py` line 45 refuses P1 unless the Q0 hashes are current |
| market-split-opus | `design.yaml` `budget:` | `src/common.py` line 16; `src/coordinator.py` lines 25-34 |
| sybil-scale-xl (and its sister studies) | `design.yaml` | `src/study.py` line 22 `source_hash`; `src/coordinator.py` line 14 |
| soc07-private-judgments | `execution.json` | `src/config.py` lines 80-96; `src/launch.py` line 31 (`runtime_changed_since_approval`) |

Consequence: "raise the cap after the qualification shows what the model costs" is not available. It costs a fresh rehearsal and qualification, and in SOC-07 a new world set. compositional-safety is in this position now: q0-007 passed on a design whose ledger cannot hold P1. SOC-07's amendment A6 did it the right way round: cap for S1-R and S1-L set before S1-Q.2.

For every plan: before the qualifying stage, compute calls x worst-case price for every later stage at the new model's prices and put that cap in the design. Check the stage timeout the same way.

## 2. Ledgers that keep full reservations run out about ten times early on Opus.

compositional-safety reserves `(request bytes + 4096) x 4 + 4096 x 20` millionths of a dollar per call and never releases it. q0-007 spent USD 1.69 and reserved an estimated USD 22 to 29. With an 8,192 cap the reservation is about USD 0.20 per call (market-split-opus plan). Studies that count settled cost plus open reservations (sybil-scale-xl A1, market-split-opus, SOC-07) do not have this problem. Any study still on nonrefundable reservations needs its cap multiplied accordingly or its accounting changed before an Opus stage.

## 3. Opus 5.5 request shape: what has now run clean, and what to copy.

Rules (from dmarz/fleet-monitor, confirmed by q0-006's 24 rejected requests): thinking cannot be disabled; `thinking: {type: enabled, budget_tokens}` is rejected; temperature, top_p and top_k are rejected; depth is set only by `output_config.effort`; thinking counts against `max_tokens`; responses carry thinking blocks before the text block; refusals are possible; `fallbacks` stays off.

Configurations that have run tonight with zero invalid responses:

| Study | Effort | max_tokens | Calls | Per call |
|---|---|---|---|---|
| compositional-safety q0-007 | high | 4,096 | 178 | USD 0.0095, 4.25 s |
| discussion-v3-d1-opus d1o-a1 (in progress) | high | 16,000 | 53 so far | USD 0.019, 6 s |
| sybil-scale-xl q0-a1 and q0-a2 | low | 8,000 | 24 each | USD 0.41 (about 100,000 input tokens per call); every answer 38 output tokens, no thinking tokens; 2.5 to 4.7 s per call |
| soc07 S1-Q.2 and S1-R | medium | phase cap + 4,096 | 684 | USD 0.0078, 0 failures |
| market-split-opus I0, Q0, S1 | medium | 8,192 | 570 so far | USD 0.01 to 0.02, 0 invalid |

- A one-call probe before any paid stage costs about USD 0.01 to 0.02 and would have saved q0-006 (24 rejected calls and a full plan, review and post-mortem cycle).
- Small visible-output caps (SOC-07's 64 and 128, compositional-safety's 350) must be raised or given a separate thinking allowance. SOC-07 m3 adds 4,096 on top of each phase cap.
- Adapters differ on `redacted_thinking`: compositional-safety and SOC-07 drop both `thinking` and `redacted_thinking` blocks; sybil-scale-xl and sybil-specialists-opus drop only `thinking` (`provider.py` lines 145 and 125), so a redacted block would be scored `invalid_structured_answer`. I do not know whether this model emits redacted blocks; none has been reported tonight.
- Still on the old shape: `sybil-budget-sonnet/src/provider.py` line 81 sends `temperature: 0`. Any Opus follow-on of the budget grid must port the sybil-scale-xl adapter first.

## 4. Runs are minutes; the gaps between them are waits for a person or an agent.

| Lane | Model time of the stage | Idle before or after it |
|---|---|---|
| sybil-scale-xl | Q0 59 s | 8 s to S1 (tmux chain under the software gate) |
| compositional-safety | Q0 12.6 min | idle since 07:53Z; no successor plan |
| discussion-v3-d1-opus | about 8 min | ready from 07:48Z, waited for dmarz's first-hand go until 07:53Z |
| sybil-specialists-opus | S0 40 s | idle since 07:42Z waiting for a review waiver |
| market-split-opus | S0 about 1 min | idle since 07:48Z waiting for the reviewer's go |
| soc07-private-judgments | S1-Q 40 s | 19 min from failure to the next manifest; S0, approval and S1-Q still to come |

What removes the waits: (a) a go that covers the whole ladder, conditional on the software gates and a written projection rule, instead of one go per stage; (b) the review waiver recorded when the study folder is created; (c) the next stage's pre-run file written before the current stage starts; (d) a chain command, as sybil-scale-xl used.

## 5. In the sybil family the model is not the lever (two studies so far).

sybil-scale-sonnet: primary contrast +52.8 pp against Haiku's +51.4 pp on identical packets. sybil-newcomer-sonnet: +11.1 pp against +8.3 pp, interval on the difference -2.8 to +8.3 pp. Both post-mortems say the effect comes from admission, which is computed before the model call. Three more model replications are in flight (budget on Sonnet, specialists and scale-xl on Opus). If they agree, further model replications of full grids are spend without information; sample the grid, and put the next server on a design that changes admission (proposal 3 in `notes/next-experiments-2026-10-04/README.md`, which has no study folder yet).

## 6. Read the failing answers before changing the model.

SOC-07 failed qualification twice and swapped the model twice without reading the answer text. An offline regeneration of the worlds (no model calls) found that one of Sonnet's three misses sits on a rule the prompt does not state (delivery equal to the deadline), and that the other two are superseded-estimate slips with final margins of 4 and 1 units. A post-mortem for a "valid but wrong" qualification failure should include the rendered prompt and the returned text for every miss. The discussion v3 Q0 post-mortem did this (a table of the constraint each wrong choice violated) and it is why D1, D1-Opus and D2 were well aimed.

## 7. Small gates misclassify often, and a bigger set alone does not fix it.

A solver that is right 90% of the time fails a 10 of 12 gate about 11% of the time (the same for 5 of 6); at 85% it fails about 26% of the time. Doubling to 20 of 24 moves these only to about 9% and 29%. What helps is removing ambiguous items before the run (item 6) and writing down in advance what a near miss triggers: at 9 of 12, read the three misses before anything else.

## 8. Long stages stop on the first HTTP error, with no retry. One 429 or 529 ends the stage.

Read in the code, not yet observed tonight. In the sybil chains (`sybil-scale-xl/src/provider.py` lines 121-122 and `src/worker.py` line 59; the same shape in sybil-newcomer-opus, sybil-specialists-opus and the sybil-scarcity-opus design: `retries: 0`), any HTTP error becomes a failed row, a failed row stops new dispatch, and every remaining assignment is recorded as not started. market-split-opus fails the bundle, writes a stop marker and exits the worker (plan, "S1 execution"). compositional-safety is different: it records the episode as invalid and continues (q0-006 ran all 24 rejected requests to the end). A repair is a new batch, which for the hashed designs means S0 and Q0 again.

Tonight's base rate is good: about 10,000 Haiku and Sonnet calls and about 350 Opus calls with zero provider errors. The exposure is the size of what is now starting: sybil-scale-xl S1 (576 calls, about USD 240, four in flight, packets up to about 200,000 tokens, so rate limits on input tokens per minute are the likeliest error), sybil-newcomer-opus S1 (1,944 calls), sybil-scarcity-opus S1 (1,440 calls, about USD 150), market-split-opus S1 (864 calls over 2.3 hours).

A 429 or 529 response carries no model output and is not billed, so retrying it does not resample anything. SOC-07 already does this (`execution.json` `retry`: statuses 429 and 529, backoff 2 s and 6 s, `retry_after` capped at 20 s). For chains not yet launched, copying that rule costs one edit before S0. For runs already going, the thing to prepare is a resume path: a command that dispatches only the not-started assignments at the same source hash.

## 9. Moving every lane to the strongest model fixes the floor and can hit the ceiling.

Tonight's qualifications failed from below on Haiku and Sonnet (SOC-07 7 and 9 of 12; discussion v3 2 and 3 of 6; compositional-safety 21 of 24) and pass at or near the maximum on Opus 5.5 with reasoning (12 of 12; 12 of 12 and 6 of 6; 24 of 24 three times). For studies whose measure is a difference between arms, that is a risk in the other direction. SOC-07's S1-R came out at team success 1.00 in both arms, and S1-L (4,080 calls, USD 32.60) repeated it exactly: +0.000. compositional-safety P1 looked the same after two D1 bundles (14 of 14 safe) and then showed spread in D2/risk (3 of 7: the fragmented arms stalled, receipts completed), so it is not at ceiling. discussion-v3-opus is different: its clean reports-only arm is 6 of 6 while the other clean arms abstain, so it still has spread.

For the next plans: give each qualification an upper bound as well as a lower one, or add a difficulty dial (more records, narrower margins, lower effort) that is set so the control arm lands between about 60% and 90%. A run where every arm scores 100% costs the same as one that can answer its question.

The other half is where to stop. The cheap stage usually already shows the ceiling: SOC-07's S1-R (672 calls, USD 5) showed 1.00 against 1.00, and S1-L (4,080 calls, USD 33, 42 minutes) could only repeat it. Rule adopted for SOC-07 v2 and worth copying into any ladder with a cheap stage before an expensive one: if the cheap stage is at ceiling (or floor) in every arm, the expensive stage is not launched. It can be enforced without touching the hashed design by launching the stages in parts and making the last launch conditional on the earlier stage's reported flag.

## 10. Nobody can say what the Opus rate limit is, because no adapter keeps the response headers.

At 09:20Z the question was whether sybil-scale-xl's S1 (about 6 to 7M input tokens per minute, four in flight) and sybil-scarcity-opus's S1 (about 1M per minute) can overlap. The number that settles it, `anthropic-ratelimit-input-tokens-limit`, is returned on every successful call. No dmarz adapter stores it; I searched every record and log on all nine servers. The largest volume shown to work is 2.46M input tokens in one minute (scale-xl Q0).

Measured at 09:20Z by the scale-xl session with one header call: 5,000,000 input tokens, 1,000,000 output tokens and 5,000 requests per minute for the workspace. Against that: scale-xl's S1 asks for about 5.9M per minute by itself (q0-a2 records: 2,458,711 tokens completing inside 22 seconds with four in flight), scarcity's S1 0.9M, every other lane together under 0.2M. The fleet monitor paused scale-xl's worker until scarcity was nearly done.

For the next adapter revision: record the `anthropic-ratelimit-*` limit and remaining values from each response (numbers only, no other headers) next to the usage counts. Then any session can read the headroom from the records, and a chain can hold itself when `remaining` is low instead of finding the limit by hitting it.

## 11. A credit outage is an HTTP 400, not a 429. No retry rule covers it, and each adapter fails differently.

(The fleet monitor refers to this as the credit-outage lesson; item 10 above is the rate-limit header lesson.)

What happened: for about 20 to 30 seconds around 10:10:30Z to 10:10:50Z the account's prepaid credit ran out, then calls succeeded again. Reported spend had gone from about USD 390 at 09:15Z to about USD 780 at 10:12Z.

| Lane | Timestamp (UTC) | What the record shows | What the adapter did |
|---|---|---|---|
| sybil-scale-xl S1 | last reservation 10:10:26; failure on the next count_tokens request, by 10:10:36 | 1 x `count_http_400` | Stage stopped: 481 of 576 done, 94 not started. Same code path in sybil-scarcity-opus, sybil-split-opus and sybil-newcomer-opus: any failed call stops dispatch |
| discussion-v3-opus S1 | 61 consecutive failures ending at about 10:10:48 (no timestamps in the journal; derived from the 12 later calls' latencies) | 61 x `provider_failure`, reason `provider_credit_balance_low`, `http_status_class` 4xx | Each call recorded as missing and the run continued, so 61 calls across 7 of 24 worlds (54101, 54119 to 54124) are lost in this attempt |
| compositional-safety | none in the credit window (its four invalid episodes at 10:06Z to 10:07:30Z are `http_429`) | | Would record the episode as invalid and continue; no retry |
| soc07 v2, sybil-split-opus, market-split-opus, sybil-scarcity-opus | no call in the window | | |

Rules that follow:

- A credit error is a 400. The 429/529 retry added tonight does not catch it. Treat it as "pause the stage and report", never as a failed call or a missing response.
- A canary check must read the failure reason, not a count of 429s or a latency. My 10:06Z and 10:08Z canary readings on discussion-v3-opus (0 failures) were true when taken and were read as "small-request lanes are safe"; two minutes later that lane had 61 failures from a different cause, and a no-retry lane had already lost four episodes to 429s. A canary shows that nothing has failed yet, in lanes that retry.
- Only the discussion adapters name the cause in the record. The sybil adapters keep `count_http_400` or `http_400` with no message. Keep the provider's error type and the first 300 characters of its message on every 4xx (compositional-safety already does).
- Before any stage over about USD 50: someone with console access confirms the balance and the auto-reload setting.

Reference implementation as of 10:17Z: compositional-safety design v12 (`src/provider.py` lines 96-110, `design.yaml` `capacity_retries: 10`, `billing_wait_seconds: 1800`). A 429 or 529 is resent unchanged up to ten times, honouring `retry-after`; a 400 whose message contains "credit balance" is treated as a billing outage and waited out in 60-second steps for up to 30 minutes before the call is failed as `billing_outage`. The sybil chains and the discussion adapter still stop or lose the call on a credit error.

## 12. The rate limit behaves as a 5M-token bucket; a lane with no retry pays for every 429 with data.

Measured on sybil-scale-xl S1: 5.8M input tokens per minute against a 5.0M limit ran clean for about five and a half minutes, then 429s began. That is a bucket of 5M refilled at 5M per minute: a stage can exceed the limit by X for about 5/X minutes from full. Timestamps from scale-xl's ledger: first calls 10:01:36Z; 429s at about 10:07:10Z to 10:07:14Z (four calls) and 10:08:23Z (four calls), each cleared by the 20-second retry. compositional-safety (`retries: 0`) lost four episodes to `http_429` between about 10:06:30Z and 10:07:30Z and had to relaunch. discussion-v3-opus recorded no failed call in that period; its adapter retries 429s and does not log cleared retries, so whether it drew any is not known. Every adapter needs the 429/529 retry, including the ones whose own traffic is tiny, and a stage that will exceed the limit should be scheduled when no no-retry lane is running.
