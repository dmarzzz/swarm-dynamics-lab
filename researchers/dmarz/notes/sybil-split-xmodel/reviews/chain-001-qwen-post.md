# Post-mortem for sybil-split-xmodel, chain 001, qwen/qwen3.7-flash

Status: assessment complete for the Qwen chain, which stopped at its Q0 gate. S1 did not run.

- Study / owner / model: sybil-split-xmodel / dmarz / `qwen/qwen3.7-flash` through OpenRouter, Alibaba only, reasoning disabled.
- Batches: `s0-001-qwen`, `p0-001-qwen`, `q0-001-qwen`.
- Parent: sybil-split-opus chain-001. Assessed 2026-10-04.
- Assessor: dmarz/pipeline-split-qwen, the package's builder. This is the builder's own review. dmarz waived cross-researcher review, and **this run is not independently reviewed**.
- Frozen inputs: [chain-001-pre.md](chain-001-pre.md); launch commit `f673f09b`, code `0ca09f04`, source hash `ebfb2bc3703cbb5ac882641ca0f71dfb9dfda0ee5436dd1a8b4879dcef97c2cd`. The server setup ran the 97 selftests and confirmed the hash. The chain ran on the same server as the gpt-6-sol chain, after it.
- Records: sanitized copies are in [records/](../records/) with the prefix `qwen-`: chain status with server paths redacted, S0, P0 and Q0 summaries, P0 and Q0 rows, and the Q0 assignments. They were scanned and contain no addresses, keys or tokens.
- Review verdict: **diagnostic. Qualification failed on one shape out of six, by abstaining on facts that two unchecked rows support.** This is a valid result under the frozen gate. The thresholds are unchanged, there is no repair (preregistration item 9), and S1 does not run.

| Dimension | Status |
|---|---|
| Execution | complete |
| Response validity | 61 of 61 valid |
| Qualification | failed (`sparse`) |
| Process | the chain stopped itself at the gate |

## Reconcile the recorded facts

| Quantity | Planned | Observed | Evidence |
|---|---|---|---|
| S0 (scripted) | 1,853 rows, 0 calls | 1,853 valid, 0 invariant violations; byte identity with the parent held on the server; 17:51:09Z to 17:57:45Z | qwen-s0-summary.json |
| P0 | 1 call | Passed. Answer exactly right; response model `qwen/qwen3.7-flash`, provider Alibaba, finish `stop`, 0 reasoning tokens; 3,563 input and 33 output tokens; 0.345 tokens per message byte; USD 0.000111 (reported by the provider and equal to the computed cost) | qwen-p0-summary.json |
| Q0 input-ceiling gate | ≤ 31,000 tokens | projected 4,665 tokens for the largest request (13,515 bytes × 0.345), within the ceiling | qwen-chain-status.json |
| Q0 | 60 calls | 60 of 60 structurally valid, 0 failed; gate failed; 199,840 input and 3,127 output tokens; USD 0.006404; 37 s | qwen-q0-summary.json |
| S1 | 2,688 calls | not queued | qwen-chain-status.json |
| Ledger | caps 2,749 calls, USD 3 | 61 calls, 61 transport attempts (no retry, no billing pause), USD 0.006515 settled, nothing open | qwen-chain-status.json |

The parent's Opus 5.5 passed every shape at 1.0 on the same 60 packets. Qwen's results by shape:

| Shape | Exact packets | Field accuracy | Withheld abstention | Passed |
|---|---|---|---|---|
| full | 1.0 | 1.0 | — | yes |
| common_only | 1.0 | 1.0 | 1.0 (30/30) | yes |
| sparse | **0.70** | 0.95 | 1.0 (10/10) | **no**: exact packets need ≥ 0.90 |
| multirow1 | 1.0 | 1.0 | — | yes |
| multirow3 | 1.0 | 1.0 | — | yes |
| multirow9 | 1.0 | 1.0 | — | yes |

## Native trace audit: every miss

All 60 answers were read against their packets. There are **3 missed fields in 3 packets, all in `sparse`, all on skill 3, and all nulls on a fact that two unchecked rows report with the same value**. There are no wrong values. All 40 withheld fields are null.

| Root | Skill | Expected | Rows for the skill | Returned | Output tokens |
|---|---|---|---|---|---|
| community 5145 | 3 | 62 | 2 rows, both 62, both unchecked | null (0-2 and 5 right) | 53 |
| community 5146 | 3 | 60 | 2 rows, both 60, both unchecked | null (0-2 and 4 right) | 53 |
| ring 5142 | 3 | 78 | 2 rows, both 78, both unchecked | null (0-2 and 4 right) | 53 |

Totals over all 320 present fields:

| Field supported by | Right | Null |
|---|---|---|
| a trusted row | 60 | 0 |
| at least one passed row | 216 | 0 |
| unchecked rows only | 41 | 3 |

In `sparse`, each packet has two rare skills with exactly two unchecked specialist rows each. Qwen answered:

| Skill | Answered right |
|---|---|
| 3 | 5 of 8 |
| 4 | 6 of 6 |
| 5 | 6 of 6 |

Every answer finished `stop`, with 0 reasoning tokens and 32 to 65 output tokens, at provider Alibaba.

## What kind of error it is

- **Misread row, wrong plurality:** no. There are no wrong values, and each missed field had a single value in its rows.
- **Answer-shape confusion from the appended paragraph:** no structural effect. All 61 answers had exactly the shape, with no strings, code fences or extra keys.
- **Reasoning cut off:** not applicable. Reasoning is disabled, every answer finished `stop`, and the largest output was 65 of 1,000 tokens.
- **What it is:** abstention on the thinnest evidence in the gate. Two agreeing rows from identities with no passed check, under the parent's warning that repetition is not independent evidence and that null is right when evidence is "too ambiguous".

  The gate counts these fields as answerable. The parent's fixture rule makes every present fact rest on at least two honest single-row identities, and `sparse` holds exactly that minimum. Qwen abstained on 3 of the 20 such fields (15%).

  All three are on skill 3. In `sparse`, skill 3 is the first rare skill listed. Whether the position matters is not established by three cases. This is an observation, not a verified cause.

## Whether any part is an instrument problem introduced by the port

As far as the records show, no.

- The packets were byte-identical to the parent's, as S0 proved on the server.
- The interface worked on every call.
- The miss is the same kind as gpt-6-sol's: a null on an unanchored, unanimous fact. It is much rarer here (3 fields against 25).
- As with gpt-6-sol, I cannot exclude without model calls that the appended answer-shape paragraph ("an integer or null for each skill") nudges toward null. The parent's prompt and schema already permitted null.

The gate itself is the parent's and is strict: one null among 20 two-row fields in `sparse` costs one exact packet, and a shape fails at two misses. Qwen missed three.

## Is a repair justified?

**No repair.** Preregistration item 9 makes a Q0 stop the result. Changing the prompt would break the identical-input premise. There is no reasoning setting to vary on this route: Qwen already runs with reasoning disabled, and the program fixes that.

Qwen's result stands as stated: 5 of 6 shapes perfect, `sparse` failed by 3 abstentions on two-row unchecked facts.

## Closeout and handoff

- Assessment: this file. The replication outcome for all chains is in [RESULTS.md](../RESULTS.md).
- Evidence registry: updated with the observed qualification outcome. Score 0/4, because no S1 contrast exists.
- The chain process exited after the Q0 stop. The claim on the server is the fleet monitor's to manage.
- Next: the pre-registered follow-up configuration of amendment A1 (gpt-6-sol, reasoning_effort none) is the only further run of this study.
