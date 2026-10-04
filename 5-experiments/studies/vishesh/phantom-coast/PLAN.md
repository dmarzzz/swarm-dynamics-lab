# Phantom Coast PC-1: Two Swarms, One World

Prospective exploratory design, 2026-10-04 UTC. Owner: vishesh/codex-phantom-coast. Canonical question DM-01. Written before implementation. No previous Phantom Coast model run exists in the inspected repository; the parent is the PHANTOM-COAST handoff and REIMAGINING design review. This is an instrument-development plan, not an accepted formal hypothesis or a scientific result.

## TLDR

Can different early report histories leave two swarms with different maps after both receive the same final observations? We cross history order, private versus social decisions, and retained versus reset external state, and compare pooled and deterministic solvers. Primary measurements are paired whole-map error and between-history disagreement, with missing predictions bounded rather than discarded. A common-input reset sends byte-identical requests to detect serialization and service variability. This first stage tests history-dependent judgment, not self-reinforcing exploration or changed model weights; adaptive scouting requires a separate frozen stage.

## Question and prediction

The practical decision is whether to spend resources on communication, resetting stale summaries, or acquiring independent observations. Retained histories may produce more divergence than reset histories, particularly with social exchange; convergence and a deterministic-baseline win are equally valid outcomes. No minimum harmful effect is needed to pass instrument qualification. The mechanism is motivated by existing self-confirming learning and collective sensing work discussed in ../decision-models/REIMAGINING.md; this document does not claim completed literature review or new novelty evidence.

## Setup

Use 6 by 6 synthetic equal-area grids, twelve land cells and twenty-four water cells, with neutral row/column IDs. Each world has a randomized two-by-two land island (the exposed region) plus eight other land cells. The grid is text, not a vision task. Every cell remains an available observation target. World truth is evaluator-only; actors see cell IDs, evidence records, retractions, their previous output where applicable and permitted peer records. Condition, seed, exposed-region membership, correctness and future events are never actor fields.

Three model actors receive the same factual evidence in the first study, which isolates communication rather than distributed sensing. Agents differ only in counterbalanced neutral ID and initial call variation. Independent actors receive no peers. Social actors see all three previous-round maps with source ancestry; a copied endorsement is not a new observation. Private and social arms have the same number of decision opportunities, facts and per-call maximum output; realized input tokens differ and must be reported. This is a matched-call contrast, not a claim of equal token expenditure.

Early evidence contains two four-cell report batches: one matches the island and the other labels it water. Both histories have exactly these eight records; A receives false then true, B receives true then false. All initial reports have the same declared reliability. At step 2, both receive the same explicit retraction of the false batch and a complete set of 36 fresh, noiseless observations. Unique IDs and acquisition IDs distinguish direct observations from peer interpretations. Primary inference is about order, not false versus benign exposure. A separately reported clean control omits false reports. Geometrically random corruption, deletion-only, and genuine terrain change are deferred factors, not implemented claims.

## Protocol

1. Freeze source, assignment table, prompt, response schema and this plan before any model calls. Development seeds 100-103 only are available to unit fixtures. Qualification seeds 200-211 and later holdout seeds 1000-1099 remain ungenerated during development. Twelve qualification worlds are a readiness screen, not a powered effect study.
2. For each world cross two early histories, two communication conditions and two state conditions: eight trajectories, each containing three actor maps at each of three logical steps (72 calls/world). Reset and retained arms behave identically in steps 0 and 1. At step 2 reset excludes prior maps and peers; retained includes the preceding private map and, for social arms, preceding peer maps. Raw evidence contains the complete cumulative ledger and retraction in all arms.
3. At step 2 canonical reset inputs are byte-identical across history and communication for each actor. IDs, run metadata and treatment labels stay outside the model request. Schedule calls in a seeded interleaving, record exact request hashes, provider/model identity, start time and raw response status. Do not treat identical-request variability as history causation.
4. Each actor returns a complete mapping of cell ID to LAND, WATER or UNKNOWN, plus visible evidence IDs supporting the map. Validate exact cell coverage and allowlisted labels/IDs; invalid responses become missing maps. No model-generated confidence is required or interpreted as calibrated probability. Synchronous rounds read only the completed preceding round, never the next actor's fresh output.
5. Aggregate per cell by strict majority of the three assigned actors. Missing actors and UNKNOWN cannot create a majority; unresolved cells remain missing. Do not substitute a deterministic answer for a model failure. Preserve all scheduled assignments, including not-started ones.
6. Pooled single-solver baseline sees the exact union of facts, in both histories and state modes, without peers: four trajectories x three calls = 12 calls/world. It is a cost-efficient comparator, not equal compute. Deterministic mapper ignores retracted records, deduplicates acquisition IDs and takes the latest observation per cell; conflicting equally fresh observations return UNKNOWN. It sees only actor evidence and no truth. An exact rule that solves this task is a valid baseline result.
7. Clean competence: three independent reset actors per world at the complete-evidence endpoint (3 calls/world). Byte-identical reset duplicates already embedded above provide a service-consistency check. Qualification cap = 12 x (72 + 12 + 3) = 1,044 calls, no automatic retries, one worker, 60 minutes maximum, and the smaller of approved monetary cap and provider reservations. This is a proposed maximum, not spending authorization. Budget exhaustion preserves every remaining assignment as not-started.
8. Before launch require independent design review or explicitly scoped diagnostic approval, applicable research gates, experiment-specific allocation, budget authority, public registration and verified immutable plan with per-condition TLDR. The offline instrument has no network dispatch path; offline fixtures are software tests and cannot authorize model calls.

