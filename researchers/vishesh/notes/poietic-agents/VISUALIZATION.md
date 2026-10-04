# Poietic Agents visualization mapping

Mapping version 0.1. Planned measured replay; no measured frames exist. Every rendering binds `study`, `run_id`, `attempt_id`, `stage`, `arm`, `root_id`, `replicate`, source/design hashes and logical epoch. This is a specification, not a synthetic result.

## What a viewer should learn

Show whether identical agents actually become providers, reduce their loaded capabilities and execute with cheaper models, then whether those changes reverse after disruption. A second panel must show whether quality and total cost justify those transitions. A beautiful graph with poor answers is visibly a failure.

## Recorded signals and encodings

| View | Recorded fields | Encoding and interpretation |
| --- | --- | --- |
| Stable agent grid | `agent_id`, effective `model_id`, loaded skill/tool masks, availability | Fixed positions ordered by initial permuted ID; model color plus text label; capability count as labeled bars; unavailable node crossed out |
| Service graph | request/response IDs, provider/consumer IDs, endpoint key, bytes, response version | Directed edges for actual requests, thickness proportional to request count within an epoch; advertised but unused links are separately dashed |
| Configuration events | proposal ID, accept/reject reason, old/new definition hashes, effective epoch | Mark provider creation, capability removal/restoration, model switch and procedure version; rejected proposals remain visible |
| Outcome timeline | assigned, started, correct/fresh/on-time successes, failure classes | Successes over all assigned jobs; failed, pending and unavailable states displayed; no interpolation through missing epochs |
| Resource timeline | cumulative actual USD, tokens, CPU/GPU seconds, API calls, bytes; cost category | Separate real-money and physical-resource axes; synthetic API tolls off by default and explicitly labeled |
| Dependency and recovery | service shares, intervention type/time, provider withdrawal and restoration | Mark exogenous versus targeted intervention; never imply a role label proves causal dependence |

Quality, hidden change schedule, protected truth and targeted-intervention selection are evaluator-only. They may appear in the viewer after the relevant event, but the visualizer cannot send them back to agents. The renderer reads an observer export, has no model tool, and never influences policy RNG or scheduling.

## Time and publication

Logical epoch is the shared comparison axis; show wall time separately. Retain every configuration event and per-epoch aggregate in an append-only public-safe event stream. Live PNG updates at most every 15 seconds, on completed epochs or a terminal failure. Preserve initial, pre-change, immediate post-change and final frames. Do not encode this nonspatial experiment as invented flock coordinates.

Produce a bounded animated GIF with the step cursor and a final PNG at least 1600 pixels wide. A local HTML replay may add pause/scrub/speed controls, but public support must be verified against the current hub contract; an uploaded HTML/JSON artifact is not automatically a public player. Use the GIF and static image as the supported fallback, retain full authorized history separately, and label any downsampling. A run without events shows a pending/failed state rather than an empty successful graph.

Keep node positions and comparison scales fixed across arms within a root. Use readable text and shapes as well as color. A5 labels its common parent with A3; it is not drawn as an independent discovery. Display acquisition cost from time zero in both hypothetical deployment curves, while the physical experiment ledger counts shared prefix execution once.

## Acceptance checks before and after execution

Before native launch, feed the renderer a plainly labeled constructed fixture containing identical initialization, a provider transaction, an actual-model receipt substitution, capability removal, a stale response, missing output and provider recovery. Check field-to-pixel labels and plotted totals against independent arithmetic. This fixture qualifies rendering only. Bound render time to five seconds per frame, cap the animation at 200 frames, and keep rendering outside the run's actor budget.

After each attempt verify initial, pre-event, post-event and final states against saved receipts; reconcile totals with the outcome ledger; inspect legibility and actual animation playback on the public surface. Rendering failure records a reporting defect and retains raw results. It must not restart scientific episodes or erase failures. Link mapping version, range, omissions and checks in the post-mortem.
