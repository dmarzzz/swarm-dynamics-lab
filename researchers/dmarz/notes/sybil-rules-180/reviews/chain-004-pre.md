# Pre-run assessment: chain-004, replication R1 (gpt-6-sol, second economy seed); launch review for R1 and R2

Owning builder's assessment, 2026-10-04, dmarz/flagship-market. Amends [chain-003-pre](chain-003-pre.md), which holds for everything not named here. R2 has its own short review, [chain-005-pre](chain-005-pre.md); both run from the same launch commit and source hash, and the launcher reads this file for that commit.

- **Source hash `a1371e7c2df0f3ff171726a6da121b03df86e76b7ec8dc320cb8b820a567729e`**, code commit `16b6c82ec03e14ae9d261d5b4bba686d8887f574`; the launch commit is the first main commit containing this review.
- Status: ready for dmarz/fleet-monitor's check. No call of R1 or R2 has been made.
- Authority and origin: replications added by dmarz/fleet-monitor on 2026-10-04 after seeing attempt 002's result; follow-ups, not confirmations of a hypothesis stated before all data ([pre-registration Amendment 2](../preregistration.md)). Not independently reviewed: same-researcher check only; cross-researcher review waived by dmarz.
- What R1 is: the frozen design of attempt 002 on gpt-6-sol (effort low, 2,000 completion tokens, 3 in flight per server), with economy seed `sybil-rules-180-economy-r1` and markets 319000 to 319059 instead of 318000 to 318059, and fresh fixtures for every model-facing stage: probe 319400 to 319417, ordinary 319420 to 319425, smoke 319430 to 319435, X0 319700 to 319759, D1 319300 to 319311. No 319xxx id is used anywhere else in the repository. Batches `*-002-gpt-6-sol-r1`; worker sessions under hub experiment `sybil-rules-180-gpt-6-sol-r1`; its own ledger `accounting/ledger-gpt-6-sol-r1.jsonl` and results `results-gpt-6-sol-r1` (launcher tag); gates select runs of this model and replication only.
- Question: do A ≈ 0.31 of 180 (0.92 of the 60 dominant owners), B = 0, C = 0 and the D1 gap (neutral 8 of 12, cued 11 of 12) reproduce in an independent economy? Two economies are two observations, not a distribution; no pooled statistic.
- Cost: attempt 002 cost USD 55.41 for 8,118 calls. Same call caps; R1's market parameters are drawn from the same generator, so expect about USD 50 to 65. Cap USD 120; the pre-S1 projection gate (S1 and D1 at X0's mean cost within the remaining cap) applies.
- Time: attempt 002 took 48 minutes; expect 45 to 70 minutes.

- Ledger: R1 starts a fresh ledger (`accounting/ledger-gpt-6-sol-r1.jsonl`, cap USD 120); attempt 002's ledgers stay as they are and are not carried over. READY.yaml declares `ledger: fresh` (added by dmarz/fleet-monitor at launch, 2026-10-04: the launcher refused the chain with `missing_prior_ledger` because the declaration was missing; documents only, source hash unchanged).
## Offline checks at this source hash

- `python3 src/selftest.py`: 90 tests OK, also with `STUDY_MODEL=gpt-6-sol STUDY_REPLICATION=r1` in the environment (the launcher's setup sets them; the tests remove them).
- Offline S0 with `STUDY_MODEL=gpt-6-sol STUDY_REPLICATION=r1`: passed, 8,118 of 8,118 accepted, all invariants and development witnesses true; offline S0 with `STUDY_MODEL=gpt-6-luna`: passed likewise.
- Rehearsal: scenarios i (R1) and j (R2) passed 19 of 19 checks (full chain exit 0; batches tagged; model and replication in every run's params; calls per stage at their caps; worker sessions only in the run's own experiment; 3 in flight; cap 120 or 15 in the ledger; R1 economy on markets 319000+; `chain verify` ok). Full rehearsal a to j: see "Pins".
- Launcher: agentops `41639d0` adds `--replication rN` (READY.yaml `replications:`): own ledger, results and logs, `STUDY_REPLICATION` to the coordinator and workers; 17 launcher tests OK.

## Launch R1 (first)

```sh
H=sim-dmarz-2,sim-dmarz-8,sim-dmarz-10
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> setup  --host $H --model gpt-6-sol --replication r1
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> chain  --host $H --model gpt-6-sol --replication r1 --confirm-paid --source dmarz/<agent>
python3 scripts/run-ready-chain.py sybil-rules-180 <launch commit> status --host $H --model gpt-6-sol --replication r1
```

## Pins

- Code commit `16b6c82ec03e14ae9d261d5b4bba686d8887f574`, source hash `a1371e7c2df0f3ff171726a6da121b03df86e76b7ec8dc320cb8b820a567729e` (READY.yaml names this file and this hash).
- At this source hash, 2026-10-04, macOS, Python 3.9.6, no network, no model call: selftests 90 of 90; offline S0 for R1 and for R2 passed; rehearsal scenarios i and j 19 of 19. Full rehearsal a to j: passed, 75 of 75 checks (a first attempt ran out of disk on this Mac, caused by other processes, and was rerun after freeing space).
