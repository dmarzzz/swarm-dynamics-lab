# Incident Q2 proposal: contract repair and paired readiness

Prospective offline preparation, 2026-10-04. **Not admitted or authorized for paid execution.** Q1 remains failed5/9; its source, scores,9/9 threshold and traces are unchanged. This document precedes implementation of the new offline contract. Read [Q1 post-mortem](../reviews/incident-q1-post.md) first.

## Question and decision

Can a batching singleton and a fixed coordinated three-context baseline each investigate, diagnose and safely complete all nine necessary development case types under one explicit contract and equal total tool capacity? This is a readiness screen, not a treatment-effect estimate. Require9/9 correct per arm, zero unsafe attempts and zero operational faults. Both must pass before considering a scaling study. Do not replace an incapable singleton with a larger team and call that a swarm-size result.

## Prospective contract repair

Use one typed tool vocabulary: `query`, `patch_service`, `rebalance`, `finish`, `wait`. Service IDs never become evidence handles. Reveal issued/pending handle sets from the public query history; exhaustion means all relevant records in this synthetic incident scope have been visited. A serial `local_check=pass` excludes a local fault at that hop; it does not prove downstream health. Only an observed unavailable record justifies missing-evidence escalation. Reject mutations before complete investigation or after observed unavailability.

Diagnoses have exactly `service`, `cause`, `evidence` (nonempty handle list). Accepted causes are capacity, revision, protocol and allocation. Freeze this small alias map before new native outputs: capacity_shortfall→capacity; revision_mismatch→revision; protocol_mismatch→protocol; shared_allocation→allocation; shared_pool→shared-pool for the entity only. These are lexical aliases of the same typed concept; no fuzzy, free-text or model judging.

An allocation diagnosis targets `shared-pool` and cites the pool record plus all affected and unaffected service metrics needed to establish feasible total demand. Service-level allocation diagnoses are not automatically equivalent to a system-level feasibility claim. This restriction must be actor-visible, including the full citation requirement. Do not reinterpret Q1's service-level output as a pass. Diagnosis lists remain exact and duplicate claims fail. Separate identified fault, citation support, decision, attempted/applied action, physical recovery and safety; justified escalation has no required fault diagnosis or recovery.

Coverage uses the issued-handle set intersected with successfully returned known handles. Unknown/rejected handles neither satisfy nor poison coverage; repeated queries cannot invent progress. Reference and negative fixtures must exercise those conditions, incorrect citations, missing repairs, wrong entity aliases and shared resource limits. Q1's underlying world remains untouched; implement a versioned contract wrapper.

## Paired cohort and independence

Nine matched development cases: three authored structures (independent, serial, coupled/mixed) × fault, clean, unavailable evidence. Reuse seed31 deliberately to diagnose the contract repair, with the original files retained. These inputs were inspected and are **not fresh holdouts**. Eighteen planned arm episodes, one native sample per arm/case; three semantic template roots and dependent variants, not18 independent real incidents. No confidence interval, significance test, or population accuracy claim. A later main study needs separately constructed independent incidents and protected evaluation families; renaming alone does not provide them.

The strongest simple reference is the existing deterministic public-evidence controller, qualified against the repaired contract. It is same-author, template-aware development engineering. Publish its results without claiming zero engineering/infrastructure cost or independent authorship. No hidden gold enters native contexts or the fixed coordination policy.

## Equal capacity and fixed coordination

Both arms receive the same full public incident history at the start of each round, at most ten rounds, and **three total evidence/action units per round**. A queried handle or single service-field patch costs one unit. An atomic three-service rebalance consumes all three units in both arms. Finish/wait consumes no tool units but still uses a charged model response. Newly discovered handles are unavailable until the next round; repairs cannot consume same-round unseen evidence. Never give the three-context team nine tools while calling this an agent-count comparison.

