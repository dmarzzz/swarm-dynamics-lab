# Next-run design after Q-A1, Q-A2 and the schema repair

2026-10-04 UTC. Prospective design proposal; not implementation, launch admission or a claim of preregistration. No runs dispatched. Supersedes stale operational proposals in q1-pre.md for the next attempt, without changing historical records.

## TLDR

First qualify the repaired instrument end to end with four tiny N=1 episodes, one in each family/structure cell. Separate transport/schema validity from task correctness and from process/publication compliance. Only after inspecting that canary should a separately admitted full-width N=1 screen be considered. Do not compare swarm sizes until the dependency and resource controls below are resolved.

## Evidence and diagnosis

- Q-A1: 16/16 terminal failures before item work; 32 calls. The logs establish a planning-contract bottleneck but do not establish the exact contents of rejected replies.
- Q-A2: two terminal failures, fourteen unstarted under its early-stop rule; all four planning/repair responses were fenced and unparseable. Stronger prose did not fix the transport contract. Both executed cases' artifacts were acknowledged.
- The schema repair now requests native structured output in every phase. Forty-one experiment and five credential tests pass. This is offline evidence, not hosted end-to-end qualification.
- The successful one-message transport diagnostic never tested a task plan, worker artifact, final integration or evaluator. It was insufficient evidence for launching the full screen.
- Historical a3 had a stale public-plan receipt during registration propagation. Execution success and process compliance must remain separate.

## Question and prediction

Can the pinned schema-constrained model complete the actual plan → worker → integration → evaluation → publication path for both task families and both dependency structures? Predict all four tiny episodes reach integration, satisfy their structural contracts and produce correct on-time final artifacts. A schema-valid wrong answer is a capability failure; it is not a transport success sufficient for promotion.

## Setup

Four fixed canaries: evidence/parallel/root0, repository/chain/root0, evidence/chain/root0, repository/parallel/root0, in that order. Each has width=2, N=1 and fresh actor state. This order covers both families immediately; it avoids spending the first several failures on one cell, as Q-A2 did. Seeds/roots remain development-only; fit/validation/transfer stay unopened.

Width=2 is a new qualification population, not the same 16-item fixture. The assignment must record width, generator version, public-task hash, parent development root and an unused attempt namespace such as q-a3-canary. The current generator's task ID omits width: fix manifest/identity handling before dispatch so two different task sizes cannot share an apparent fixture identity. The current runner hardcodes full-width Q-A: it cannot execute this proposal unchanged.

Freeze the native Haiku snapshot, schema-contract version, schema hashes, generator/evaluator hashes, prompts, provider configuration and Python runtime. Change no model, sampling setting or evaluator during this attempt. Task schemas use only public field names, never evaluator truth. Preserve strict parsing; do not extract JSON from fenced replies or repair scores after execution.

## Protocol and predeclared decisions

Each episode permits one plan, at most one existing plan repair, two work turns and one integration: four ordinary calls, five maximum. Retain 600 seconds/episode with 60 reserved for integration, 4096 output tokens and a 48,000-byte full-payload limit. Schema compilation and hosted queue delay count toward wall time; neither is local CPU service time.

Keep the original canonical $20 ledger. Last verified exposure was $0.328990; re-read it before admission. Proposed canary sublimits are $1.25/episode and $5 additional exposure across this attempt, both enforced atomically inside the original authority. This is not new funding. At the currently configured $0.220480 worst-case reservation per call, 20 calls bound the canary at $4.409600; earlier exposure remains counted. Actual charges may be lower. Do not create a second independent spend ledger to implement the sublimit.

Stop immediately on route/credential/usage/claim/public-registration failures, schema API rejection, missing billing metadata, invalid JSON despite schema mode, truncated output or unacknowledged terminal publication. Do not spend a second episode reproducing a known shared interface failure. A valid-JSON dependency-map error retains the existing single repair allowance; repeated plan failure stops. A schema-valid but substantively incorrect final answer is preserved; finish the other tiny cells if infrastructure remains healthy so capability is diagnosed across families.

Promotion requires all four assigned canaries to complete plan/work/integration, all expected schemas and local validators to pass, all four final artifacts to be correct and on time, complete usage/budget accounting, and acknowledged plus sampled readback-verified public artifacts. This is a conservative readiness rule for four tiny deterministic tasks, not a statistical reliability estimate. Failure means a post-mortem and versioned repair, not rerunning until lucky.

