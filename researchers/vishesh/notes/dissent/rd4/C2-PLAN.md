# Completing recovery evaluation with verified transport

Prospective S4-C2 amendment, 2026-10-04, before transport-admission implementation. Scientific protocol: [RD4](PLAN.md). Prior continuation: [C1 plan](C1-PLAN.md), [C1 post-mortem](reviews/S4-C1-POST.md).

## TLDR

Finish only the 38 still-unstarted trajectories (152 decisions) from the same 576-decision comparison. Preserve all 424 prior terminal decisions and all failures, even those that never reached the provider. Require an end-to-end non-inference relay probe before dispatch and every trajectory. Same qualified model, actor, policy, evaluator, source hashes and budget; no failed request is retried. Report the final combined cohort with segment and infrastructure-failure bounds.

## Question and prediction

The scientific contrasts remain fixed. The engineering prediction is that checking the actual forwarded HTTP endpoint prevents dispatch into a dead tunnel. Passing that health check is not model qualification or guaranteed future connectivity. No scientific improvement is assumed.

## Setup

The immutable combined prefix is derived from S4-A1's 104 terminal assignments plus C1's two terminal assignments. Validate their exact disjoint union and unchanged original order; it has 106 terminal and 38 planned trajectories. Store parent file hashes and source-segment hashes. The original qualified decision core remains bc0a79cd2f90fb13262a2b625a2e029fc0c01e7b7e51d7870c7550e0fb3dea72; only the external continuation wrapper gains readiness checks and a configured subset count. Dmarz's current exclusive claim remains required.

## Protocol

1. Publish this amendment and C1 post-mortem before implementation. Preserve both failed segments and their original records, calls, summaries and receipts.
2. Build the combined parent manifest from the two nonoverlapping terminal partitions, not from outcomes. Freeze parent and continuation hashes. Reject ambiguous or duplicate rows. Inherit all 158 saved request records, including 11 failed records; they remain successes/failures exactly as saved and are never sent again.
3. Start the existing bounded relay and reverse tunnel. Before dispatch, verify that GET to the remote loopback decision port returns the relay's default 501 response. This is a non-inference request: no token reservation, credential transmission or model invocation. Check the same condition before marking each trajectory started. If unavailable, stop with that trajectory still planned. Do not retry a model request to repair connectivity.
4. Verify immutable public registration, actual host, current exclusive claim, exact qualified core, source/parent hashes, and passing Q4 summary. Use the new continuation ID S4-C2 and condition-specific TLDR. Execute only the 38 planned trajectories, unchanged policy order, per-trajectory state reset and original two-check cap.
5. At most 109 further provider reservations fit below the 481 lifetime ceiling; current provider count remains 372. Original $1 API/$2 total approval persists. One worker, 45 minutes, five-new-failure stop. No automatic extra batch. A health failure itself is recorded as a setup/transport stop, not as a fabricated model answer.
6. Reconcile separate segments and the combined 576 assignments. Preserve all failed rows and score with the original all-assigned denominator. Audit exact saved-response replay, segment immutability, per-arm metrics and measured visuals. Release resources after verified artifacts.

## Metrics

Report C2 assigned 152, terminal, missing, new versus inherited requests, health-stop status, costs and elapsed time. The combined denominator remains 96 per policy. Separate valid model mistakes from infrastructure-related unknown outcomes and report worst/best outcome bounds for the latter; do not impute successful answers. Keep root pairing and direction/regime summaries. Distinct worker request records are not automatically provider calls.

## Visualization and limits

Use RD-V4 and visibly label all contributing segments. Prior partial figures remain archived. Exact records supply action, memory, alias suppression and fresh recovery frames; no invented reasoning. The cause of SSH exit 255 is still unknown. This amendment fixes inadequate readiness admission, not network reliability or prior scientific missingness. The authored-template and formal-review limitations remain.
