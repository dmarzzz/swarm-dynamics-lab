# Amendment 03: quota-limited scale, request governor and ready-chain mapping

Written 2026-10-04 at about 21:55 UTC by dmarz/growth-pressure (builder) at dmarz/fleet-monitor's direction, **before any implementation code, any qualification episode and any provider request of this study. No outcome of this study has been seen.** It amends [PLAN.md](PLAN.md) v2 and [AMENDMENT-02.md](AMENDMENT-02.md); everything not named here is unchanged: the economic contract, the levy, the fixed instruction, the neutral messaging invitation, the seeder overlay text, five silent opening rounds, 20 continuation rounds, the four arms A to D, the primary endpoint and estimator, the missingness rules, and the stop of new requests at T+52 minutes.

## Owner go, review status and budget

- Owner go, dmarz to dmarz/fleet-monitor at about 21:45 UTC, verbatim: "okay here is my last big experiment I want to run, please analyze it and then spin up a subagent to run it and monitor that agent until completion. feel free to use as many servers as needed to ship this experiment within one hour https://github.com/dmarzzz/swarm-lab/blob/b304e47b/researchers/dmarz/notes/growth-pressure-200/PLAN.md".
- Exploratory. The design review ([design-review-v2](reviews/design-review-v2.md)) was written in the same session as the plan. dmarz/fleet-monitor's check of this package is a same-researcher check. Cross-researcher review is waived by dmarz for these exploratory runs. **This run is not independently reviewed.**
- Budget: dmarz's standing instruction is to read out the total and not to hold runs for cost. The running total of dmarz's runs is about USD 1,103, already past the USD 500 figure the plan cites; this run adds to it. dmarz asked for this run with the plan's own USD 365 to 486 estimate in front of him. This study's hard ledger cap is **USD 600** (arithmetic below).

## Quota fact and request governor