A pass permits preparation, not automatic dispatch, of a separately identified full-width 16-case N=1 screen using the same frozen instrument and unchanged semantics. Qualification roots are repeated development fixtures, not independent evidence across attempts. Full-width deadlines/token/context bounds still need calibration; a two-item pass does not establish 16-item feasibility. Q-B/core remain closed pending that result and the controls below.

## Metrics and diagnostic evidence

Keep three separate ledgers of status (not spending authorities):

1. Execution and scientific outcomes: assigned, started, reached plan/work/integration, terminal, schema-valid, evaluator-valid, substantively correct, on time. Report failure phase and reason; unstarted assignments remain visible and are not model failures.
2. Financial exposure: call count, input/output tokens, settled charges, retained reservations, per-episode and cumulative authority exposure. The original unresolved hold remains held.
3. Process and delivery: exact plan/source registration, condition TLDR, exclusive claim, publication acknowledgments and readback. Report executed-artifact completeness separately from full-assignment execution completeness.

Record safe validation categories and schema hashes for every phase, plus schema-validity of partial worker artifacts. Keep semantic correctness evaluator-side: it must not leak back into subsequent worker prompts. Existing format flags alone cannot diagnose a schema-valid wrong dependency map or partial answer. Avoid raw provider error bodies or secret-bearing context in public evidence.

Publish this plan's eventual frozen revision, register its exact URL, verify the live URL/commit/hash after metadata propagation, and check every condition-specific TLDR before model dispatch. A generic “some plan exists” check is insufficient. Obtain a fresh exclusive fleet allocation and use only the dedicated Swarm Lab credential under standing policy. Prior claims and runtime receipts are expired/released evidence, not admission.

## Controls required before a swarm-size comparison

### Dependency integrity

The current plan validator checks only keys, references and acyclicity. It does not require the supplied task dependencies. A chain can therefore be scheduled as independent work. Before interpreting a size effect as a dependency/serial-bottleneck mechanism, decide and freeze whether the supplied graph is mandatory. Recommended: require all supplied prerequisite edges, allow extra acyclic edges but record their overhead; test an empty dependency map for a chain as a negative control. This is a declared design change, not a retrospective invalidation of historical scores.

All actors currently receive the entire public task. They can reason about prerequisite computations without retrieving another worker's artifact. A scheduling chain therefore does not establish an information-access bottleneck. Keep this full-context setting explicit for the first size comparison; a restricted-information variant would be a separate treatment. Do not bundle that change into the schema canary.

### Capacity and fairness

N is a roster count; service slots are a different intervention. With four slots, N=8/16 cannot imply eight/sixteen simultaneous provider requests. Freeze aggregate dollars, deadline, slots and per-call limits across sizes; report allocated/used actors, concurrent requests, queue time and integration overhead. Treat hosted latency as hosted latency; do not infer GPU/RAM scaling from it.

Use paired roots across sizes, balanced/interleaved execution order and fresh histories. Apply the same schema contract to every size; do not compare repaired N>1 against old prompt-only N=1. Choose a small feasible size grid only after full-width baseline timing/cost evidence, rather than spending the remaining budget on the entire draft grid by default.

## Visualization mapping

Canary view: four small task graphs with real plan/work/integration lanes, status transitions, settled/reserved cost and validation markers. A failed plan produces no moving worker nodes. For later matched sizes, align recorded clocks and show available slots, runnable work and the integration lane. This supports a queueing/serial-bottleneck explanation when measured, without implying a biological law or fabricated activity.

## Required implementation before admission

- Width-aware immutable assignment identities and an explicit four-cell canary manifest.
- Attempt sublimit enforced against the canonical ledger; existing total cap unchanged.
- Phase-specific schema/semantic diagnostic categories and the immediate interface-failure stop policy.
- Separate executed-publication versus full-assignment completion reporting.
- Regression tests for canary denominator/stop behavior, namespace collisions, schema-contract wiring and no hidden-truth leakage.

Do not launch the current hardcoded 16-case runner and call it this canary. The proposal is reviewable design work; live implementation and verification remain outstanding.