## Metrics

Primary fixed-evidence endpoint: whole-world cell error after step 2, averaged equally across independent worlds, and absolute disagreement between history A and B within world/communication/state. For each map, error lower bound = observed wrong / 36; upper bound = (observed wrong + missing) / 36. Report completeness separately. For disagreement, missing in either map contributes zero to the lower and one to the upper bound. A contrast of bounded quantities [a,b] - [c,d] is [a-d,b-c]. No observed-case-only accuracy substitutes for these all-assignment endpoints.

The planned social-history interaction is (retained social disagreement minus reset social disagreement) minus (retained private disagreement minus reset private disagreement). It is exploratory and service variation may remain. Secondary metrics: missed land / 12 with missing land bounded; error inside/outside exposed region; all eight trajectories' error across logical time; retraction response; unique acquisition count versus peer endorsements; calls, input/output tokens, reserved and actual spend, latency and response validity. Do not count cells, agents, arms or steps as independent replicates. Report paired per-world distributions; reserve world-cluster bootstrap intervals and multiplicity decisions for a larger preregistered study. Twelve roots cannot justify a robust population claim.

Qualification requires zero truth leakage, zero assignment loss, exact-source and request-hash audit, at least 95% valid responses overall, and clean complete-evidence error <=10% across worlds with <=20% error separately on land and water. Report denominators and bounds. Reset variability is measured, not required to be exactly zero. Failure leads to bounded diagnostics on new development tasks, never retuning and relabeling the same qualification seeds as fresh. A valid null or adverse effect does not trigger a repair rerun.

## Adaptive extension PC-2 (not authorized or implemented as a run)

Only after fixed-evidence competence works, freeze a second plan. Let actors choose any cell under a twelve-inspection budget after matched initial reports; do not forbid predicted water. Compare adaptive choice with a seeded uniform exploration schedule and a deterministic uncertainty/coverage policy, plus pooled evidence. Randomize one of those twelve slots to an independent audit in a specified factorial arm, so an audit does not add free sensing budget. Primary outcome becomes whole-map error per observation; candidate mediator is actual exposed-region inspection count, not a claim inferred from a final map. A separately randomized replay of observed packets distinguishes acquired evidence from interpretation. Include true terrain changes and equal-size random false reports. All realized observations and requests remain recorded. This stage may find efficient recovery; do not program avoidance or guarantee a rescue.

## Visualization mapping

PC-V1, bound by world, arm, history, actor and logical step in each saved trace. Show evaluator truth beside the three maps and aggregate; land is ochre, water blue, UNKNOWN/missing gray with distinct text labels. Outline the directly exposed island only in the evaluator view. A time slider, play/pause and final-state control use saved events, including explicit report/retraction markers. Show acquisition count separately from endorsement count and all-assignment error bounds. Fixed evidence uses observation markers, not fictional scout paths. PC-2 will require actual recorded target choices before drawing paths.

The offline viewer is an explicitly labelled software fixture. Retain every initial/event/final frame in replay JSON, ordered by logical step; no interpolation of invented model outputs. Limit to 36 cells, three actors, three frames per fixture and 500 KB. A failed frame remains visible with its status. Static JSON and a final table are the fallback. Live frames/public embedded replay are pending executor integration and supported hosting through DMars/CD; no Cloudflare deployment. Verify metric agreement, time cursor, missing map and retraction transitions before claiming playback validation.

## Issue ledger and stage boundaries

| Earlier design gap | PC-1 resolution | Acceptance evidence |
|---|---|---|
| Equal facts confused with identical prompts | Canonical reset excludes history and peers | Byte-level equality tests |
| Engineered water avoidance | Fixed evidence now; no avoidance policy | No adaptive causal claim; PC-2 separately specified |
| Tiles counted as independent | Paired world unit | Metrics retain world IDs |
| Copies inflate independent evidence | Acquisition IDs survive forwarding | Dedup/conflicting-copy tests |
| Retraction conflated with deletion | Explicit withdrawn IDs plus complete fresh observations | Retraction and reset tests |
| Missing outputs disappear | Strict fixed-denominator bounds | Partial/total failure tests |
| Viewer invents a successful narrative | Saved-event renderer; conspicuous fixture labels | Replay/data consistency checks |
| No previous run to assess | Parent design review, no fabricated post-mortem | Audit records zero native runs |

No implementation or publication makes this a reviewed hypothesis. Model transport, monetary reservations, exclusive fleet allocation, current provider qualification, run registration and live visualization are launch work still required. Results and process compliance will be reported separately.