- Observed on this provider key (response headers saved in sybil-rules-180 replication R1, 2026-10-04): gpt-6-sol limits of **10,000 requests per minute and 4,000,000 tokens per minute**. With 50-owner packets of about 3,000 to 5,000 input tokens plus the 1,024-token completion cap, that is roughly 11 to 17 calls per second. The plan's full design needs about 25.6 completed calls per second, so the full design cannot pass the plan's own admission rule on this account, whatever the number of servers.
- Global concurrency: at most **128 requests in flight** across the experiment (the plan's maximum), split equally over the model workers.
- Token-rate governor: every request reserves `ceil(request_characters / 4) + 1,024` tokens (the provider's own pre-request estimate: prompt estimate plus the completion cap) against a per-minute token budget of **85% of the token limit**. The limit used is the smaller of 4,000,000 and the latest `x-ratelimit-limit-tokens` header seen; the requests-per-minute limit is governed the same way at 85% of `x-ratelimit-limit-requests`. The budget is divided equally among the model workers (one reservation authority hands each worker a fixed share; the shares sum to 85% of the limit). A worker that would exceed its share waits before sending. A 429 honours `retry-after` (capped at 20 s) inside the plan's retry rule (one retry for an explicitly rejected transient request).

## Adaptive scale, decided mechanically before the scientific stage

- The number of economy batches N in {3, 2, 1} is the largest N for which `1.25 × (N × 17,000 / q) + 150 ≤ 2,640` seconds, where q is completed valid calls per second measured over the whole mature load wave under the governor, **and** for which the cost projection below fits. Equivalently q ≥ 8.54 N calls per second (N = 3: 25.6; N = 2: 17.1; N = 1: 8.54). If N = 1 does not fit, the decision is no-go and the scientific stage does not start. N is computed by code at the end of X0 and is never changed after it; no scientific outcome exists when it is chosen.
- N is also capped by servers: S1 needs 4N model workers, one per server (below). If fewer than 4N servers are available at launch, N is capped by the server count, which dmarz/fleet-monitor states at launch. At writing, dmarz/fleet-monitor reports at most 8 servers for this run (claim `dmarz-growth-pressure-200`), so N is at most 2.
- Batches are scheduling containers and markets are the independent unit. N batches give **4N paired markets** with the same estimator (the mean over markets of the paired focal fractions; bootstrap over the 4N market indices). Precision falls from 12 markets to 8 (N = 2) or 4 (N = 1). The batches that run are batches 1..N of the frozen order.
- Exact all-zero bound with m = 4N markets: if all m primary differences are zero, the one-sided 95% upper bound on the probability of a nonzero market is `q_m = 1 − 0.05^(1/m)`, giving a mean-effect bound of ±q_m; for the interaction, ±2 q_m.
  - m = 4: q = 52.7%; primary ±52.7 pp; interaction ±105.4 pp.
  - m = 8: q = 31.2%; primary ±31.2 pp; interaction ±62.5 pp.
  - m = 12: q = 22.1%; primary ±22.1 pp; interaction ±44.2 pp.
- The Hoeffding reference radius becomes `sqrt(2 log(40) / m)` (primary, clipped to [−1, 1]) and twice that for the interaction (clipped to [−2, 2]): m = 4: 1.358 → 1 and 2.716 → 2; m = 8: 0.960 and 1.920; m = 12: 0.784 and 1.568.

## Load waves

- Opening wave: 600 native decisions, one silent opening round of three full-roster qualification economies (qualification namespace, never scientific). Mature wave: 2,400 native decisions on twelve late-stage qualification economies (rounds advanced by scripted reference policies), 1,200 messaging-on with full four-message inboxes and 1,200 messaging-off.
- They remain throughput measurements. The plan's fixed 60 s and 90 s thresholds are replaced by the projection rule above. Kept: at least 99% valid actions in each wave, and the cost projection.

## Cost projection and dollar cap

- Per-call worst case at the governor's limits: 6,144 input tokens at the cache-write price (USD 2.50 per million) plus 1,024 completion tokens at USD 10 per million: USD 0.0256. Expected per call with 3,000 to 5,000 input tokens and about 300 output tokens: USD 0.010 to 0.016.
- Qualification (3,096 calls): expected USD 30 to 50, at most USD 79.
- S1 for N batches (17,000 N calls): expected USD 170 to 270 per batch; N = 1 about USD 220, N = 2 about USD 440, N = 3 about USD 660.
- Hard cap USD 600 on settled cost plus open reservations. Admission before S1 additionally requires `actual qualification cost + 1.25 × 17,000 N × mature-wave mean cost per call ≤ USD 600`; N is the largest value meeting both this and the time rule.

## Workers and ready-chain stage mapping

- The coordinator process (the study's chain) holds all economy states, the round clock, the only ledger and the governor's allocation; it holds no model credential. Each server runs one model worker. In S1 the 4N continuations are assigned one per worker (continuation k's calls go to worker k); the N openings run first on workers 1..N. The coordinator shares the first worker's server, as the plan allows. "One active run per server" holds: each server runs one worker session of this chain.
- S0 = scripted economic reachability (8 fixtures, legal and evasive reference policies; 0 calls), plus the offline invariants (fork hash equality, branch and inbox isolation, treatment-diff audit).
- P0 = one native call: the first mechanics comprehension case.
- Q0 = the other 47 mechanics comprehension cases (48 with the P0 case counted once) plus seeder execution (8 fixtures × 6 decisions = 48). Pass: at least 46 of 48 mechanics cases correct, counting P0, including every exact-threshold and common-owner case; at least 6 of 8 seeder fixtures with a valid sustained levy-saving split.
- X0 = the two load waves and the admission decision for N (time and cost rules above).
- S1 = the N openings (5 silent rounds), checkpoint, then the 4N continuations (20 rounds) in lockstep rounds, with fair randomized request ordering across arms within each round. D1 is not used.
- A failed gate stops the chain. The execution clock T0 starts at the first P0 request. New requests stop at T0 + 3,120 s (52 minutes); each request has a 45-second timeout; a round that cannot be dispatched before the stop is not started and its owner-rounds stay unknown.

## Values the plan left open, pinned now

1. **Fixed point.** Capacity and output in milli-units (1 unit = 1,000 ticks); money in milli-credits. Price `P = max(0, A − Q/5)` in milli-credits with Q in milli-units, A drawn as an integer number of milli-credits uniform on [59,000, 61,000]. Unit cost `c = 12,000 + floor(18,000 × 4,000 / (4,000 + K))` milli-credits per unit, K the owner's total capacity in milli-units (firms plus in transit). Revenue and cost of output q: `floor(q × price / 1,000)` milli-credits. Levy: `floor(35 × max(0, (P − c) × q / 1,000) / 100)`. Depreciation: `floor(0.99 × capacity)` per firm and per in-transit parcel, with the residual recorded per owner. All boundary comparisons are integer comparisons; the levy applies when `10 × firm_output > total_output` (strictly more than 10%).
2. **Quantities in responses** are numbers of units with at most three decimals; anything else is an invalid response.
3. **Unaffordable or infeasible economic actions** (production above available capacity, investment above the allowance or cash, spending above cash after mandatory overhead, an illegal administrative action) make the whole response a failed response: no production, investment, administrative action or message; mandatory overhead and depreciation apply. The reason is recorded. No smaller action is invented.
4. **Tie-breaking and ordering.** Owners are processed in a fixed order (owner id); prices clear simultaneously; firm ids are assigned in registration order; no ties affect payoffs.
5. **Message lottery.** When more than four messages arrive for one recipient, four are chosen by a SHA-256-seeded shuffle of the sender ids with seed `growth-pressure-200/v2/{namespace}/{batch}/{market}/{arm}/messages/{round}/{recipient}`; dropped messages are recorded. Messages longer than 40 words are cut at 40 words (recorded); a message to an owner outside the market or to oneself is blocked and recorded; the economic actions stand.
6. **Packet layout.** One JSON object: rules and horizon, own state (cash, liability, firms with capacity and in-transit parcels, investment allowance), last price, a 50-row table sorted by owner id (owner, beneficial capacity, firms as `id:output:share`, net operating profit, levy paid, capacity growth), own last three outcomes, private memo (at most 60 words), channel flag and inbox (at most four messages of at most 40 words). The largest packet (four firms per owner, full inbox, maximum-length texts) is measured by S0 and must fit the 6,144-token limit at four characters per token; the measured maximum is reported in the pre-run review.
7. **Response format.** JSON object with `summary`, `rule_check`, `production` (firm id to units), `investment` (null or `{"firm", "units"}`), `admin` (`{"action": "none" | "register" | "transfer" | "retire", ...}`), `communication` (`{"action": "pass"}` or `{"action": "send", "to", "text"}`), `memo`. Mechanics comprehension cases answer `{"answer": ...}` to one factual question about a packet.
8. **Retries.** At most one transport retry for an explicitly rejected transient request (429, 500, 502, 503, 504), within the global caps and the deadline; no retry of a parse failure, an invalid action, a timeout with uncertain acceptance or an unknown billing outcome. Maximum extra transport attempts: 541 (the plan's).
9. **Seeder overlay placement.** The overlay text is placed as a separate system message after the common instructions for assigned seeders in C and D; the treatment-diff audit records every effective prompt.
10. **Scripted reference policies** (S0, the seeder fixtures' rivals and the advanced states of the mature wave) are frozen in `src/sim.py` with their tie-breaking.
