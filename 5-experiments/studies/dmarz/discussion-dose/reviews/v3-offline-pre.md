# Pre-run assessment: v3 offline package qualification

- Owner/stage: dmarz/discussion-bench-v3; local engineering tests only.
- Status: diagnostic-only. The user requested implementation and shipping. No paid calls, server allocation or queue entries are part of this attempt.
- Parent evidence: [v2 issue review](../V2-ISSUE-REVIEW.md), [H5/H6 post-mortem](v2-calibrate-H5-H6-post.md), [v3 design](../V3-EVAL-PLAN.md).

## Design and assessment

Test a focused three-agent benchmark, with worlds as the unit, paired clean/attacked exposures, shared acquisition snapshots and independent/reports/private/board continuations. Three rounds is the default; round count is configurable and frozen per manifest. The board/private comparison matches calls and output ceilings, not actual input tokens.

Keep evaluator truth outside actor requests. Establish answerability from finite public domains and explicit source precedence; compare the optimized solver to an independent brute-force reference on bounded fixtures. Validate every generated development world before use. Include source conflicts, missing keys, correlated copies, updates and inherited false records in 36 parent fixtures. Reserve disjoint qualification and holdout namespaces; do not open the holdout during package development. External task-domain transfer and formal research review remain unestablished.

## Latest v2 evidence at implementation start

Read-only hub snapshot, 2026-10-04 UTC: H4 S0 `723dad8e` is terminal, 48 assigned episodes, 4 invalid, clean accuracy 23/24, attacked target wins 12/24, attacked false memory 17/24. Its output-contract failures still block qualification. H5/H6 terminal results are in the linked post-mortem; H6 has no clean copy and is an unrecoverable anchor. Private-control `d0725be0` was still running at 20/24 episodes. No board/private scientific conclusion is frozen from that partial result.

## Frozen execution plan

Build and run stdlib-only local tests, scripted known-answer and deliberately faulty policies. Maximum paid calls and spend: zero. One local process; no network in the offline runner. Source/config hashes recorded in each generated run directory. No automatic retry, overwrite or outcome replacement. All assigned episodes remain in the manifest and terminal ledger; interrupted runs remain detectable by reconciliation.

The scripted stage has six development worlds, two exposures and four arms; 12 full-evidence diagnostics and 36 memory fixtures. At three rounds its normal path is 708 policy calls. These are software calls, not LLM results. Run failures and fixture/scorer mutations separately as unit tests. A valid bad-memory outcome is a passing test of measurement, not a bug to repair away.

## Acceptance checks

- Exact pairing, no unintended treatment differences, each private view ambiguous and raw clean union uniquely answerable.
- Strict parsing rejects duplicate JSON keys, duplicate sources, booleans as integers and unauthorized identifiers without checking hidden truth.
- Fixed majority threshold, independent private state, synchronized posts and no ballot feedback.
- Known clean, poisoned, omitted and conflicting memory outcomes; always-abstain loses clean utility.
- Every assigned row terminal; requests, usage and events reconcile; saved responses reproduce outcomes without network.
- Tampered logs, altered outcomes, provider failures and interrupted writes are detected.
- Existing v1/v2 regression suites and repository checks pass.

## Visualization mapping

Mapping `v3-stage-ledger-1`: a local HTML replay uses an event slider/playback and episode selector. Logical stages are acquisition, report exchange, each round, merge and parent. Views show agent choices, endorsed values, distinct source origins, required memory coverage and parent support/ground-truth status. Evaluator labels belong only in results/replay. Missing and invalid states are text-labeled. Requests and raw responses remain in the hash-chained journal; no transition is thinned. Replay rendering must escape all actor strings. The stage table and JSON journal are the supported fallback; no public deployment is included. Final view must agree with the saved terminal record, and playback must be checked locally.

## Remaining gates

The different-researcher review task remains open. This implementation can be shipped and independently inspected while that gate is pending; it cannot honestly be marked externally reviewed or model-qualified. Review terminal private-control artifacts and write a new pre-run assessment before any v3 model launch. Formal hypothesis/confirmation gates remain unchanged.

## Amendment before release qualification, 2026-10-04 UTC

The final [private-control report](pc-H4-a1-post.md) is now available and has been read alongside [RESULTS-V2.md](../RESULTS-V2.md). All 24 private-control assignments are terminal, with one invalid board episode. The reported attacked target counts are board 2/6 and private 4/6; neither a neutral private trajectory nor a preferred discussion-effect sign is required for v3. These small numbers do not establish a protective effect.

Share one exact post-report checkpoint between reports/private/board arms, in addition to the private acquisition snapshot. This avoids independent starting-ballot resampling while retaining matched continuation calls. The frozen release allocation is now **636 policy calls**, 96 cases, three rounds. Per-round work and probes remain separate and never feed probe ballots back into actors. The original 708-call local prototype completed and replayed successfully; it was an engineering prototype, not an LLM run, and its local output remains in `data/discussion-v3/offline-a1`.

Final release tests include the native-provider request/strict-decoder mock, vote-to-own-claims consistency, public-domain rejection, usage/dispatch accounting, and an explicit model-qualification result that cannot be true for scripted outputs. No qualification or holdout IDs are opened by these tests. The new [review packet](../benchmark-v3/REVIEW.md) supplies six hand-derived development cases and mutation instructions. The code is committed before the final release qualification run; its manifest freezes file hashes and Python/platform information.
