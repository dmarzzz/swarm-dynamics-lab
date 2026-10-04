# AI Village memory and handoff replay pilot

Status: prospective exploratory design, 2026-10-04. Not an executable packet or launch approval. [Setup and gates](SETUP.md). [Source coverage and study mapping](README.md).

## TLDR

Test whether a structured, evidence-linked handoff helps a fresh agent recover task state better than a prose handoff under the same context allowance. Compare both with recent-history and retrieval baselines on frozen AI Village episodes. Score supported facts, stale claims and admissible next steps; do not score imitation of historical actions. Proposed main sample: 24 task clusters, four paired arms. This is a feasibility pilot, not evidence about whole-swarm performance.

## Question and prediction

Does explicit status, provenance and unresolved-work structure improve grounded task-state recovery after a context reset? The candidate prediction is fewer stale or unsupported commitments than prose memory. The structured approach must also justify itself against inexpensive retrieval. A null, adverse or retrieval-dominated result argues against adding a more elaborate handoff mechanism.

This is a hunch informed by source documentation and existing study post-mortems. The corpus has not been inspected for suitable episodes; no exhaustive prior-art survey or novelty claim is made.

## Setup

1. Pin dataset revision `838b4150303ca8228e8edb432d8b8ccae353d258`, source file digests, UTC boundaries and schema version. Begin with table indexes and text; fetch screenshots only when a candidate's label requires them. No full image-archive download by default.
2. Identify a task cluster and a consolidation/handoff cutoff from recorded events. Join turns through `session_id` to sessions and agents; join chat through event message IDs. Use `event_index` for event order and UTC timestamps for cross-table alignment. Ties, updates after the cutoff and unverifiable visibility are quarantined, not resolved with arbitrary ordering.
3. Create an explicit eligible archive: the focal agent's own observable actions/results, verified room-visible messages and goals known by that time. Exclude others' private goals, unshared memories, later corrections and evaluator labels. Export-time room/goal fields do not establish past access. If actual historical visibility cannot be established, exclude from the primary cohort or label a separate constructed-information task; never silently pool the two.
4. Choose one cutoff per connected task cluster. Link clusters that reuse artifacts, conversations, goals or dependent claims before splitting. Partition by connected component and time; hold out later tasks and report scaffolding/model strata. If there are too few independent groups, shrink the claim and amend the plan before outcomes, not the definition of independence.
5. Make the task a structured recovery record: current objective, supported completed work, unresolved blocker, superseded claim and admissible next-step category with source IDs. Require at least one decision-relevant fact outside the recent window. Include no-change and genuinely uncertain cases, not only dramatic failures.

Actor startup is a fresh process/request with no operating-assistant context, hidden history, inherited provider session or persistent cache. Pin system prompt, exact model/provider, tokenizer, decoding, output schema and dependency versions. Hash the complete delivered inputs and every context selection. Seeds reproduce assembly/order, not guaranteed hosted-model responses. Synthetic agent identifiers and metadata must not reveal condition or label.

## Protocol

| Arm | Available packet | Construction |
|---|---|---|
| R Recent history | Fixed most-recent allowed records | Deterministic ordering and truncation |
| B Retrieval | Task-query retrieval from the identical eligible archive | Deterministic BM25, frozen query/tie-breaks, no label-derived query |
| P Prose memory | Prose summary of the identical eligible archive | One fresh bounded writer call |
| S Structured memory | Facts, status, source IDs, unresolved work and superseded claims | One fresh bounded writer call with the same model and input allowance as P |

Primary contrast: **S minus P**. B is the strong practical baseline; R tests recency loss. P and S writers see the same prefix and generic handoff instruction, not the evaluation questions or labels. They have the same output-token cap; all four decision packets have the same maximum context allowance and common task instructions. Record actual tokens and total construction/inference costs. Equal caps are not equal information or equal spend: assess the end-to-end representation method, not a pure formatting effect. No truncation may break a source record silently.

Proposed allocation, conditional on the inventory:

- 8 development clusters for visibility, label design, extraction and baseline debugging. Exclude permanently from reported evaluation. No model development calls are allocated in this draft.
- 8 disjoint qualification clusters, four arms: 32 decision calls plus 16 memory-writer calls, at most 48 calls.
- 24 sealed evaluation clusters, four arms: 96 decision calls plus 48 memory-writer calls, at most 144 calls.
- Maximum proposed collection: **192 requests, 128 decision outputs, 64 generated handoffs**. No automatic retries, expansion, cross-model sweep or repair allowance. Additional repeats do not create new clusters.

