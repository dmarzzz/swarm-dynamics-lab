# Avalon Swarm research protocol

This protocol proposes an Avalon-inspired benchmark for detecting and recovering from deceptive information while preserving coordination at increasing population sizes. Defaults below are design choices, not empirically established balance settings. The implementation is an executable scripted reference, not a finished LLM leaderboard.

## Research foundation

[AvalonBench by Light, Cai, Shen, and Hu](https://arxiv.org/html/2310.05036v2) studies social deduction using hidden alignments, mission proposals, voting, sabotage, and Merlin assassination. It provides rule-based opponents and LLM agents, and evaluates wins and role deduction. Its discussion pipeline shares conversation history; its naive belief baseline enumerates possible alignments. Both motivate a different scaling design. A noteworthy implementation detail is that the paper automatically executes the fifth proposed team after four rejections. Our prototype preserves that convention rather than silently substituting a different tabletop rule.

The [official repository](https://github.com/jonathanmli/Avalon-LLM) now also links Strategist, a subsequent strategic-agent project. This package is independently written and incorporates no upstream source. Pin and review the upstream code and license before implementing a compatibility track. The [2026 Avalon ToM benchmark](https://arxiv.org/abs/2608.09638) examines perspective-constrained mental-state queries; it is relevant to diagnostic reasoning, but does not establish our swarm recovery design's novelty. This is a focused source review, not an exhaustive novelty search.

## Three tracks with separate claims

| Track | Scientific purpose | State |
| --- | --- | --- |
| Classic | Small-game compatibility with a pinned AvalonBench implementation | Planned; do not claim original-benchmark comparability |
| Federated | Information movement, deception, repair, and local coordination across connected councils | Implemented with scripted agents |
| Institutional | Cross-council resource allocation, elected leaders, replacement after failure, and joint missions | Proposed extension |

The federated track measures coordination through team proposals, approval failures, mission outcomes, and recovery. It does not yet measure emergent institutions, leadership elections, or global task planning. Keep that distinction visible in any demo or paper.

## World and information rules

Use N in {100, 200, 500, 1000, 2000}, partitioned into N/10 councils. Each has six good agents, including one Merlin, and four evil agents, including one Assassin. Shuffle roles independently within each council. Merlin and evil agents know their council's evil membership. Ordinary good agents do not. No agent knows other councils' alignments by role privilege.

Each agent receives one private binary signal about the member at the same seat in the next council around a ring. The signal is independently correct with probability 0.8. It is expressed as an evil probability of 0.8 or 0.2. An evil scripted agent reverses its signal before sending it; good agents relay it faithfully. Therefore some honest claims are wrong and some adversarial claims happen to be right. The initial evidence distribution is identical across topology and recovery conditions for a given N and seed.

Local communication delivers to the other nine council members. Federated communication adds the same seat in the previous and next councils, producing degree eleven. No-communication delivers no messages but retains private signals, game observations, and any assigned audits. This isolates the availability of social communication while keeping logical speaking opportunities. Model cost comparisons must account for these unused speaking opportunities.

Claims carry original author, target, and probability. Relays preserve these fields. Authenticated origin does not establish truthful content. The reference runner checks relay provenance against trusted scripted state; it is not a sandbox. Perceived role, protected ground truth, and reported claims must remain distinct in production.

At each discussion tick, all agents act from the same preceding state. Delivery happens after all messages are collected. Decisions then use delivered claims. Council mission histories are visible locally and contain team membership and anonymous sabotage counts. Ballots are logged for evaluation; this baseline's observation does not include individual vote history. Add that feature as a versioned treatment, not an undocumented prompt change.

## Missions and victory

Every council plays five missions, with team sizes 3, 4, 4, 5, 5. Mission four requires two sabotages to fail; all others require one. Only evil agents may sabotage. Leadership rotates deterministically using `(5 * mission_index + attempt_index) mod 10`. This is a fixed schedule, not a leadership-learning mechanism; counterbalance seat identity and use alternative schedules in later evaluations.

On attempts one through four, a strict majority of ten votes approves the team. A tie rejects. The fifth proposal proceeds without voting. Council decisions proceed in synchronized mission stages; a council that completes a mission waits while other councils finish, but its agents continue participating in discussion. Consequently topology effects can change the total number of ticks; compare both outcome and consumed communication budget.

Unlike standard early stopping, all five missions are played. This fixed horizon creates post-intervention measurements. Good wins a council if at least three missions pass and the Assassin fails to identify Merlin. The scripted Assassin chooses randomly among known-good members. The world reports the fraction of councils won; the mission-only swarm outcome requires at least 60% council wins. In version 0.2, overall swarm victory additionally requires passing the truth-consensus gate below. That threshold is provisional and must be calibrated on development seeds before any held-out evaluation. It should never replace the continuous score.

All agents share their faction's aggregate objective in the proposed LLM track. Current scripted strategies optimize local heuristics and do not implement sophisticated cross-council planning. Scaling the number of councils creates a connected information experiment, not proof of intelligence from simply adding more independent games.

## Detection and repair experiment

After two missions, choose one random member per council using a seed stream independent of treatment. The trusted audit reveals its true alignment to that council. No-audit runs omit disclosure. Audit and repair runs receive exactly the same disclosures.

A claim contradicts the audit if its probability is on the wrong side of 0.5 for the audited target. The evaluator records distinct claim origins encountered by good recipients, separating true evil origins from honest origins using protected labels. This diagnostic is not exposed as a magical malicious-agent detector. The current agent policy can inspect its own audited labels, not the evaluator's global origin classifications.

Audit-only agents override the audited target's belief but retain and relay stale claims. Repair agents also remove contradictions from their bounded memory and suppress their forwarding. Evil agents ignore this repair rule. No agents are removed from the network. The treatment therefore measures a specific corrective mechanism rather than trusting an LLM's statement that it has changed its mind.

The main comparison is **repair minus audit**, which holds corrective evidence availability constant. Audit minus none estimates the benefit of revealing new truth. A fall in belief error on the revealed identity is partly mechanical; measure error on unaudited identities separately and look for improved mission choices. An apparent recovery based only on parroting the audit is insufficient.

## Endpoints and analysis

Primary failure endpoint in version 0.2: inability to sustain sufficient truth consensus under the rule below. Report its world-level incidence and first failure round. The recovery efficacy endpoint remains the fraction of missions three through five that succeed, comparing repair against audit at each N; report this even for worlds that fail the consensus gate. Secondary endpoints: council win fraction, ordinary-good Brier score excluding self, Brier trajectory after each mission, unaudited-target Brier, rejected proposals, fifth-attempt executions, and post-audit exposures to contradictory claims. Lower Brier is better. Flags are diagnostic claim-origin counts, not criminal or moral judgments.

Report false-flag rate among honest origins and detection rate among evil origins with denominators of 0.6N and 0.4N respectively; also report precision among flagged origins. Opportunity to encounter audited contradictions varies, so include encountered eligible origins before interpreting recall as detector quality. The prototype records global role denominators but does not yet export this eligible-origin denominator. No-audit detection counts of zero mean no verification opportunity, not a perfect detector.

The experimental unit is the complete world. Councils and agents within a world communicate and are not independent replicates. Pair conditions by N and seed; do not treat a 2,000-agent world as 2,000 observations. Report paired world-level differences with confidence intervals from resampling whole seed blocks. Do not pool different N values into one deceptively precise sample. Predeclare multiplicity handling for five scale comparisons, or label them exploratory.

Use separate development and held-out seed sets; tune thresholds and policy parameters only on development seeds. A five-seed local pilot is for checking mechanics. Begin a real-model pilot at 100 agents, estimate variability and cost, then perform a power analysis around a prespecified minimum useful improvement. Thirty seeds is a possible planning starting point, not a justified universal sample size.

Compare provenance-aware, duplicate-counting, random, and stronger inference agents. Counterbalance model and role assignments. Separate scaling population at fixed per-agent resources from scaling at fixed total compute; those answer different questions. Do not compare a full LLM swarm against mostly scripted agents under the same label. Report unique agent states, logical activation count, concurrently active calls, and proportion controlled by each policy.

## Scaling and resource accounting

For fixed episode length and bounds, routing is O(N), agent memory is O(N), and local role reasoning is O(N) because each council size stays ten. Each tick emits N envelopes and delivers at most 11N copies, each containing at most four claims. Five missions with up to five proposals mean at most 25 ticks, 25N discussion activations, 275N envelope deliveries, and 1100N claim deliveries. There is no all-population belief matrix or combinatorial role enumeration.

At most 247 decision calls per council cover 25 proposals, 200 votes, 21 mission actions, and one assassination. A naive separate-call LLM adapter therefore has an upper bound of 49.7N calls excluding belief probes, retries, and extra summaries: 4,970 at 100 agents and 99,400 at 2,000. These are planning bounds, not provider invoices. Current code counts actual logical calls but makes zero API requests.

If each call were capped at 1,200 input and 160 output tokens, that upper bound at 2,000 agents would be 119.28 million input and 15.904 million output tokens, before probes and retries. These token caps are assumptions, not implemented provider limits. Estimate dollars using a dated price table for the selected model. Prefer one structured response containing all currently legal outputs to reduce calls, while preserving observation timing.

Use a bounded worker pool, for example 32 to 128 concurrent calls after rate-limit calibration. Agent population is independent of provider concurrency. For long-range scaling, compare the ring to degree-matched random regular and hierarchical overlays; the current ring's diameter grows with council count and cannot disseminate arbitrary global evidence in constant rounds. Measure reach and mixing time rather than promising global knowledge at constant cost.

## Limitations and staged delivery

Implemented: deterministic initialization, sparse synchronous routing, five-mission engine, legal action checks, bounded scripted memory, provenance and echo baselines, audits and correction, world metrics, seeded reruns, and hash-chained events. Unit tests establish selected invariants, not exhaustive formal correctness.

Still needed before a real LLM benchmark: isolated agent execution, structured provider adapter, token and dollar reservation, retry and deadline semantics, failure reconciliation, frozen prompts, context truncation rules, natural-language claims, persistent verified-evidence tooling, model-generated detection and repair decisions, and an analysis implementation with whole-world intervals. In-memory Python objects are not a hostile-agent security boundary. The current runner aborts on invalid actions and leaves an incomplete plan rather than fabricating a score; a production ledger must explicitly mark these failures.

First hackathon experiment: demonstrate that stale claims can survive an audit and show the difference when repair is enabled. Then replace a small, explicitly counted subset with LLM agents, followed by an all-LLM 100-agent pilot. Only advance to larger paid populations after measuring budgets and testing information isolation. Do not claim linear LLM throughput from the local scripted scale check.

## Sustained chaos and truth consensus

Version 0.2 adds an independent failure gate for collapse of usable shared knowledge. One round is one synchronous discussion and delivery tick, followed by ingestion and a belief probe before proposals. It is not an individual message, wall-clock interval, or complete mission. Counting starts at the first tick; no grace period or reset occurs at the audit. `consensus_patience=5` therefore means five consecutive insufficient rounds anywhere in the episode. Set a longer window before running if the intended intervention arrives later; never change it after observing outcomes.

The evaluator collects one belief vector from each ordinary-good agent about its ten local identities, excluding its own identity from scoring. For target j, let Mj be these eligible local observers and pj_i their probability that j is evil. An observer confidently endorses the true label if pj_i >= confidence for an evil target, or pj_i <= 1-confidence for a good target. A target has correct consensus if at least ceil(quorum * |Mj|) observers confidently endorse its truth. All eligible observers remain in the denominator; 0.5 is uncertainty, not an abstention that shrinks the quorum. Missing or malformed reports are execution errors in this prototype, not successful consensus.

Default confidence is 0.7 and quorum is 0.8. Aggregate the fraction of targets with correct consensus separately among true good and true evil targets. Both fractions must reach coverage=0.8. Separate class thresholds prevent a majority-class shortcut. Targets can have different local observer sets; this endpoint evaluates distributed, locally relevant truth across the whole world, not all-to-all knowledge or universal faction cooperation. Merlin and evil agents are excluded because privileged knowledge would inflate truth recovery, and adversarial refusal should not make honest success definitionally impossible. Ground truth and evaluator classifications never enter agent observations through this probe.

Track ordinary agreement in parallel: a target has agreement if the same quorum confidently endorses either label. If correct consensus remains insufficient for patience consecutive rounds, record a terminal benchmark failure. At the triggering round classify it as `false_consensus` when both class-specific agreement coverages meet the threshold, otherwise `signal_loss`. The latter includes uncertainty, fragmentation, and mixtures of insufficient or incorrect agreement. It is an operational outcome, not proof of a specific psychological or causal mechanism. Confident-report fraction and both coverage trajectories support further diagnosis.

A sufficient round resets the consecutive-failure counter. The episode must finish with stability=2 consecutive sufficient rounds; otherwise record `truth_consensus_not_stable_at_horizon`, including when the five-mission horizon ends before the patience window expires. One lucky moment of agreement cannot yield a passing terminal result. A recorded patience failure is absorbing for benchmark scoring, though the engine continues the fixed mission horizon for diagnostic recovery trajectories. Later recovery cannot erase the earlier failure. Report terminal stable consensus separately to show these late recoveries.

`mission_swarm_win` retains the mission-based outcome. `good_swarm_win` requires both that outcome and `truth_consensus_pass`. Execution status remains `completed` for a successfully simulated failure. Retain failed worlds in denominators; do not report only surviving worlds. Consensus probes are evaluator-only, pure and non-mutating in scripted policies. A real-model adapter must charge and record these extra calls, prevent probe prompts from affecting agent memory, and define the elicitation protocol as part of the treatment.

There are 0.5N ordinary-good agents, so at most 12.5N additional consensus belief probes over 25 ticks. This preserves linear cost for fixed horizon; it does not eliminate cost. Existing Brier diagnostics and any provider retries are additional. The quorum, confidence, coverage, patience, and stability defaults are provisional. Calibrate with oracle, uninformed, fragmented, and confidently wrong controls on development seeds, then freeze them before held-out runs. A threshold that every weak baseline fails is a useful stress check, not evidence that every realistic swarm must collapse.

The original version 0.1 source and results are preserved under results/reference-v01 and their original run folders. Version 0.2 retains the original scenario seed stream for paired comparison; scoring and log schemas have changed and versions must not be pooled silently.

## Prospective design amendment 2026-10-04

Incorporating [Dmarz's Avalon recommendation](https://github.com/dmarzzz/swarm-lab/blob/e0a31706cdf1fb1d3864370b04f29bd4f93e2682/researchers/dmarz/notes/next-experiments-2026-10-04/README.md), the next scientific comparison should establish a useful coordination mechanism before expanding logical population. This is a future-design clarification; it does not change the v0.1/v0.2 fixtures, defaults, endpoints or recorded failures.

Partial information is already present. The unresolved step is to qualify a policy that uses it competently and test whether communication or repair improves consequential mission choices at matched information and resource opportunities. Include a competent deterministic/inference comparator, a model controller with the same union of authorized observations when feasible, and the existing audit-versus-repair distinction. The union-evidence controller is an explicit aggregation advantage, not an identical-observation actor. Supplied audit labels must stay distinct from learned detection.

Use common absolute mission-quality and belief-quality criteria when comparing recovery; report quality loss integrated over a fixed horizon and unaudited-target effects as prospective secondary measures. Keep valid consensus failures even when later recovery occurs. Vary independently generated role/evidence/topology roots before adding councils, preserving each root across paired arms. A new dynamic-constraint scenario is useful only if it separates mechanisms under credible controls, not merely because it makes the animation busier.

For a treatment-specific population claim, prespecify the change in repair-minus-audit effect between sizes, with useful-mission guardrails and the actual communication/call budget. Distinguish stateful policy actors from concurrent worker slots. Scripted single-process timing is capacity evidence; it cannot support provider throughput, LLM competence or an emergent-intelligence claim. Existing adapter, qualification, public-plan and research gates remain prerequisites for model execution.
