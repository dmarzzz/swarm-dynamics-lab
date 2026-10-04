# Attempt2 post-mortem and handoff

Assessor: shadow/Sol, 2026-10-04. This is the owning operator's review, not independent validation. Native evidence: [requests](requests.jsonl), [responses](responses.jsonl), [all episode outcomes](summary.json), and [finding](FINDING.md). No further model calls are authorized or running.

## Separate completion statuses

- **Execution:** the frozen assignment sequence finished, including optional Opus. All22 episode assignments have terminal files:20 complete,2 parse-stopped. All16 primary Sonnet repair episodes are complete. No unstarted episode or unmatched HTTP receipt.
- **Response validity:**1,188 HTTP200 responses;1,186 valid final names;2 invalid final-name responses. No retries, HTTP errors, fallback providers, or duplicate execution.
- **Qualification:** passed the unchanged12-decision gate. Four unanimous controls correct, six of six Sonnet conflicting-history choices not final-item copying. No prompt tuning or response-curve fitting.
- **Scientific conclusion:** primary mean change-0.0833, interval[-0.1667,0]. Operational freeze not established, preregistered classification inconclusive. Both secondary requirements for the full predicted pattern fail their point thresholds. This is a valid completed primary result, not a reason to rerun for a different sign.
- **Cost:**$0.968330 actual response-reported OpenRouter cost from every receipt. Pending reservations0, unresolved OpenRouter exposure0. Historical pool spend remains unknown. Actual lineage attempts1,196/1,500, including the previous8 errors.
- **Process:** amendment `34aa78f7` and transport/pre-review `70a65a81` were on main before calls. Qualification and scientific admission receipts exist. Original attempt files remain unchanged. Administrative deadline extension and analyzer file-format compatibility were prospectively disclosed. All model calls ended22:58:45Z.
- **Reporting:** native traces, root and per-agent scores, missingness, complete accounting, static measured-trajectory figure, source/artifact hashes and reproduction/audit scripts retained in this directory. SUBMISSION section7 updated; no other submission section changed.

## Trace-grounded failures and causes

| Issue | Evidence and cause assessment | Disposition |
|---|---|---|
| Attempt1 transport unavailable | Eight errors, zero outputs in retained parent records | Authorized OpenRouter transport produced responses in attempt2; no historical record overwritten. |
| Two attack episodes lack endpoints | Task170/full request993 and task171/full request1070 returned null final content with finish reason`length`; all32 completion tokens were reported as reasoning | High-confidence output-budget exhaustion on this route, not a final-name choice. Stop affected episode at incomplete round3, no parse retry, no inferred decision. Preserve other valid responses from that incomplete round but do not update state with them. |
| Apparent stability can be individual motion | Memory1 change0, but42/228 switches per arm. Saved decisions in every memory1 repair episode exactly copy the current encountered partner | Aggregate conservation is consistent with synchronous pairwise swaps, not frozen individuals. Report per-agent denominators and rates, not just curves. |
| Freeze point estimate is constrained by the floor | Mean baseline1/12, two of four roots already at zero; complete elimination still gives mean change-1/12 inside the freeze band | Retain preregistered interval criterion; do not call the point estimate alone freeze. Optional Opus roots are both at the floor and provide weak confirmation value. |
| Fixture differs from intended motivating regime | Frozen scripted full/removal change+0.250, versus Sonnet-0.0833 | Known before relaunch, explicitly retained by owner direction. No replacement seeds or scientific tuning. Narrow conclusion to this standardized-state fixture. |
| Frozen analyzer main assumes total transport failure | Main asserts all HTTP statuses non200 and no episodes, hard-codes original figure text | Prospective compatibility disclosure in amendment1. Keep source untouched, verify identical original summary in a temporary-copy replay, and use its unchanged bootstrap/mean functions in the new reporting adapter. |

## Scientific quality assessment

1. **Question and intended decision:** narrowly scoped to whether the existing qualified raw-history Claude instrument meets the operational freeze criterion in these fixed states. No natural model-capture or original S1b replication claim.
2. **Scenario relevance and challenge:** relevant to coordination after scripted committed-minority capture, but reduced population/horizon and half the roots at the zero-original floor limit discrimination.
3. **Controls and qualification:** unchanged unanimous and conflict histories pass. Twelve decisions are a sparse competence/non-copying screen, not a calibrated stochastic policy estimate.
4. **Agent/context integrity:** exact original system/user text and visible raw histories reconstructed from records. No last-event answer metadata, original-label marker, persistent conversation or operator context introduced.
5. **Interventions and pairing:** same four frozen roots, memory projection, wipe manipulation and random matching schedules. Every repair arm completes, so primary and paired repair results have no missing outcomes.
6. **Sample units and precision:** four roots, not1,188 independent requests. Whole-root bootstrap retained. Degenerate intervals are sample properties, not general certainty. Optional Opus reuses roots and is not pooled.
7. **Outcomes and scoring:** exact-name parser, round20 endpoint, per-agent switch rates and ten-consecutive-round recovery retained. Zero binary recovery in all repair arms. Parse failures are not counted as behavioral choices.
8. **Missingness and adverse outcomes:** both full-memory attack outcomes are missing after round2. All-assigned capture/endpoint bounds remain[0,1] for that arm. No survival claim based on the incomplete traces.
9. **Analysis and reproducibility:** same numeric estimators; successful-record wrapper transparently documented. Saved-data reconstruction independently recomputes arithmetic relative to the report implementation, but shares authorship and imports original prompt/state helpers.
10. **Resource and execution quality:** request/dollar/deadline gates respected, provider fallbacks disabled, served model IDs and all cost receipts saved, no new infrastructure. Conservative per-call reservations were an operating exposure estimate, not a provider invoice guarantee; actual spend closed far below cap.
11. **Visualization and claim quality:** measured mean Sonnet trajectories, root histories and switch tables retained. Static visualization was the prospective fallback; no animation claimed. Figure does not portray missing attack endpoints or offline scripted curves as Claude observations.

## Checks and finalization

`report.py` reproduces attempt1's frozen analyzer summary in a temporary directory, then builds attempt2 results with the same root bootstrap. `check_attempt2.py` reconciles1,188 request/response pairs, all episode updates, exact prompts and schedules, gate outcomes, cost, source hashes and confidence-interval arithmetic. Original7 instrument tests and6 new transport fault tests pass, along with the original attempt1 saved-data audit. Repository checks are recorded in [CHECKS.md](CHECKS.md). There is no shared operations adapter for this historical lane; this manual closeout is the explicit saved-evidence bridge rather than a fabricated automatic-hook receipt.

## Next action

**Finish and retain the result. Do not rerun this instrument for a favorable outcome.** A separately authorized successor could first establish an informative scripted freeze regime without selecting roots on Claude outcomes, and prospectively qualify an output-budget/reasoning contract that reliably yields final names on attack histories. Neither adjustment is made here. Preserve attempt1 and attempt2, all spent/unknown costs and missing full-memory attack outcomes. No worker, resource claim, deployment or continuing model job remains to release.
