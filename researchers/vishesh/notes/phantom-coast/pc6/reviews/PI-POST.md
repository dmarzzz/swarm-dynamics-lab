# PI post-mortem: saved-data review and PC6 pre-run stop

Retrospective assessment, 2026-10-04, vishesh/codex-phantom-coast. Scientific verdict: **complete_valid_result** for the saved-data review; PC6 **parked/unexecuted**, not failed qualification. No preregistration or execution is claimed for this analysis. The prospective PC6 plan was published before its implementation, then rejected for insufficient decision value before model calls. No worker or claim needs teardown.

## Evidence and critique

PC4's report-heavy acquisition improved fully false-report loss by 4.296875 percentage points, below its 5.555556-point practical target; it harmed benign reports by 1.5191 points. Its directly measured label reconstruction was accurate, narrowing the practical problem to acquisition/allocation rather than label parsing. PC5 addressed the decision contract, met its mean-regret improvement target, and still failed to establish a reliable controller. Sources: [PC4 post-mortem](../../pc4/reviews/S1-A1-POST.md) and [PC5 post-mortem](../../pc5/reviews/S1-A1-POST.md).

The PC5 paired audit is sharper than marginal success rates: all seven reliable-source changes went from optimal to suboptimal; all nineteen unreliable-source changes went from suboptimal to optimal. Four reliable and eight unreliable cases remain wrong under both prompts. The 19/64 explicit errors cannot be explained away by valid JSON. Order and label strata show errors in both positions and both terrain labels, but feature groups are small/confounded; this is exploratory description, not causal attribution. There is no exact recurrence test or proof that coordinate/order causes the failures.

The decisive missing comparator was a strong simple policy. Under the equally weighted declared .8/.2 risks, always checking has regret .025, below explicit .07734375. The analytic minimum rule has zero regret by construction. This does not contradict the registered improvement over legacy; it limits engineering value. The legacy instructions also omitted the scoring/transition contract, so utility disclosure and transition clarification are bundled. The evidence does not identify which component helped or harmed.

Dmarz verify-cost-qwen attempt002 independently reproduces a related action-cost mapping problem in a different route: 8/24 correct cost pairs, 11 exact reversals, 4 reversed/zeroed, 1 other; 23/24 decisions minimize the declared costs and all 14 misses reverse their true ordering. These written outputs are not access to private reasoning. Attempt001 and002 used different layouts, so their performance difference is not a paired causal test of asking for costs. Do not pool these samples with TypeSafe or revive the stopped Qwen configuration.

## Evaluation of the proposed update

PC6 tightened the relevant strata and replaced the 768-choice grid with 48 paired choices. It also corrected the old interface-only qualification weakness and added a durable duplicate-claim rollback repair. Ten offline checks pass. But its supplied consequence table already contains the answer-relevant computation. There is no current downstream decision changed by passing versus failing minimum selection: both lead to the exact analytic policy and reject a larger swarm claim. The minimum scientific contribution would be a narrow interface boundary result; without a demonstrated interface-selection need, that is insufficient reason to collect more.

Decision: retain the plan and code for provenance, explicitly disable native admission/entry, and finish the saved-data interpretation. This is scientific futility, not an access, budget, reviewer or permission blocker. An unclaimed-host read-only SSH probe failed; no attempt to borrow the occupied historical host or provision elsewhere followed. That access result did not determine the stop.

## Run-quality assessment

- Question — gap for PC6: no consequential outcome-dependent choice remains. Acceptance for reopening: a written pass/fail decision table whose branches change a justified next action; a supplied-minimum check alone is insufficient.
- Scenarios — gap for broad claims: only two arithmetic templates with coordinate permutations and known calibration. Acceptance: real task-specific uncertainty, development-selected meaningful challenge and sealed task-family holdouts.
- Controls — pass for the scoped saved-data comparison: matched original PC5 layouts/inputs audited; analytic, always-check and always-explore counterfactuals added and labelled. Collective effects are not claimed.
- Capability — gap: 19/64 explicit TypeSafe actions remain suboptimal and the old Q0 was interface-only. Acceptance: task-relevant semantic qualification by stratum before any harder model study; no new screen justified yet.
- Measurement — pass: expected regret is recomputed from saved selected cells and fixed loss rules; paired changes and denominators retained. It is not realized real-world utility.
- Sample size — pass for candid pilot description only: 32 PC5 roots with128 dependent choices; separate12 Qwen roots with24 choices; zero PC6 samples. No powered noninferiority/generalization claim.
- Agent context — pass for retrospective scope: original input hashes and reconstructed requests match; no new native context was sent. Table assistance is disclosed in the unexecuted plan.
- Data integrity — pass: original PC5 native trace audit succeeded; portable decisions/worlds match their original hashes; all128 assigned outcomes retained. Qwen row hashes/counts recomputed separately.
- Resources — pass: zero new calls/spend/claims/VMs, closed predecessor ledger hash verified read-only, original cumulative uncertainty retained. No credential transfer occurred.
- Reproducibility — pass: portable source data, deterministic analysis, policy, tests and plot generator retained; no claim of hosted-output determinism or independent audit.
- Visualization — pass: paired-change totals, simple-policy regrets and distinct Qwen cost categories recomputed, rendered and inspected. No invented replay trajectory or native PC6 result.

## Closeout and future decision

Execution: saved-data analysis completed; native PC6 not started. Qualification: no PC6 result. Scientific interpretation: PC5 remains a valid diagnostic with a material reliable-source regression and a superior simple policy. Reporting: analysis JSON, byte-matched saved rows, plot, source-hashed rubric and this review retained. Cost: known .845052138, conservative .857148138, nine old uncertain charges; new zero. Allocation: none acquired, historical PC5 claim already released.

A future study should begin from a useful application question, not another coordinate grid. For example, source reliability may have to be inferred from limited observations, but that needs a defensible environment and a budget-matched Bayesian/simple-controller comparison before any model implementation. This is a research direction, not an approved next run. Preserve historic plans and outcomes; do not call this parked screen a negative model result.
