# Post-mortem: i0-001

- Experiment / owner / stage / date: market-split-opus; dmarz/market-split-opus; I0 action mechanics; 2026-10-04, 08:01-08:02 UTC.
- Pre-run assessment: [i0-001-pre](i0-001-pre.md) and [phase2-pre](phase2-pre.md); parent `s0-fleet-002`. Commit `b097331b874f2dcab2b31a830e54cdc39f9d321d`; engine `56c67cd0…c047b`; design `8d952af0…a687d`; model `claude-opus-5-5`, adaptive thinking, effort medium, 8,192 output ceiling.
- Run id: `market-split-opus/i0-001`. Artifacts `calls.jsonl`, `summary.json`, `final_frame.png`.
- Disposition: advance to Q0. These were the first model calls of the study.

## What ran and what happened

- 6 calls planned, 6 attempted, 6 priced, 6 passed: every response used the mandated operation and passed the unchanged validator. No retry, no unpriced call, every stop reason `end_turn`, served model equal to the pinned id.
- Usage: 9,173 input and 1,215 output tokens; USD 0.060992. Per call 1,529 input and 203 output tokens (largest response 267). Latency 3.5 to 5.1 s.

| Task | Firms before | Mandated | Returned quantities (A, B per firm) | Per-firm capacity | Output tokens |
|---|---|---|---|---|---|
| 102 | 1 | register | (15.25, 17) ×2 | (24, 22) | 161 |
| 103 | 2 | register | (11, 10), (11, 10), (11.5, 9.5) | (16, 14.67) | 231 |
| 104 | 3 | register | (8.625, 8) ×4 | (12, 11) | 191 |
| 105 | 2 | consolidate | (33, 33) | (48, 44) | 133 |
| 106 | 3 | maintain | (11, 10), (11, 10), (10, 10) | (16, 14.67) | 267 |
| 107 | 4 | consolidate | (11, 11), (11, 10), (10, 10) | (16, 14.67) | 232 |

- Expected versus observed: the request shape was accepted on the first call, which closes issue O1. The pilot's unmodified probe wording was followed in all six cases; the risk that the model would prefer a more profitable operation than the mandated one, as Haiku V1 did, did not occur. Quantities were below capacity and near a best response in every case, as the notes say.
- Observation for the later stages: output per call is about a third of the Sonnet pilot's probe (203 against 569 tokens, before allowing for a tokenizer that counts more tokens). At effort medium this model spends few tokens on thinking for this task. Input per call is 1.37 times the pilot's (1,529 against 1,116), in line with the tokenizer difference.

## Visualization review

Static 1800×1000 table, inspected: six rows with task, starting firm count, requested operation, status and returned quantities, "6/6 valid | 6 calls | $0.060992", and the line "Mandated mechanics only. Not natural-discovery evidence." Quantities are rounded for display only (15.25 shows as 15.2). No animation: six independent one-action fixtures have no time dimension. The three artifacts match the hub by SHA-256.

## Experiment-quality assessment

- This establishes that the model can execute each legal operation with legal quantities through this interface. It is not evidence about profit competence or discovery: the operation was mandated.
- The mandate field appears only in these six stateless calls. Nothing from them enters Q0 or S1 contexts.
- Evidence metadata unchanged in substance: no discovery outcome observed.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
|---|---|---|---|---|---|
| O1 design | Six requests accepted, priced and terminal from `claude-opus-5-5` | Settings follow the model's rules | none needed | First I0 call accepted | Closed |

## Next run

`q0-001`: tasks 100/101, 32 calls, unchanged 75% floor. Launched immediately after this gate passed, as the reviewer directed.
