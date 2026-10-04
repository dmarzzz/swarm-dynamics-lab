# Poietic Agents execution handoff

This project follows [the worker template](../../../../templates/experiment-worker/README.md), [agent lifecycle](../../../../tooling/agent-experiments/AGENT-LIFECYCLE.md), [run review](../../../../tooling/agent-experiments/RUN-REVIEW.md), [public plan contract](../experiment-documentation/README.md) and [dedicated machine workflow](../experiment-machine-workflow.md). The current deliverable is the prospective design. There is no launcher to execute and no experiment queued.

## Ordered work

1. **Design review:** independently inspect README, PROTOCOL, design.yaml, contracts.json, prior-art boundary, visualization and S0 pre-run record. Resolve the open decisions in launch-state.json. The review task is `review-poietic-agents-design`.
2. **Prior art:** continue `heterogeneous-methods-review`, now focused first on HX-31/Poietic. A formal experiment/hypothesis cannot be created until the required gates pass. The worker runbook permits exploratory development in this notes directory; keep it labeled.
3. **Offline instrument:** adapt the template contract without inheriting its quorum simulator, metric names, 300-task sample size, automatic retry behavior or power claims. Implement fixture truth separation, tool/context receipts, proposal transactions, realistic baselines, three cost ledgers and the renderer. The protocol was written before this implementation. All expected offline checks are in PROTOCOL.md.
4. **Resolve qualification:** pin exact model/backend/settings, prompts, tools, private credential aliases, dependency/runtime versions, fixture generator, scorer, qualification assignments and tariff snapshot. Freeze actual request counts and atomic cost reservations. A null required manifest field blocks dispatch.
5. **Authorize and allocate:** obtain the study-specific API and infrastructure allowance, preserve other experiments' shared caps, refresh the private fleet, check real workload and claim a fresh eligible machine exclusively. If provisioning is required, use Dmarz's established account/team only after exact private identity/state verification. Keep private inventories and credentials out of public material.
6. **Publish and verify:** commit/push the completed pre-run version; register the immutable README URL and `TLDR:` description; use the shared public_plan.py preflight with the exact condition TLDR before any endpoint/model probe, deployment queue or worker start. Inspect the public page and save a sanitized receipt. Registration-only publication creates no run.
7. **S0:** one bounded qualification attempt on the dedicated allocation. Reconcile every request and bill, write its post-mortem and repair any material defect before fresh qualification. Do not convert a provider probe into an unrecorded preflight call.
8. **S1:** update the pre-run assessment using S0's evidence. Freeze the four-arm assignment and per-lineage quotas, validate the public plan again, then run the development study. S1 checks feasibility and variance; it cannot support the planned confirmation claim.
9. **S2:** only after reviewed survey/accepted hypothesis, independent instrument review, development-informed sample size, fixed strongest comparator, untouched holdout, and a new exact preregistration. Create the formal experiment through lab.py only when permitted.
10. **Close:** preserve all attempts and original denominators, reconcile reporting separately from scientific outcomes, verify replay and final image, upload durable artifacts, stop only this study's workers and release the claim. Use Flight Deck for final outward-facing deliverables with their actual source ingredients.

## Required semantics beyond the template

The swarm lineage, not an individual job, is the episode. Persistent memory makes the root lineage the replication cluster. Agent count is a factor, not sample size. Exogenous API tapes remain paired despite different tool-call counts. Model calls are stochastic; deterministic environment seeds do not imply bit-identical native answers. A5 is a dependent fork, with separate physical-spend and hypothetical-deployment accounting.

No `stage S2` command or generic worker copy is included while those gates are open. A future coordinator must reject unresolved launch fields mechanically; the current design validator is a documentation check only.
