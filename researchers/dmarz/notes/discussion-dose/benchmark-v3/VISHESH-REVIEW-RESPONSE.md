# Response to Vishesh's discussion-dose review

Author: dmarz/discussion-bench-v3, 2026-10-04 UTC. The user requested implementation of the fixes in [Vishesh's independent retrospective review](../../../../vishesh/notes/independent-reviews-2026-10-04/discussion-dose.md).

**The successor now passes the review's software acceptance checks. This is an author repair report, not independent approval of v3.** The reviewed original pilot is retired. Its code, saved results and the reviewer-owned report are unchanged; reproduce that historical review at its recorded revision. These repairs apply to the current `bench_v3` package.

Runtime: `d76146b` (including initial guards committed by the shared clone's sync in `e657f8e`). [Exact source hashes and validation](review-fixes-validation.json) identify the patched files. The original [release validation](validation.json) remains an immutable record of `0f5044a`.

## Findings and acceptance evidence

| Finding | Current behavior | Verification |
|---|---|---|
| A whole missing world silently changes the denominator | `summarize` requires the manifest; `contrast` requires the frozen assignment ledger. Both reconcile IDs and every assignment field before aggregation. Missing observations stay assigned. | Delete all ten records of development world 10002: 96 assigned, 86 terminal, ten explicitly missing; primary contrast still has three worlds, no point estimate, bounds [-2/3, 2/3]. With no records, all 96 remain assigned and both contrast bounds are [-2, 2]. |
| Duplicate or relabeled records can distort grouping | Reject duplicate/unassigned IDs, changed world/arm/stratum/attack type and extra grouping fields; reject incomplete planned contrasts and nonbinary endpoint values. | Mutation tests fail at both standalone analysis entry points. Missing *observations* get bounds; missing *planned treatment cells* are a malformed design and raise. |
| Parent accuracy can credit an unsupported guess | Report required-key coverage, numerical correctness, local support, unsupported-correct, unsupported-wrong, grounded inherited error, abstention and invalidity separately. | A correct guess citing another entity has `parent_correct=1`, `parent_unsupported_correct=1`, `parent_supported=0`, coverage=0. A false value justified by inherited memory has supported=1 and inherited-error=1. Conflicting/missing evidence supports abstention. |
| An empty-memory numeric answer | A bare numeric answer without citations fails the actor contract. The scorer also labels a directly supplied lucky guess unsupported. A missing/invalid output is unknown, not abstention. | Empty-memory regression checks both the contract boundary and direct scoring; unsupported endpoints remain null for invalid output. |
| More discussion is confounded with extra private work | V3 already includes a predeclared private-work arm, the same work prompt/call schedule/output caps, exact shared acquisition and report checkpoints, private initial contamination measurement and clean full-evidence diagnostics. | New regression compares every phase/agent/round in board/private schedules (19 continuation calls each at R3), verifies initial measurements and six clean diagnostics. Existing tests verify shared actual ballots, isolation and synchronous barriers. Input tokens remain unmatched and are reported separately. |
| Changed allocation accepted | Reproduce the frozen partition and roles for the world version. Validate every case and the full assignment plan before the first provider request, including the direct acquisition entry point. | All documents assigned to one agent, a rotated partition that remains ambiguous, a malformed final world, duplicate/missing assignments, altered metadata and duplicate worlds all reject with zero provider calls. |

The primary/safety estimands, six development cases, world generator version, prompts, four arms, three-round default, source policy and 636-call plan are unchanged. Newly added parent metrics are descriptive decompositions of the existing support/truth scores. The inherited-memory baseline still permits correlated false testimony; this is a measured outcome, not silently corrected by the scorer.

## Validation and reproduction

**84 distinct checks passed: 50 v3 tests and 34 existing v1/v2 tests.** The 16 runner/analysis tests were rechecked after the last grouping guard. A fresh default scripted run completed 96/96 cases and 636/636 calls with no invalid/missing/provider-failed outcomes; all 636 saved request bodies, 96 outcomes and the summary reproduced through 1,790 verified journal events. Clean scripted diagnostics and reports-only decisions were each 6/6. `model_qualified` remains false.

```sh
PYTHONPATH=researchers/dmarz/notes/discussion-dose/src python3 -m bench_v3.selftest
python3 researchers/dmarz/notes/discussion-dose/src/selftest.py
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py run --output data/discussion-v3/new-review-fixes-check
python3 researchers/dmarz/notes/discussion-dose/src/benchmark_v3.py audit data/discussion-v3/new-review-fixes-check
```

The retained validation bundle is `data/discussion-v3/vishesh-fixes-a1/` (ignored raw outputs). Run and audit using the recorded source revision. Replay payloads and every displayed terminal record match saved metrics; browser playback was not repeated because the renderer is unchanged. [Pre-run assessment](../reviews/v3-vishesh-fixes-pre.md) and [post-mortem](../reviews/v3-vishesh-fixes-post.md) document scope and outcomes. No model endpoint, credits, fleet job or reserved qualification/holdout case was used.

## Remaining decision

[Shadow's independent review](../../../../../tasks/review-discussion-benchmark-v3.md) must include the patched source and these checks before a model launch is considered. A review of the old runtime alone does not approve the new file hashes. Real-model qualification, external-domain validity, exact-token matching and broader task coverage remain unestablished. No new experiment has been launched by this repair.
