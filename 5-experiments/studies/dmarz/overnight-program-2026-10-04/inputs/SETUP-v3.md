# Setup record: 180-agent overnight program, proposed v3

Based on the [setup runbook](../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md) and [setup record template](../../../../tooling/agent-experiments/templates/experiment-setup.md).

Status: model and prospective population selected. No native experiment, qualification, paid request, server claim or session loop launched by this task. The owner asked us to consider three machines and select an affordable OpenRouter model. V3 supersedes v2; historical versions remain frozen.

## Decision

- Owner: dmarz. Population: 180 persistent identities, 60 per host; ten communities of eighteen, six community members on each host.
- Model: qwen/qwen3.7-flash, only provider alibaba, reasoning disabled, provider fallbacks disabled, JSON-object output with local validation. Observed canonical version: qwen/qwen3.7-flash-20260727. Exact request settings are in selected-model.json.
- Price checked around 09:01 UTC, 4 October 2026: $0.03/M input and $0.13/M output in the under-32K prompt tier. Study input cap is 8K. Token scenarios for all 6,880 calls: $0.68 at 2K/300 tokens; $2.55 at 8K/1K. Proposed cap reduced to $5, subject to verified remaining authority. This record creates no allocation. Claude management sessions and credit-purchase fees/taxes are excluded from token estimates.
- Candidates currently online and unclaimed: sim-dmarz-2 and sim-vishesh (4 CPUs / about 7.8 GiB each), research-01 (2 CPUs / about 3.8 GiB). Refresh ownership and claims before work. sim-dmarz-3 is now claimed and excluded. No new server requested.
- Actual per-IP constraint remains unidentified. Three machines do not create three provider quotas. Global and per-host pacing are both required.

## Gate evidence and exact next action

| Gate | Status | Required next step |
|---|---|---|
| Research and current directives | Pending | Verify applicable runbook/research gates for the named successor; no silent inheritance of waivers |
| Model choice | Selected, unqualified | Verify pinned endpoint and reasoning-off behavior in the bounded qualification |
| Evaluator | Pending | Freeze checkable task and independent scorer by T+30; another task's shortlist is not an implementation receipt |
| Instrument | Unbuilt | Bounded sparse graph, complete checkpoint restore, and global accounting authority by T+60 |
| Admission | Pending | Verify current quota, exact manifest, remaining budget and all three host claims |
| Qualification | Unrun | At most two 200-call small fixtures of the selected model, then one 180-call scale check; pass by T+90 |
| Main collection | Unrun | 900 shared prefix + 2,700 ordinary + 2,700 source-aware continuation calls |
| Closeout | Future | Stop new dispatch T+300; reconcile T+330; deliver T+420 |

Exact next action is prospective implementation: freeze the evaluator, validate the thin wrapper and complete admission receipts before any qualification call. Current stage is design/model selection; there is no native launcher.

## Fixed operational envelope

- One world and one checkpoint. 180 interacting identities are dependent; no independent-world confidence claim.
- Five shared rounds, then fifteen rounds per sequential continuation: 35 executed rounds, 6,300 main calls. At most 180 active identities at once.
- Qualification ceiling: 400 small-fixture calls plus 180 scale-check calls = 580. Total ceiling 6,880. Second small slot permits one bounded repair on fresh fixtures using the same selected model, not another model search. A failed scale check ends launch.
- Four fixed local neighbors and one cross-community neighbor; previous-round messages only. Input ≤8,000 tokens, billed output ≤1,000, public message ≤160 and retained summary ≤800. Validate local schema; no automatic model repair calls.
- Start two in-flight requests per host/six globally; ceiling three per host/nine globally, only within verified provider limits.
- One reservation authority spans all hosts. Local file locks alone are insufficient. Fence branch-qualified assignments, reconcile ambiguous sends, fail closed if authority is unavailable.
- Full checkpoint restores world, agent memories, source assignments, messages, schedules and RNG. Ordinary-first order/model stochasticity remain limitations.
- At 0.75 accounted calls/s plus 25% overhead, main collection is 175 minutes, leaving 35 minutes. Max-context scale-check round latency and queue tails must support this; no measured runtime is claimed.

## Source and artifact index

Current program: program.json / program.html. Selected request template: selected-model.json. Generator: src/build_program_180.py, reusing the historical display renderer in src/build_program.py. Rebuilding the document does not launch an experiment.

Historical plans/setup records are frozen under inputs/program-v1.json, inputs/program-v2.json, inputs/SETUP-v1.md and inputs/SETUP-v2.md. Live model catalog, endpoint quotes and the sanitized fleet audit are also frozen in inputs/. V3 preserves all 21 timestamped historical evidence entries. methods-review-v3.json records the separate Codex subagent's arithmetic review; this is same-researcher review, not independent implementation or different-researcher approval.

## Failure and handoff

Exact task/source catalog, graph, prompts, scorer, manifests, hashes and launcher are pending. If readiness fails, deliver the saved-data explorer and audit. Preserve failures and all assigned outcomes; do not show mocked/partial records as a completed native swarm. Future closeout records measured costs, source hashes, artifacts, post-mortem and resource release.
