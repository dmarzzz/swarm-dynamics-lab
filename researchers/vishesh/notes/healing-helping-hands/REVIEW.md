# Healing Helping Hands: pre-revision review

2026-10-04 UTC. Local code, manifests, event journals, rendered replay and current public protocol reviewed after pulling swarm-lab main at 951142a. This is a self-review by the implementing assistant, not an independent cross-researcher review or a gate-passed survey.

| Area | Assessment of routing v1 | Required change |
|---|---|---|
| Scientific question | Useful recovery concept, weak LLM application. An exact routing rule solves it cheaply. | Evidence curation with short semantic decisions; distinguish engineered memory repair from model reasoning. |
| Controls | Exact algorithm and no-damage controls exist; only one map. Hybrid adds compute and sees Qwen's answer. | Repeated corpus seeds, independent attachment, same-Qwen extra-head control, paired tapes and explicit cost accounting. |
| Measurement | Validity and shortest paths correctly separated; recovery affected by unequal initial exposure. | Fixed source withdrawals across arms, score invalidations separately from erasure, full trajectories and integrated post-event loss. |
| Robustness evidence | Six worlds are not six independent replicates. Zero invalid outputs is not proof of reliability. | Seed-level contrasts, local fault injection, one terminal record per assignment, no success-only reporting. |
| Agent specification | Weights shared; per-node path state; exit fixed. RULE string and actual prompt diverge; model tag mutable; Laya probabilities lack argmax check. | Exact executable prompts, digest verification, pinned Laya source/weights, explicit independent evidence, finite normalized distributions and choice validation. |
| Run architecture | Deadline checked only between rounds; thread-pool shutdown may wait. Concurrent budget check double-counts outstanding jobs and can overshoot per-round Laya caps. Three provider errors reset on success; failed Laya calls undercounted. | Sequential bounded local calls with atomic pre-dispatch budget reservation; explicit timeouts, wall budget checked before each call; failed calls count; no automatic decision retries. |
| Failure preservation | Event journal rewritten at success; exception occurs before some failing events are saved. Qualification failure mislabels first algorithm world failed though it never ran. | Append-only call journal before and after dispatch, distinct attempt failure vs not-run assignments, durable round checkpoints and terminal outcomes. |
| Reproduction | Source hashes exist, but actual route certificates and cache references are missing from replay traces; code absent from public plan. | Publish portable instrument, seeded fixtures, frozen extraction tapes, state hashes and replay data; reproduce deterministic dynamics from tape. |
| Visualization | Attractive 200-cell display; hover follows contemporaneous next hops rather than stored route certificates. Partial replay can show a past frame under a later slider label. | Versioned scenario timeline, explicit extraction/propagation semantics, claims and source identities, paired controls, no animation beyond recorded frames. |
| Spec/plan | Public plan registered only after execution; documented failure retained. Prototype qualifications changed repeatedly. | New public immutable plan before implementation runs; check that registration matches executing source, not merely any valid README. |
| Scenario | Damage plus erasure bundled; shortest paths suffer different disruption than model detours. | Separate no event, withdrawal, erasure and combined events; no irreversible unique-information loss in the erasure control. |

## Trace checks

Qwen-control made 288 non-minimum decisions among 2,126 decisions with available routes; Qwen-damage 310/2,236. Hybrid-control 268/2,090 and hybrid-damage 290/2,200. Across the final ten frames, shortest-route fraction varies from 5% to 7%, so final 6.5% is a snapshot, not convergence. Final valid routes are 100% in all arms. These are within-world diagnostics, not independent samples.

## Failed attempts and disposition

- Missing `laya.backends`: installation/package failure before inference. Pin both source checkout and cached weights, qualify imports first, record it as initialization failure, never an algorithm failure.
- Qualifications at 3/5, 5/10 and strict-tie 6/10: model/task or scoring failures, not network failures. Preserve them. New semantic task uses balanced three-way fixtures and disjoint pilot seeds; no retries until a changed protocol is published.
- Missing registered plan: process failure already recorded on the hub. New launcher checks exact committed source and registered plan, and saves the receipt before model load.
- Cloudflare login expired: publication infrastructure failure. Hub publication still works; use the existing live hub for verified results and provide a local replay. Do not promise standalone hosting until it is verified.
- Full archive publication blocked by approval review: avoid silently republishing that archive. The new user-authorized design, implementation and synthetic results are separate, reviewable outputs; preserve the original archive locally.

No design can promise zero failures. The target is reliable execution, explicit failures and recovery paths, honest negative outcomes, and no silent fallback to scripted answers.
