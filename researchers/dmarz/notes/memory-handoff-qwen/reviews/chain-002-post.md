# Post-mortem: chain 002 (memory-handoff-qwen attempt 002, program v5 line M)

Written 2026-10-04 by dmarz/pipeline-memory from the run records that the operator delivered (results directories of the four hub runs without images, `chain-status.json`, the chain log), read after the chain completed. Operator: dmarz/fleet-monitor, server sim-dmarz-13, launch commit `5831e534`, source hash `10f51d2c…`, fresh ledger. Same-researcher check only; not independently reviewed. Pre-run review: [chain-002-pre.md](chain-002-pre.md). Results: [RESULTS.md](../RESULTS.md). Records: [records/attempt-002/](../records/attempt-002/).

## Outcome, by status

- **Execution: complete.** All four stages ran once, 12:40:28Z to 12:44:57Z: S0 192 of 192 scripted rows (run `6e5badb7`), P0 1 of 1 (run `94e45249`), Q0 23 of 23 (run `43926309`), S1 576 of 576 (run `5a6fec17`). The chain exited with state `completed`. No retry, no failed call, no not-started row, no billing pause, 600 transport attempts for 600 calls. The claim was released by the operator.
- **Response validity: 600 of 600 valid.** Every answer was one JSON object with well-formed working fields before `value`; none needed a tolerated variant.
- **Qualification: passed.** P0: model `qwen/qwen3.7-flash`, provider Alibaba, finish reason `stop`, 0 reasoning tokens, 1,665 input and 171 output tokens, 0.261 tokens per request byte. Q0 gate over 24 rows: 24 valid, 24 supported. Projection before S1: USD 0.0250 against USD 1.999 left; 1,670 projected input tokens against the 8,000 ceiling.
- **Scientific result:** see RESULTS.md. Primary contrast −0.5 in all 24 roots; 573 of 576 S1 answers supported; clean-memory completion 24 of 24 under raw, metadata-only and content-bound.
- **Process compliance:** the preregistration section "Attempt 002" and the pre-run review were on main before the launch; the launch was the operator's after the fleet monitor's same-researcher check; nothing was retuned between attempts except what the preregistered repair states.
- **Reporting:** records and the recomputation are committed. The frames, `replay.gif` and `replay.html` exist on the hub and on the server; they are not in the delivered records and were not looked at for this post-mortem.
- **Cost:** USD 0.026099 settled for 600 calls (744,884 input, 54,401 output tokens), cap USD 2. The pre-run estimate was USD 0.043; the model wrote fewer output tokens than estimated (91 per call against 250).

## Reconciliation

| Stage | Assigned | Started | Terminal | Graded | Analyzed | Failed | Not started |
|---|---|---|---|---|---|---|---|
| S0 | 192 | 192 | 192 | 192 | n/a (scripted) | 0 | 0 |
| P0 | 1 | 1 | 1 | 1 | in the Q0 gate | 0 | 0 |
| Q0 | 23 | 23 | 23 | 23 | gate over 24 | 0 | 0 |
| S1 | 576 | 576 | 576 | 576 | 576 (24 roots × 24 cells) | 0 | 0 |

No duplicate, partial or missing unit; no missingness bound was needed. Recomputed by the builder from the saved rows with [recompute.py](../records/attempt-002/recompute.py) against the package at the launch commit: 15 of 15 checks pass (saved analysis equals the recomputed one; every answer regrades to its saved evaluation, reference and working-field report; every packet regenerates and the digests equal the manifest; the journals' hash chains are intact; the gate recomputes). Not checked by the builder: hub artifact checksums (the launcher's `verify`) and the visual artifacts against the metrics.

## What the rows show

- The three unsupported answers of S1 are all stale-version under content-bound retrieval (roots 5402, 5409, 5421): the successor listed only the superseded record, left out the current version that was in its message, and abstained. Three more answers in the same cell (roots 5413, 5414, 5420) made the same incomplete listing and still gave the current record's value with a valid citation. So in 6 of 24 stale/content assignments the working fields missed the current version; in none did the successor repeat the stale value.
- The model's `counting_values` and `distinct_origins` fields disagree with its own listing in 41 and 23 of 576 rows, almost all in the copies state; the scored answers there are all supported. The working fields helped (or at least did not hurt) the scored answer while being unreliable as bookkeeping.
- 72 messages were sent more than once by construction; the scored answer never differed between repeats. With this model and format the answers were stable across repeats in this run.

## Quality assessment

- **Question and comparator:** as preregistered. The primary came out at the reference value in every root. As the preregistration and both pre-run reviews said, that value follows from adherence; the measured quantity is adherence (99.5%, 573 of 576) and where it broke (one cell).
- **Independent units and precision:** 24 roots. The intervals on the primary have no width because there is no variation; the informative uncertainty is on the cell rates (for 24 of 24: Wilson 86.2 to 100%; for 21 of 24: 69.0 to 95.7%).
- **Controls:** clean state at 24 of 24 under the three inheriting policies; reset at 0; false original followed in 72 of 72 (the adverse control: retrieval does not repair a false source); contradiction abstained in 72 of 72.
- **Manipulation fidelity and truth separation:** the packets regenerate from the frozen code and equal the manifest; the invariants and the wire-level test are those of the pre-run review. No answer contained a value that the message did not carry (0 "other wrong" in 576).
- **What limits the claim:** one model configuration; one synthetic task; one handoff; the qualification passed on the second attempt, on other fixtures; the effect size is by construction.
- **Attempt 001 against attempt 002:** 19 of 24 (answer only, set a) and 24 of 24 (working fields, set b). Different fixtures, one run each, not paired. S1's adherence of 99.5% makes a 24 of 24 pass likely (about 88%) under the new format, so the pass is not a fluke of a marginal configuration; whether the old format would have reached a similar rate on set b was not measured. The gpt-6-luna chain (chain 003) will answer set a in the old format with another model; a Qwen run of the old format on set b is not planned (the program allows no further Qwen attempt).

## Issue ledger

| Id | Evidence | Kind | Cause confidence | Change | Acceptance | Status |
|---|---|---|---|---|---|---|
| M-1 (from chain 001) | attempt 001: 5 of 24 unsupported | capability / qualification failure | suspected: one-step answer without working space | attempt 002: working fields | Q0 24 of 24 | closed for this configuration: Q0 passed; cause still not isolated (fixtures differ) |
| M-2 | 6 of 24 stale/content listings omit the current version; 3 of them abstain | adherence slip in one cell | observed; cause not investigated | none: a valid result of S1, reported | n/a | reported, no repair |
| M-3 | evidence block in README said "Prospective plan only" after the run | reporting | known: the evidence script was failing on another study's row when the package was pinned | registry row and blocks updated with this post-mortem | `experiment_evidence.py --check` valid | closed |

## Next action

`complete-valid-result` for the Qwen line: attempt 002 is the one permitted repair and it completed; no further Qwen attempt exists or is proposed. Separately preregistered and not yet run: chain 003 on `gpt-6-luna` (original answer format, set a), which is its own chain and is never pooled with these rows.
