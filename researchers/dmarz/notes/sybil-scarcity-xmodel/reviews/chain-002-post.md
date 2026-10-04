# Post-mortem: sybil-scarcity-xmodel, gpt-6-sol chain at reasoning effort low

Status: scientific review complete for this chain by its builder; not independently reviewed (dmarz waived cross-researcher review for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check).

- Study / chain: sybil-scarcity-xmodel / `gpt-6-sol`, `reasoning_effort: low`, batches `s0-002-sol`, `p0-002-sol`, `q0-002-sol` (S1 never queued), hub experiment `sybil-scarcity-xmodel-sol`; launched 2026-10-04 17:54Z by dmarz/fleet-monitor on sim-dmarz-13 at launch commit 1e56c70e, code commit 21eb3fe0, source hash `f3ffc908…`. An earlier setup at 4997223e failed (selftests read `STUDY_MODEL`) and its chain was stopped during S0 before any model call; see the amendment in [chain-002-pre.md](chain-002-pre.md).
- Assessor: dmarz/pipeline-scarcity-qwen (the builder), from the server records fetched by the fleet monitor; every Q0 row was read.
- Records: [records/](../records/) `sol-*` (chain status, S0/P0/Q0 summaries, P0 and Q0 rows); scanned before commit, no key, token, address or hub URL.
- **Verdict: complete_valid_result for this configuration — a qualification stop.** Execution valid (0 failed calls, 0 truncations, all `finish_reason: stop`); responses 49/49 valid structures, 0 normalized; qualification **failed in all three carrier profiles**; S1 not run. As pre-registered, the stop is the result for this configuration. A separately pre-registered follow-up (F1, effort none) is [chain-003-pre.md](chain-003-pre.md).

## Reconcile

| Quantity | Planned | Observed | Evidence |
|---|---|---|---|
| S0 rows | 168 | 168 valid, 0 violations | `sol-s0-summary.json` |
| P0 | 1 | 1 valid interface; answer **not** exact (all six values null) | `sol-p0-summary.json` |
| Q0 | 48 | 48 valid, 0 failed; gate failed | `sol-q0-summary.json`, `sol-q0-episodes.jsonl.gz` |
| S1 | 1,440 | 0 (never queued) | `sol-chain-status.json` (`stopped_at_gate`, Q0, `gate_failed`) |
| Tokens | — | P0 18,232 in / 68 out (29 reasoning); Q0 875,136 in / 8,242 out | summaries |
| Spend | cap USD 150 | P0 USD 0.0463 + Q0 USD 2.2702 = USD 2.3165 (computed from the pinned prices at the cache-write upper bound) | summaries; ledger 49 calls |

P0 measured **0.319 tokens per byte** (18,232 tokens for 57,092 bytes); the largest Q0 projection was 18,230 tokens against the 50,000-token ceiling.

## Q0 by carrier profile (thresholds: field accuracy ≥ 0.95, exact packets ≥ 0.90, null on every withheld fact)

| Carriers | Field accuracy | Exact packets | Withheld facts null | Present facts null | Wrong values |
|---|---|---|---|---|---|
| 1 | 0.573 | 1/16 | 8/8 | 41 (34 common, 7 rare) | 0 |
| 9 | 0.563 | 5/16 | 8/8 | 42 (26 common, 16 rare) | 0 |
| 81 | 0.313 | 2/16 | 8/8 | 65 (31 common, 34 rare) | 1 |

Over all 48 packets: 264 present facts, 115 answered correctly, **148 answered null**, 1 wrong value (root 7905, 81 carriers, skill 5: 49 instead of 89; 49 is skill 2's value, reported 93 times). All 24 withheld facts null. 4 packets were all-null (P0 also all-null).

## Reading the misses

- Every clean packet is truthful and unanimous per skill; every report is `unchecked` except the packet's two `trusted` anchors.
- **Anchoring separates the answers completely:** facts with a `trusted` report among their rows were answered correctly 36 of 36 times; facts with only `unchecked` rows were answered null 148 of 228 times (79 correct, 1 wrong). The model abstains on present, unanimous, unanchored facts, including common skills with about 80 to 160 identical reports.
- The null rate is highest at 81 carriers (34 of 48 rare facts null), where each rare fact has 81 identical unchecked reports: more agreeing unchecked reports did not help.
- Reasoning tokens: mean 174 on the 8 exactly right packets and 125 on the 40 missed packets. Unlike the split study (164 against 53), missed packets here did not reason more.
- Not shape, not truncation, not invented values. Inferred, not tested: the parent's warning ("Some identities may be controlled by one adversary and repeat a fabricated value. Repetition is not independent evidence ... use null if evidence is ... too ambiguous") is read as a reason to distrust agreement among unchecked reports. This is the same pattern dmarz/fleet-monitor reported for the split study's gpt-6-sol qualification (25 null fields on present, unanimous, unanchored facts; 0 wrong values).
- Contrast with Opus 5.5 on the identical 48 packets and prompt: 48/48 exact.

## Interpret

- Primary contrast for gpt-6-sol at effort low: not estimable; S1 did not run.
- The run shows that on the parent's clean packets and prompt, gpt-6-sol at effort low declines to report a value that only unchecked identities support, even when all of them agree. On attacked packets this tendency would have produced abstention instead of the parent's fabricated answers, so its S1 accuracy would have measured caution, not scarcity; the gate prevents that confound.
- Deviations: none in this chain. The setup failure at 4997223e was a test-harness defect fixed before any model call.

## Quality

| Item | Status | Evidence / next action |
|---|---|---|
| Inputs identical to the parent | pass | S0 byte-identity; Q0 ids and hashes equal the manifest |
| Clean competence gate | pass (worked as designed) | stopped before S1 |
| Response validity | pass | 49/49 valid, 0 normalized, 0 failed |
| Budget | pass | USD 2.32 of USD 150 |
| Visual artifacts | unknown | hub frames not inspected |
| Next run | follow-up F1 pre-registered | gpt-6-sol at effort none, own batches and cap; a second stop ends the gpt-6-sol route |
