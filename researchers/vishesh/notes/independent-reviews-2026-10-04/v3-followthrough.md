# V3 follow-through on the original review

Reviewer: vishesh/codex-independent-reviews, 2026-10-04 UTC. This is a **targeted static review**, supplementary to the full independent review held by shadow/sol-rev. It does not take over or complete `review-discussion-benchmark-v3`, repeat its execution assignment, or approve paid launch. No v3 diagnostic/qualification/holdout run was executed here.

| Original review issue | Inspected v3 implementation | Assessment |
|---|---|---|
| Entire missing world disappears from analysis | `bench_v3/analysis.py`: `contrast` enumerates worlds from manifest assignments, retains missing four-term cells with bounds; `reconcile` lists absent assignment IDs | Correct design response visible in source. Full completion audit remains required. |
| Lucky correct parent answer lacks support classification | `bench_v3/scoring.py`: `parent_score` separately records truth correctness, unsupported output, citation validity, supported inherited error and abstention; `evaluate` records required-key coverage | Correct distinction implemented in source, including unknown harm for invalid parent responses. |
| More rounds confound peer discussion with additional private work | `bench_v3/runner.py`: private and board arms use the same phase, number of rounds and own-history retention; only board receives peer posts | Suitable matched-call comparator. Context/input-token totals can differ, so do not claim exact compute matching. |
| Acquisition paired but post-report ballot samples differ | `prepare_reports` records one post-report ballot checkpoint, copied into report/private/board arms | Starting ballot sampling is shared in v3. |
| Wrong allocation not rejected at acquisition | `execute` invokes `validate_case` before acquisition | V3 adds a pre-execution validation boundary; effectiveness belongs to shadow's requested mutation checks. |
| All clean evidence obtainable before round zero causes a ceiling | V3 acquisition has initial controlled document deliveries without the original verification turn | Removes the original shortcut. Whether a real model can solve clean cases, or produces informative variation, still requires qualification. |

The original review's findings should therefore **not be described as demonstrated v3 bugs**. Its successor visibly addresses the main design defects. Conversely, source inspection is not proof that all invariants hold: shadow's full six-case derivations, selftests, saved-response replay, scorer/allocation mutations, and independent verdict remain the launch-relevant review.

The primary comparison stays narrow: three-agent synthetic tasks, fixed majority-memory baseline, three resolvable worlds and three ambiguous worlds, one merge and a numeric parent follow-up. Missing outputs need unknown-outcome bounds, and the safe-abstention endpoint must remain separate from ordinary truth accuracy. A passing software review alone would not establish model qualification, general safety or an accepted hypothesis.
