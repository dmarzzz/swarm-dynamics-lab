# Post-mortem for sybil-split-xmodel, amendment A1: gpt-6-sol at reasoning effort none

- **Study and stages.** sybil-split-xmodel, owner dmarz. Configuration `gpt-6-sol/r1` (amendment A1, preregistration item 13), batches `s0-001-solnone`, `p0-001-solnone`, `q0-001-solnone`.
- **Assessment.** Assessed 2026-10-04 by dmarz/pipeline-split-qwen, the package's builder. This is the builder's own review. dmarz waived cross-researcher review, and **this run is not independently reviewed**.
- **Inputs.**
  - Pre-run assessment: the A1 section of [chain-001-pre.md](chain-001-pre.md).
  - Launch commit `8f70000865fa7e1e8fc28933aeacf190303bed1b`, code `52139693`, source hash `5ce08e7d0e09232f610b28f63ef57f1d48dda04ebbf1e72aac40c0da48af3d1b`.
  - Launched 18:39Z on sim-test-01 with `--model gpt-6-sol --replication r1`. Setup ran 100 selftests, all OK. Launcher `verify` exited 0.
  - The fleet monitor released the claim after the run.
- **Records.** Sanitized copies are in [records/](../records/) under `solnone-*`: chain status with server paths redacted, S0/P0/Q0 summaries, P0 and Q0 rows, and the Q0 assignments. They were scanned and contain no addresses, keys or tokens.
- **Verdict.** Diagnostic. Qualification failed (3 of 6 shapes). This was the one pre-registered follow-up, and **its stop ends the gpt-6-sol route and the study**. S1 was not run.

## Reconcile

| Stage | Outcome |
|---|---|
| S0 | 1,853 of 1,853 valid, 0 calls; byte identity with the parent held. 18:39:53Z to 18:46:44Z |
| P0 | 1 call, passed. Answer exact; response model `gpt-6-sol`; finish `stop`; 0 reasoning tokens; 3,228 input and 33 output tokens; USD 0.008399 |
| Q0 | 60 calls, 60 of 60 valid, 0 failed, `gate_failed`. USD 0.47249; 18:46:48Z to 18:47:28Z |
| S1 | not queued |
| Ledger | 61 calls, 61 transport attempts; no retries, no billing pause; USD 0.480889; 184,328 input and 2,013 output tokens; nothing open |

The request carried no sampling parameter. All 61 responses reported 0 reasoning tokens and finished `stop`. Every Q0 answer used exactly 33 output tokens.

## Every Q0 miss

| Shape | Exact packets | Field accuracy | Passed |
|---|---|---|---|
| full | 0.4 | 0.85 | no |
| common_only | 1.0 | 1.0 | yes |
| sparse | 0.4 | 0.83 | no |
| multirow1 | 1.0 | 1.0 | yes |
| multirow3 | 0.7 | 0.85 | no |
| multirow9 | 1.0 | 1.0 | yes |

There are **28 missed fields in 15 packets. Every one is a null on a present fact whose rows all agree, and none is backed by a trusted row.** There are 0 wrong values, and all 40 withheld fields came back null.

The misses by shape:

| Shape | Missed fields | Rows per missed fact |
|---|---|---|
| full | 9 | 18 agreeing rows, 0 to 2 of them passed |
| multirow3 | 9 (3 packets × 3 rare skills) | 11 agreeing rows, mostly unchecked |
| sparse | 10 | 2 agreeing rows, unchecked |

All 60 answers were read against their packets. The per-field list can be regenerated from `solnone-q0-episodes.jsonl.gz` and `solnone-q0-assignments.jsonl.gz`.

| Field supported by | Right | Null |
|---|---|---|
| a trusted row | 60 | 0 |
| at least one passed row | 211 | 5 |
| unchecked rows only | 21 | **23** |

## The three configurations on the same 60 packets

| | gpt-6-sol, effort low | gpt-6-sol, effort none | Qwen3.7 Flash, no reasoning |
|---|---|---|---|
| Shapes passed | 3 of 6 | 3 of 6 | 5 of 6 |
| Missed fields (of 320 present) | 25 in 12 packets | 28 in 15 packets | 3 in 3 packets |
| Wrong values | 0 | 0 | 0 |
| Null where only unchecked rows | 10 of 44 | 23 of 44 | 3 of 44 |
| Null where a passed row exists | 15 of 216 | 5 of 216 | 0 of 216 |
| Null where a trusted row exists | 0 of 60 | 0 of 60 | 0 of 60 |
| Reasoning tokens | 0 to 373 (mean 75) | 0 | 0 |

Missed fields shared between configurations:

| Pair | Shared missed fields |
|---|---|
| effort low and effort none | 11 |
| Qwen and effort none | 3 (all of Qwen's) |
| Qwen and effort low | 1 |
| All three | 1 |

The three configurations miss 42 distinct fields in total.

**Removing reasoning did not remove the abstention; it shifted it.** With effort none, gpt-6-sol abstains far more on facts that only unchecked identities report (52%, against 23% at effort low). It abstains less where at least one passed check exists (5 fields against 15). The pre-registered rationale, that the low-effort misses came with more reasoning, is therefore not borne out as a cause. The same tendency appears without any reasoning. This is an observation; no discriminating call was made.

## Port and instrument

There is no structural problem: 61 of 61 answers had the exact shape, and none was truncated. What remains open, as for the earlier chains, is whether the answer-shape paragraph's "integer or null" wording contributes. It cannot be settled without calls, and none is planned.

## Closeout

- **Result:** three configurations tried; none passed the clean qualification that Opus 5.5 passed on the same packets, and no S1 comparison exists. See [RESULTS.md](../RESULTS.md).
- **No further attempt.** A1 was the single pre-registered follow-up, and a second gpt-6-sol stop ends that route. No threshold is revisited, and the prompt is not changed.
- **Not tested:**
  - any reasoning effort above low;
  - any prompt variant, including one without the shape paragraph;
  - JSON-schema mode on the OpenAI route;
  - other models;
  - S1 behaviour of these models, which could only be observed past the gate.
- **Spend.** USD 0.480889 for this configuration. The study total is USD 1.017073: effort low 0.529669, Qwen 0.006515, effort none 0.480889. No reservation is open.
- **Workers and claim.** The chain is not active (launcher status). The claim has been released by the fleet monitor.
