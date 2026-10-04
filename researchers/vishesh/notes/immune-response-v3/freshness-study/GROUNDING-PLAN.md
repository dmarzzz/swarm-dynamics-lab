# Immune Response — evidence grounding and advice isolation

Prospective design,2026-10-04; offline preparation authorized after A8. Native dispatch is not yet admitted. [A8 post-mortem](reviews/a8-post.md) is the starting evidence. No independent review required.

## TLDR

A8's interface worked but both crash arms failed and three healthy trajectories were damaged. Separate two empirical questions: does deterministic interpretation of visible evidence improve decisions, and does exposure to the specific erroneous A8 advice worsen them? Prepare a2×2 comparison of grounding off/on and saved advice absent/present. Keep worlds, raw observations, freshness receipts, legal actions, scoring, two-tick horizon, model settings and controller-call budget fixed. No action is automatically corrected or filtered.

## Question and prediction

Grounding may help the controller distinguish RPC compatibility, readable data, required feature and current liveness. Saved erroneous advice may induce incorrect downgrades; grounding may or may not protect against it. These are unproven predictions. A8's repeated prose cannot establish advice causality without a no-advice comparison. The new no-advice controller is a strong cheaper architecture baseline; a scripted same-visible-information controller remains the feasibility reference.

The practical decision is whether any controller architecture qualifies at all, and whether advice adds harmful dependence in these cases. If no-advice succeeds and advice fails, prefer the simpler architecture for further development. If grounding helps only without advice, treat advice resistance as unresolved. If all fail, stop adding swarm complexity and revisit task interpretation. If all pass, report feasibility and no measured benefit; do not claim a grounding effect. Transport failure is inconclusive, not a behavioral zero. No automatic successor.

## Setup

Use the same three inspected development roots (healthy_fresh,fresh_crash,stale_false_alarm), seed9401. Four conditions per root: plain_solo, plain_advice, grounded_solo, grounded_advice. Twelve trajectories, two ticks each, at most24native controller calls, no new advisor calls. Advice is exactly the two A8 outputs per world, shared across both advice-present arms; retain hashes/source revision. This intentionally selected harmful-advice challenge is not representative natural advice or a claim about live multi-agent quality. One world and its four dependent trajectories form a sample unit;3roots cannot support population inference or useful population uncertainty intervals. No held-out performance claim.

All conditions use current/stale receipts. Grounding adds a deterministic evidence table computed solely from the actor-visible catalog, deployed versions, data format, required feature and cached probe. It explicitly compares gateway RPC requirement with worker RPC, data format with worker readable formats, store format with data, and feature membership. Current liveness is unknown when the probe is stale; cached liveness remains visible with its epoch. A grounding table never receives the hidden simulator state, case label, success score or correct action. It neither rejects advice nor proposes an action. Catalog facts are assumed accurate in this toy world; production authentication/verification is not demonstrated.

All conditions use the same instructions and legal-action-id-v1 output contract; only the declared evidence table and advice exposure differ. Removing advice reduces input tokens and adding grounding increases them: report those resource differences. Equal model calls/output ceiling does not imply equal token cost. No padding or extra deliberation calls. No cross-condition model memory. Rotate condition order per case prospectively; no outcome-dependent assignment.

## Protocol

Offline first: hash the saved A8 advice; verify factorial input isolation, stale-liveness unknown handling, catalog comparison arithmetic and action-space invariance. Exhaustively replay the deterministic visible reference for all12trajectories, with no model calls. Include catalog mutations and probe contradictions so grounding cannot silently substitute hidden truth. Preserve A8 unchanged.

Proposed native stage requires owner approval of this materially changed design, immutable public registration, a source-pinned launcher, fresh dedicated approved-account allocation and current budget/credential/runtime checks. Existing A8 entrypoints do not implement this stage. Model remains Anthropic-only Haiku4.5 through OpenRouter, temperature0,512outputtokens,16000inputbytes.24calls maximum, additional reservation<=USD0.457728. Preserve cumulative429requests/USD3.492196reserved under originalUSD8; historical uncertainty stays counted. Expected native execution2–4minutes, preparation/review20–40minutes. Reuse eligible exclusive researcher capacity; no new infrastructure purchase proposed. Hard stop1hour; stop on transport, invalid output, missing usage or route/cost failure; no retry. Wrong valid decisions continue the bounded assigned cohort.

## Metrics

Preserve A8 capability gates per trajectory: healthy cases2/2healthy ticks,no deployment/no health loss; stale alarm also refreshed probe. Crash finalhealthy,>=1healthy tick,>=1useful same-version restart,no configuration change/rejection. All3roots must pass for a condition to qualify. Primary outputs are the12per-trajectory gates and absolute health, useful restart, unnecessary mutation and healthy-service loss. Report within-world grounding and advice contrasts, then their interaction descriptively; no p-values or population causal claims.

Inspect every answer against the exact visible source: factual catalog/liveness errors, stale-evidence use, time-budget claims and action/reason consistency. These authored judgments are separate from deterministic scoring. A valid action is not a correct action. Retain raw response, decoded action, evidence table/hash, cached/current epoch, state transition, request/usage and original denominator. Missing outcomes remain missing, never zero-filled or replaced by retries.

## Visualization mapping

For each world, four synchronized lanes display service health over initial state and two ticks, with inspect, useful restart and harmful configuration markers. Put the raw catalog comparison, derived grounding table, advice text and actual action side by side on selection; absence of advice/table is explicit. Show12assigned/started/completed and a4condition×3world gate table. Native animation uses recorded states only; offline output is prominently scripted. No hidden state enters the actor through visualization. Historical A8 plots stay separate.

## Offline implementation evidence

[Validation](reviews/grounding-offline.json):39tests pass, all12scripted trajectories satisfy unchanged capability gates and replay. Tests cover each visible catalog relation, stale liveness, internally contradictory probes, factorial input isolation, unchanged ten-action space and request-size bounds. The prepared runner is offline-only and cannot call a provider or allocate a host. No native improvement is claimed. The next owner decision is whether to run the specified24-call diagnostic under the unchangedUSD8lineage.

## A9 owner approval and implementation admission

Owner approved this exact changed design and requested the native comparison. Execute it once as freshness-a9:24controller calls,12trajectories,originalUSD8ledger unchanged. Implement a dedicated source-pinned native entrypoint, durable partial records, allowlisted failure diagnostics and four-condition saved-data visualization; retain the tested offline mode. This supersedes the earlier pending-approval/offline-only status, without changing scenarios, conditions, metrics or resource envelope. No repeated owner/researcher approval is needed for this named scope. After completion, perform operational and scientific closeout before any successor.
