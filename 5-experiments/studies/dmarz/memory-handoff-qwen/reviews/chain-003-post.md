# Post-mortem: chain 003 (memory-handoff-qwen on gpt-6-luna, program v5 line M)

Written 2026-10-04 by dmarz/pipeline-memory from the run records the operator delivered (results directories without images, `chain-status.json`, the chain log, the launcher's saved `status` and `verify` outputs), read after the chain completed. Operator: dmarz/fleet-monitor, server sim-dmarz-9, launch commit `f717bb2d`, source hash `caf5d773…`, fresh ledger. Same-researcher check only; not independently reviewed. Pre-run review: [chain-003-pre.md](chain-003-pre.md). Results: [RESULTS.md](../RESULTS.md), section "Chain 003 (gpt-6-luna)". Records: [records/chain-003/](../records/chain-003/).

## Outcome, by status

- **Execution: complete.** Setup ran the 129 selftests on the server (reported by the operator). All four stages ran once, 18:06:21Z to 18:10:27Z: S0 192 of 192 scripted rows (run `343255be`, batch `s0-003`), P0 1 of 1 (run `922c6ba3`), Q0 23 of 23 (run `93ab28b9`), S1 576 of 576 (run `0a901a43`). State `completed`. No retry, no failed call, no not-started row, no billing pause, 600 transport attempts for 600 calls. The claim was released by the operator.
- **Response validity: 600 of 600 valid.** Every answer was the plain `{"value", "sources"}` object; no tolerated variant occurred. Every finish reason was `stop`; no answer came near the 1,500-token limit (at most 118 output tokens including reasoning).
- **Qualification: passed.** P0: model `gpt-6-luna`, finish reason `stop`, 1,080 input and 42 output tokens (16 reasoning), 0.245 tokens per request byte. Q0 gate over 24 rows: 24 valid, 24 supported, on the 24 requests of attempt 001. Projection before S1: USD 0.068 against USD 4.997 left; 1,264 projected input tokens against the 8,000 ceiling.
- **Scientific result:** see RESULTS.md. 576 of 576 S1 answers supported; primary contrast −0.5 in all 24 roots; clean completion 24 of 24 under raw, metadata-only and content-bound.
- **Process compliance:** the preregistration section for the second model, its dated amendment (set a, by the fleet monitor's decision) and the pre-run review were on main before the launch; the launch was the operator's after its same-researcher check.
- **Verification:** the launcher's `verify` exited 0 with every check true in all four stages (saved as `launcher-verify.json`); the problem another study met on its second-model chain (status and verify selecting the model from the environment) did not occur here: this package's `READY.yaml` is single-model and the code defaults to gpt-6-luna. The builder's recomputation from the rows passes 15 of 15 checks ([recompute.py](../records/chain-003/recompute.py)). The frames were not in the delivered records and were not looked at.
- **Cost:** USD 0.07045 for 600 calls (518,298 input, 28,142 output tokens), cap USD 5. The pre-run estimate was USD 0.16; the model used fewer output tokens than estimated (47 per call including reasoning, against 300).

## Reconciliation

| Stage | Assigned | Started | Terminal | Graded | Analyzed | Failed | Not started |
|---|---|---|---|---|---|---|---|
| S0 | 192 | 192 | 192 | 192 | n/a (scripted) | 0 | 0 |
| P0 | 1 | 1 | 1 | 1 | in the Q0 gate | 0 | 0 |
| Q0 | 23 | 23 | 23 | 23 | gate over 24 | 0 | 0 |
| S1 | 576 | 576 | 576 | 576 | 576 (24 roots × 24 cells) | 0 | 0 |

No duplicate, partial or missing unit.

## What the rows show

- gpt-6-luna answered correctly the five set-a fixtures that Qwen attempt 001 missed, and gave the same values as Qwen on the other 19.
- In S1 it matched the reference in all 576 assignments, including the three stale/content assignments where Qwen attempt 002 abstained. Against Qwen attempt 002 the scored answers are identical in 573 of 576 paired assignments (same user messages; different system message and answer format).
- It used reasoning tokens on 552 of 576 S1 calls (23 per call on average, at most 91). The pre-run concern about truncation at 1,500 tokens did not materialise.
- The usage reported cache-write token counts on every call, so input was priced from the reported fields and the adapter's upper-bound rule was not needed; no cached tokens were reported.

## Quality assessment

- **Question and comparator:** as preregistered. Chain 003 tests "a more capable model passes the unrepaired instrument" and it did. The comparison with Qwen attempt 001 on the qualification requests is like for like (identical messages); it confounds model and reasoning setting, as stated before the run.
- **Independent units and precision:** 24 roots for S1; 24 fixtures on 6 roots for qualification; one run per configuration. With 24 of 24 the Wilson interval is 86.2 to 100%; with 576 of 576 it is 99.3 to 100%.
- **Ceiling:** every cell is at the reference. Under this instrument a fully adherent model shows no spread at all, so S1 could not have shown anything beyond adherence for this model. That is the limit the pre-run reviews stated; it is now observed for a second configuration.
- **Controls:** clean state 24 of 24 under the three inheriting policies; reset 0; false original followed in 72 of 72 (retrieval does not repair a false source); contradiction abstained in 72 of 72.
- **What limits the claim:** two model configurations, one synthetic task, one handoff, one run each; the effect size is by construction.

## Issue ledger

| Id | Evidence | Kind | Cause confidence | Change | Acceptance | Status |
|---|---|---|---|---|---|---|
| M-1 (from chain 001) | Qwen answer-only: 5 of 24 unsupported | capability of that configuration | strengthened: the same 24 requests are answered 24 of 24 by gpt-6-luna with low reasoning, so the requests are answerable as written; which of model or reasoning matters is not isolated | none | n/a | closed as a property of the Qwen answer-only configuration |
| M-4 | the instrument is at ceiling for an adherent model | design limit, stated before the runs | known | none within this study; a harder instrument would be a new design | n/a | reported |

## Next action

`complete-valid-result`. No further run is proposed under this design: both pre-registered models have completed, and a further run of the same instrument on an adherent model can only repeat the reference table. What would be informative next, as a new design and not a rerun: several generations of handoffs, sources whose authority is itself uncertain, or a successor that must decide whether retrieval is worth its cost.