Singleton: one context can propose up to three tool units in a typed batch, or finish with all diagnoses. Fixed-three: three persistent contexts, one response each per round, one tool unit per context except the shared repair below. Query candidates are sorted pending public handles distributed by position modulo3 each round; no evidence-aware routing. All receipts and proposals are shared at the next round boundary. Ordinary repair ownership is sorted service index modulo3. The first context owns shared-pool diagnosis and can propose atomic rebalance; peers must wait for that round, and the broker charges all three units. Same-round conflicts are explicitly rejected and logged, never silently deduplicated into uncharged help.

The team finishes only when all three return finish in the same round, with matching decision. Merge typed diagnoses by exact canonical pair, union their cited handle sets, and retain all original proposals. Conflicting claims or decisions keep the episode unfinished; no model coordinator, voting over truth or hidden scorer feedback. Claims must respect service ownership; shared-pool belongs to context0. Singleton has the same public ownership map but owns all partitions. This is a deliberately interface-assisted coordinated baseline. Equal tool capacity does not equal model compute: team has up to3× calls, duplicated context and communication. It is not a pure identity effect or evidence of emergent coordination.

Before native use, implement/freeze this broker and batch adapter and verify serial disclosure, equal capacity, shared atomic charge, disjoint repair ownership, no free coordinator, finish aggregation, shared context, and reference completion within ten rounds. The current offline contract wrapper alone is **not** a launch-ready paired runner.

## Collection, scoring and stopping

Alternate arm order by case index, fixed and disclosed. Each case starts an independent context history; no operator conversation, previous case answers, evaluator state or gold. Retain frozen manifest, request/response/parse, assigned ownership, proposed/admitted/rejected tool units, receipts, per-round evidence coverage, claims, actions, recovery, safety and costs. Freeze the full roster even if a systemic fault prevents later starts. Keep semantic failures in the nine-case denominator and continue the remaining cases to localize defects. First transport/schema/accounting/publication fault stops scheduling with no retry or fallback. No pooled intermediate majority or post-hoc threshold change.

Report case-paired descriptive outcomes, first divergence after acquisition, canonical-label sensitivity versus exact spelling, calls/tokens, cumulative actual and held cost, and measured wall time separately from simulated rounds. Component scores cannot silently override the joint endpoint. Recompute all grades from retained traces; inspect every miss and matched controls. Success of both arms permits proposing a subsequent study; it does not automatically dispatch one.

## Cost and machine envelope

Proposed route remains the qualified OpenRouter Anthropic Haiku4.5 endpoint, temperature0, maximum1024 output tokens and24000 serialized request bytes per physical call, no automatic retries. Recheck endpoint/pricing before any dispatch. Conservative reservation remainsUSD0.038632/call.

At most9×10=90 singleton calls and9×3×10=270 fixed-team calls: **360 total**, maximum reserved **USD13.907520**, proposed attempt cap **USD14**. Singleton case capUSD0.40; team case capUSD1.20. Refuse dispatch before serialization if a bound is exceeded; a bound failure ends the attempt without silent truncation or retries. Include all model roles and coordination costs; scripted broker/controller has no model call. Current cumulative settledUSD3.418709 plus retained unknown/fee exposureUSD0.381547 givesUSD3.800256 exposure under the originalUSD20 ceiling. Reserving the fullUSD14 would leaveUSD2.199744; no ledger reset, tier increase or release of old holds. There is no new spending authorization in this proposal.

Need one current exclusively claimed existing worker in the approved Dmarz account, exact source/runtime, original single-writer ledger, finite relay contract, current public immutable plan/condition TLDR verification and native admission. Existing allocation is released; obtain a fresh claim only after appropriate scope approval. No new infrastructure purchase is included; if incremental infrastructure is needed, reprice within the same envelope before admission. Claims, credentials, account verification and ledger refresh remain private.

## Current disposition

Offline contract implementation and unit validation are authorized preparation. Paired native adapter, frozen request-size/reference trace checks and admission remain outstanding. Present the concrete artifact and cost bound for the next scope decision; **no paid run, allocation or40-agent stage is authorized by this plan**. Finalize any future attempt with operational and scientific post-mortems, all-case reconciliation, uncertain costs retained, worker/relay shutdown and claim release.
