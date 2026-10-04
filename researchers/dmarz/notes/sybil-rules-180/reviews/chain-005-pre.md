# Pre-run assessment: chain-005, replication R2 (gpt-6-luna, original economy)

Owning builder's assessment, 2026-10-04, dmarz/flagship-market. Same launch commit and source hash as [chain-004-pre](chain-004-pre.md) (source hash `a1371e7c2df0f3ff171726a6da121b03df86e76b7ec8dc320cb8b820a567729e`), which the launcher reads; this file adds what is specific to R2. Not independently reviewed: same-researcher check only; cross-researcher review waived by dmarz.

- Origin: replications added by dmarz/fleet-monitor on 2026-10-04 after seeing attempt 002's result; follow-ups, not confirmations of a hypothesis stated before all data ([pre-registration Amendment 2](../preregistration.md)).
- What R2 is: the original economy (seed `sybil-rules-180-economy-001`, markets 318000 to 318059) with model `gpt-6-luna` through the same OpenAI adapter: `reasoning_effort: low`, `max_completion_tokens: 2000`, JSON-object mode, price row input 0.10 / cached 0.01 / cache write 0.125 / output 0.50 USD per million (equal to the adapter's PRICES row, checked), reservation margin 1, 3 in flight per server. Batches `*-002-gpt-6-luna`; worker sessions under `sybil-rules-180-gpt-6-luna`; ledger `accounting/ledger-gpt-6-luna.jsonl`.
- Fixtures: fresh probe 318676 to 318693, ordinary 318694 to 318699, smoke 318626 to 318629 and 318636 to 318637, the last unused ids of the reserved range. X0 context, the main economy and D1 tasks are those gpt-6-sol saw in attempt 002: a different model reusing clean fixtures, which is the point of a model comparison on the identical economy.
- Question: does the attempt-002 pattern depend on the model? A qualification stop at P0, Q0 or X0 is a result ("gpt-6-luna at effort low does not qualify on this instrument"), not a defect to repair.
- Cost: attempt 002's token use (17.66 M input, 1.20 M output) at gpt-6-luna prices is about USD 1.8 to 2.2 for input (input or cache-write price) and USD 0.60 for output: about USD 3. Worst case per call USD 0.0023 (10.5 KB × 0.125 + 2,000 × 0.50 per million). Cap USD 15.
- Offline checks: as listed in chain-004-pre (selftests with `STUDY_MODEL=gpt-6-luna` independent of the environment; offline S0 as gpt-6-luna passed; rehearsal scenario j passed).

- Ledger: R2 starts a fresh ledger of its own (cap USD 15); READY.yaml declares `ledger: fresh` (added by dmarz/fleet-monitor at launch, 2026-10-04; documents only, source hash unchanged).
## Launch R2

```sh
H=<three free servers, coordinator first>
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> setup  --host $H --model gpt-6-luna
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> chain  --host $H --model gpt-6-luna --confirm-paid --source dmarz/<agent>
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> status --host $H --model gpt-6-luna
```

The claim must list exactly those three servers (one claim per server triple; the launcher refuses overlapping claims).

**Not run, on dmarz's instruction (2026-10-04, dated by dmarz/flagship-market).** At about 19:16Z dmarz said: "dont spin up anymore experiments once these have ended, just make sure all the results and post mortems are pushed and then notify me". R2 was cancelled before launch: no server was claimed for it, no stage ran and no model call was made. Model dependence on the identical economy remains untested.
