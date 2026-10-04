# Independent pre-launch review of factory provenance attempt 2

**Verdict: BLOCK. Not launch-ready under HANDOFF.md.**

- Reviewed PR [#107](https://github.com/dmarzzz/swarm-lab/pull/107), head `3eb852faf8a940027230ab46315854a01cccb567`; implementation revision `bb9fa715294cc79bb621e4ecfa5e3ab68444527b`.
- Reviewer: separate Sol review agent, session `be6113f8-501d-445a-b79c-df5edbc2390b`, 2026-10-04. I did not author the successor implementation or historical experiment. This is independent execution/code inspection by another agent, not an independent human replication or independently authored historical checker.
- Main-based review worktree: `factory-provenance-review`; detached, read/test-only PR worktree: `factory-provenance-review-source`.
- **Zero model requests, zero experiment launches, zero experimental ledger writes.** All additional dispatch exercises used temporary fixtures, dummy credentials, and mocked HTTP transports. No `prepare` or experimental `run` CLI was invoked.
- Read HANDOFF, SPEC, PRE-RUN, SETUP, HISTORICAL-REVIEW, all seven successor Python source/test files, and the attempt-1 SPEC, POSTMORTEM, admission, assignments, initialization/outcome records, call/paid ledgers, checker, and factory PI review/handoff.

All file/line references below are relative to `5-experiments/studies/shadow/factory/provenance/attempt2/` at the reviewed PR head unless otherwise specified.

## Blocking findings

### R1, high: direct dispatch bypasses the mandatory stop and frozen order

**`run.py:92-116,143-149,225-227,257-273`.**

The advertised shared boundary validates membership in the assignment set, existing terminal/init files, and the main qualification gate. It does **not** validate that this is the next frozen assignment, that all preceding assignments finished successfully, or that a preceding response already required termination. The stop-on-failure and fixed-order policies exist only in `execute_cohort`, outside that boundary. `dispatch` writes a failed outcome and returns without latching the cohort stopped.

Reproduced using the existing `test_pilot.Tests` temporary fixtures and mocked `urllib.request.build_opener`:

1. Directly dispatch Q0 with a mocked HTTP400, then Q1 with a valid mocked response. Result: `http_400`, then `completed`; **two transports**. The first contract failure did not end the attempt at its shared boundary.
2. On a fresh fixture, directly dispatch Q5 first. Result: `Q-05-ancestry-01 completed`, despite Q0 being first in the frozen schedule.
3. Complete the six qualification fixtures, dispatch the first main cell with HTTP400, then the next main cell with a valid fixture. Result: `http_400`, then `completed`; **eight transports total**. Main failure can likewise be bypassed.

The normal CLI loop stops correctly, and this bypass does not defeat the 149-request or dollar reservation caps. It nevertheless violates the frozen stop rule and permits outcome-dependent selection/order through the exact direct-call entry point the prior PI acceptance checklist requires to be safe. No code or admission mutation was necessary.

**Required before admission:** under the shared request lock, enforce the next frozen assignment and reject any predecessor failure, wrong qualification, incomplete/ambiguous initialization, or stopped cohort before credentials/reservations/transport. Preserve the failed row and make the stop durable. Add direct-call regression tests for all three cases, including the first call after a failed/invalid/wrong qualification and after a main failure. Run them normally and under `-O`.

### R2, medium: the reporting freeze is incomplete and not enforced at closeout

**`run.py:26,39,53-56,94-95`; `closeout.py:16-52,55-56,64-102`; `analyze.py:65-89`; `recompute.py:24-25,118-123`.**

`closeout.py` is committed prospectively but absent from `SOURCES`, so it is not included in admission's source hashes or the runtime drift check. It chooses the public finding wording, evidence score and figure. Additionally, saved-data `analyze.report`, `recompute.check`, and `closeout.main` do not verify the admitted source hashes before deriving/writing results. The checker verifies assignment/outcome digests, not the reporting implementation against the prospective admission.

The numeric contrast formulas I inspected are fixed and reasonable; this is **not evidence that anyone changed the analysis after seeing data**. It is a concrete hole in the claimed freeze: reporting code can drift after the final request without this workflow refusing or identifying the result as a revised analysis. HANDOFF says all runtime source must be frozen and the setup says the scientific/checker files are pinned.

**Required before admission:** include `closeout.py` in the source manifest and make the saved-data closeout/check path verify its frozen scientific/reporting/checker sources before emitting a success receipt. Test drift after simulated data collection, not just drift before dispatch. Any later narrative-only amendments should be identified as such, not silently represented as the admitted implementation.

## Checks that passed

### Prospective plan and untouched attempt 1

- `e080d613f6e5db6c5dab0a972b9f3b1df1774d82`, **19:50:25Z**, added only SPEC, PRE-RUN and HISTORICAL-REVIEW. It is an ancestor of the implementation commit `7041ed5bf27d6e911dd3ccb79be8b072852d70dd`, **19:53:50Z**. The plan therefore precedes successor code. Source corrections followed at `bb9fa715`, **20:00:55Z**.
- No attempt-2 admission, assignments, initialized calls, outcomes or terminal records exist in the reviewed PR. The separately committed main-branch FINDING is a blocked report, not an outcome.
- The PR's changes are confined to attempt2. Diffing from the parent of the preregistration through the reviewed head, excluding attempt2, produces **zero changes** under provenance. Historical pins, records and terminal objects were not rewritten.
- Fresh qualification seed is `202610040604`, versus attempt-1 OpenRouter `202610040602`. The supplied test compares all 144 main assignments to their historical counterparts and passes. Keeping the unobserved main roots is honestly documented, not a new replication.

### Routing, errors, qualification and durability

- `run.py:100` rejects pool dispatch before credential access; `run.py:280` calls OpenRouter only. The retained pool body/key/transport branches are dead behind this admission check, not a reachable fallback. Removing them would simplify future audits but is not itself a blocker.
- OpenRouter body fixes the model, Anthropic provider order, `allow_fallbacks=False`, required parameters and price ceiling (`run.py:126-136`). Redirects are rejected (`139-140`); there is no HTTP retry loop. The normal cohort loop stops on HTTP400, availability failure, schema failure and wrong qualification.
- Strict local answer bounds remain enforced while unsupported numeric wire bounds are absent (`instrument.py:14-15,108-130`). Main dispatch requires all six fresh correct qualification records, scoring, model and effective-config linkage (`run.py:105-115`).
- Initialization and outcome objects use fsynced temporary files plus atomic create-only hard links (`durable.py:18-31`). Duplicate assignment dispatch and outcome overwrite tests pass. Existing cohorts are closeout-only through the normal runner; unknown reservation liability survives interrupted closeout. The bypass in R1 concerns choosing another assignment, not overwriting an existing one.

### Original ledger and exact remaining allocation

- Independently folded the original paid ledger with `decimal.Decimal`: **USD1.851345**, from **129 reservations, 120 settlements, 9 unresolved reservations**. Attempt-1's unresolved reservation is **USD0.044376**; no refused request was assumed free.
- `run.py:25` resolves to the existing factory `results/paid-ledger.jsonl`, not an attempt2-local ledger. `durable.py:71-87` locks that ledger inode, reserves before transport, enforces **USD9** for the attempt and **USD10.851345** factory-wide, and retains unknowns. The concurrent final-reservation test passes.
- Historical provenance call ledger has exactly **2** requests. Original ceiling **151 - 2 = 149** new requests. The supplied full-success mock executes **149**, preserves **150** assigned outcomes, and leaves **1** not-run.
- Thus **6 qualification + 143/144 main cells**, at most **11/12 completely observed roots**. The omitted final frozen cell is **`M-11-padding-16`**. Raw16-minus1 pairs can still cover all 12 roots. This is not permission to complete the final padding cell.
- Recomputed sum of the first 149 conservative reservation envelopes: **USD6.561000**, below USD9 even if all costs remain unresolved. Cap constants are enforced without CLI budget/model overrides. No silent 150th successor call was found in the normal loop or shared call-count guard.

### Analysis inspected

- Root-level paired contrasts, a fixed seed and 10,000 whole-root bootstrap draws, intervals withheld below 10 complete paired roots, explicit all-12-root missingness bounds, and difference-in-differences bounds of [-2,+2] are implemented in `analyze.py:15-49` and independently reconstructed by the saved-data checker.
- No data-dependent root replacement, endpoint selection, bootstrap seed choice, or favorable-result retry occurs in the inspected normal workflow. Raw observations remain dependent cells of 12 numeric roots in one grammar. The analysis-freeze problem is R2, not an observed favorable-result selection.

## Validation receipts

Executed from the detached PR worktree's attempt2 directory:

```text
/tmp/factory-provenance-venv/bin/python -m unittest -v test_pilot
Ran 16 tests in 5.707s: OK

/tmp/factory-provenance-venv/bin/python -O -m unittest -v test_pilot
Ran 16 tests in 5.758s: OK
```

The three additional adversarial direct-dispatch probes above were executed separately using `Tests.setUpClass()`, `Tests().setUp()`, mocked opener responses and `doCleanups()`. They exposed behavior not covered by the 16 supplied tests. They made no real HTTP/model request.

Ran the historical standard-library checker with its `base` argument pointing at a **temporary copy of historical result artifacts**, because it rewrites `recomputation.json`. The checker still read the original paid ledger read-only. Result: **2,026 checks pass; initialized=2; valid=0; factory liability=1.851345; attempt-1 liability=0.044376**. Original historical files were not modified.

Also independently inspected the two saved requests/outcomes: pool confidence schema includes unsupported `minimum`/`maximum`, its response is HTTP400; OpenRouter is HTTP403. Both served models are unknown. No saved provider error body establishes the exact reason for either refusal. This confirms the post-mortem's carefully bounded diagnosis, not a competence result. All 144 scientific main cells remain missing in attempt 1; its 300 terminal assignments are two conditional route plans, not 300 calls.

## Additional operational cautions, not separate launch blockers

1. **Admission publication is currently procedural, not checked at dispatch.** `run.py:85-87` creates admission/assignments; `92-104,276-280` checks their local hashes but does not prove those files were committed/pushed. Follow HANDOFF steps 3-4 literally. A future hardening test should ensure locally prepared but unpublished admission cannot dispatch.
2. **Preserve the actual historical ledger and execution checkout.** `durable.py:35-37,97-100` can create a missing ledger or report zero if it is absent; `prepare` records the prior amount but does not assert the USD1.851345 historical baseline. The inspected ledger is present and correct. Do not launch from another worktree with a stale/missing copy or concurrent independent ledger inode. A fail-closed baseline/prefix check would strengthen the guarantee.
3. `analyze.py:87` retains stale wording about conditional fallback assignments, although this successor has only one route. Remove that misleading report text prospectively. `closeout.py:103-104` also assumes `calls.jsonl` exists, so a prepared-but-never-dispatched closeout can fail while building the inventory. Include a zero-dispatch closeout fixture when hardening reporting.
4. Public status is still blocked/incomplete; code review is not fresh model qualification or review of future scientific results. Hub terminal publication, evidence registry and final report steps remain operator obligations as HANDOFF explains.

## Release decision

This review **satisfies the requested separate-agent historical inspection**, and confirms that the prospective plan, normal-path routing, stated monetary allowance, exact request arithmetic and preserved historical evidence are materially correct. It **does not approve dispatch** at the reviewed revision.

Fix R1 and R2 offline, commit and push the fixes prospectively, obtain a separate-agent readback of those changes, then perform the remaining HANDOFF admission/publication steps and fresh six-case gate. Do not launch, silently enlarge the request allowance, change old outcomes, or claim an independently checked scientific contrast on the strength of this review.
