# Post-mortem: sybil-scarcity-xmodel, Qwen chain (qwen/qwen3.7-flash, chain-001)

Status: scientific review complete for this chain by its builder; not independently reviewed (dmarz waived cross-researcher review for these exploratory runs; dmarz/fleet-monitor's check is a same-researcher check).

- Study / owner / stage / attempt: sybil-scarcity-xmodel / dmarz / Qwen chain S0, P0, Q0 (S1 never queued) / batches `s0-001-qwen`, `p0-001-qwen`, `q0-001-qwen`, hub experiment `sybil-scarcity-xmodel-qwen`; launched 2026-10-04 at about 17:30Z by dmarz/fleet-monitor on sim-dmarz-13, launch commit c0537bf7, code commit 2753b03d, source hash `06cbd97e…`.
- Assessor and scope: dmarz/pipeline-scarcity-qwen (the builder), from the server records fetched by the fleet monitor; every Q0 row was regraded locally.
- Pre-run assessment: [chain-001-pre.md](chain-001-pre.md). Records kept here: [records/](../records/) (`qwen-*`: chain status, S0/P0/Q0 summaries, P0 and Q0 rows). Scanned before commit: no key, token, address or hub URL; directory paths on the server only.
- **Verdict: complete_valid_result for this model's route — a qualification stop.** Execution: valid (0 failed calls). Response validity: 49/49 valid structures, 0 normalized. Qualification: **failed** (carrier profile 1 below both thresholds). Scientific conclusion: the comparison on S1 does not exist for Qwen; as pre-registered (item 8), the stop is the result and is not repaired or retuned. Process: compliant. Artifacts: rows and summaries retained.

## Reconcile the recorded facts

| Quantity | Planned | Observed | Missing / uncertain | Evidence |
|---|---|---|---|---|
| S0 scripted rows | 168 | 168 valid, 0 violations, gate passed | none | `records/qwen-s0-summary.json` |
| P0 calls | 1 | 1 valid, interface passed, answer exact | none | `records/qwen-p0-summary.json` |
| Q0 calls | 48 | 48 valid, 0 failed, gate failed | none | `records/qwen-q0-summary.json`, `qwen-q0-episodes.jsonl.gz` |
| S1 calls | 1,440 | 0 (never queued, by the gate) | the whole comparison | `records/qwen-chain-status.json` (`stopped_at_gate`, Q0, `gate_failed`) |
| Tokens | — | P0: 20,503 in / 33 out; Q0: 983,490 in / 2,413 out; 0 reasoning tokens | none | summaries |
| Spend | cap USD 4 | USD 0.000619 + USD 0.029249 = USD 0.0299 | none | summaries, ledger `ledger-qwen.jsonl` (49 calls) |

- Regrading: all 48 Q0 rows regraded by `study.evaluate` at the pinned code give identical evaluations; assignment ids equal the manifest's Q0 list; every packet hash recomputes. The gate recomputes as failed.

## Input ceiling

P0 measured **0.359 tokens per byte** (20,503 tokens for a 57,092-byte request); Q0's largest was 0.359 as well. Projected largest Q0 request: 20,500 tokens, and S1's largest (57,169 bytes) would be about 20,530: about two thirds of the 31,000-token ceiling, inside the under-32,000 price tier. The ceiling was not the problem; my pre-run worry (0.54 tokens per byte needed) was unfounded for these packets.

## Q0 by carrier profile (the parent's thresholds: field accuracy ≥ 0.95, exact packets ≥ 0.90, null on every withheld fact)

| Carriers | Valid | Field accuracy | Exact packets | Null on withheld | Passes |
|---|---|---|---|---|---|
| 1 | 16/16 | 90/96 = **0.9375** | 13/16 = **0.8125** | 8/8 | **no** (both thresholds) |
| 9 | 16/16 | 95/96 = 0.9896 | 15/16 = 0.9375 | 8/8 | yes |
| 81 | 16/16 | 96/96 = 1.0 | 16/16 | 8/8 | yes |

For comparison, Opus 5.5 scored 16/16 exact in every profile on the same 48 packets (parent `records/q0-summary.json`).

## Every miss (4 packets, 7 fields)

Clean packets: every report is truthful and no attacker exists; badges are `unchecked` for all 23,274 reports except the 54 `trusted` anchors (no audit in Q0).

| Packet (root, carriers, withheld) | Skill | Expected | Returned | Reports of that skill in the packet | Reading |
|---|---|---|---|---|---|
| 7907, 1, skill 4 withheld | 3 | 42 | null | 1 (`unchecked`, 42) | abstention on a single unchecked report |
| 7905, 1, none | 3 | 89 | 85 | 1 (`unchecked`, 89) | wrong value: 85 is skill 0's value, reported 158 times |
| 7905, 1, none | 5 | 89 | 12 | 1 (`unchecked`, 89) | wrong value: 12 appears in no report |
| 7903, 1, none | 3, 4, 5 | 36, 19, 14 | null, null, null | 1 each (`unchecked`) | abstention on all three single unchecked reports |
| 7901, 9, none | 3 | 56 | null | 9 (`unchecked`, all 56) | abstention despite nine agreeing reports |

- Failure type: **not shape** (49/49 valid JSON of the right shape, nothing normalized). Of 7 missed fields, **5 are abstentions on present facts** (4 on single unchecked reports, 1 on nine agreeing unchecked reports) and **2 are wrong values** in one packet (one copied from another skill's majority value, one not present anywhere). All 24 withheld facts were correctly null.
- Single-report rare fields across Q0: 40, of which 34 answered correctly (85%); the misses concentrate in the 1-carrier profile, as expected for the hardest profile.
- Interpretation (inferred, not tested): with reasoning disabled, a 486-row packet with one row for a skill sometimes leads the model to treat the lone row as insufficient evidence ("too ambiguous", in the prompt's words) or to lose track of it; the two invented values in packet 7905 suggest the row was not found at all. The same model qualified 24/24 on trust-credit's 162-row compact packets, so packet length (486 rows, about 20,500 tokens in a verbose key-per-field format) is a likely factor; this run cannot separate length from format.

## Interpret the result

- Primary contrast: not estimable for qwen/qwen3.7-flash; S1 did not run. No claim about whether Qwen collapses at one carrier on attacked packets.
- What the run does show: on clean packets, qwen/qwen3.7-flash without reasoning already loses 3 of 16 one-carrier packets (and 1 of 16 nine-carrier packets) where Opus 5.5 lost none. Its S1 accuracy at low carrier counts would have mixed scarcity under attack with this baseline difficulty in reading single reports; the gate exists to stop exactly that confound.
- Deviations: none. No repair, no retuning, thresholds unchanged.
- Context from tonight (relayed by dmarz/fleet-monitor): gpt-6-sol failed sybil-split-xmodel's qualification on wrong values in present facts while abstaining perfectly. The Qwen misses here are mostly the opposite kind (abstention on present facts). The gpt-6-sol chain of this study launched at 17:54Z (pin 1e56c70e); its Q0 will be read the same way.

## Assess experiment quality

| Item | Status | Evidence / next action |
|---|---|---|
| Inputs identical to the parent | pass | S0 byte-identity checks; Q0 ids and hashes equal the manifest (which equals the parent's) |
| Clean competence gate | pass (worked as designed) | stopped S1 on a pre-registered threshold |
| Response validity | pass | 49/49 valid, 0 normalized, 0 failed calls |
| Budget | pass | USD 0.03 of USD 4 |
| Visual artifacts | unknown | hub frames not inspected in this review; the chain status and summaries are complete |
| Next run | not planned | a Qwen repair (reasoning on, or a compact packet) would change the model configuration or the packets and so leave the replication; any such run is a new study needing the owner's decision |
