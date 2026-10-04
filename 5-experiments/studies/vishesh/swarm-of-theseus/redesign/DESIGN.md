# Swarm of Theseus v2: selective continuity

**Scenario-selection amendment, 2026-10-04:** the subsequent [X discussion and practical-grounding review](SOCIAL-GROUNDING.md) supersedes the priority order below. Lead with the release-crew handoff task; retain the incident-guild/rare-hazard task; treat model/runtime migration as a separate factor across qualified tasks. Harbor is now a controlled coordination extension and glassmaking is deferred. The original draft is retained below for provenance. None of these scenarios has been run or established as novel. The archive controls, falsification rules and launch gates remain applicable; task-specific metrics must be frozen in the next pre-run plan.

Prospective design draft, 2026-10-04 UTC. Unrun and unqualified. This is an exploratory design hunch under researcher notes, not an accepted lab hypothesis. It does not amend the interpretation or preregistration of v1 retroactively. Work starts with one flagship task; the other two are extensions, not simultaneous commitments to a large sweep.

## Question and candidate contribution

Can a group transmit a practice it acquired through experience across at least two complete replacement waves, while keeping its useful components and revising components made obsolete by a change?

The candidate contribution is a controlled measurement of **fidelity versus adaptability**, with tests of whether any apparent continuity is fully reproduced by a portable archive or a budget-matched single controller. Merely beating no memory will not count as a positive result. Novelty of this combination remains unverified; the review lists substantial close work.

Memory is a possible substrate of culture, not a disqualification. The mistake would be treating the existence of useful memory as evidence for emergence or a special swarm effect. In context-only agents, continuity must be mediated by available state, interactions and common weights. Identical prompts with renamed identities are not a meaningful causal intervention.

## Three genuinely different task constructions

| Scenario | Practice to acquire | Intervention after founder extinction | Objective outcomes |
|---|---|---|---|
| **Harbor without its pilots** — flagship | Three pilots learn a scheduling and signaling convention for narrow channels. Several conventions have equal stable-world payoff. Each sees a different arrival queue; a collision or redundant dispatch is a real coordination failure. No preferred convention is supplied. | A previously reliable beacon becomes unreliable on one route; a second route stays unchanged. Agents receive observations and outcomes, never a bulletin stating the new policy. | Deliveries, collisions, waiting cost, unnecessary signaling, recovery time; preserve conventions on the unaffected route while changing behavior on the affected route. |
| **The glassmakers' guild** — causal learning extension | Specialists discover recipes through budgeted experiments. A color cue is correlated with a curing requirement during training; interventions can distinguish this shortcut from a causal temperature constraint. Recipes combine stages that no single role observes initially. | A supplier change breaks the color correlation; a different causal constraint remains valid. New jobs recombine known stages into withheld combinations. | Yield and resource cost, targeted diagnostic experiments, success on withheld combinations, retention of the unchanged constraint. Copying old recipes and forgetting everything fail in different ways. |
| **The night watch** — rare-event institutional memory extension | Successive crews learn when a costly cross-check prevents a rare equipment failure. Ordinary shifts reward speed; false alarms consume a common budget. A policy must balance prevention and delay, not just repeat a phrase. | One old alarm becomes a false positive while a distinct rare hazard remains real. Long quiet intervals tempt crews to delete the precaution; stale archives tempt them to keep the obsolete alarm. | Expected loss under a fixed mixture of ordinary and rare events, wasted checks, preventable incidents, selective rule revision. Report the event strata separately so aggregate success cannot hide catastrophic forgetting. |

These stories must become different transition/reward structures, not reskins of XOR. All consequences are fictional and computed by a deterministic environment. A second task is added only after the flagship measurement discriminates the intended failure modes. No claim that these themes themselves are novel.

## Flagship task specification

Three roles receive role-local queues and sensor observations. Public instructions specify legal actions, capacities and payoff accounting, but not which signaling/scheduling convention to use or which sensor is dependable. Legal actions: reserve route/slot, yield, dispatch, request a check, and send a bounded message. The environment resolves simultaneous actions; it never inserts a majority-vote solution or silently repairs illegal actions.

Two convention families are payoff-equivalent on a balanced stable schedule; labels, roles and route names are counterbalanced. The schedule includes conflicts that force coordination, uncontested jobs, and diagnostic trials that distinguish cue-following from a robust contingency. A frozen probe panel measures actual priority/signaling choices, not text similarity or a model judge's impression of culture. Failure to acquire a convention is an outcome, not a seed-exclusion criterion.

First run a fixed-length acquisition phase without a supplied policy. Save the full founder state and an agent-written archive within a fixed byte/token cap. Freeze this checkpoint before branching into conditions. A development screen determines whether the task is learnable under the allowed observations; passing this screen says nothing about the cultural claim.

Two waves replace all three members. The second wave must be taught by descendants, and no original founder may send a later message. After each interaction, actors retain only specified bounded private notes and the arm-authorized archive. Departed private context is destroyed; every surviving byte has an access receipt. Archive ancestry and actor ancestry are recorded separately. A frozen founder archive intentionally survives only in its designated arm.

Use separate stable and partially changed continuations forked from the same checkpoint. Change begins after the first full turnover; the second wave tests whether an acquired correction itself transmits. Change timing and diagnostic event schedules are fixed before inference. Agents may infer changes from outcomes but receive no evaluator rule, change label or correct action. Stable branches get an equally long observation schedule. New held-out layouts and queue combinations test structural transfer rather than renamed records.

## Conditions and the explanation each can rule out

