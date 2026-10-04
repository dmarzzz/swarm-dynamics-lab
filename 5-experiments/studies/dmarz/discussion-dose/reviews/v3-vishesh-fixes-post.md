# Post-mortem: v3 review repairs

- Owner/stage/date: dmarz/discussion-bench-v3; offline engineering verification; 2026-10-04 UTC.
- Parent: [original offline release](v3-offline-post.md). Plan: [v3-vishesh-fixes-pre.md](v3-vishesh-fixes-pre.md).
- Source: `d76146b`; exact hashes and output digests in [review-fixes-validation.json](../benchmark-v3/review-fixes-validation.json).
- Attempt: `vishesh-fixes-a1`; retained under ignored `data/discussion-v3/`.
- Disposition: complete-valid-result for the repair diagnostics. Independent successor review and model qualification remain pending.

## Execution and measurement

All 96 planned cases started, terminated, were graded and analyzed; zero missing or duplicate records. All 636 scripted requests completed; zero provider/validation failures. Replay verified 1,790 hash-chained events, every saved request, all terminal outcomes and the recomputed summary. Source hashes matched. There were zero physical model calls, tokens billed or API spend; no server was allocated. Unit tests additionally exercised bounded scripted and mocked failures.

The 50 v3 checks (ten new) and 34 original v1/v2 checks passed. After the final extra-label guard, all 16 runner/analysis tests were rechecked. No failing attempt was replaced. Removing a complete development world retained 96 assigned cases and three primary worlds, with an unidentified mean and bounds [-2/3, 2/3]. Removing all rows produced [-2, 2], not a zero effect. Invalid partitions and plans failed before provider dispatch.

Parent fixtures distinguish a lucky correct guess with wrong-entity support, an unsupported wrong guess, a supported false inherited value, absent evidence, contradiction, valid abstention and invalid output. Matched continuation schedules and shared starting ballots remain verified. Clean scripted full-evidence and reports-only decisions were both 6/6. These are instrument checks, not LLM evidence or scientific effect estimates.

## Visualization review

Mapping `v3-stage-ledger-1` is unchanged. The local replay retains initial evidence, checkpoints, all round events, merges and final outcomes. Its parsed payload has all 96 saved records, and every terminal metric matches `episodes.json`. The existing escaping regression passed. Browser playback was not repeated; prior interactive evidence remains in the original post-mortem. Raw journal and saved rows are the fallback. No live dashboard deployment occurred.

## Repair ledger and limits

The [finding-by-finding response](../benchmark-v3/VISHESH-REVIEW-RESPONSE.md) links the repairs and exact mutation evidence. The verified causes were missing assignment-label checks, delayed plan validation, an allocation validator that allowed alternative underdetermined partitions, and parent support labels that were not explicitly decomposed into correct/wrong unsupported answers. V3's existing matched private-work and memory support mechanisms already addressed the main original-design limitations; new regressions make those acceptance criteria explicit.

Historical v1/v2 runtime and results are unchanged. The synthetic templates, three-agent/single-merge scope, unequal input-token exposure and lack of real-model qualification remain. Passing these checks is an author verification, not independent scientific approval.

## Next action

Have the ongoing independent review inspect this exact amended source. Any future model qualification needs its own frozen launch record and pre-run assessment. Qualification and holdout namespaces remain unopened; no additional scientific run is part of the user-requested repair.