Before collection, two separate annotation passes must establish a fact inventory and acceptable answers from evidence available at the cutoff. A second blind scoring pass can be performed by the owning researcher; it is not an independent researcher approval. Resolve disagreements, report unresolved labels and exclude unanswerable cases prospectively. Future data may audit historical claims separately but cannot define information the actor should have known. Do not choose cases according to which experimental arm wins.

Offline acceptance: timestamps/joins resolve; future and cross-agent private evidence cannot enter any actor payload; opaque names preserve payload invariance; reset is clean; budgets include both writer and decision calls; label/scoring checks and unknown/missing outcomes work. Archive a mutation test that inserts future evidence and confirms it is excluded. Use hand-authored fixtures for software tests, not sealed evaluation cases.

Qualification must exercise the complete context, not only an empty-history version. Proposed screen: all 48 scheduled calls valid, every citation resolves to visible evidence, and at least 7/8 task-state recoveries correct in the stronger of P/B with no unsupported high-impact next step. Freeze the final threshold and label rubric after offline development and before S0. If the baseline is at ceiling, report it and do not escalate just to obtain a treatment effect. A writer failure makes its decision unavailable; retain both statuses. Stop collection on the first transport failure or safety/data-boundary violation, retain reservations and close out the partial attempt.

## Metrics

Primary endpoint: per-cluster binary task-state recovery, requiring all predeclared critical facts, correct stale/uncertain status and an admissible next-step category. Additional correct noncritical details cannot compensate for an unsupported critical commitment. Secondary: critical-fact recall, unsupported/stale claims, citation validity, useful abstention, tokens, latency and total cost. Report scalar/rule-based extraction performance where a task permits it; a simple method solving the task is a result.

Use equal cluster weights and paired S−P differences; report the full paired outcome table, discordant cases and an interval respecting pairing. Show separate comparisons to B/R as exploratory. With 24 independent clusters, a single binary rate near one half has an approximate 95% margin of 20 percentage points; a paired difference may be substantially less precise. This is not powered for modest gains. If connected components reduce the effective sample, report that count and widen the claim limits.

Account for assigned, started, terminal, valid, scored and analyzed units separately. Present completion and score coverage; missing model responses are not measured wrong decisions or zeros for an unobserved treatment difference. Report conservative success bounds over all assigned units and completed-pair estimates with the missingness limitation. Do not silently replace failed episodes.

Advance only to a new, separately planned study if the pilot demonstrates usable labels, competent baselines and plausible residual headroom. A provisional practical signal is at least three additional correct clusters for S over P out of 24 with no additional unsupported critical commitments; report uncertainty even if this descriptive screen passes. Retrieval matching or exceeding S favors retrieval. No automatic larger run follows.

## Resources and release

Source inspection and offline preparation need no new machine or hosted model. Model/provider choice, token ceilings, exact request envelope, data-transfer terms and privacy screening remain unresolved; therefore no dollar estimate is claimed yet. If adopted as a Theseus or Dissenter successor, charge its existing cumulative ledger and cap. Naming this dataset lane does not create a new allowance. Obtain the concrete updated-plan decision and current exclusive approved-account allocation before model collection.

Freeze and publicly register the immutable condition-specific plan before each admitted stage. Raw licensed episodes, labels with sensitive source text and requests remain in the authorized private evidence store; publish hashes, original methods and safe aggregate results. Check detailed terms before any redistribution/provider transfer. Cite AI Digest/AI Village and arrange the required publication notification without sending a message under this planning task.

Visualization: private episode replay shows allowed evidence arriving, consolidation cutoff, each arm's retained/omitted facts and scored decisions. Public fallback is an aggregate paired-outcome table and missingness timeline without raw source text. This is a proposed mapping, not an implemented renderer.

Every stopped or completed attempt gets operational reconciliation and a scientific post-mortem against the existing run-quality rubric. The next session reads that evidence before changing sampling, memory or scenarios. Offline replay findings never become a claim that the original Village swarm would have behaved differently.
