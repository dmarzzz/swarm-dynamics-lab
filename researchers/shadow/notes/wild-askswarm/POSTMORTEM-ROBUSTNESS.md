# Robustness-v1 closeout, 2026-10-04

## Scope and reconciliation

Authorized post-hoc saved-data analysis, not a fresh model experiment. The original
[PLAN](PLAN.md), [results](results/) and registry confidence 1/4 remain valid for descriptive
answerability only. This analysis narrows interpretation rather than upgrading evidence.
[Amendment](ROBUSTNESS-PLAN.md) was committed before helper implementation; direct-review
judgments were separately committed before unblinding. No experimental trials, no provider
requests, no retries and no spend. One local nice-10 process completed 15 corpus/arm reports
in **383.768 seconds**. No data were uploaded to a model. Raw audit text remains outside git.

The input denominator is the same original 14,591 wiki / 189,579 artifact / 2,673 git records.
Five arms per source (baseline plus four sensitivities) all completed. No arms omitted.
30 offline tests pass (29 before the corpus run, plus a later missing-clock regression test).
A separate arithmetic implementation checks all 15 reports, including
pairwise-difference Gini, counts, time-to-k medians, rank support and unchanged original
baseline summaries. [Validation](results/robustness-v1/validation.json). Frozen source hashes
are checked again in [source manifest](results/robustness-v1/source-manifest.json).

## Scientific assessment

- Observation-unit dependence is large. Wiki earliest-page reduction retains 1 of 10 original
  phrasing-credit leaders; exact-text removal eliminates 26 of 34 git multi-identity clusters.
- Wiki conservative fallback-clock exclusion is small in aggregate (109 rows removed, original
  credit top 10 retained), but individual ranks can still move. Non-reqlog is not a verified
  imputation label, and unchanged aggregates are not clock validation.
- SwarmTraces remains without observable actor/clock data in every arm; root reduction is
  189,579 -> 128,454 artifacts. Missing endpoints cannot become failed outcomes.
- The manual-style assistant audit is **not independent or human-reviewed**. 15/15 sampled git
  links were sync boilerplate. Wiki 10/15 cross-root task-specific repeats provide a descriptive
  precision estimate of 66.7% (nominal Wilson 41.7-84.8%), not causal/semantic adoption precision.
  Five wiki links were same-page snapshots. Both prose-coordination pairs were in that group.
  Directed endorsement is unestablished for all 30, which is not evidence it never occurred.
- Full-arm HTML and rank HTML are available; static source-bound tables are the visualization.
  A live-run animation would misrepresent an offline sensitivity comparison.

## Defects, repairs and limitations

- A display-only provenance locator in the first runner export was one directory short.
  Original result bytes were preserved; source-manifest.json supplies corrected paths and
  hash verification. Future runner output uses the corrected locator. Numerical results did
  not change and no favorable rerun occurred.
- After analysis, a generic-helper edge case was fixed: an undated wiki row with no clock
  grade must remain missing, not be removed as if it had an imputed timestamp. The frozen
  wiki has 14,591/14,591 dated rows, so this branch affected no reported record or result.
  Original package hashes remain in the saved reports; the final helper includes this guard.
- The source genre and third-party body sign-offs defeat full audit blinding. The report
  discloses this. B02's initially omitted middle was read before locking the judgment.
- Root aggregation means one actual earliest representative, not root-weighted retention of
  all editors. Exact text dedup removes genuine repeats too. These change the estimand and
  observation support; do not describe them as corrected causal truth.
- Root matching between reclustered arms is a greedy shared-event match. Unmatched/split
  clusters and matched-record coverage are reported rather than treated as the same idea.
- Same assistant wrote code and reviewed text. Separate arithmetic is not independent
  researcher validation. No semantic-adoption precision estimate is available without a
  provenance-aware gold standard. No population confidence interval is claimed.

## Next action and handoff

Closed for Shadow's zero-API priority steer. Halflife and identity may import
`askswarm.robustness.variants`, `aggregate_roots`, `exact_deduplicate`, `exclude_imputed`,
`root_ids`, `rank_change`, or `robustness`. They supply their own Event metadata and scorer.
Do not edit the shared package from another lane. No new models/features are needed to use it.
Future substantive work would be diff-introduced wiki text, non-administrative git content,
and independent source-aware annotation, separately planned rather than silently retrofitted.
