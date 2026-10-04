# Regrowth 200: distributed route repair

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — The added Laya heads did not improve final routing quality on this one map; both model arms remained far below exact routing on shortest paths. Basis: Descriptive trajectories only; model arms share100%valid but6.5%shortest final routes, so fast recovery to poor quality is not advantage. Hybrid adds compute and sees Qwen proposals. Missing original public registration is preserved separately.
- **sample_size_summary:** One fixed map × 3 architectures ×damage/control =6/6 worlds;200 cell identities,80 rounds. No replicated map sample.
<!-- experiment-evidence:end -->

**Registration status: retrospective repair.** The pilot ran with a local protocol and source hashes, but no plan URL was registered on the live hub. That is a process failure, recorded in [REGISTRATION-FAILURE.md](REGISTRATION-FAILURE.md). This public explanation was added after the results were known. It is not a preregistration or a confirmatory study.

## TLDR

Can 200 agents rebuild useful routes after a door closes and some agents lose their memory? We compared Qwen3 0.6B agents with the same swarm plus Laya decision heads on 20 cells, and with a deterministic routing algorithm. Each condition ran once with damage and once without. We measured whether routes reached the exit, whether they were shortest, how quickly they recovered, and inference cost. Both model swarms restored valid routes, but only 6.5% were shortest at the end; Laya did not improve those final outcomes on this one map.

## Question and prediction

TLDR: does adding a second model to some local agents improve collective route repair? The intended question was whether local neighbor communication restores useful paths after disruption, and whether Qwen plus Laya performs better than Qwen alone. No directional prediction was publicly registered before this pilot. Any claim about a general benefit of heterogeneous models remains untested.

The useful distinction is connectivity versus quality: a long detour can reach the exit while still being a poor route. A low recovery time can also reflect avoiding the damaged doorway before it closed.

## Setup

A 20 × 10 warehouse contains 200 cell identities and two partitions with doors. The exit cell is fixed by the environment; 199 cells make routing decisions. Qwen3 0.6B weights are shared, with separate route state and exact-input decision memory per cell. In the hybrid arm, IDs 5, 15, …, 195 also query the pinned Laya choice model, which sees Qwen's proposal and selects the final local action. This adds compute, not agents.

Each agent receives local candidate directions and neighbors' previous-round route lengths. It has no global map or evaluator distances. The controller carries path-vector certificates and excludes routes that contain the receiving cell, preventing loops. This is engineered routing with model choices, inspired by local-update damage tests; it is not a trained neural cellular automaton.

## Protocol

Six worlds: algorithm/control, algorithm/damage, Qwen/control, Qwen/damage, hybrid/control and hybrid/damage. Every world uses the same fixed map and 80 synchronous rounds. Before updates at round 40, damaged worlds close one doorway and erase route memory in a 4 × 4 region; controls continue unchanged. All 200 cells remain connected. Same-round observations are frozen, and actions apply together. Exact repeated inputs reuse that cell's earlier decision.

Qwen uses temperature zero, thinking off, a 1,024-token context and a 24-token output cap, with at most four concurrent calls. Laya runs on CPU. Qualification prompts were revised during development; both models reached 8/10 when equally short routes were accepted. This was adapted development qualification, not held-out validation. Four earlier stopped attempts are retained locally. No confirmatory stage ran.

## Metrics

The primary descriptive endpoint is the fraction of cells whose stored route reaches the exit through currently open links. Report shortest-route fraction and mean excess hops separately. Recovery is the first round after damage with at least 95% valid routes for three consecutive rounds. Also record invalid decisions, calls, tokens and wall time. The algorithm supplies an achievable local-information baseline; no-damage worlds separate disruption from ordinary evolution.

A world/map is the experimental unit, not an agent or a model call. With one fixed map, these are descriptive trajectories, not replicated estimates. Hybrid versus Qwen bundles extra compute, a second model and access to Qwen's proposal. It does not isolate diversity or independent checking.

## Results

All six worlds completed. Both model arms ended at 100% valid routes and 6.5% shortest routes, with and without damage. The algorithm ended at 100% on both measures. In damaged worlds, mean excess length was 11.97 hops for both model arms and zero for the algorithm. Laya overrode two decisions per world without changing those final endpoints.

The model arms met the recovery threshold after four rounds, versus 18 for the algorithm. This is not evidence of superior repair: their long detours sustained less initial damage. Final-pilot totals, including its qualification, were 9,446 Qwen calls and 486 Laya calls over 596.424 seconds, with zero invalid decisions. Prior development adds 34 Qwen calls and 25 Laya calls. No paid inference API or new cloud compute was used.

## Run guide

| Run suffix | What this run tests |
|---|---|
| pilot-v4-algorithm-control | Can exact local routing establish and retain optimal paths without disruption? |
| pilot-v4-algorithm-damage | What recovery is achievable with exact local decisions after the same disruption? |
| pilot-v4-qwen-control | Can tiny-model decisions establish and retain useful routes without damage? |
| pilot-v4-qwen-damage | Does that swarm recover connectivity and route quality after disruption? |
| pilot-v4-hybrid-control | Does attaching 20 Laya heads change ordinary route formation? |
| pilot-v4-hybrid-damage | Does the composite swarm change post-damage recovery and route quality? |

## Next run requirements

Before launch, publish a versioned plan, register its URL and a reader-facing TLDR, verify both through the public page, and store a preflight receipt. Each run must identify its exact condition and comparison. See the [documentation contract](../experiment-documentation/README.md). Follow-up research needs repeated held-out maps, randomized head locations, equal-compute extra-Qwen controls, a Laya head blinded to Qwen's proposal, and matched initial damage exposure.

[Live experiment](https://swarm-live.pages.dev/#/x/regrowth-200)

## Prospective design amendment 2026-10-04

Incorporating [Dmarz's Regrowth recommendation](https://github.com/dmarzzz/swarm-lab/blob/e0a31706cdf1fb1d3864370b04f29bd4f93e2682/researchers/dmarz/notes/next-experiments-2026-10-04/README.md), a follow-up should make coordination necessary through partial observations or changing constraints and evaluate it on independently generated maps. The completed six-world pilot and its retrospective-registration label remain unchanged.

Use a **common absolute route-quality target** for every arm, alongside connectivity, excess hops and integrated quality loss after damage. Match pre-damage quality and damage exposure where the estimand permits; otherwise report those differences explicitly. Returning quickly to a poor or minimally disrupted baseline is not superior repair. Keep the exact local-information routing algorithm, and charge the hybrid's extra calls against an equal-budget extra-Qwen control. Randomize second-head placement and separate seeing Qwen's proposal from an independent second judgment.

The independent unit is the map/disturbance root. Keep damage/control arms, head placements and repeated executions clustered within it; cells and rounds do not replace map diversity. Define total compute versus per-cell compute as separate resource regimes. Qualify the same initialization, context/reset rules and current-source action contract on fresh development maps before freezing a successor. No new run or registration is implied by this amendment.

## PI next decision — 2026-10-04

[Design disposition](DESIGN-TRANSFER.md): **park new inference; finish negative-result analysis**. Historical results and current launch authority remain separate.
