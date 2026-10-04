# Q-A6: prospective matched-roster diagnostic

2026-10-04 UTC. Design prepared during Q-A5; dispatch requires its completed post-mortem and artifact readback. Owner authorized successive PI-review/revision/runbook/execution/post-mortem cycles within the original cumulative budget. This is a revised exploratory qualification design, not a declaration that Q-A4's all-success gate passed.

## TLDR

Compare N=1 with N=2 on four fresh width-16 evidence tasks (two development roots, parallel and chain), with matched model, schema, task, aggregate caps and service slots. Test whether splitting work across two contexts changes verified success, error propagation, cost and latency. Eight separately executed episodes; small mechanistic pilot, not an optimal-N estimate or confirmatory result.

## Question and prediction

Q-A4's evidence weakness survived schema repair; Q-A5 tests whether errors begin in workers or integration. Q-A5 completed all eight cases: 128 worker/final item comparisons found no correctness transitions; all errors were already present at the worker stage. Changing integration alone therefore lacks support in this cohort. The next diagnostic changes roster size, the study's intended intervention, while keeping prompts/protocol consistent across arms.

Directional mechanistic prediction: N=2 may reduce parallel-task elapsed time; it should not enable simultaneous dependent chain work under enforced prerequisites. Accuracy can improve, worsen or remain unchanged; no directional success hypothesis is registered. Smaller per-context histories can change errors/token cost, so latency differences alone cannot establish a universal scaling law.

## Setup

Evidence tasks only; qualification roots4 and5, width16, fresh episode histories, same public-task hash within each N pair. These roots are new to paid runs, but remain development data; they are not held-out validation/transfer. Four paired tasks share only two independent root seeds; they are not four independent roots or eight independent worlds. Pin the native model, temperature, schema, generator/evaluator and source for both arms. No tools, fallback or evaluator feedback. Four service slots for both N; N=2 can occupy at most two. Full public task visibility remains explicit.

Order counterbalances which N runs first: root4 parallel N1,N2; root4 chain N2,N1; root5 parallel N2,N1; root5 chain N1,N2. Hosted-model calls are fresh; no saved-response replay or history sharing. This fixed order mitigates simple ordering imbalance but is not a randomized large-sample trial.

## Protocol

Implement required-edge validation in BOTH arms: every supplied prerequisite must appear in the returned plan, extra acyclic edges are allowed and recorded. Missing required edges receive the existing single semantic plan repair, then fail. This closes a known design loophole; Q-A4 plans had zero omissions, so it is not offered as the explanation for historical errors. Freeze this change before either arm runs. Preserve worker artifacts and post-termination stage audit for both arms.

Eight episodes, at most 19 calls each, 600-second deadline with 60 reserved for integration, 4096 output tokens and 48000-byte full-payload cap. $4 attempt/$2 episode sublimits inside the original canonical $20 ledger, including every previous stage and unresolved charge. Check fresh exposure before dispatch; no new ledger, replenishment, automatic retry or cap increase. Stop on interface/schema/route/usage/claim/publication failures; substantive errors remain measured outcomes and do not trigger an arm-specific retry.

Exact immutable public plan/source and condition TLDRs must be verified before calls. Existing experiment host may be reused only with current exclusive claim and stopped preceding worker, acknowledged/readback-verified Q-A5 artifacts, fresh runtime/manifest, dedicated Swarm Lab credential policy and safe SSH. No unrelated project's credential, no provisioning through a personal cloud account. Retain each assigned condition, pair ID, width/hash, N, actor IDs actually used and all failed/unstarted outcomes.

## Metrics

Primary pilot summaries are paired per-root/per-structure differences in on-time task success (including failures), quality, settled/held cost and elapsed time. Also report arithmetic/provenance accuracy, worker-to-final transitions, active context count, peak concurrent service spans and supplied/extra prerequisite edges. Chain concurrency greater than one work request is a scheduling defect, not a speedup. Compare complete assigned denominators; do not drop a difficult arm or pick favorable items. No p-value, fitted optimal size, pooled independent-item estimate or retrospective oracle.

Readiness is instrument integrity and interpretability, not requiring the baseline model to be perfect. Q-A4 remains failed against its original all-success criterion. This prospective revision allows observing genuine performance failures while keeping structural/runtime gates; it does not retrospectively promote earlier runs or open the formal core. Interpret Q-A6 as qualification of the matched-N instrument and preliminary response heterogeneity only.

## Visualization mapping

Use actual actor/service/dependency traces to compare paired N1/N2 runs, with common task and wall-clock origin, cost and outcome annotations. Distinguish allocated contexts, used contexts and simultaneous requests. Mark inaccurate results visibly. The physical interpretation is bounded scheduling capacity and serial dependencies; no GPU measurements or biological-law claim.

## Closeout and next decision

Complete a PI-perspective post-mortem on all four pairs, separate scientific results from process compliance, and release/extend only this experiment's resources as appropriate. If effect estimates differ by structure, design a larger preregistered development study; if a scheduling/accounting defect appears, repair before collecting more. Do not automatically sweep N4/8/16 or tune on these roots and call them held-out. Retain the original spending authority across any later cycle.
