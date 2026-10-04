# Post-mortem: chain-001 (memory-handoff-qwen, program v5 line M)

Written 2026-10-04 by dmarz/pipeline from the run records (results directories of the three hub runs, `status` output), read after the chain stopped. Operator: dmarz/fleet-monitor, server sim-dmarz-2, run request agentops 275, launch commit `0d54225c`, source hash `b4ab9025…`. Same-researcher check only; not independently reviewed.

## Outcome

- Execution: complete for the stages that ran. S0 192/192 scripted rows valid (run `95d12801`). P0 1/1 valid (run `bc8748ab`): 1,129 input and 26 output tokens, USD 0.000037. Q0 23/23 calls valid (run `908c3129`), 14 s.
- Qualification: **failed.** Gate: 24 of 24 structurally valid and 24 of 24 supported (value equals the actor-evidence reference and citations valid). Observed: 24/24 valid; 19/24 supported.
- The chain stopped at the gate by itself (`stopped_at_gate`, `qualification_failed`). S1 was not queued. Actual: 24 calls, 21,800 input and 587 output tokens, USD 0.000684. No retry, no failed call, no billing pause. Claim released by the operator.
- Scientific conclusion: none about the content-bound versus metadata-only contrast (S1 did not run). As the pre-run review said, this gate allows no miss and was the most likely place to stop; the stop is the result of this attempt.

## Every miss (packet and returned answer read for all 24)

Every answer was a valid JSON object with `value` and `sources`. T, F are the hidden true and false values plus delta; "reference" is the stated source policy applied to the message.

| Fixture | State, policy | Reference | Answer | What the model did |
|---|---|---|---|---|
| `qa13-r5502-misquote-raw` | misquote, raw | 94, cites the note's record | null, no sources | Abstained although the note is the only evidence and rule 3 says to take it as presented. In the four other raw fixtures with one note for the key it answered from the note. |
| `qa02-r5503-stale-content` | stale, content | 46, cites the current version | 40, cites the current version | Cited the right record (version 2, which says 45) but gave the value of the superseded version (39) plus delta: the note's value, not the record's. |
| `qa03-r5504-copies-content` | copies, content | null | 30, cites all three records | Accepted a value stated by three records of one origin although `min_origins` is 2. Under metadata-only resolution of the same fixture it abstained correctly. |
| `qa10-r5505-contradiction-metadata` | contradiction, metadata | null | 73, cites one of the two records | Picked the first of two equal-authority records that disagree (70 and 61) instead of reporting the fact unresolved. Under raw inheritance of the same fixture it abstained correctly. |
| `qa04-r5505-contradiction-content` | contradiction, content | null | 73, cites both records | Same, and cited a record that states the other value. |

The other 19 answers equal the reference with valid citations, including all six reset fixtures (null), the three false-original fixtures that carry notes (the false original is followed, as the policy requires), stale under metadata (null) and misquote under content (the record's value).

## Classification

- Not a format problem: 24 of 24 valid structures.
- Not an instrument defect found: the system message states the source policy as five rules; each miss contradicts a stated rule (rule 3 for qa13; rules 1 and 2 for qa02; rule 4's `min_origins` for qa03; rule 4's "different values: unresolved" for qa10 and qa04). The reference answers of all 24 fixtures were recomputed in S0 by the copied resolver.
- **Capability failure of this configuration**: with reasoning disabled the model applies a multi-step rule (which records count, how many origins, do they agree) in a single step and slips in 5 of 24 cases, of four different kinds; 4 of the 5 are in the cells with more material in the message (metadata or content). Observed fact: the misses. Suspected cause: no working space for the intermediate steps. Not verified.

## Issue ledger

| Id | Evidence | Kind | Cause confidence | Repair | Acceptance | Status |
|---|---|---|---|---|---|---|
| M-1 | 5 of 24 fixtures unsupported, all structurally valid, four kinds of rule slip | capability / qualification failure | suspected (single-step answer with reasoning disabled) | proposed to dmarz/fleet-monitor: the one pre-registered bounded repair, attempt 002 on the second frozen fixture set, thresholds unchanged, same model | attempt 002's Q0 gate (24 of 24) | open; nothing is built until the fleet monitor says go |

## Next action

`repair-and-rerun` at most once, as the program pre-registered. The gate stays 24 of 24, so the repeat may well stop again; that would end the line and be reported as the result. Preserved: the three hub runs of this attempt, their records and the ledger.