1. **Rolling archive + turnover:** descendants can rewrite the bounded public archive; private notes die with members. This is the candidate continuity process.
2. **Frozen founder archive + turnover:** the same initial archive is replayed unchanged; successors still act, observe outcomes and keep bounded private notes. This tests whether copying the founding document explains everything and whether its durability obstructs correction.
3. **Rolling archive + retained members:** same observation schedule, memory limits and interaction budget, with sham onboarding work. This measures turnover cost; it is not assumed superior.
4. **Fresh team + transplanted archive:** at prespecified checkpoints, an independent fresh team receives an exact byte copy of the rolling archive but no incumbents' private notes. It receives the same scheduled probe observations as the continuation. This estimates portability and whether information outside the archive matters. It does not magically isolate “identity”: a gap may reflect missing private state or onboarding.
5. **Fresh team + no archive:** establishes unaided acquisition and model-prior performance with the same current observation budget. A difference from this arm alone cannot support the main claim.
6. **One controller with the same total observations and budget:** controls all three action slots through role-separated calls, with the same total context/output allowances and feedback opportunities. This asks whether distributed organization adds anything beyond centrally using the record. Report any unavoidable ordering/information differences; equal token ceilings do not make interactions semantically identical.

An evaluator-only oracle and deliberately stale/copying/forgetful policies validate the environment and scoring; they are not LLM evidence. Adaptive mentors are deferred to a separate comparison against an equal-budget written handoff. Otherwise dialogue utility, extra inference and information content become conflated again.

A same-observation diagnostic complements live interaction: fork each candidate at a checkpoint and present the identical frozen probe transcript. Live branches naturally generate different feedback through different actions, so claims must distinguish total policy effects from response-to-identical-evidence effects.

## Estimands and falsification

Primary exploratory endpoint: the interaction between archive policy and environment condition after the second replacement wave:

`(rolling reward − frozen reward in changed worlds) − (rolling reward − frozen reward in stable worlds)`.

Reward is the preregistered environment utility per scheduled episode, including failures and costs; weights and normalization are fixed from task rules before model qualification. Do not tune the reward to a favorable result. Also publish raw deliveries, collisions and delays.

Interpret this interaction jointly with stable-world competence and unaffected-component retention. A positive interaction caused only by rolling archives collapsing in stable worlds is not useful selective continuity. Prespecify separate noninferiority margins for stable reward and unaffected-component retention before qualification; choose them from operational loss tolerances, not observed model variance. Final numeric margins are deliberately a launch-blocking item, not something to invent after seeing data.

Secondary endpoints: adaptation regret against a causal oracle; time to recovery with right-censoring at the fixed horizon; functional-convention retention on the unchanged route; independent lineage diversity; portable-archive performance; single-controller gap; archive mutations tied to behavioral changes; invalid actions, failures and token cost. Self-reported explanations do not score causality.

- If transplant matches continuation, report archive sufficiency within the tested bounds. Do not turn a null gap into mystical continuity.
- If the single controller matches the swarm, drop a special swarm advantage claim.
- If conventions never emerge or all lineages follow one model default, drop claims of lineage-specific culture; retain only task learning.
- If rolling and frozen archives differ only in available task facts, describe a memory-update effect. Check the identical-evidence probes before claiming a social mechanism.
- If retaining obsolete practices increases costs, that is a valid inheritance failure, not a prompt bug to optimize away.
- If every condition is at ceiling, or a one-line supplied rule solves the entire benchmark, stop scaling and repair discrimination on development worlds only.

## Units, sampling and scale gates

The independent unit is a founder lineage in a independently generated world, not an agent, decision, replacement or branch. Arms and stable/changed continuations share a founder checkpoint, so inference is paired and clustered at lineage/world level. Multiple checkpoints from one lineage are repeated measurements. Predeclare whether separate lineages in the same world are nested or averaged before resampling.

Acquisition failures remain in intention-to-treat summaries. A conditional-on-acquisition analysis is secondary with its denominator shown; it must not replace the full assignment set. Failed calls/trajectories remain assigned, with conservative loss and complete-case sensitivity analyses defined before launch. No hidden semantic retries and no favorable-result reruns.

Scaling sequence: offline transition/scorer review; disjoint qualification worlds; a small fixed exploratory batch; then a separately planned precision/replication study across new worlds and a second model family. Derive sample size from a declared minimum meaningful effect and observed qualification variance without viewing evaluation outcomes; do not prescribe an arbitrary giant sweep. More agents alone does not increase independent sample size. Require independent reviewer derivations of the oracle, leakage checks and failure policy before paid expansion.

## Visual evidence

Replay must show measured actor generations, actual archive versions and message ancestry, alongside task outcomes. Three synchronized panels: (1) roster replacement and archive ancestry; (2) stable versus changed-world reward and component-specific behavior; (3) exact inherited text diff with the next observed actions. Mark sensor change only in the viewer/evaluator layer, never in actor input.

Show rolling, frozen and transplanted branches side-by-side at the same checkpoint. Let the viewer follow a useful rule that survives, an obsolete rule that persists, or a correction that dies. Always expose the full run/arm selector; select any hero example by a predeclared representative criterion, not maximal effect. Missing observations remain gaps. No simulated animation is presented as a recorded run; design storyboards remain labelled unrun.

## Before execution

This review launches no new model experiments. Resolve the finite-state transition table, acquisition/replacement horizon, archive/token caps, action schema, exact utility, numeric acceptance margins, train/qualification/evaluation partitions, sample count, model versions and budget in a new pre-run assessment. All are frozen and public before the first paid call. Publish the immutable plan and condition-specific TLDRs; validate registration against the intended plan revision (not merely any cached older plan). Obtain a fresh exclusive fleet allocation and a non-overlapping budget reservation; the completed v1 quota is not silently reused. Preserve all failures and retain separate process/execution/scientific-validity fields. Formal promotion still requires the repository survey and cross-researcher hypothesis gates.
