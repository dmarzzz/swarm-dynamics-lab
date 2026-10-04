# Pre-run assessment: chain-003, attempt 002 with gpt-6-sol (S0, P0, Q0, X0, S1, D1)

Follows [the review cycle](../../../../../tooling/agent-experiments/RUN-REVIEW.md). Owning builder's assessment, written 2026-10-04 by dmarz/flagship-market. It amends [chain-002-pre.md](chain-002-pre.md), which still holds for everything not named here (design, units, endpoints, void limits, gates, transport, visualization, limits of interpretation).

- Study / stage / attempt: sybil-rules-180, attempt 002, model `gpt-6-sol` (OpenAI), batches `s0-002-gpt-6-sol`, `p0-002-gpt-6-sol`, `q0-002-gpt-6-sol`, `x0-002-gpt-6-sol`, `s1-002-gpt-6-sol`, `d1-002-gpt-6-sol`.
- Status: **ready for dmarz/fleet-monitor's check.** No gpt-6-sol call has been made by this study.
- **Code commit and source hash:** see "Pins" at the end of this file (source hash `17665ae01f3291848e57cd54b745f75afc5249eb8a3edc6543f9c7d94aa3810c`).
- Authority: dmarz to dmarz/fleet-monitor at 12:00Z, "we have no experiments running! fix that and or use opus 5 or an oai model, that key should be somewhere"; the model, effort, output allowance, in-flight and USD 150 cap are dmarz/fleet-monitor's decisions of 2026-10-04.
- Review policy: cross-researcher review is waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check. This run is not independently reviewed.
- Why this run is now the flagship: the Qwen configuration of attempt 002 failed Q0 (174 of 185 accepted; mechanics probes 11 of 17, transfer cases void; ordinary-profit ratios 0.36 to 0.64 in the flexible arm against the 0.75 gate). It was the second and last Qwen configuration the program allows, so the program's model does not qualify on this instrument (post-mortem `reviews/chain-002-post.md` to follow). This run uses the same economy seed, design and endpoints with a different model. It is not the program's model choice; the program's text names Qwen, and results are reported as gpt-6-sol's, never pooled with Qwen's.

## What changed relative to chain-002-pre

