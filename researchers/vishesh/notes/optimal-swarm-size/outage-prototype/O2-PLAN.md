# O2: explicit ownership and an eight-agent outage team

Prospective bounded repair diagnostic, 2026-10-04, written before implementation. Authority: owner requests strengthening the baseline followed by a larger swarm; standing post-mortem diagnostic authority covers the necessary controlled repair check. Original cumulative USD20 cap, settled/held exposure USD2.903680 before admission; no new funds. Prior [O1 post-mortem](../reviews/outage-o1-post.md) showed duplicated repairs and a confounded contraction trigger. No contraction arm or broad optimal-N sweep here.

## TLDR

Test explicit ownership against the old duplicate-prone four-agent baseline, then compare one/four/eight contexts plus a public-state controller on matched eight-service endpoint outages. Equal tool slots within each stage; recovery, duplicate writes and cost are measured. Two variants of one development template do not identify optimalN.

## Question and prediction

Does explicit disjoint service ownership remove O1's duplicate-write failure, and does an eight-context roster improve outage recovery compared with a competent four-context roster or single context at equal tool capacity? First qualify ownership on the old four-service changing endpoint world (same development replica11): legacy-four and owned-four. Continue only if owned-four succeeds with zero unsafe commits and no within-round duplicate patch targets. Legacy failure is not required; retain either outcome. If qualification fails, stop and diagnose saved traces. This gate is bounded development readiness, not population reliability.

## Setup

Ownership is a deterministic public service-to-actor mapping: sorted service IDs round-robin over the roster. Model actors see all the same public observations and may inspect/patch only their owned services. The engine rejects off-owner proposals (counted as violations), never silently reroutes them or supplies correct repairs. Legacy-four retains the old unstructured coordination instruction. No free model coordinator, hidden answer, evaluator feedback or cross-episode memory. Histories use O1's identical rolling policy. Ownership is an interface treatment plus enforcement, not evidence of emergent coordination.

After qualification, use one endpoint-failover template, eight services, stable and changing variants, replica21. Compare single context, owned-four, owned-eight and deterministic public-state controller. Each arm has eight total tool slots per tick: single may propose eight, four actors two each, eight actors one each. Same eight-tick window, same service world/event schedule and scoring. The global tool cap rises from four to eight only for this matched eight-service stage, equally for every arm. All actors in a round drain before the next tick. Higher N has more model calls and aggregate token allowance; this is a team-policy comparison at equal tool capacity, not an equal-compute or pure-identity effect. Report these costs explicitly.

Service count/capacity scale together; endpoint failover remains the sole measured mechanism. Four-service qualification is the exact old world; eight-service demo is a workload extension, not an independent real incident. Two variants share one authored template. No inferential intervals, population conclusions, production-speed claims or optimal-N identification. Fixed order is balanced across variants: stable single/four/eight/controller; changing reverse. Different semantic mechanisms and untouched incident holdouts are deferred until this smallest comparator-repair diagnostic is interpretable.

## Protocol

Offline: unchanged O1 regressions; exclusive ownership partition, off-owner rejection, equal total tool slots, eight-service reference recovery, exact four-service compatibility, independent checker faults, finite manifest/call allowlist, source/admission/ledger accounting checks. Qualify then conditionally demonstrate, ten assigned episodes maximum. No automatic successor.

Same owner-approved OpenRouter Haiku4.5 route pinned to Anthropic, no fallback, local-only bounded credential relay. To accommodate eight patches, all O2 arms use the same1024 output-token ceiling and24000-byte request ceiling. Conservative reservation30000 input +1024 output tokens at verified USD1/5 per million plus10% uncertainty = USD0.038632/call. Worst-case qualification64 calls plus demonstration208 =272 calls, USD10.507904. O2 hard subcap USD11 inside original20, per-episode USD3. No new machine purchase; reuse an exclusively claimed approved-account worker with current verification. Historical holds retained. Per-request reservation precedes dispatch; no retries. Stop on first transport, schema, route, accounting, claim or publication fault, draining charged in-flight requests. Maximum watchdog2hours; fresh claim must cover watchdog plus closeout. Pricing and model catalog reverified before launch. Actual cost and retained fee uncertainties reported separately.

Original ledger remains sole authority on its existing host. No migration or clone-as-new-authority. Reconcile915 previous calls, exposure2903680 microdollars and original cap before launch. No dispatch without exact source/runtime, immutable public registration and condition TLDR, owner scope, current account/claim, native credential route and offline checks. Researcher review not required by owner direction.

## Metrics

Primary descriptive endpoints: full terminal recovery with zero unsafe committed configurations; final service predicate fraction. Secondary: health over ticks, earliest all-healthy tick and persistence, duplicate patch targets, rejected off-owner actions, stale writes, model and tool calls/concurrency, wall time, token/cost exposure. Never confuse simulated ticks with real latency. All assignments reconcile as planned/started/terminal/graded/analyzed/unstarted; qualification-failed unstarted cells remain missing. Recompute all terminal grades from saved state, inspect every effective model request/visible output for misses, locate first divergence and preserve alternatives. No model-performance claim from scripted validation.

## Closeout and usefulness

Inspect saved native replays, verify every uploaded artifact by hash, invoke offline native finalization, complete eleven-dimension scientific assessment and release only this study's claim. If single/controller matches larger rosters, retain that useful negative result and recommend the simpler solution on this support. A larger roster is not a desired outcome. Any subsequent collection must have a concrete evidence-led purpose and its own finite plan; no favorable-result reroll.