1. **Model and request.** OpenAI Chat Completions through the reference adapter (`src/openai_provider.py`, copied unchanged from swarm-lab `8290d7ad`, its 28 tests run inside `src/selftest.py`). Request template exactly `model: gpt-6-sol`, `reasoning_effort: low` (the documentation allows none, low, medium, high, xhigh, max; low is the lowest value other than none, as decided), `max_completion_tokens: 2000` (visible plus reasoning tokens), `response_format: json_object`. No sampling parameters. The system text contains the word JSON (the adapter refuses JSON mode otherwise; selftest). Response model accepted as `gpt-6-sol` or its dated form.
2. **Failure handling** (adapter's own): re-send only on 429, 500, 502, 503, 504, at most twice; billing or quota stop (402, or 400/403/429 naming quota, billing, credit or a limit) pauses that worker, re-sends every 60 s for up to 20 minutes, then the stage stops with `provider_billing_stopped`. Refusals, truncation and reasoning use are recorded per call.
3. **Cost accounting.** Usage has no cost field; cost is computed from the pinned price row (USD per million: input 2.00, cached input 0.20, cache write 2.50, output 10.00; `budget.prices` must equal the adapter's PRICES row, checked in the adapter and a selftest). `reservation_margin` 1 instead of the adapter default 10: the byte bound (request bytes as input tokens at the cache-write price plus 2,000 output tokens at the output price) is already an upper bound on every call; with margin 10 a round's 180 open reservations would hold about USD 60 of the cap. The coordinator's permits use the adapter's own formula (selftest: permits equal the adapter's reservations, with a lost task re-issued).
4. **Own run.** Batch suffix `-gpt-6-sol`; ledger `accounting/ledger-gpt-6-sol.jsonl` and results `results-gpt-6-sol` on the coordinator (the launcher's model tag), so not the Qwen ledger; dollar cap USD 150; worker sessions under hub experiment `sybil-rules-180-gpt-6-sol`, so they can never be taken by, or take, another run's workers; gates select runs of this model only. 3 requests in flight per server (X0 measures both halves at 3).
5. **Own fresh fixtures:** probe 318640 to 318657, ordinary-profit 318660 to 318665, smoke 318670 to 318675, from the unused part of the reserved range. Main economy (318000 to 318059), X0 context (318700 to 318759) and D1 (318300 to 318311) are the same as Qwen's configuration; Qwen never reached X0, S1 or D1, so no model has seen them.
6. **Documentation of transfers (from Qwen's Q0).** Qwen's transfer probes voided with `production_exceeds_available_capacity`, for example `transfer_reserve` with the instructed command `{"command":"transfer","from":"reserve","to":"firm-00-04","amount":528}`. With a transfer from the reserve nothing leaves a firm, so that reason can only arise from an order above a firm's listed capacity, most plausibly ordering the incoming 528 at the destination in the same round. The manual did say the capacity "is idle this round, and is usable in the destination from the next round", but in a different paragraph from the production rule, and the round prompt said nothing. Judged partly an interface trap of the same kind as the zero order. Fix (documentation only; the feasibility rule is unchanged): the Production paragraph now says "Capacity you transfer this round produces nothing this round, in the source or in the destination: an order for a firm may not exceed its listed `capacity` minus anything you transfer out of it this round, and capacity transferred into a firm (from your reserve or another firm) can be ordered only from the next round, when the firm's listed `capacity` includes it.", and `portfolio.production_orders_rule` in every round prompt adds "Each order is at most the firm capacity listed here minus what you transfer out of that firm this round; capacity transferred in this round cannot be used until next round." This inference was made from the void reason and the case, not from reading Qwen's answer text; reading two or three of Qwen's voided transfer rounds (`results/sybil-rules-180__q0-002/calls.jsonl.gz`) is still worth doing for the post-mortem.
7. **Counts reported.** `dropped_zero_orders` and `normalizations` are now also written into each stage's `summary.json` and the chain status (Qwen's Q0 summary lacked them; they were only hub metrics). Rehearsal check `a_metrics_reported` requires both on every stage's hub metrics.

## Cost and time arithmetic (USD 150 cap)

- Measured request sizes of this package: 4.8 KB (main economy, first round) to 10.5 KB (X0 maximum context), about 1,400 to 3,000 tokens; dmarz/fleet-monitor's range of 1,000 to 3,800 tokens covers it.
- Calls: 8,118 planned (S0 0, P0 1, Q0 185, X0 180, S1 7,560, D1 192) plus at most 360 re-issues, 8,478 at most.
- Input: 8,478 × 3,000 tokens × USD 2.50 per million (cache-write price as the upper bound) = USD 63.6; at 2,200 tokens and the 2.00 input price, USD 35.7 for 8,118 calls.
- Output including reasoning: 8,118 × 500 tokens × USD 10 per million = USD 40.6; at 300 tokens, USD 24.4.
- Expected about USD 60 to 105; the cap leaves USD 45 or more above the upper planning figure. Worst case per call (10.5 KB × 2.50 + 2,000 × 10.00 per million) is USD 0.046; 8,478 such calls would be USD 392, so the cap, not the arithmetic, is the hard limit: the ledger refuses any reservation that would take settled cost plus open reservations above USD 150, and before S1 the chain refuses unless S1 and D1 calls (7,752) at X0's measured mean cost fit the remaining cap (X0 is the maximum-context case, so this is pessimistic on input). That gate passes while X0's mean cost per call is below about USD 0.0187, i.e. on average below about 1,100 output-plus-reasoning tokens at maximum context.
- Open reservations: one round holds at most 180 × USD 0.046 = USD 8.3 of the cap.
- Time: 3 in flight per server, 9 in total. With 3 to 8 s per call the rate is about 1.1 to 3 calls per second, S1 about 0.8 to 2.4 hours, the chain about 1.2 to 3 hours. The X0 time gate (S1 within 21,600 s) is unchanged.

## Offline checks at the pinned source hash

- `python3 src/selftest.py`: 89 tests OK (the 60 of chain-002, the adapter's 28, and the gpt-6-sol configuration test with fixtures, prices, effort, JSON word and transfer text, plus the permit-equals-adapter-reservation test).
- Offline S0 with `STUDY_MODEL=gpt-6-sol`: passed, 8,118 of 8,118 accepted, 0 model calls, all invariants true.
- Rehearsal (`src/rehearse.py`, throwaway hub on 127.0.0.1, three worker threads, stubs): see the result line under "Pins". Scenario h runs the whole chain as gpt-6-sol against an OpenAI-shaped stub (no cost field, dated model id, reasoning tokens): exit 0, every batch tagged `-002-gpt-6-sol`, the model in every run's params, calls per stage at their caps, worker sessions only under `sybil-rules-180-gpt-6-sol`, 3 in flight per host, cap USD 150 in the ledger, `chain verify` ok.
- Launcher: READY.yaml with `providers:` and `--model gpt-6-sol` validated with agentops main (`c7b8b42`, `7560167`, `18aed12`).
- Not tested: any live gpt-6-sol response, real latency and reasoning-token use under JSON mode, the real hub with this run's session experiment.

## Launch

On the existing claim `dmarz-sybil-rules-180` (sim-dmarz-2 coordinator and worker, sim-dmarz-8, sim-dmarz-10, until 22:53Z):

```sh
H=sim-dmarz-2,sim-dmarz-8,sim-dmarz-10
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> setup --host $H --model gpt-6-sol
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> chain --host $H --model gpt-6-sol --confirm-paid --source dmarz/<agent>
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> status --host $H --model gpt-6-sol
```

The launcher sends only `SWARM_OPENAI_API_KEY`, to the three workers only, and sets `STUDY_MODEL=gpt-6-sol` for the coordinator and the workers.

## Pins

- **Code commit: `1299b4bef2a05d46b9bf9fe1474e04caaa2311f6`. Source hash: `17665ae01f3291848e57cd54b745f75afc5249eb8a3edc6543f9c7d94aa3810c`** (same value in [READY.yaml](../READY.yaml)). The launch commit is the first main commit containing this review; documents after it do not change the hash.
- At this source hash, 2026-10-04, macOS, Python 3.9.6, no network, no model call: selftest 89 of 89 (also with `STUDY_MODEL=gpt-6-sol` in the environment, as the launcher's setup runs them); offline S0 as gpt-6-sol passed; rehearsal passed 56 of 56 checks, scenarios a to h (a to g as in chain-002-pre with the Qwen stub; h the full chain as gpt-6-sol, 61 s).
