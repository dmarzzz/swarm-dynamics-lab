# Research question atlas

219 candidate questions, tentative hypotheses and test sketches across all 15 research areas.

Owner: dmarz/question-atlas. Human-requested brainstorming, 2026-10-03. **Every item is an unreviewed hunch.** These are selection materials, not accepted hypotheses, approved protocols, measured effects, or novelty claims.

[Start with the synthesis and review guide](../../../../3-synthesis/research-question-atlas.md). [Open the local review browser](review.html). [Machine-readable bank](candidates.json). [Review scope and limitations](scope.md).

Update 2: **76 new, 36 revised, 107 unchanged** candidates. All original IDs are retained. [What changed and why](update-v2.md).

Feasibility labels describe a possible first test, not a verified installation, price or runtime. Source depths are inherited catalogue metadata, not claims that this pass fully read those sources. The open evidence-depth audit still applies.

## Areas

- [Collective motion models](#collective-motion): 6 candidates.
- [Collective decision-making in biology](#collective-decision): 6 candidates.
- [Swarm robotics](#swarm-robotics): 8 candidates.
- [Swarm intelligence algorithms](#swarm-intelligence): 6 candidates.
- [Active matter physics](#active-matter): 6 candidates.
- [Synchronisation, consensus and networked control](#sync-consensus): 6 candidates.
- [Criticality, information and measurement](#criticality-measurement): 8 candidates.
- [Multi-agent RL and emergent coordination](#marl-emergence): 9 candidates.
- [LLM agent swarms](#llm-agent-swarms): 51 candidates.
- [Human crowds and traffic](#crowds-and-traffic): 6 candidates.
- [Meta and tooling](#meta): 22 candidates.
- [Sybil resistance and adversarial identity](#sybil-resistance): 24 candidates.
- [Fork-and-merge agents and corruption on reintegration](#fork-merge-security): 22 candidates.
- [Detecting AI agent swarms in the wild](#swarm-detection): 16 candidates.
- [Agent budgets and resource allocation](#agent-budgets): 23 candidates.

## Shared design requirements

For any selected candidate: define the independent assignment unit, interference boundary, primary outcome, smallest effect worth pursuing, and an uncertainty-aware decision rule before a confirmatory run. An estimate near zero with a wide interval is inconclusive. Set seed/case counts from a pilot and the intended precision, then freeze the comparison. Log unsuccessful runs and all tuning costs. Use held-out worlds, operators or model families only when the labels really support that split.

API tests need matched inference and communication budgets. Training tests need matched steps, capacity and tuning effort. Simulators need explicit scheduling, observation and boundary rules. Security tests use synthetic or authorized environments. Oracle information is a diagnostic ceiling only. Replication, measurement and boundary tests can be valuable without claiming a new mechanism.

<a id="collective-motion"></a>
## Collective motion models

<a id="phy-01"></a>
### PHY-01 — Neighbour rules under actual visibility

**Update 2:** unchanged.

**Question:** Does choosing a fixed number of neighbours still preserve cohesion when robots can only see unoccluded neighbours?

**Candidate hypothesis:** The topological rule will lose part of its density robustness when visibility constrains its inputs; an occlusion-aware rule will recover some robustness without increasing the observation budget.

**How to test:** Randomize independent simulated flocks to metric, topological, or visual neighbour selection, then impose the same density change and turning disturbance. Match the number of observations delivered and use paired initial conditions across rules. Hold out obstacle geometries for evaluation; analyse whole-flock outcomes rather than treating birds as independent replicates.

**Comparison:** Unoccluded topological and metric rules are ideal-information controls; random visible-neighbour selection controls for observation count.

**Measurements:** Largest connected component; Collision count; Heading error after disturbance; Recovery time; Observations used.

**Would count against it:** No visual-rule advantage survives equal observation budgets, or apparent cohesion comes from slower movement.

**Main confounds:** Nearest-neighbour identities require position knowledge; visibility and density alter available degree. Cohesion is not proof of correct navigation.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Specify sensor field of view and a fair observation-budget matching procedure; inspect original visual-network methods before promotion.

**Closest prior and evidence limits:**

- [[ballerini-2008-interaction]] — [Interaction ruling animal collective behavior depends on topological rather than metric distance: Evidence from a field study](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ballerini-2008-interaction.md). Closest prior compares topological and metric structure, with a perturbation simulation. Catalogue depth: full.
- [[strandburg-peshkin-2013-visual]] — [Visual sensory networks and effective information transfer in animal groups](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/strandburg-peshkin-2013-visual.md). Closest prior motivates sensory networks; empirical species-specific finding, not universal superiority. Catalogue depth: abstract.
- [[bastien-2020-model]] — [A model of collective behavior based purely on vision](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bastien-2020-model.md). Related perception-only model; catalogue read only in this pass. Catalogue depth: abstract.

<a id="phy-02"></a>
### PHY-02 — What mechanism carries a turning wave?

**Update 2:** unchanged.

**Question:** Can measured propagation distinguish behavioural inertia from front-biased interactions?

**Candidate hypothesis:** The same average turning-wave speed can arise from both mechanisms, but responses to reversed sensory bias and paired pulses will distinguish them.

**How to test:** Fit inertial-spin and front-biased alignment models to the same synthetic undisturbed trajectories and single-turn response. Randomize simulated flock episodes to sensory-bias reversal, a second pulse, or sham perturbation. Compare held-out arrival-time and attenuation predictions, including fits where both mechanisms are present. Score episodes independently, with uncertainty across seeds and fitted parameter sets.

**Comparison:** An overdamped reciprocal alignment model and a common external steering signal provide mechanism and common-drive controls.

**Measurements:** Turn-arrival curve; Wave attenuation; Pulse interference error; Held-out predictive likelihood.

**Would count against it:** Both mechanisms predict all interventions equally well at sensor resolution, or the supposed discriminator vanishes after matching speeds and noise.

**Main confounds:** Fitting a linear wave does not establish a conservation law. Locomotor delay, non-reciprocity and measurement smoothing can mimic inertia; present conclusions as identifiability within tested models. 

**Framing / first-test class:** measurement / offline.

**Before promotion:** Reproduce the two update equations and calibrate observation bandwidth before selecting interventions.

**Closest prior and evidence limits:**

- [[attanasi-2014-information]] — [Information transfer and behavioural inertia in starling flocks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/attanasi-2014-information.md). Biological turning-wave evidence and inertia interpretation; abstract-level catalogue anchor. Catalogue depth: abstract.
- [[hang-2026-self]] — [Self-reorganization and information transfer in large-scale models of fish schools](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hang-2026-self.md). Recent simulated front-bias mechanism provides the explicit competing explanation. Catalogue depth: full.
- [[vicsek-1995-novel]] — [Novel Type of Phase Transition in a System of Self-Driven Particles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vicsek-1995-novel.md). Overdamped alignment reference model. Catalogue depth: full.

<a id="phy-03"></a>
### PHY-03 — Polarization versus navigation value

**Update 2:** revised.

**Question:** When does increasing collective alignment reduce actual task performance?

**Candidate hypothesis:** Stronger alignment will increase polarization while slowing response to a rapidly moving goal, producing an intermediate optimum for useful transport.

**How to test:** Randomize whole simulated flock episodes to alignment strength and goal-switching frequency, fixing population, sensing range, speed limits and message budget. Give the same small informed subset access to goal changes in each paired episode. Evaluate a held-out switching schedule and score displacement toward the true goal, cohesion and collisions separately.

**Comparison:** Independent goal followers when information is available, a fixed low-alignment rule, and a matched static-goal setting separate social cost from lack of information.

**Measurements:** Goal-directed progress; Tracking lag; Polarization; Fragmentation; Control effort.

**Would count against it:** Task value rises monotonically with alignment across the tested regime, or the intermediate optimum disappears after equalizing speed and information.

**Main confounds:** Alignment, neighbour count and coupling strength are different interventions. Finite run length can reward initial conditions; a visually ordered flock can still move in the wrong direction.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Define transport utility and inspect responsiveness prior art. SwarmBench v02/v05 agent/game logs offer a separate discrete-task proxy audit after schema validation; they cannot estimate an alignment-strength intervention or establish physical-flock behavior.

**Closest prior and evidence limits:**

- [[mateo-2017-effect]] — [Effect of Correlations in Swarms on Collective Response](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mateo-2017-effect.md). Closest prior already predicts a responsiveness trade-off with connectivity. Catalogue depth: abstract.
- [[couzin-2005-effective]] — [Effective leadership and decision-making in animal groups on the move](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/couzin-2005-effective.md). Informed-minority guidance is an established mechanism. Catalogue depth: abstract.
- [[data-swarmbench-2025]] — [SwarmBench experiment logs: LLMs as decentralised agents on five 2D-grid swarm tasks (Flocking, Pursuit, Synchronize, Foraging, Transport), 13 models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-swarmbench-2025.md). LLM-grid analogy for comparing observed coordination with pursuit/transport utility; not continuous heading dynamics. Catalogue depth: skim.

<a id="phy-04"></a>
### PHY-04 — Distributed expertise under local failure

**Update 2:** unchanged.

**Question:** Does spreading informed agents through a flock make guidance more reliable than concentrating them near its front?

**Candidate hypothesis:** Spatially distributed informed agents will improve recovery from a local sensor outage, but may slow initial turns when their cues disagree.

**How to test:** Assign entire simulated flock episodes to clustered, dispersed or randomly placed informed subsets of equal size. Cross this with an independently randomized local sensor blackout and controlled disagreement among goal estimates. Use identical geometry, speed and total information for paired episodes; analyse goal error and recovery by episode, including episodes with no failure.

**Comparison:** Random placement is the primary comparator; an oracle with independent accurate cues supplies a ceiling and a fully uninformed flock supplies a negative control.

**Measurements:** Goal-direction error; Time to resume progress; Collision rate; Between-subgroup disagreement.

**Would count against it:** Dispersion provides no recovery benefit, or all benefits are explained by more favourable initial visibility rather than redundancy.

**Main confounds:** Knowledge location changes network centrality. Randomizing only identities without locations will not test spatial distribution. Synthetic failure results do not establish drone or animal resilience.

**Framing / first-test class:** extension / offline.

**Before promotion:** Read the recent controller and observation definition; first use scripted rules so training does not obscure the mechanism.

**Closest prior and evidence limits:**

- [[couzin-2005-effective]] — [Effective leadership and decision-making in animal groups on the move](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/couzin-2005-effective.md). Closest established informed-minority mechanism. Catalogue depth: abstract.
- [[choi-2026-communication]] — [Communication-Free Collective Navigation for a Swarm of UAVs via LiDAR-Based Deep Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choi-2026-communication.md). Recent five-UAV study motivates testing beyond one implicit leader; record reports limited real trials. Catalogue depth: full.
- [[strandburg-peshkin-2013-visual]] — [Visual sensory networks and effective information transfer in animal groups](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/strandburg-peshkin-2013-visual.md). Sensory networks motivate visibility control. Catalogue depth: abstract.

<a id="phy-05"></a>
### PHY-05 — Hydrodynamic breakup beyond a single model

**Update 2:** unchanged.

**Question:** Does size-dependent school fragmentation survive replacing idealized long-range fluid coupling with a screened interaction?

**Candidate hypothesis:** Breakup attributed to hydrodynamics will weaken when coupling is screened, even with the same local disturbance magnitude; this would identify long-range coherence rather than generic noise as the driver.

**How to test:** Randomize independent simulated schools to full dipolar coupling, distance-screened coupling, matched random forcing or no fluid coupling. Calibrate treatments to comparable local velocity-perturbation variance before evaluating across group sizes. Match initial density and visual rules, track groups long enough to observe remerging, and analyse whole-school episodes.

**Comparison:** Matched random forcing is the main mechanistic comparator; visual alignment without fluid coupling tests the non-hydrodynamic explanation.

**Measurements:** Fragmentation frequency; Largest-component fraction; Reunion time; Fluid-induced velocity variance.

**Would count against it:** Screening leaves breakup unchanged or matched independent forcing reproduces all breakup statistics, weakening the long-range explanation.

**Main confounds:** Screening is an artificial intervention, not a faithful model of every fluid. Near-field interactions, dimensionality and constant-speed assumptions can dominate. No inference about natural large schools follows from simulation alone.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read and reproduce the hydrodynamic model, then justify a variance-matched screening intervention and check later physical-validation work.

**Closest prior and evidence limits:**

- [[hang-2026-self]] — [Self-reorganization and information transfer in large-scale models of fish schools](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hang-2026-self.md). Closest recent prior reports size-dependent breakup under far-field dipolar flows. Catalogue depth: full.
- [[vicsek-1995-novel]] — [Novel Type of Phase Transition in a System of Self-Driven Particles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vicsek-1995-novel.md). Non-hydrodynamic alignment baseline. Catalogue depth: full.
- [[strandburg-peshkin-2013-visual]] — [Visual sensory networks and effective information transfer in animal groups](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/strandburg-peshkin-2013-visual.md). Sensory interactions must remain fixed while fluid coupling changes. Catalogue depth: abstract.

<a id="phy-06"></a>
### PHY-06 — Alternating bursts in larger groups

**Update 2:** unchanged.

**Question:** Can the pairwise benefit of alternating movement bursts scale to a school without a shared clock?

**Candidate hypothesis:** Local burst alternation will improve turn-following in small neighbourhoods, but mutually incompatible timing constraints will limit its benefit in larger dense groups.

**How to test:** Randomize simulated school episodes to reactive burst timing, independent renewal timing or closed-loop phase-response timing while matching mean speed, burst count and energy proxy. First reproduce the two-agent case, then change network motifs and group size using held-out geometry. Apply identical leader turns and analyse the entire school, recording pairwise timings as dependent measurements.

**Comparison:** A global alternating schedule is an unattainable coordination ceiling; shuffled phase responses preserve timing statistics without local feedback.

**Measurements:** Turn-following error; Neighbour retention; Burst conflict rate; Travel per energy proxy.

**Would count against it:** Closed-loop timing gives no benefit after speed matching, or independent schedules perform equally across all graph motifs.

**Main confounds:** A temporal oscillator without movement cannot establish locomotor coordination. Pairwise empirical coupling does not imply a school-wide optimum; visual and hydrodynamic feedback may change the phase-response curve.

**Framing / first-test class:** extension / offline.

**Before promotion:** Inspect phase-response extraction and couple timing to a validated movement model before scaling beyond pairs.

**Closest prior and evidence limits:**

- [[amichay-2024-revealing]] — [Revealing the mechanism and function underlying pairwise temporal coupling in collective motion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amichay-2024-revealing.md). Closest pairwise biological and virtual-reality evidence; scaling is unresolved in the record. Catalogue depth: full.
- [[wang-2025-collective]] — [Collective phases and long-term dynamics in a fish school model with burst-and-coast swimming](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wang-2025-collective.md). Related asynchronous burst-and-coast school model. Catalogue depth: abstract.
- [[amichay-2025-integration]] — [On the integration of collective motion and temporal synchrony in animal collectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amichay-2025-integration.md). Conceptual bridge between movement and timing, not empirical proof of this prediction. Catalogue depth: skim.

<a id="collective-decision"></a>
## Collective decision-making in biology

<a id="phy-07"></a>
### PHY-07 — Why can less communication help adaptation?

**Update 2:** unchanged.

**Question:** Does constrained communication improve changing-environment decisions by preserving independent sampling or simply weakening social commitment?

**Candidate hypothesis:** The benefit will depend primarily on maintaining fresh independent samples; sparse communication without increased information freshness will provide less improvement.

**How to test:** Randomize simulated robot-swarm episodes in a factorial design: communication degree and independent sampling rate vary separately, while options switch quality on a held-out schedule. Match delivered messages and locomotion costs where possible. Measure group decisions at fixed deadlines and use whole episodes as independent units.

**Comparison:** Dense and sparse voter rules with frozen sampling rates; a dense rule carrying equally fresh evidence controls for degree itself.

**Measurements:** Post-switch regret; Time to reverse majority; Independent observations per decision; Wrong-consensus duration.

**Would count against it:** Sparse communication retains its benefit after freshness and social exposure are matched, contradicting the proposed mechanism, or never benefits adaptation in the replication.

**Main confounds:** Reducing radio range changes connectivity, encounters and travel. Packet volume and unique environmental samples must be logged separately; agreement is not correctness.

**Framing / first-test class:** extension / offline.

**Before promotion:** Reproduce the voter-model result and inspect original sampling schedules; publisher access was blocked in this pass.

**Closest prior and evidence limits:**

- [[talamali-2021-when]] — [When less is more: Robot swarms adapt better to changes with constrained communication](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/talamali-2021-when.md). Closest prior already finds improved adaptation with constrained communication. Catalogue depth: abstract.
- [[march-pons-2024-honeybee]] — [Honeybee-like collective decision making in a kilobot swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/march-pons-2024-honeybee.md). Motion and density jointly affect robot communication networks. Catalogue depth: abstract.
- [[valentini-2017-best]] — [The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/valentini-2017-best.md). Best-of-n taxonomy distinguishes changing quality from sampling cost. Catalogue depth: full.

<a id="phy-08"></a>
### PHY-08 — Finite populations and multi-option deadlock

**Update 2:** unchanged.

**Question:** Does a mean-field cross-inhibition policy still make accurate decisions when only a small number of agents compare several options?

**Candidate hypothesis:** Finite-population noise will break apparent deadlocks more often than deterministic predictions suggest, while also increasing incorrect early commitments.

**How to test:** Implement the documented multi-option transition process as both an ODE and a stochastic agent model. Randomize independent swarm realizations across equal-quality and near-equal-quality option sets at matched rates. Compare decision distributions over a predeclared horizon and separately classify non-decision, correct decision and premature commitment.

**Comparison:** The original two-option parameterization, the revised multi-option rule and a simple independent-sampling majority rule provide mechanistic controls.

**Measurements:** Decision probability by deadline; Selection accuracy; Decision-time distribution; Spontaneous switching rate.

**Would count against it:** Observed stochastic decisions match the deterministic prediction without meaningful extra errors, or the difference vanishes under a faithful discretization.

**Main confounds:** Noise-induced commitment is not automatically useful symmetry breaking. Quorum threshold, population size and rate discretization interact; each trajectory is one replicate, not each time step.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Check for later finite-population analyses and verify stochastic rates conserve population before claiming a gap.

**Closest prior and evidence limits:**

- [[pais-2013-mechanism]] — [A Mechanism for Value-Sensitive Decision-Making](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pais-2013-mechanism.md). Two-option value-sensitive cross-inhibition reference. Catalogue depth: full.
- [[reina-2017-model]] — [Model of the best-of-N nest-site selection process in honeybees](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/reina-2017-model.md). Closest multi-option mean-field result; finite stochastic treatment is an explicit catalogue limitation. Catalogue depth: full.
- [[seeley-2012-stop]] — [Stop Signals Provide Cross Inhibition in Collective Decision-Making by Honeybee Swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/seeley-2012-stop.md). Biological cross-inhibition evidence, not proof of this synthetic policy. Catalogue depth: abstract.

<a id="phy-09"></a>
### PHY-09 — Group size versus independent evidence

**Update 2:** unchanged.

**Question:** Is collective accuracy determined more by the number of independent environmental cues than by the number of agents?

**Candidate hypothesis:** Accuracy will saturate or decline as agents share increasingly correlated cues; adding independently sampled agents will help more than duplicating existing evidence.

**How to test:** Randomize entire decision groups to cue-generation processes with matched marginal accuracy but different shared-noise structure. Cross group size with the number of independent cue sources, keeping total sampling cost explicit. Test both independent voting and social updating on held-out cue distributions; score known synthetic ground truth.

**Comparison:** Independent cues establish the ordinary aggregation baseline; perfect cue duplication and a single best sensor are negative and economical controls.

**Measurements:** Decision error; Calibration; Effective independent sample count; Accuracy per observation cost.

**Would count against it:** Larger groups improve equally under duplicated and independent cues, or the predicted saturation is explained solely by changing marginal cue quality.

**Main confounds:** Shared environmental noise differs from copying another agent. Estimating correlation after social interaction cannot recover the original cue process without intervention. This is a benchmarked mechanism test, not a new wisdom-of-crowds principle.

**Framing / first-test class:** replication / offline.

**Before promotion:** Choose a transparent generative cue model and examine original finite-group assumptions before extending to embodied sampling.

**Closest prior and evidence limits:**

- [[kao-2014-decision]] — [Decision accuracy in complex environments is often maximized by small group sizes](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kao-2014-decision.md). Closest prior already derives finite optimal groups under correlated cues. Catalogue depth: abstract.
- [[couzin-2005-effective]] — [Effective leadership and decision-making in animal groups on the move](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/couzin-2005-effective.md). Information distribution within moving groups offers an embodied follow-up. Catalogue depth: abstract.
- [[valentini-2017-best]] — [The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/valentini-2017-best.md). Formal option-quality comparison context. Catalogue depth: full.

<a id="phy-10"></a>
### PHY-10 — Correcting fast-sampling option bias

**Update 2:** unchanged.

**Question:** Can a swarm identify the best option when inferior options are faster to inspect?

**Candidate hypothesis:** Weighting reports by independent completed inspections, with an explicit travel-cost correction, will reduce bias toward cheap options at a possible delay cost.

**How to test:** Randomize simulated group episodes to option layouts that independently set true quality and sampling time. Compare fixed decision rules at equal wall-clock deadlines and at equal total inspection counts. Analyse the whole group; record every attempted inspection, completed measurement and repeated report. Hold out quality-cost correlations when evaluating.

**Comparison:** Uncorrected majority, the fastest-to-sample option and centralized access to the same completed samples form practical comparators.

**Measurements:** Selected true quality; Regret at deadline; Travel and inspection cost; Time to adequate confidence.

**Would count against it:** Correction fails to reduce bias or harms quality enough that the speed-adjusted trade-off is worse than simple voting.

**Main confounds:** Quality and cost must be independently manipulated. Counting repeated reports as new samples manufactures evidence; correction may need unavailable travel-time knowledge and should be tested with estimated as well as oracle costs.

**Framing / first-test class:** extension / offline.

**Before promotion:** Search existing antagonistic best-of-n controllers; specify which cost estimate each robot can actually observe.

**Closest prior and evidence limits:**

- [[valentini-2017-best]] — [The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/valentini-2017-best.md). Closest prior explicitly formalizes antagonistic quality-cost choices. Catalogue depth: full.
- [[reina-2017-model]] — [Model of the best-of-N nest-site selection process in honeybees](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/reina-2017-model.md). Quality-sensitive recruitment provides a mechanism to compare. Catalogue depth: full.
- [[march-pons-2024-honeybee]] — [Honeybee-like collective decision making in a kilobot swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/march-pons-2024-honeybee.md). Embodied communication and movement can confound sampling frequency. Catalogue depth: abstract.

<a id="phy-11"></a>
### PHY-11 — When uninformed participants help

**Update 2:** unchanged.

**Question:** Do uninformed agents improve a decision because they dilute commitment or because their movement changes connectivity?

**Candidate hypothesis:** Uninformed participants will help resolve conflicting preferences in some regimes, but that benefit will shrink when degree and movement are held constant.

**How to test:** Randomize simulated group episodes to informed, uninformed or inactive replacements while preserving total bodies. Cross this with static versus moving communication graphs and conflicting directional preferences. Use a task where compromise and choosing either alternative have explicit utilities; evaluate complete-group outcomes.

**Comparison:** A smaller informed-only group and a full-size group with neutral message relays distinguish population, dilution and connectivity effects.

**Measurements:** Probability of each decision; Utility of compromise; Decision time; Connectivity history.

**Would count against it:** Uninformed agents never improve task utility in the prespecified conflict regimes, or their benefit remains equally large after motion and contact histories are matched.

**Main confounds:** There may be no objectively correct option. Do not label any consensus a success; define the payoff before simulation. An inactive physical body is not equivalent to removing a node, and subgroup means hide fragmentation.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Inspect the subgroup model and define task utility for compromise, including symmetric equal-value cases.

**Closest prior and evidence limits:**

- [[leonard-2012-decision]] — [Decision versus compromise for animal groups in motion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leonard-2012-decision.md). Closest prior predicts decision-versus-compromise effects of uninformed groups. Catalogue depth: abstract.
- [[couzin-2005-effective]] — [Effective leadership and decision-making in animal groups on the move](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/couzin-2005-effective.md). Established informed-minority framework. Catalogue depth: abstract.
- [[march-pons-2024-honeybee]] — [Honeybee-like collective decision making in a kilobot swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/march-pons-2024-honeybee.md). Motion changes communication structure in an embodied decision system. Catalogue depth: abstract.

<a id="phy-12"></a>
### PHY-12 — Reopening a settled decision

**Update 2:** unchanged.

**Question:** Can occasional independent reinspection reverse an obsolete consensus without creating constant churn?

**Candidate hypothesis:** A small continuing reinspection rate will improve cumulative utility after option changes, with excessive reinspection causing instability in stationary environments.

**How to test:** Randomize whole swarm episodes to permanent commitment, fixed reinspection, or evidence-triggered reopening. Independently vary option change points and sensor noise; use the same event schedules across policies. Match the inspection budget or report its cost explicitly, and evaluate stationary sequences as well as changing ones.

**Comparison:** A standard voter-style adaptive rule and an oracle change detector separate the value of reconsideration from detecting the switch.

**Measurements:** Cumulative option-quality regret; Wrong-consensus duration; Unnecessary reversals; Inspection cost.

**Would count against it:** No policy improves the joint regret-and-churn trade-off over the standard adaptive rule, or benefits disappear at equal inspection cost.

**Main confounds:** A detector may accidentally receive privileged change information. Permanent commitment can be artificially weak; recent adaptive decision literature must be checked before novelty claims. The environment, not the number of votes, defines correctness.

**Framing / first-test class:** extension / offline.

**Before promotion:** Identify the strongest existing adaptive baseline and freeze a realistic change-point schedule before protocol selection.

**Closest prior and evidence limits:**

- [[talamali-2021-when]] — [When less is more: Robot swarms adapt better to changes with constrained communication](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/talamali-2021-when.md). Closest prior establishes dynamic adaptation and communication trade-offs. Catalogue depth: abstract.
- [[leonard-2024-fast]] — [Fast and Flexible Multiagent Decision-Making](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leonard-2024-fast.md). Related nonlinear opinion dynamics review emphasizes flexibility. Catalogue depth: abstract.
- [[valentini-2017-best]] — [The Best-of-n Problem in Robot Swarms: Formalization, State of the Art, and Novel Perspectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/valentini-2017-best.md). Dynamic option quality is an established best-of-n variant. Catalogue depth: full.

<a id="swarm-robotics"></a>
## Swarm robotics

<a id="phy-19"></a>
### PHY-19 — Who creates the observed coordination?

**Update 2:** unchanged.

**Question:** How much apparent yielding and collision avoidance comes from a learned policy versus a testbed safety filter?

**Candidate hypothesis:** Some coordination attributed to the policy will be introduced by command projection; policy rankings will change when evaluated on raw commands as well as executed motion.

**How to test:** Replay identical simulated navigation episodes with each controller followed by no filter, the same collision-avoidance filter or a minimal independent filter. Randomize controller-filter combinations across paired seeds and log both proposed and executed commands. No unsafe physical runs are required; compare episode-level success and intervention burden.

**Comparison:** A naive goal controller with the full safety filter and the learned controller without it separate policy capability from infrastructure support.

**Measurements:** Success rate; Collision rate in simulation; Filter intervention magnitude; Travel delay; Raw-command safety margin.

**Would count against it:** Rankings and coordination signatures remain unchanged across filters, with negligible projection in successful episodes.

**Main confounds:** Removing a filter can move the policy outside its design assumptions; that limitation should be reported rather than hidden. Hardware testbeds may use global tracking, so results are not automatically local-sensing swarm results.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Identify the exact deployed control stack and preserve intended operating constraints; first audit policies in simulation only.

**Closest prior and evidence limits:**

- [[pickem-2017-robotarium]] — [The Robotarium: A remotely accessible swarm robotics research testbed](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pickem-2017-robotarium.md). Closest source explicitly uses barrier-certificate command projection. Catalogue depth: skim.
- [[zhang-2025-learning]] — [Learning vision-based agile flight via differentiable physics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2025-learning.md). Recent learned communication-free navigation motivates careful attribution. Catalogue depth: full.
- [[gh-proroklab-vectorizedmultiagentsimulator]] — [VMAS: vectorised differentiable 2D multi-agent simulator in PyTorch with multi-robot scenarios including flocking](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-proroklab-vectorizedmultiagentsimulator.md). Possible batched simulation environment; its physics differs from an aerial robot. Catalogue depth: ran.

<a id="phy-20"></a>
### PHY-20 — When a few messages add value

**Update 2:** unchanged.

**Question:** Does limited communication help decentralized navigation specifically when visual observations are ambiguous?

**Candidate hypothesis:** A small intent message will improve throughput under occlusion and symmetric encounters more than under fully visible scenes, provided it is fresh and reliable.

**How to test:** Train or obtain paired navigation controllers with the same sensors and parameter budget, allowing one a fixed-rate local intent channel. Randomize held-out simulated episodes to visibility conditions, message delay and silent-channel controls. Keep safety filtering identical and analyse whole-episode success, travel time and communication cost.

**Comparison:** A stronger vision-only policy, a stale-message condition and a centralized intent oracle bound the incremental value of communication.

**Measurements:** Collision-free completion; Bottleneck throughput; Time-to-goal; Bytes per completed task; Sensitivity to stale messages.

**Would count against it:** Messages offer no improvement over the matched vision-only controller, or gains require unrealistic latency or hidden global state.

**Main confounds:** Adding a communication module also changes training capacity and optimization. Co-navigation does not establish flocking, and simulation throughput does not establish flight safety or hardware scalability.

**Framing / first-test class:** extension / training.

**Before promotion:** Confirm released policies, training recipe and compute budget; define message contents that can actually be produced by local observations.

**Closest prior and evidence limits:**

- [[zhang-2025-learning]] — [Learning vision-based agile flight via differentiable physics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2025-learning.md). Closest recent communication-free co-navigation anchor. Catalogue depth: full.
- [[choi-2026-communication]] — [Communication-Free Collective Navigation for a Swarm of UAVs via LiDAR-Based Deep Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choi-2026-communication.md). Recent implicit leader-following with local LiDAR motivates comparison under constrained sensing. Catalogue depth: full.
- [[berlinger-2021-implicit]] — [Implicit coordination for 3D underwater collective behaviors in a fish-inspired robot swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/berlinger-2021-implicit.md). Underwater visual coordination illustrates an embodied alternative with different optics. Catalogue depth: abstract.

<a id="phy-21"></a>
### PHY-21 — Correlated disturbances in transfer

**Update 2:** unchanged.

**Question:** Do policies robust to independent sensor noise fail when an entire swarm shares the same bias?

**Candidate hypothesis:** Shared localization or timing errors will cause larger collective failures than independent errors of the same marginal magnitude; training only with independent noise will overstate resilience.

**How to test:** Randomize held-out simulated multi-robot episodes to independent, spatially correlated or common-mode disturbances, matching each robot's marginal error distribution. Compare a frozen controller with versions trained using each noise structure. Use identical task layouts, actuator bounds and safety filters; treat entire episodes and training seeds as separate uncertainty levels.

**Comparison:** Noise-free evaluation and a simple geometry-based controller provide ceilings and interpretable references.

**Measurements:** Group completion; Collision count; Systematic drift; Error amplification; Performance per training seed.

**Would count against it:** Matched shared noise causes no extra degradation, or independently randomized training generalizes equally to all correlation structures.

**Main confounds:** A global coordinate shift can be harmless if the task shifts with it; perturb sensors while keeping world truth fixed. Common random numbers aid paired comparison but are not extra independent trials. Hardware transfer remains untested.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Choose a released controller and define physically meaningful sensor perturbations; read existing correlated domain-randomization work.

**Closest prior and evidence limits:**

- [[zhang-2025-learning]] — [Learning vision-based agile flight via differentiable physics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2025-learning.md). Simple-physics sim-to-real policy is the relevant transfer context. Catalogue depth: full.
- [[sun-2023-mean]] — [Mean-shift exploration in shape assembly of robot swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/sun-2023-mean.md). Common reference-frame dependence creates a concrete shared-error pathway. Catalogue depth: full.
- [[gh-proroklab-vectorizedmultiagentsimulator]] — [VMAS: vectorised differentiable 2D multi-agent simulator in PyTorch with multi-robot scenarios including flocking](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-proroklab-vectorizedmultiagentsimulator.md). Candidate simulation scaffold; no claim that its stock scenarios reproduce either paper. Catalogue depth: ran.

<a id="phy-22"></a>
### PHY-22 — Correlated evidence in physical identity vetting

**Update 2:** unchanged.

**Question:** Does collaborative identity vetting remain reliable when neighbours share correlated radio-observation errors?

**Candidate hypothesis:** Collaborative voting will overstate confidence when trust observations have shared bias; explicit dependence-aware aggregation will reduce false exclusion at a possible detection delay cost.

**How to test:** In an authorized synthetic radio-observation simulator, randomize whole network episodes to independent versus common-mode errors with identical per-message accuracy. Add a fixed number of simulated duplicate identities and keep physical transmitters constant. Compare trust aggregation on the same observation traces; score whole-network outcomes and never target live networks.

**Comparison:** The published independence-based scheme, direct local vetting and an oracle physical-identity map are reference conditions.

**Measurements:** False exclusion of legitimate robots; Duplicate-identity acceptance; Rounds to decision; Target-tracking error.

**Would count against it:** Correlation has no measurable effect, or the proposed correction sacrifices detection without reducing false exclusions.

**Main confounds:** Physical transmitter identity differs from software authorship. Multiple actual radios, mobility and multipath violate different assumptions and should not be conflated. Synthetic scores cannot establish real radio robustness.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read the original guarantee and reproduce it under its own assumptions before relaxing observation independence.

**Closest prior and evidence limits:**

- [[mallmann-trenn-2021-crowd]] — [Crowd Vetting: Rejecting Adversaries via Collaboration With Application to Multirobot Flocking](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mallmann-trenn-2021-crowd.md). Closest collaborative vetting prior; record explicitly notes independence and static-membership assumptions. Catalogue depth: full.
- [[gil-2015-guaranteeing]] — [Guaranteeing Spoof-Resilient Multi-Robot Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gil-2015-guaranteeing.md). Underlying spatial radio-fingerprint evidence, with physical assumptions. Catalogue depth: skim.
- [[leblanc-2013-resilient]] — [Resilient Asymptotic Consensus in Robust Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leblanc-2013-resilient.md). Robust consensus context; graph robustness is not a substitute for a reliable identity signal. Catalogue depth: abstract.

<a id="phy-23"></a>
### PHY-23 — Seed dependence in shape formation

**Update 2:** revised.

**Question:** How much of distributed shape assembly relies on a small privileged set of coordinate seeds?

**Candidate hypothesis:** Losing coordinate seeds early will damage goal-shape accuracy more than losing the same number of ordinary robots, even when surviving robots remain connected.

**How to test:** Randomize independently seeded shape-assembly simulations to equal-count seed failure, ordinary-node failure or sham removal at matched assembly stages. Include stationary failed bodies as well as removed bodies. Compare coordinate-based and seedless morphogenetic controllers on compatible shape tasks, separating precise shape fidelity from successful connected assembly.

**Comparison:** Random robot failure is the primary comparator; an intact seeded controller and a global-coordinate oracle reveal localization dependence.

**Measurements:** Shape error; Completion time; Connected mass; Localization inconsistency; Recovery from seed loss.

**Would count against it:** Seed failures are no worse than matched ordinary failures, or the effect disappears once physical blockage and available robot count are controlled.

**Main confounds:** Seedless organic growth need not solve the same specified-shape problem. Give each method an attainable target and do not declare a winner on incompatible objectives; simulator localization may leak global coordinates.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Retrieve compatible robot controllers and verify coordinate privileges. Separately inspect SwarmBench v01 agent views, prompts and game states for assumed global coordinates; its shape-task traces motivate a synthetic information-control analogue, not robot seed-failure evidence.

**Closest prior and evidence limits:**

- [[rubenstein-2014-programmable]] — [Programmable self-assembly in a thousand-robot swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rubenstein-2014-programmable.md). Closest seeded programmable shape-assembly reference. Catalogue depth: abstract.
- [[slavkov-2018-morphogenesis]] — [Morphogenesis in robot swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/slavkov-2018-morphogenesis.md). Seedless morphogenesis is a contrasting task family, not a drop-in equivalent. Catalogue depth: abstract.
- [[data-swarmbench-2025]] — [SwarmBench experiment logs: LLMs as decentralised agents on five 2D-grid swarm tasks (Flocking, Pursuit, Synchronize, Foraging, Transport), 13 models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-swarmbench-2025.md). A shape-formation prompt appears in the Flocking log preview; a coordinate-information analogy only, with task semantics requiring code verification. Catalogue depth: skim.

<a id="phy-24"></a>
### PHY-24 — Damage recovery with immobile survivors

**Update 2:** unchanged.

**Question:** Do swarms that recover after robots are removed also recover when damaged robots remain as obstacles?

**Candidate hypothesis:** Recovery will be substantially worse when failed bodies occupy important passages, and local failure-aware rerouting will help more than simply adding healthy robots.

**How to test:** Randomize whole simulated assembly or transport episodes to equal-count removal, actuator failure in place, communication failure or combined failure. Match the location and timing of each failure across treatments. Compare standard local rules with explicit blocked-region avoidance, and measure functional task recovery independently from reformed shape.

**Comparison:** The same number of robots absent from initialization controls for lower capacity; static obstacle insertion controls for physical blockage.

**Measurements:** Recovered task throughput; Persistent trapped mass; Recovery time; Collision pressure proxy; Additional motion cost.

**Would count against it:** In-place failures are no worse than removal after geometry matching, or failure-aware rerouting gives no advantage over a generic obstacle controller.

**Main confounds:** Disabled agents that still transmit differ from silent obstacles. A point-particle model cannot test jamming, and a regrown image says nothing about cargo transport or task competence.

**Framing / first-test class:** extension / offline.

**Before promotion:** Find the exact source damage protocol and choose a simulator with contact and actuator-failure semantics.

**Closest prior and evidence limits:**

- [[slavkov-2018-morphogenesis]] — [Morphogenesis in robot swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/slavkov-2018-morphogenesis.md). Regrowth after removed material motivates the stronger failure model. Catalogue depth: abstract.
- [[sun-2023-mean]] — [Mean-shift exploration in shape assembly of robot swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/sun-2023-mean.md). Shape assembly and cargo transport offer separate geometric and functional outcomes. Catalogue depth: full.
- [[gh-ilpincy-argos3]] — [ARGoS 3: physics-based multi-robot simulator built for large swarms (multiple physics engines, thousands of robots)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-ilpincy-argos3.md). Potential embodied simulator, subject to controller and contact-model verification. Catalogue depth: skim.

**Related team work:** [nca-observatory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/nca-observatory.md).

<a id="phy-37"></a>
### PHY-37 — Neural cellular repair beyond familiar lesion shapes

**Update 2:** unchanged.

**Question:** Does a learned NCA repair task-critical hidden-state cuts as reliably as equally large random circular lesions?

**Candidate hypothesis:** A cut across an active reasoning front will delay valid-solution recovery more than an equal-area random lesion, even when rendered outputs appear similarly restored.

**How to test:** Using one documented maze NCA checkpoint, randomize held-out puzzle rollouts to hidden-state erasure across the reasoning front, matched-area random erasure or sham damage. Preserve task inputs, freeze weights and pair update randomness. Match erased-state magnitude where feasible; evaluate exact valid paths over a fixed cell-update budget. Analyse independent puzzles, with rollout seeds nested within puzzles.

**Comparison:** The source circular-damage condition tests replication; restarting the same checkpoint from the intact input measures whether continued-state repair actually saves work.

**Measurements:** Exact path validity; Recovery cell updates; Output-image similarity; Failure probability.

**Would count against it:** Front-crossing damage is no worse than matched random damage, or apparent differences disappear after erased-state magnitude and pre-damage progress are matched.

**Main confounds:** The reasoning front must be defined before seeing recovery. Maze NCAs are computational systems, not physical robots; morphology scores and constraint satisfaction are separate outcomes.

**Framing / first-test class:** boundary-test / access-dependent.

**Before promotion:** Confirm checkpoint access and training damage, reproduce the baseline and search existing structured-lesion tests.

**Closest prior and evidence limits:**

- [[etcheverry-2026-reasoning]] — [Reasoning with Neural Cellular Automata](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/etcheverry-2026-reasoning.md). Closest prior already studies maze damage and adaptive updates; the proposed difference is lesion topology. Catalogue depth: skim.
- [[mordvintsev-2020-growing]] — [Growing Neural Cellular Automata](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mordvintsev-2020-growing.md). Earlier learned regeneration baseline; image recovery alone does not test maze validity. Catalogue depth: skim.

**Related team work:** [nca-observatory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/nca-observatory.md).

<a id="phy-38"></a>
### PHY-38 — Masked parallel updates versus independent cell clocks

**Update 2:** unchanged.

**Question:** Does an NCA trained with random update masks preserve its task performance under event-driven local execution with stale neighbour reads?

**Candidate hypothesis:** Removing common snapshot reads will reduce accuracy at matched cell-update count; extra robustness training may be necessary even when each cell has the same marginal firing rate.

**How to test:** Randomize held-out NCA maze episodes to source-style masked parallel updates, sequential fresh-state updates, or event-driven updates with bounded read delays. Freeze the learned rule, initial state and total cell updates; vary scheduling independently of task difficulty. Analyse full episodes, with seeds nested within task instances, and separately measure actual execution time.

**Comparison:** The released masked-update implementation is the reference; sequential execution with zero read delay separates update ordering from stale information.

**Measurements:** Task success; Cell updates to criterion; Wall-clock time; Long-horizon stability.

**Would count against it:** Task performance and stability remain equivalent across schedules within prespecified tolerance, or degradation is explained entirely by unequal updates rather than execution semantics.

**Main confounds:** Bernoulli masking emulates asynchrony but need not reproduce a distributed runtime. Dense masked arithmetic is not dormant-cell energy savings. Classical cellular automata are separate controls, not substitutes for learned weights.

**Framing / first-test class:** boundary-test / access-dependent.

**Before promotion:** Obtain runnable weights, specify read/write semantics and check asynchronous-NCA prior work before selecting tolerances.

**Closest prior and evidence limits:**

- [[mordvintsev-2020-growing]] — [Growing Neural Cellular Automata](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mordvintsev-2020-growing.md). Original learned NCA uses stochastic per-cell masking. Catalogue depth: skim.
- [[etcheverry-2026-reasoning]] — [Reasoning with Neural Cellular Automata](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/etcheverry-2026-reasoning.md). Reasoning NCA reports dense computation before masking, motivating an execution-semantics boundary test. Catalogue depth: skim.

**Related team work:** [nca-observatory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/nca-observatory.md).

<a id="swarm-intelligence"></a>
## Swarm intelligence algorithms

<a id="opt-01"></a>
### OPT-01 — Performance after shifting and rotating the problem

**Update 2:** unchanged.

**Question:** Do attractive optimizer rankings survive removal of coordinate advantages?

**Candidate hypothesis:** Rankings on centered axis-aligned functions will change after random translation and rotation, beyond seed variability.

**How to test:** Run frozen implementations on paired original, shifted and rotated instances of several function families. Use equal objective-call and tuning budgets; analyze independent function instances, with repeated seeds nested within instance.

**Comparison:** Random search, differential evolution, CMA-ES and a standard PSO implementation.

**Measurements:** Anytime best-value curve; evaluations to target; rank stability; failure rate.

**Would count against it:** Rankings remain stable across transformations within uncertainty on held-out families.

**Main confounds:** Boundary handling can reintroduce bias; transform constraints consistently and charge all evaluations.

**Framing / first-test class:** replication / offline.

**Before promotion:** Pin optimizer versions and reserve transformed functions for evaluation rather than tuning.

**Closest prior and evidence limits:**

- [[kudela-2023-evolutionary]] — [The Evolutionary Computation Methods No One Should Use](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kudela-2023-evolutionary.md). Direct center-bias test predecessor. Catalogue depth: full.
- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Broad benchmarking and budget-sensitive rankings. Catalogue depth: full.

<a id="opt-02"></a>
### OPT-02 — Communication topology under a fair budget

**Update 2:** unchanged.

**Question:** Does sparse communication improve search by preserving diversity or merely by changing computation cost?

**Candidate hypothesis:** A sparse PSO topology will delay premature collapse on multimodal tasks at equal objective evaluations, with task-dependent tradeoffs.

**How to test:** Randomize independent optimizer runs across global, ring and degree-matched rewired graphs. Match particle count, objective calls and update frequency; separately report wall-clock and messages. Evaluate on held-out multimodal and unimodal functions.

**Comparison:** Global-best PSO, independent restarts, and a fixed sparse topology.

**Measurements:** Best objective; population diversity; evaluations to target; messages; wall-clock.

**Would count against it:** Sparse topology does not delay collapse or improve search over dense PSO after matching updates and evaluation budgets. If independent restarts match the gain, prefer the simpler method; that alone does not refute the topology effect.

**Main confounds:** Stale best values and asynchronous updates can change the algorithm independently of topology.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read topology/update definitions and include objective-evaluation cost in every comparison.

**Closest prior and evidence limits:**

- [[kennedy-1999-small]] — [Small worlds and mega-minds: effects of neighborhood topology on particle swarm performance](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kennedy-1999-small.md). Direct topology precedent; not a new sparse-swarm idea. Catalogue depth: abstract.
- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Benchmarking framework to prevent single-function conclusions. Catalogue depth: full.

<a id="opt-03"></a>
### OPT-03 — How much of ant-colony performance is local search?

**Update 2:** unchanged.

**Question:** Does pheromone sharing contribute after a strong local-search component is matched?

**Candidate hypothesis:** The incremental benefit of pheromone will shrink when all variants share identical local search, particularly on easy instances.

**How to test:** Use a factorial design over pheromone sharing and local search on held-out routing instances. Pair random seeds and initial tours; charge edge evaluations and local-search calls to the same total budget.

**Comparison:** Multistart local search, randomized construction plus local search, and full ant-colony system.

**Measurements:** Tour gap to reference; objective evaluations; improvement attributed to each component.

**Would count against it:** The pheromone benefit is unchanged or larger after adding matched local search, rather than shrinking, on held-out instance families. A smaller but still positive benefit is compatible with the prediction.

**Main confounds:** Wall-clock alone can reward a faster implementation; also measure operation and objective-call budgets.

**Framing / first-test class:** replication / offline.

**Before promotion:** Read exact update rules and select routing instances with reliable reference solutions.

**Closest prior and evidence limits:**

- [[dorigo-1997-ant]] — [Ant colony system: a cooperative learning approach to the traveling salesman problem](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dorigo-1997-ant.md). ACS and ACS with local search are the closest original comparisons. Catalogue depth: abstract.
- [[camacho-villalon-2023-exposing]] — [Exposing the grey wolf, moth-flame, whale, firefly, bat, and antlion algorithms: six misleading optimization techniques inspired by bestial metaphors](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/camacho-villalon-2023-exposing.md). Component-level analysis motivation, not evidence about this ablation. Catalogue depth: abstract.

<a id="opt-04"></a>
### OPT-04 — Independent evaluations versus noisy consensus

**Update 2:** unchanged.

**Question:** When does a shared best solution amplify measurement noise?

**Candidate hypothesis:** Reevaluating promising solutions with independent noise will reduce false convergence more than adding particles at equal objective-call budget.

**How to test:** Add controlled unbiased and correlated noise to known objectives. Randomize runs to more particles, repeated evaluations, or robust selection. Hold calls fixed and evaluate final solutions with a separate high-precision audit stream.

**Comparison:** Naive best-observed selection, independent restarts, and equal-call averaging.

**Measurements:** True final objective; winner selection bias; noise sensitivity; evaluation count.

**Would count against it:** Extra independent evaluation does not outperform particles, or benefit disappears under held-out noise models.

**Main confounds:** A high-precision evaluator is a diagnostic unavailable to the optimizer; never feed audit truth back into selection.

**Framing / first-test class:** extension / offline.

**Before promotion:** Check noisy-optimization prior work before claiming novelty and separate shared from independent noise.

**Closest prior and evidence limits:**

- [[pinnau-2017-consensus]] — [A consensus-based model for global optimization and its mean-field limit](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pinnau-2017-consensus.md). Weighted collective optimization mechanism to stress under noisy objective values. Catalogue depth: full.
- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Budget-aware evaluation precedent; noisy setting is an extension to verify. Catalogue depth: full.

<a id="opt-05"></a>
### OPT-05 — When collective memory becomes stale

**Update 2:** unchanged.

**Question:** Can selective forgetting beat full restart after the objective changes?

**Candidate hypothesis:** Age-weighted best-state memory will reduce post-change regret compared with permanent memory, while retaining more value than full restart.

**How to test:** Create independent dynamic objective sequences with randomized changes in optimum and irrelevant surface details. Compare fixed memory, age decay, detected-change reset and full restart with equal objective-call budgets and hidden change times.

**Comparison:** Permanent personal/global best, periodic restart, and oracle change notification as ceiling.

**Measurements:** Dynamic regret; recovery evaluations; false resets; stationary performance loss.

**Would count against it:** Periodic restart matches the gain or age decay loses more in stationary periods than it recovers after changes.

**Main confounds:** Decay can merely inject exploration; compare with matched random perturbation.

**Framing / first-test class:** extension / offline.

**Before promotion:** Survey dynamic optimization before promotion; fix change distributions and scoring horizon.

**Closest prior and evidence limits:**

- [[grassi-2021-particle]] — [From particle swarm optimization to consensus based optimization: stochastic modeling and mean-field limit](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/grassi-2021-particle.md). Personal-best memory is explicit in the PSO-to-CBO framing. Catalogue depth: full.
- [[dorigo-1996-ant]] — [Ant system: optimization by a colony of cooperating agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dorigo-1996-ant.md). Pheromone persistence/evaporation provides a related memory mechanism. Catalogue depth: abstract.

<a id="opt-06"></a>
### OPT-06 — Where the small-inertia approximation stops helping

**Update 2:** unchanged.

**Question:** Does a consensus approximation retain practical optimizer behavior outside the asymptotic regime?

**Candidate hypothesis:** CBO-like and PSO-like trajectories will agree better as inertia shrinks; optimization rankings will diverge more at small than large particle counts in the chosen test regime.

**How to test:** Reproduce a simple published small-inertia setting, then vary inertia and particle count independently on paired objectives. Compare distributional trajectories and held-out optimization success, using independent run seeds.

**Comparison:** Original PSO formulation, its stated CBO approximation, and a numerical step-size convergence control.

**Measurements:** Distribution distance; final objective; failure probability; numerical stability.

**Would count against it:** After controlling discretization, trajectory error does not fall as inertia shrinks, or rankings are no less stable at small particle counts. Score these two predictions separately; neither alone decides the other.

**Main confounds:** Parameters must be mapped according to the derivation; arbitrary matching is not a test of the approximation.

**Framing / first-test class:** replication / offline.

**Before promotion:** Read the parameter mapping and convergence assumptions fully; do not equate consensus with a global optimum.

**Closest prior and evidence limits:**

- [[grassi-2021-particle]] — [From particle swarm optimization to consensus based optimization: stochastic modeling and mean-field limit](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/grassi-2021-particle.md). Direct formal-limit predecessor; replication first. Catalogue depth: full.
- [[pinnau-2017-consensus]] — [A consensus-based model for global optimization and its mean-field limit](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pinnau-2017-consensus.md). CBO formulation and assumptions. Catalogue depth: full.

<a id="active-matter"></a>
## Active matter physics

<a id="phy-13"></a>
### PHY-13 — Same cluster, different mechanism

**Update 2:** unchanged.

**Question:** Can localized release distinguish density-dependent motility from alignment-driven aggregation when snapshots look similar?

**Candidate hypothesis:** A temporary local motility release will dissolve density-trapped clusters differently from equally dense alignment clusters, allowing a small intervention to identify mechanism.

**How to test:** Construct two simulated particle models calibrated to similar cluster-size and density distributions. Randomize independent realizations to a local speed pulse, local heading randomization or sham pulse. Freeze calibration before testing and compare both immediate transport and return to the previous state on held-out densities.

**Comparison:** Constant-speed repulsive particles and a non-interacting density-matched snapshot distinguish collective feedback from passive dispersal.

**Measurements:** Escape flux; Cluster lifetime; Polarization change; Recovery trajectory prediction.

**Would count against it:** No intervention separates the fitted models at measurement resolution, or discrimination comes entirely from unmatched initial densities or speeds.

**Main confounds:** Similar shapes do not imply equivalent dynamics. Soft overlaps, boundaries and definitions of a cluster can create artificial differences; report the result as identification within explicit model families rather than a universal diagnostic.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Choose two models that can genuinely be matched on baseline observables; verify that perturbations do not change particle number or packing fraction.

**Closest prior and evidence limits:**

- [[fily-2012-athermal]] — [Athermal Phase Separation of Self-Propelled Particles with No Alignment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fily-2012-athermal.md). Established phase separation without alignment is the competing mechanism. Catalogue depth: full.
- [[cates-2015-motility]] — [Motility-Induced Phase Separation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cates-2015-motility.md). Review supplies density-speed feedback context. Catalogue depth: full.
- [[vicsek-1995-novel]] — [Novel Type of Phase Transition in a System of Self-Driven Particles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vicsek-1995-novel.md). Alignment reference, requiring additional cohesion or confinement for fair comparison. Catalogue depth: full.

<a id="phy-14"></a>
### PHY-14 — Wall geometry as a control input

**Update 2:** unchanged.

**Question:** Can boundary shape guide an inertial robot aggregate while preserving useful bulk mixing?

**Candidate hypothesis:** A shaped boundary will bias collective transport, but apparent guidance will partly be paid for by trapping particles near walls and reducing bulk exploration.

**How to test:** Randomize independent simulations of inertial active rods among circular, asymmetric and deformable arenas with equal accessible area. Match propulsion, dissipation and wall interaction law; assign source and target regions independently of the shape orientation. Score transport and visited area across complete episodes, then rotate the geometry as a directional control.

**Comparison:** An isotropic boundary and a propulsion-bias controller with matched energy provide geometry-only and actuation comparators.

**Measurements:** Net material transport; Bulk area visited; Wall residence time; Work proxy; Target arrival rate.

**Would count against it:** Boundary shaping produces no directional advantage, or apparent gain disappears after accounting for wall-trapped mass.

**Main confounds:** Geometry changes collision frequency and effective area. The source system uses inertial vibration-driven rods, so an overdamped point-particle simulator is not a faithful replication. Shapes must not grant a shorter trivial route.

**Framing / first-test class:** extension / offline.

**Before promotion:** Recover an inertial rod model and establish comparable accessible area; later hardware validation would require suitable actuators and an arena.

**Closest prior and evidence limits:**

- [[deblais-2018-boundaries]] — [Boundaries Control Collective Dynamics of Inertial Self-Propelled Robots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/deblais-2018-boundaries.md). Closest prior already demonstrates surface clusters and arena transport. Catalogue depth: abstract.
- [[deseigne-2010-collective]] — [Collective Motion of Vibrated Polar Disks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/deseigne-2010-collective.md). Physical bounded polar-disk system illustrates boundary and collision effects. Catalogue depth: full.
- [[brambilla-2013-swarm]] — [Swarm robotics: a review from the swarm engineering perspective](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/brambilla-2013-swarm.md). Task-oriented robotics context rather than evidence of this trade-off. Catalogue depth: abstract.

<a id="phy-15"></a>
### PHY-15 — Delayed density sensing in motility control

**Update 2:** unchanged.

**Question:** Does delayed quorum sensing destabilize otherwise stable active-particle aggregates?

**Candidate hypothesis:** Delayed density-dependent speed updates will induce repeated aggregation and dissolution beyond a response-time range, and hysteretic switching may suppress that cycle.

**How to test:** Randomize simulated particle populations to instantaneous, delayed or hysteretic speed control with matched sensing range and mean propulsion budget. Introduce a standardized density displacement after equilibration and evaluate independent realizations over long horizons. Compare explicit asynchronous update clocks with synchronous updates at the same mean rate.

**Comparison:** Constant motility, instantaneous quorum control and a low-pass filtered estimate separate delay from measurement noise.

**Measurements:** Aggregate persistence; Density oscillation amplitude; Response overshoot; Energy proxy; Time outside target density.

**Would count against it:** Delay causes only a smooth slowing without cycles, or hysteresis fails to improve persistence at matched energy and target density.

**Main confounds:** The experimental anchor computes local rules externally using camera and laser infrastructure. It does not establish autonomous colloid sensing. Numerical time steps, delayed-state interpolation and density estimation can create spurious oscillations.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Reproduce the undelayed rule and derive dimensionless delay relative to rotational and aggregation times before choosing a sweep.

**Closest prior and evidence limits:**

- [[bauerle-2018-self]] — [Self-organization of active particles by quorum sensing rules](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bauerle-2018-self.md). Closest experimental quorum-motility rule; heading is not directly controlled. Catalogue depth: full.
- [[cates-2015-motility]] — [Motility-Induced Phase Separation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cates-2015-motility.md). Density-speed positive feedback explains a plausible instability mechanism. Catalogue depth: full.
- [[fily-2012-athermal]] — [Athermal Phase Separation of Self-Propelled Particles with No Alignment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fily-2012-athermal.md). Constant-rule active-particle baseline. Catalogue depth: full.

<a id="phy-16"></a>
### PHY-16 — Reciprocity and useful collective rotation

**Update 2:** unchanged.

**Question:** Can asymmetric interactions generate useful rotation without simply increasing total actuation?

**Candidate hypothesis:** Changing the balance of reciprocal and non-reciprocal coupling at fixed overall strength will induce persistent rotation in some regimes, but only part of that rotation will transfer work to a load.

**How to test:** Randomize independent two-population active-particle simulations to reciprocal, directional and sign-reversed interaction matrices normalized to the same total coupling norm. Add an identical passive rotor or cargo after equilibration. Evaluate unloaded and loaded conditions and measure outcomes per population realization.

**Comparison:** Reciprocal coupling, externally driven rotation with matched power and label-swapped populations provide mechanism and efficiency controls.

**Measurements:** Angular current; Load displacement; Input power proxy; Rotation persistence; Population segregation.

**Would count against it:** Changing reciprocity produces no persistent rotation at matched total forcing, or reciprocal coupling produces the same rotation under matched initial conditions. Loaded efficiency remains exploratory.

**Main confounds:** Coupling normalization does not guarantee identical physical energy consumption; specify the accounting model. Phenomenological interaction matrices may lack a realizable local controller, and spontaneous clockwise versus anticlockwise choices must be aligned only for analysis.

**Framing / first-test class:** speculative / offline.

**Before promotion:** Read the non-reciprocal model equations and define load coupling and an honest actuation budget; physical implementation remains separate.

**Closest prior and evidence limits:**

- [[fruchart-2021-non]] — [Non-reciprocal phase transitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fruchart-2021-non.md). Closest theoretical framework links non-reciprocity and time-dependent phases. Catalogue depth: abstract.
- [[ceron-2023-diverse]] — [Diverse behaviors in non-uniform chiral and non-chiral swarmalators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ceron-2023-diverse.md). Related heterogeneous chiral structures; model-specific offsets need scrutiny. Catalogue depth: full.
- [[deblais-2018-boundaries]] — [Boundaries Control Collective Dynamics of Inertial Self-Propelled Robots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/deblais-2018-boundaries.md). Embodied collective transport provides an analogy, not a validation of the chosen interaction law. Catalogue depth: abstract.

<a id="phy-17"></a>
### PHY-17 — Recovery of shape versus recovery of function

**Update 2:** unchanged.

**Question:** Does an acoustically coupled aggregate that regains its shape also regain its sensing and transport performance?

**Candidate hypothesis:** Morphological recovery will precede functional recovery when damage changes phase or frequency organization without removing many particles.

**How to test:** Randomize complete simulated aggregates to equal-size particle removal, phase scrambling, spatial displacement or sham perturbation. Reuse matched initial states and evaluate an independently defined reflecting-object detection or target-transport task before and after damage. Analyse episode-level recovery times and include failures that never recover within the horizon.

**Comparison:** Undamaged aggregates and a geometry-only reassembly rule control for elapsed time and shape restoration without acoustic organization.

**Measurements:** Task accuracy; Useful transport rate; Shape similarity; Functional recovery time; Acoustic signal budget.

**Would count against it:** Task performance returns whenever shape does, or the acoustic policy offers no recovery advantage beyond a geometry-only controller.

**Main confounds:** A pretty regrowth animation is not task evidence. Wave reflections, boundary conditions and numerical field solvers can create behaviour; the cited acoustic result is a model study, not microrobot hardware proof.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Confirm accessible acoustic simulation code or budget a faithful implementation; select a functional task independent of the shape score.

**Closest prior and evidence limits:**

- [[ziepke-2025-acoustic]] — [Acoustic Signaling Enables Collective Perception and Control in Active Matter Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ziepke-2025-acoustic.md). Closest prior already reports regeneration and acoustic collective functions. Catalogue depth: abstract.
- [[slavkov-2018-morphogenesis]] — [Morphogenesis in robot swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/slavkov-2018-morphogenesis.md). Robot regrowth is an analogous recovery mechanism with different physical assumptions. Catalogue depth: abstract.
- [[bauerle-2018-self]] — [Self-organization of active particles by quorum sensing rules](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bauerle-2018-self.md). Quorum-controlled shapes offer a different organization baseline. Catalogue depth: full.

**Related team work:** [nca-observatory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/nca-observatory.md).

<a id="phy-18"></a>
### PHY-18 — Transport by fluctuating active flows

**Update 2:** unchanged.

**Question:** Can a deliberately disordered active flow transport tracers more effectively than an ordered flock at the same propulsion budget?

**Candidate hypothesis:** Intermediate temporal disorder will improve mixing and target encounter rates, while strongly aligned motion will maximize directional transport but leave poorly explored regions.

**How to test:** Randomize independently seeded simulated active populations to interaction rules spanning ordered, clustered and fluctuating regimes. Release passive tracers from held-out locations with matched propulsion and particle density. Evaluate mixing and directional delivery as distinct tasks on periodic and bounded domains; analyse simulation episodes rather than individual tracer samples as independent replicates.

**Comparison:** Passive diffusion matched to short-time displacement, constant directed advection and non-interacting active particles provide simple baselines.

**Measurements:** Mixing time; First-passage distribution; Unvisited volume fraction; Net delivery; Propulsion budget.

**Would count against it:** No fluctuating regime improves task performance over matched passive or directed baselines, or gains vanish when boundary recirculation is removed.

**Main confounds:** Active turbulence is not ordinary inertial turbulence, and a spectral power law does not establish useful mixing. Tracers sharing one flow are dependent; fluid-mediated transport cannot be inferred from point particles without a coupling model.

**Framing / first-test class:** speculative / offline.

**Before promotion:** Choose consistent tracer coupling and inspect active-mixing prior work before claiming novelty.

**Closest prior and evidence limits:**

- [[alert-2022-active]] — [Active Turbulence](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/alert-2022-active.md). Review context for fluctuating active flows; not evidence of the specific task optimum. Catalogue depth: abstract.
- [[fily-2012-athermal]] — [Athermal Phase Separation of Self-Propelled Particles with No Alignment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fily-2012-athermal.md). Clustering without alignment supplies a contrasting regime. Catalogue depth: full.
- [[vicsek-1995-novel]] — [Novel Type of Phase Transition in a System of Self-Driven Particles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vicsek-1995-novel.md). Ordered motion supplies a deliberately different transport baseline. Catalogue depth: full.

<a id="sync-consensus"></a>
## Synchronisation, consensus and networked control

<a id="phy-25"></a>
### PHY-25 — The order of communication opportunities

**Update 2:** revised.

**Question:** Can two networks with identical aggregate connectivity have very different finite-time consensus because contacts occur in a different order?

**Candidate hypothesis:** Schedules that repeatedly isolate the same subgroup will converge more slowly than temporally interleaved contacts, despite equal edge counts and identical aggregated graphs.

**How to test:** Construct paired contact sequences with the same edges, total contact duration and aggregate Laplacian but different ordering. Randomize independent network episodes to schedules and initial states, then apply one fixed consensus rule. Repeat with a moving-agent-generated contact sequence to test whether the controlled result survives a physical encounter process.

**Comparison:** A static time-averaged graph and randomized edge ordering are the main comparators; disconnected schedules are a known failure control.

**Measurements:** Time to specified disagreement; Error at fixed deadline; Temporal reachability; Communication cost.

**Would count against it:** Ordering makes no practical difference over the allowed schedules, or the effect is completely captured by unmatched total contact time.

**Main confounds:** Asymptotic joint-connectivity theorems do not guarantee a useful finite deadline. Row-stochastic versus average-preserving rules can converge to different values; report both agreement and error to the intended target.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Define average-preserving weights and check temporal-network rate bounds. Social-LLM-Networks experiment JSON may ground a later text-network comparison only if timestamps, exposure order and repeat units are recoverable; archived sentiment trajectories alone cannot identify a scheduling effect.

**Closest prior and evidence limits:**

- [[jadbabaie-2003-coordination]] — [Coordination of groups of mobile autonomous agents using nearest neighbor rules](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/jadbabaie-2003-coordination.md). Established joint-connectivity convergence result, not a finite-time ranking claim. Catalogue depth: full.
- [[ren-2005-consensus]] — [Consensus seeking in multiagent systems under dynamically changing interaction topologies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ren-2005-consensus.md). Directed switching-network convergence context. Catalogue depth: abstract.
- [[data-social-llm-networks-2026]] — [Social-LLM-Networks: opinion exchange among LLMs connected over communication networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-social-llm-networks-2026.md). Candidate opinion-exchange traces with topology metadata; temporal exposure reconstruction is an unresolved prerequisite, not established physical consensus evidence. Catalogue depth: skim.

<a id="phy-26"></a>
### PHY-26 — Fast consensus under realistic link delays

**Update 2:** unchanged.

**Question:** Does adding long-range links still accelerate agreement when their latency and service cost are included?

**Candidate hypothesis:** Shortcuts will help only below a latency-and-budget boundary; nominally better connectivity can worsen error at a fixed wall-clock deadline.

**How to test:** Randomize simulated network episodes to local links, added shortcuts or rewired links with matched total communication budget. Assign delay using a transparent distance-dependent model and compare to zero-delay controls. Hold initial values and packet schedules paired across treatments, and analyse complete network realizations.

**Comparison:** The delay-free Laplacian prediction, a budget-matched local graph and an oracle instantaneous graph bound the achievable speed.

**Measurements:** Disagreement at deadline; Consensus bias; Delivered message count; Delay-induced oscillation; Wall-clock convergence time.

**Would count against it:** Shortcut gains persist across the stated delay regime without extra cost, or worse results are solely caused by accidentally reducing baseline update frequency.

**Main confounds:** Different delayed-consensus formulations have different stability conditions. Sampling an old state, delaying delivery and freezing the receiver are distinct mechanisms; no theorem should be extended beyond its assumptions.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Inspect exact delayed update equations and identify a physical latency range before designing the benchmark.

**Closest prior and evidence limits:**

- [[olfati-saber-2004-consensus]] — [Consensus Problems in Networks of Agents With Switching Topology and Time-Delays](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/olfati-saber-2004-consensus.md). Closest theoretical anchor links topology, convergence and delay assumptions. Catalogue depth: abstract.
- [[olfati-saber-2007-consensus]] — [Consensus and Cooperation in Networked Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/olfati-saber-2007-consensus.md). Review reports shortcut benefits and provides baseline context. Catalogue depth: abstract.
- [[ren-2005-consensus]] — [Consensus seeking in multiagent systems under dynamically changing interaction topologies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ren-2005-consensus.md). Unreliable directed exchange is related but not automatically the same delay model. Catalogue depth: abstract.

<a id="phy-27"></a>
### PHY-27 — Movement as a synchronization resource

**Update 2:** unchanged.

**Question:** Can purposeful mixing synchronize locally coupled oscillators more efficiently than increasing their coupling strength?

**Candidate hypothesis:** Occasional movement between weakly connected regions will outperform stronger within-region coupling at equal energy proxy, but only if travel changes encounters before local clusters lock into incompatible phases.

**How to test:** Randomize independent mobile-oscillator groups to static placement, random mixing or targeted bridging movement while holding the contact radius and total movement budget fixed. Compare increased coupling under an explicitly stated alternative energy cost. Use held-out arena partitions, paired initial frequencies and whole-group trajectories as replicates.

**Comparison:** A fully mixed static graph is an information ceiling; random movement with the same path length controls for targeted bridging.

**Measurements:** Frequency-locking time; Residual phase disagreement; Travel cost; Contact diversity; Total control effort.

**Would count against it:** Targeted movement adds no synchronization benefit over budget-matched random motion or stronger coupling.

**Main confounds:** Moving agents alter spatial density as well as encounters. A one-way model where phase never affects motion differs from swarmalators; energy proxies require sensitivity analysis and cannot be called real hardware power measurements.

**Framing / first-test class:** extension / offline.

**Before promotion:** Read the original motion process and select a budget model; check existing mobile-relay synchronization controllers.

**Closest prior and evidence limits:**

- [[fujiwara-2011-synchronization]] — [Synchronization in networks of mobile oscillators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fujiwara-2011-synchronization.md). Closest prior establishes competition between movement and local synchronization times. Catalogue depth: abstract.
- [[amichay-2025-integration]] — [On the integration of collective motion and temporal synchrony in animal collectives](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amichay-2025-integration.md). Review framing highlights interaction-network mixing. Catalogue depth: skim.
- [[dorfler-2014-synchronization]] — [Synchronization in complex networks of phase oscillators: A survey](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dorfler-2014-synchronization.md). Synchronization definitions and static-network reference conditions. Catalogue depth: skim.

<a id="phy-28"></a>
### PHY-28 — A useful phase wave without global synchrony

**Update 2:** unchanged.

**Question:** Can a low global phase order hide a stable, useful spatial coordination pattern?

**Candidate hypothesis:** A stable phase wave will support sequential activation around a ring while global synchrony ranks it lower despite higher sequential-task utility.

**How to test:** Randomize independently initialized swarmalator simulations to phase-wave, clustered-sync and asynchronous regimes confirmed from the model. Assign a ring-inspection task requiring sequential local activations, with matched total activation count. Compare task utility and joint position-phase measures with global phase order, using held-out initial conditions and complete simulation realizations as units.

**Comparison:** A scripted travelling-wave schedule provides a task ceiling; independently shuffled phases at fixed positions provide a matched low-global-order null.

**Measurements:** Coverage gaps; Activation collisions; Joint position-phase order; Global phase order; Task completion time.

**Would count against it:** Low global order does not coincide with useful sequential activation, or joint order adds no predictive value over direct local timing statistics.

**Main confounds:** This is a metric-and-task demonstration, not discovery of phase waves. Global synchrony might be correct for a different task; the toy ring does not establish utility for drones or biological swarms.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Reproduce the source phase-wave regime and define the sequential task independently of the joint-order metric.

**Closest prior and evidence limits:**

- [[yoon-2022-sync]] — [Sync and Swarm: Solvable Model of Nonidentical Swarmalators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yoon-2022-sync.md). Closest solvable model already has phase-wave states. Catalogue depth: full.
- [[ceron-2023-diverse]] — [Diverse behaviors in non-uniform chiral and non-chiral swarmalators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ceron-2023-diverse.md). Richer spatial and phase patterns reinforce the metric distinction. Catalogue depth: full.
- [[gh-khev-swarmalators]] — [swarmalators: O'Keeffe's source code for swarmalator models (Mathematica and others) across a dozen papers](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-khev-swarmalators.md). Potential reference implementation; not run in this pass. Catalogue depth: skim.

<a id="phy-29"></a>
### PHY-29 — How distribution tails change swarmalator predictions

**Update 2:** unchanged.

**Question:** Do analytic swarmalator predictions based on Lorentzian frequency disorder remain useful for bounded physical populations?

**Candidate hypothesis:** The qualitative states will persist under bounded disorder, but synchronization boundaries and rare-agent escape rates will shift enough to matter for small swarms.

**How to test:** Randomize independent ring-swarmalator simulations to Lorentzian, truncated Lorentzian and bounded frequency distributions, matching robust central spread rather than a nonexistent Lorentzian variance. Use identical population sizes, coupling and initial phase-position draws; evaluate state frequencies over a predeclared horizon and compare held-out parameter settings.

**Comparison:** The source Lorentzian condition validates implementation; identical-frequency populations provide a simpler limit.

**Measurements:** State occupancy; Frequency-locking fraction; Outlier escape rate; Transition-location error; Sensitivity to population size.

**Would count against it:** After robust spread matching, the same predictions describe all distributions within the predeclared tolerance, or apparent differences disappear when extreme draws are handled consistently.

**Main confounds:** Truncating tails changes both rare extremes and normalizations. Finite-size, initialization and integration error can mimic a new state; numerical state labels need direct trajectory inspection.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Inspect existing non-Lorentzian follow-ups and establish integration convergence; the novelty claim is deliberately provisional.

**Closest prior and evidence limits:**

- [[yoon-2022-sync]] — [Sync and Swarm: Solvable Model of Nonidentical Swarmalators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yoon-2022-sync.md). Closest analytic result uses Lorentzian heterogeneity for tractability. Catalogue depth: full.
- [[ceron-2023-diverse]] — [Diverse behaviors in non-uniform chiral and non-chiral swarmalators](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ceron-2023-diverse.md). Related numerical study varies heterogeneity in a different two-dimensional model. Catalogue depth: full.
- [[dorfler-2014-synchronization]] — [Synchronization in complex networks of phase oscillators: A survey](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dorfler-2014-synchronization.md). Oscillator-disorder context; no automatic transfer of thresholds. Catalogue depth: skim.

<a id="phy-30"></a>
### PHY-30 — Synchrony versus shared-channel congestion

**Update 2:** unchanged.

**Question:** When does synchronizing activity overload the channel needed to maintain that synchronization?

**Candidate hypothesis:** Strongly synchronized message bursts will increase collision or queue delays, reducing useful coordination compared with a phase-spread schedule at the same message rate.

**How to test:** Couple a documented oscillator model to a synthetic finite-capacity communication queue. Randomize whole network episodes to synchronized, phase-spread and independently timed emissions while preserving total offered traffic. Test ideal delivery separately from queue-dependent delays, and evaluate recovery after a clock disturbance using episode-level outcomes.

**Comparison:** An infinite-capacity channel isolates pure synchronization dynamics; deterministic time slots provide a scheduling comparator.

**Measurements:** Delivered freshness; Queue delay; Packet loss; Clock disagreement; Completed coordination tasks.

**Would count against it:** Synchrony has no delivery penalty under realistic tested service limits, or phase spreading harms task timing more than it helps the channel.

**Main confounds:** Queue service and collision models are engineering choices and should not be presented as measured radio behaviour. Timestamp accuracy, retry policy and acknowledgement traffic must be included; equal offered traffic is not equal delivered information.

**Framing / first-test class:** speculative / offline.

**Before promotion:** Choose a concrete radio or software-message channel model and review synchronization-aware medium-access literature before promotion.

**Closest prior and evidence limits:**

- [[dorfler-2014-synchronization]] — [Synchronization in complex networks of phase oscillators: A survey](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dorfler-2014-synchronization.md). Provides oscillator and synchronization terminology, not a congestion result. Catalogue depth: skim.
- [[sarfati-2021-self]] — [Self-organization in natural swarms of Photinus carolinus synchronous fireflies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/sarfati-2021-self.md). Biological burst synchronization is an analogy, with a very different optical channel. Catalogue depth: skim.
- [[olfati-saber-2004-consensus]] — [Consensus Problems in Networks of Agents With Switching Topology and Time-Delays](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/olfati-saber-2004-consensus.md). Delay-sensitive consensus motivates the feedback path from queues to coordination. Catalogue depth: abstract.

<a id="criticality-measurement"></a>
## Criticality, information and measurement

<a id="met-01"></a>
### MET-01 — Criticality beyond a geometric signature

**Update 2:** unchanged.

**Question:** Can apparent scale-free correlation be distinguished from a finite-size or mean-subtraction artifact?

**Candidate hypothesis:** A critical interaction model will predict held-out response scaling better than independent motion with matched group geometry, even if both show a correlation zero crossing.

**How to test:** Generate independent simulated flocks across sizes and densities under interacting and noninteracting mechanisms. Apply identical tracking loss and mean subtraction. Fit scaling on some sizes, then compare predictions on held-out sizes and controlled impulse responses. Treat a flock realization as the replicate.

**Comparison:** Matched independent motion, common environmental drive, and ordered low-noise noncritical models.

**Measurements:** Correlation length/group diameter; held-out scaling error; impulse-response gain.

**Would count against it:** The nulls explain both the static scaling and response as well as the critical model.

**Main confounds:** Boundary shape, density and zero-sum constraints can move the estimated correlation length.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read the scaling estimators and predefine null generation without tuning on the held-out sizes.

**Closest prior and evidence limits:**

- [[cavagna-2010-scale]] — [Scale-free correlations in starling flocks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cavagna-2010-scale.md). Static correlation precedent; not alone a criticality diagnostic. Catalogue depth: full.
- [[mora-2011-biological]] — [Are Biological Systems Poised at Criticality?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mora-2011-biological.md). Criticality framework whose signatures require competing explanations. Catalogue depth: full.

<a id="met-02"></a>
### MET-02 — Sensitivity versus false alarms

**Update 2:** unchanged.

**Question:** Does maximum collective responsiveness also maximize useful decisions under asymmetric error costs?

**Candidate hypothesis:** The best operating point will move below the response maximum when false alarms are costly.

**How to test:** In a seeded cascade simulator, randomize signal presence and severity across independent episodes, sweep coupling, and evaluate policies under a prespecified range of false-positive/negative costs. Select coupling on training episodes and evaluate utility on held-out episodes.

**Comparison:** Always respond, never respond, fixed subcritical coupling, and coupling selected only for maximum response.

**Measurements:** True-positive rate; false-positive rate; expected loss; decision delay.

**Would count against it:** Maximum-response coupling remains utility-optimal across the tested asymmetric cost regimes.

**Main confounds:** The result may be built into the payoff; report the full response/error frontier before scalarizing.

**Framing / first-test class:** replication / offline.

**Before promotion:** Reproduce a closest-prior regime first; select a new task only if the transfer question remains open.

**Closest prior and evidence limits:**

- [[poel-2022-subcritical]] — [Subcritical escape waves in schooling fish](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/poel-2022-subcritical.md). Direct closest prior for risk-dependent distance to criticality; this is a replication/transfer test. Catalogue depth: full.
- [[klamser-2021-collective]] — [Collective predator evasion: Putting the criticality hypothesis to the test](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/klamser-2021-collective.md). Functional criticality comparison in predator evasion. Catalogue depth: full.

<a id="met-03"></a>
### MET-03 — What incomplete observation hides

**Update 2:** unchanged.

**Question:** Which collective measurements survive seeing only a biased fraction of the swarm?

**Candidate hypothesis:** Spatial or degree-biased missingness will distort inferred coordination more than random dropout at the same coverage.

**How to test:** Take fully observed synthetic trajectories with known interactions. Randomize observation masks by episode: uniform, spatial, high-degree-only, and burst loss. Estimate branching, correlation and coordination metrics blind to truth, then compare errors against the full trajectory.

**Comparison:** Full observation, uniform subsampling, and a published correction method where its assumptions hold.

**Measurements:** Estimation bias; interval coverage; regime misclassification; minimum observation fraction.

**Would count against it:** Raw estimates under biased masks perform no worse than under uniform masks at matched coverage. Successful correction is a useful outcome, not a refutation of the raw-bias prediction.

**Main confounds:** Tracking errors and missing identities can be more damaging than simple missing frames.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Choose estimators with explicit assumptions and verify ground-truth generators and mask mechanisms.

**Closest prior and evidence limits:**

- [[levina-2022-tackling]] — [Tackling the subsampling problem to infer collective properties from limited data](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/levina-2022-tackling.md). Subsampling problem and candidate corrections; catalogue at abstract depth. Catalogue depth: abstract.
- [[han-2024-collective]] — [Collective relational inference for learning heterogeneous interactions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/han-2024-collective.md). Interaction inference offers a second target beyond aggregate order. Catalogue depth: full.

<a id="met-04"></a>
### MET-04 — Does a synergy score predict useful complementarity?

**Update 2:** unchanged.

**Question:** Can an information-theoretic collective score forecast the damage caused by removing coordination?

**Candidate hypothesis:** A score measured before intervention will predict task loss after breaking complementary interactions better than pairwise correlation does.

**How to test:** Across independent simulated teams, compute scores on an initial trace segment. Randomize targeted interaction scrambling versus matched random scrambling in a later segment; hold message count fixed. Predict held-out performance loss, stratifying by baseline competence.

**Comparison:** Pairwise correlation, activity rate, team size, and a simple performance-only predictor.

**Measurements:** Held-out predictive error; intervention effect on task score; score stability across estimators.

**Would count against it:** The score adds no out-of-sample prediction over simpler baselines, or predicts activity rather than useful loss.

**Main confounds:** Observed synergy is not causal proof; information estimators and macro-variable choice matter.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Select a task with independently scored success and calibrate finite-sample entropy estimation.

**Closest prior and evidence limits:**

- [[rosas-2020-reconciling]] — [Reconciling emergences: An information-theoretic approach to identify causal emergence in multivariate data](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rosas-2020-reconciling.md). Information decomposition framework with observational assumptions. Catalogue depth: full.
- [[riedl-2025-emergent]] — [Emergent Coordination in Multi-Agent Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/riedl-2025-emergent.md). Task-specific collective information measurements; mechanism needs intervention. Catalogue depth: full.

<a id="met-05"></a>
### MET-05 — Information flow under a shared driver

**Update 2:** unchanged.

**Question:** When does apparent peer information transfer come entirely from shared external input?

**Candidate hypothesis:** Conditioning on a logged common driver and testing edge interventions will remove many apparent directed links found by pairwise transfer entropy.

**How to test:** Generate paired systems with common drive only, peer influence only, and both. Randomize selected edges across independent episodes. Compare estimated links with the known graph and intervention effects using identical observation windows.

**Comparison:** Pairwise transfer entropy, lagged correlation, and a conditional estimator with the driver observed.

**Measurements:** Edge precision/recall; false discovery rate; intervention-effect prediction.

**Would count against it:** Pairwise and conditional methods are equally accurate under shared drive or edge interventions contradict the conditional graph.

**Main confounds:** Conditioning fails if the driver is unobserved; label residual ambiguity rather than claiming causal discovery.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Verify estimator bias on small analytically tractable processes before using agent traces.

**Closest prior and evidence limits:**

- [[lizier-2008-local]] — [Local information transfer as a spatiotemporal filter for complex systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lizier-2008-local.md). Information-transfer measurement, not automatic intervention identification. Catalogue depth: abstract.
- [[shalizi-2011-homophily]] — [Homophily and Contagion Are Generically Confounded in Observational Social Network Studies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shalizi-2011-homophily.md). General warning about confounded apparent transmission. Catalogue depth: skim.

<a id="met-06"></a>
### MET-06 — A transition or a slow relaxation?

**Update 2:** unchanged.

**Question:** Does observed hysteresis survive longer observation and finite-size controls?

**Candidate hypothesis:** Some apparent regime switches will shrink as dwell time increases, indicating slow relaxation rather than a stable bistable region.

**How to test:** Use independent seeded simulations for upward and downward coupling sweeps at several sizes and dwell times. Repeat with fresh initial states at each parameter. Estimate transition locations and relaxation time without treating time steps as replicates.

**Comparison:** Independent parameter samples, known bistable reference model, and a slow single-attractor null.

**Measurements:** Hysteresis-loop area; switch-location uncertainty; relaxation time; residence-time distribution.

**Would count against it:** The loop stabilizes with increasing dwell time and a single-attractor null cannot reproduce it.

**Main confounds:** Changing size at fixed volume changes density; rare switches require long traces.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read phase definitions and identify a feasible range of relaxation times before committing a sweep.

**Closest prior and evidence limits:**

- [[vicsek-1995-novel]] — [Novel Type of Phase Transition in a System of Self-Driven Particles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vicsek-1995-novel.md). Order transition reference to reproduce before extension. Catalogue depth: full.
- [[tunstrom-2013-collective]] — [Collective States, Multistability and Transitional Behavior in Schooling Fish](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tunstrom-2013-collective.md). Collective-state and multistability motivation. Catalogue depth: abstract.

<a id="met-07"></a>
### MET-07 — Can different mechanisms produce the same trajectories?

**Update 2:** unchanged.

**Question:** Can good trajectory prediction coexist with a wrong inferred interaction graph?

**Candidate hypothesis:** Models with similar held-out trajectory error will disagree on the effect of targeted perturbations when fitted to passive traces alone.

**How to test:** Generate trajectories from known heterogeneous interactions; fit several graph models on passive data. Select equally predictive fits before revealing randomized local perturbations. Compare graph recovery and perturbation predictions on independent initial conditions.

**Comparison:** No-interaction predictor, oracle graph diagnostic, and a simple distance-based interaction model.

**Measurements:** Trajectory prediction error; edge-type accuracy; intervention prediction error.

**Would count against it:** Passive predictive accuracy reliably determines both graph and perturbation response across tested generators.

**Main confounds:** Misspecified interaction types, unobserved state and identical symmetries create non-identifiability.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read model assumptions; use oracle graph only as a diagnostic, not an achievable baseline.

**Closest prior and evidence limits:**

- [[han-2024-collective]] — [Collective relational inference for learning heterogeneous interactions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/han-2024-collective.md). Closest interaction-inference method; assumptions on types and neighborhoods need audit. Catalogue depth: full.
- [[gao-2024-learning]] — [Learning interpretable dynamics of stochastic complex systems from experimental data](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gao-2024-learning.md). Interpretable stochastic-dynamics inference comparator. Catalogue depth: abstract.

<a id="met-08"></a>
### MET-08 — Early warnings on genuinely new failures

**Update 2:** unchanged.

**Question:** Do warning signals predict future collective breakdown outside the scenarios used to design them?

**Candidate hypothesis:** A multivariate warning combining slowing recovery and rising disagreement will beat a threshold on current error at matched false-alarm rate.

**How to test:** Create independent simulator episodes with gradually changing conditions and abrupt changes. Train thresholds on one failure mechanism, lock them, and evaluate on held-out mechanisms with nonfailure episodes. Score event-level alarms and lead time.

**Comparison:** Current-error threshold, activity-only alarm, and no alarm; calibrate all at the same false-alarm burden.

**Measurements:** Event recall at fixed false alarms/hour; median useful lead time; missed-event cost.

**Would count against it:** The warning has no positive lead time or loses its advantage on unseen mechanisms.

**Main confounds:** A gradual drift generator can favor slowing-down signals by construction; abrupt failures test that boundary.

**Framing / first-test class:** speculative / offline.

**Before promotion:** Identify independent failure mechanisms and acceptable warning costs before collecting traces.

**Closest prior and evidence limits:**

- [[mora-2011-biological]] — [Are Biological Systems Poised at Criticality?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mora-2011-biological.md). Criticality provides motivation, not evidence for this warning system. Catalogue depth: full.
- [[sooter-2025-defining]] — [Defining and measuring proximity to criticality](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/sooter-2025-defining.md). Measurement definitions to audit before interpreting proximity to a transition. Catalogue depth: skim.

<a id="marl-emergence"></a>
## Multi-agent RL and emergent coordination

<a id="rl-01"></a>
### RL-01 — Skills with unfamiliar partners

**Update 2:** unchanged.

**Question:** Does training with partner diversity improve zero-shot coordination at a fixed training budget?

**Candidate hypothesis:** Partner-population training will improve held-out cross-play more than self-play, even after matching environment steps.

**How to test:** Randomize training seeds to fixed-partner or partner-population curricula. Freeze policies and evaluate on unseen partner families and task layouts. Analyze independently trained policy seeds, with held-out episodes nested within seeds.

**Comparison:** Self-play, independent learning, and a simple scripted partner-compatible policy.

**Measurements:** Cross-play return; worst-partner return; self-play to cross-play gap; training steps.

**Would count against it:** The cross-play improvement vanishes with matched steps or is confined to partners seen during training.

**Main confounds:** More partner diversity may also provide broader state coverage; include a state-coverage-matched control.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Confirm a runnable environment and choose held-out partner families before tuning.

**Closest prior and evidence limits:**

- [[lowe-2017-multi]] — [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lowe-2017-multi.md). Policy ensembles and centralized training predecessor. Catalogue depth: skim.
- [[gh-google-deepmind-meltingpot]] — [Melting Pot 2.0: 50+ multi-agent substrates and 256 test scenarios for generalisation to novel social situations](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-google-deepmind-meltingpot.md). Candidate social generalization environment; exact substrate must be selected. Catalogue depth: skim.

<a id="rl-02"></a>
### RL-02 — Credit for a rare essential contribution

**Update 2:** unchanged.

**Question:** Do counterfactual rewards help when only a few agents perform indispensable actions?

**Candidate hypothesis:** Counterfactual credit will improve discovery of rare cooperative actions relative to a shared reward at the same training budget.

**How to test:** Build a small task with a controllable fraction of essential roles and a separately measured completion condition. Randomize training seeds across shared reward, difference reward and counterfactual-critic variants; evaluate on new role assignments.

**Comparison:** Team reward with the same architecture and training steps; a scripted assignment oracle as diagnostic.

**Measurements:** Task success; essential-action frequency; sample efficiency; variance across seeds.

**Would count against it:** Counterfactual variants do not improve success, or gains vanish after matching critic capacity and observations.

**Main confounds:** The critic may get privileged state; isolate information access from credit assignment.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Read both implementations and ensure all reward variants preserve the same true objective.

**Closest prior and evidence limits:**

- [[foerster-2018-counterfactual]] — [Counterfactual Multi-Agent Policy Gradients](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/foerster-2018-counterfactual.md). Direct algorithmic precedent; novelty must be in the task boundary. Catalogue depth: abstract.
- [[rashid-2018-qmix]] — [QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rashid-2018-qmix.md). Cooperative value-factorization comparison. Catalogue depth: abstract.

<a id="rl-03"></a>
### RL-03 — Messages that remain useful under a broken channel

**Update 2:** revised.

**Question:** Does training with channel corruption yield communication that generalizes beyond its training noise?

**Candidate hypothesis:** Moderate channel dropout during training will preserve more task value under unseen burst loss than clean-channel training.

**How to test:** Train independent policy seeds under clean, independent-dropout and burst-loss channels with equal transmitted-bit budgets. Freeze them and evaluate unfamiliar delays, burst lengths and sender permutations. Include interventions that replace content while preserving message timing.

**Comparison:** No communication, clean-channel training, and hand-designed compressed state messages.

**Measurements:** Return under channel shift; useful bits per episode; performance loss after content scrambling; Representation reconstruction error apart from task return.

**Would count against it:** Gains disappear on new corruption patterns or content scrambling leaves success unchanged.

**Main confounds:** Timing and agent order can be covert communication channels; log and control them.

**Framing / first-test class:** extension / training.

**Before promotion:** Select a private-information task and audit the original communication objective; the new talk motivates separate representation and utility scores, not assuming compressed messages are safe.

**Closest prior and evidence limits:**

- [[foerster-2016-learning]] — [Learning to Communicate with Deep Multi-Agent Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/foerster-2016-learning.md). Learned communication and channel design predecessor. Catalogue depth: abstract.
- [[gh-farama-foundation-pettingzoo]] — [PettingZoo: multi-agent Gymnasium-style API and environment families (Atari, Butterfly, Classic, MPE, SISL)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-farama-foundation-pettingzoo.md). Candidate controlled multi-agent environment interface. Catalogue depth: skim.
- [[zaslavsky-2023-noga]] — [Noga Zaslavsky: Information-constrained Emergent Communication in Multi agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/talks/zaslavsky-2023-noga.md). Talk transcript distinguishes communication complexity, representation distortion and downstream utility; no security guarantee or precise effect size is assumed. Catalogue depth: full.

<a id="rl-04"></a>
### RL-04 — When a mean neighbor is misleading

**Update 2:** unchanged.

**Question:** Does mean-field compression fail specifically when rare roles carry decisive information?

**Candidate hypothesis:** Role-conditioned aggregation will improve decisions over an unconditioned mean as rare specialist observations become decisive.

**How to test:** Construct matched tasks with identical marginal observations but varied dependence on rare roles. Randomize training seeds across mean aggregation, role-conditioned mean and capacity-matched attention. Hold inputs and steps equal; test new role proportions.

**Comparison:** Unconditioned mean, simple histogram of roles, and an oracle full-state controller as ceiling.

**Measurements:** Return by specialist fraction; rare-event miss rate; compute per action.

**Would count against it:** Neither role-conditioned aggregation nor a simple role histogram improves over the unconditioned mean on held-out role-sensitive tasks. If the histogram matches attention, that argues against the extra complexity, not against the role-conditioning hypothesis.

**Main confounds:** Role labels can leak the answer; separate observable roles from hidden ground-truth importance.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Specify legitimate role observability and separate action averaging from observation pooling.

**Closest prior and evidence limits:**

- [[yang-2018-mean]] — [Mean Field Multi-Agent Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yang-2018-mean.md). Mean-field approximation to audit under heterogeneous interactions. Catalogue depth: full.
- [[huttenrauch-2019-deep]] — [Deep Reinforcement Learning for Swarm Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/huttenrauch-2019-deep.md). Mean observation embedding is a distinct baseline. Catalogue depth: full.

<a id="rl-05"></a>
### RL-05 — Size transfer or topology transfer?

**Update 2:** unchanged.

**Question:** Are policies described as swarm-size invariant actually robust to new interaction graphs?

**Candidate hypothesis:** An invariant input encoder alone will not preserve performance when neighborhood connectivity changes at fixed density.

**How to test:** Train at one size and density, then factorially vary size, density and degree distribution on independent worlds. Compare mean embedding and graph-policy encoders at matched capacity and communication budget; report each shift separately.

**Comparison:** Classical local controller and an encoder trained on the same topology distribution.

**Measurements:** Task completion; collision rate; connectivity loss; degradation per distribution shift.

**Would count against it:** Both encoders transfer across topology shifts without degradation, or size alone explains the losses.

**Main confounds:** Fixed area and fixed density are different tests; avoid silently coupling size to crowding.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Reproduce one published transfer setting before extending to topology shifts.

**Closest prior and evidence limits:**

- [[huttenrauch-2019-deep]] — [Deep Reinforcement Learning for Swarm Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/huttenrauch-2019-deep.md). Size-invariant observation representation precedent. Catalogue depth: full.
- [[tolstaya-2020-learning]] — [Learning Decentralized Controllers for Robot Swarms with Graph Neural Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tolstaya-2020-learning.md). Local graph-controller comparison, originally imitation learning. Catalogue depth: abstract.

<a id="rl-06"></a>
### RL-06 — Emergent strategy or simulator exploit?

**Update 2:** unchanged.

**Question:** Do strategies discovered by competition remain useful when nonessential simulator details change?

**Candidate hypothesis:** Some apparent strategic advances will disappear under equivalent physics implementations while robust tool use persists.

**How to test:** Train or load policies in a small competitive object-interaction task. Freeze policies, then randomize friction integration, collision tolerance and action timing within a validated range that preserves task solvability. Evaluate independent seeds in both engines.

**Comparison:** Scripted physically valid strategies and policies trained with domain randomization.

**Measurements:** Task success; constraint violations; cross-engine retention; valid tool-use frequency.

**Would count against it:** All gains transfer with preserved action feasibility, or performance changes are fully explained by changed difficulty.

**Main confounds:** An altered engine may change the actual task; verify with scripted solutions before drawing conclusions.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Use a bounded toy setting or released policies; do not budget for reproducing billions of original frames.

**Closest prior and evidence limits:**

- [[baker-2020-emergent]] — [Emergent Tool Use From Multi-Agent Autocurricula](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/baker-2020-emergent.md). Autocurriculum and simulator-exploit precedent, expensive original setting. Catalogue depth: full.
- [[gh-proroklab-vectorizedmultiagentsimulator]] — [VMAS: vectorised differentiable 2D multi-agent simulator in PyTorch with multi-robot scenarios including flocking](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-proroklab-vectorizedmultiagentsimulator.md). Possible small simulation substrate, not a reproduced hide-and-seek implementation. Catalogue depth: ran.

<a id="rl-07"></a>
### RL-07 — Good reward, bad collective behavior

**Update 2:** unchanged.

**Question:** Can a learned flock exploit an alignment reward while failing navigation or safety objectives?

**Candidate hypothesis:** Optimizing alignment alone will create policies that score well while losing goal progress under obstacles.

**How to test:** Randomize training seeds among alignment-only, task-only and combined rewards in the same simulator. Evaluate held-out layouts with independent success, safety and energy measurements, including stationary or circular-motion loophole controls.

**Comparison:** Hand-designed flocking/navigation controller and task-only policy with matched observations.

**Measurements:** Goal completion; alignment score; collisions; energy per successful task.

**Would count against it:** Alignment-only reward generalizes equally on task and safety metrics, with no proxy exploit.

**Main confounds:** Combined rewards may simply add privileged goal information; equalize observability.

**Framing / first-test class:** extension / training.

**Before promotion:** Read reward formulations and predefine the independent task evaluator.

**Closest prior and evidence limits:**

- [[durve-2020-learning]] — [Learning to flock through reinforcement](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/durve-2020-learning.md). Learning flocking predecessor to audit for reward definition. Catalogue depth: full.
- [[brambati-2025-learning]] — [Learning to flock in open space by avoiding collisions and staying together](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/brambati-2025-learning.md). Collision and cohesion learning comparator. Catalogue depth: full.

<a id="rl-08"></a>
### RL-08 — Coordinating while partners keep learning

**Update 2:** unchanged.

**Question:** Does a short history of partner behavior improve adaptation to policy drift?

**Candidate hypothesis:** A history-conditioned policy will recover faster after partner changes than a memoryless policy of similar capacity.

**How to test:** Train matched recurrent and feedforward agents. In held-out independent episodes, switch partners at randomized times among a fixed policy pool; compare sudden and gradual drift. Include no-switch episodes to measure overhead.

**Comparison:** Memoryless policy, explicit partner-type estimator, and oracle switch notification as diagnostic.

**Measurements:** Recovery episodes; post-switch regret; steady-state return; unnecessary adaptation.

**Would count against it:** History offers no improvement beyond the simple estimator or only works with known switch times.

**Main confounds:** Recurrence also improves partial-observation memory; include drifting and stationary partial-observation controls.

**Framing / first-test class:** extension / training.

**Before promotion:** Choose checkpointed partner policies and hold environment steps and model capacity explicit.

**Closest prior and evidence limits:**

- [[lowe-2017-multi]] — [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lowe-2017-multi.md). Nonstationarity in MARL motivation. Catalogue depth: skim.
- [[gh-bold-lab-ai-jaxmarl]] — [JaxMARL: GPU-vectorised MARL environments (SMAX, MPE, Overcooked, Hanabi, STORM) and baselines in JAX](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-bold-lab-ai-jaxmarl.md). Candidate training suite; no run or speed claim from this pass. Catalogue depth: skim.

<a id="sim-06"></a>
### SIM-06 — When does offline policy evaluation stop ranking policies correctly?

**Update 2:** new.

**Question:** Does sparse joint-action coverage break offline evaluation before ordinary single-agent coverage diagnostics detect trouble?

**Candidate hypothesis:** Policies whose coordinated actions fall outside joint behavior support will be misranked offline more often than policies with similar marginal but better joint support.

**How to test:** Choose one small OG-MARL archive and compatible environment after auditing its loader, license and behavior metadata. Construct matched dataset subsets that preserve individual action frequencies while reducing coverage of coordinated joint actions. Train independent policy seeds with a frozen algorithm and budget, then compare offline value estimates with fresh online environment episodes. Dataset construction and training seeds are independent units; evaluation episodes are nested replications.

**Comparison:** Behavior cloning, full-support data subset and a marginal-support diagnostic at equal transition count.

**Measurements:** Offline/online rank agreement; Value-estimation error; Joint-support score; Realized team return.

**Would count against it:** Joint-support reduction adds no ranking error beyond marginal support and sample size, or the offline estimator remains calibrated across the tested policy shifts.

**Main confounds:** Removing joint actions can alter state visitation and return quality. Match these where possible and report unmatched shifts; classical RL trajectories do not establish LLM-agent generalization.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Inspect archive size and schema before download, verify environment/version compatibility and action support, and cap one scenario. A lightweight supported environment is preferable to assuming StarCraft runs locally.

**Closest prior and evidence limits:**

- [[data-og-marl-2024]] — [OG-MARL offline multi-agent RL datasets: SMAC v1/v2, MAMuJoCo, Flatland and RWARE experience, plus re-hosted prior-work datasets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-og-marl-2024.md). Concrete offline MARL archives; the catalogue’s 74 index rows are not the trajectory count. Catalogue depth: skim.
- [[ellis-2022-smacv2]] — [SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ellis-2022-smacv2.md). Procedural task variability motivates held-out online validation, without requiring its heavy environment for the initial test. Catalogue depth: full.
- [[papoudakis-2021-benchmarking]] — [Benchmarking Multi-Agent Deep Reinforcement Learning Algorithms in Cooperative Tasks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/papoudakis-2021-benchmarking.md). Multi-environment cooperative MARL comparison context for baseline and seed discipline. Catalogue depth: skim.

<a id="llm-agent-swarms"></a>
## LLM agent swarms

<a id="soc-01"></a>
### SOC-01 — Separate information diversity from model diversity

**Update 2:** revised.

**Question:** When does mixing model families help beyond giving identical models complementary evidence?

**Candidate hypothesis:** Complementary observations explain more distributed-task improvement than family labels; family mixing adds value only when it reduces residual shared errors after capability is controlled.

**How to test:** Randomize whole task episodes to homogeneous/mixed models crossed with overlapping/complementary evidence. Keep the fact union, inference and tool caps fixed; rotate shard assignments. Choose capability-matched pools using separate calibration tasks, then freeze them. Estimate contrasts on held-out task families, including rare-fact and fully supplied synthetic-evidence strata; report matched-spend sensitivity separately.

**Comparison:** Independent voting and the strongest single model under the same resource cap; a full-information oracle is an explicit diagnostic ceiling.

**Measurements:** Designated-answer accuracy; Pre/post-discussion error correlation; Cost per correct task.

**Would count against it:** Complementary evidence has no larger benefit than family mixing at matched capability, or mixing helps without the predicted residual-error reduction.

**Main confounds:** Tokenizer differences, stronger individual models and shard difficulty can masquerade as diversity; cluster uncertainty by generated task, not agent.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit InfoDelphi methods and establish calibration/test separation plus solvable evidence unions before choosing model pools.

**Closest prior and evidence limits:**

- [[li-2026-diverse]] — [Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-diverse.md). Direct evidence-partitioning precedent; this factorial tests added family effects and task transfer. Catalogue depth: abstract.
- [[kim-2026-are]] — [Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2026-are.md). Capability-controlled audit warns that raw diversity metrics can re-express accuracy. Catalogue depth: abstract.
- [[rai-2026-when]] — [When Too Many Cooks Spoil the Broth: Three Failure Modes of Multi-Agent LLM Reliability](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rai-2026-when.md). Reported cross-family co-failure on rare queries cautions against treating vendor labels as independent evidence. Catalogue depth: abstract.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-02"></a>
### SOC-02 — Measure effective team size on distributed evidence

**Update 2:** revised.

**Question:** Does effective team size increase with population when each worker holds useful private evidence?

**Candidate hypothesis:** Communication increases effective evidence on complementary tasks but creates a ceiling when observations overlap; answer agreement alone overstates independence.

**How to test:** Randomize whole synthetic episodes to independent voting, debate, self-correction and unrelated-message placebo, crossed with overlapping/complementary evidence. Sweep team size at fixed fact union and inference budget; label fixed-per-agent-budget sensitivity separately. Estimate pre/post error covariance across independent tasks, alongside accuracy and shared-wrong-answer rates; bootstrap tasks rather than messages.

**Comparison:** Matched independent samples and a single agent with the evidence union; never treat oracle access as equivalent deployment cost.

**Measurements:** Effective team size with uncertainty; Final correctness; Evidence coverage; Tokens per correct decision.

**Would count against it:** The purported increase is absent on held-out tasks, or only appears when each added agent receives extra total evidence.

**Main confounds:** Kish-style effective size assumes a usable correlation structure; heterogeneous errors and negative correlations require reporting the covariance matrix rather than blindly applying one scalar.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Audit covariance assumptions; novelty requires split evidence and a charged placebo, not another generic effective-size ceiling.

**Closest prior and evidence limits:**

- [[bertalanic-2026-ringelmann]] — [The Ringelmann Effect in Multi-Agent LLM Systems: A Scaling Law for Effective Team Size](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bertalanic-2026-ringelmann.md). Supplies a QA-based effective-size model and placebo comparisons. Catalogue depth: full.
- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Already studies distributed evidence; qualitative overhead is not a new finding. Catalogue depth: full.
- [[begin-2026-preference]] — [Preference Optimization Drives Monoculture in LLM Prediction Markets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/begin-2026-preference.md). Already measures effective-size saturation in a prediction market; its Kish proxy is not derived from market dynamics. Catalogue depth: skim.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md).

<a id="soc-03"></a>
### SOC-03 — Distinguish group failure from a strict scoring rule

**Update 2:** unchanged.

**Question:** How much apparent deterioration with team size comes from requiring every agent to answer correctly?

**Candidate hypothesis:** All-agents-correct scoring declines faster than a designated final answer even when individual accuracy and integration quality stay stable.

**How to test:** Use the same independently generated episodes and identical saved responses for three prespecified scores: all correct, designated reporter correct, and fixed-fraction correct. Randomize population size and reporter identity before work begins; hold total evidence and token budget fixed. Fit the observed all-correct rate against an independence null using measured individual error rates.

**Comparison:** A noninteracting ensemble with matched individual accuracy and a full-information single-agent reference.

**Measurements:** All-correct and reporter success; Mean individual correctness; Excess failure beyond scoring null.

**Would count against it:** The reporter and individual scores deteriorate as strongly as the all-correct score, with little decline explained by the metric.

**Main confounds:** Reporter selection after seeing answers would inflate success; correlated errors invalidate a simple product-of-probabilities null, so report an empirical ensemble null too.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Recover exact scoring and round-budget definitions before choosing a Silo-Bench reproduction.

**Closest prior and evidence limits:**

- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Its all-agent success criterion motivates this direct measurement audit. Catalogue depth: full.
- [[kim-2025-towards]] — [Towards a Science of Scaling Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-towards.md). Documents task-dependent scaling rather than a universal population law. Catalogue depth: full.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-04"></a>
### SOC-04 — Ablate why semantic routing works

**Update 2:** unchanged.

**Question:** Do complementary-information routing signals outperform simple direct addressing once delivery is matched?

**Candidate hypothesis:** Complementarity helps when private evidence is distributed, while direct addressing alone explains gains on obvious request-response tasks.

**How to test:** Randomize complete episodes to direct-address-only, need-matching-only, complementarity-only and combined routing. Use the same generated task, initial evidence, incoming token cap and total inference allowance. Charge embedding and router calls. Include a coverage-constrained random router and evaluate on task families withheld when setting weights.

**Comparison:** Uniform random delivery with the same graph degrees and a simple append-only board under the same resource ceiling.

**Measurements:** Correct global solution; Unique useful facts delivered; Participation; End-to-end cost.

**Would count against it:** Combined routing does not beat direct addressing or random coverage within a prespecified practical margin on held-out tasks.

**Main confounds:** Semantic distance is not evidence independence; router embeddings can leak task answers and coverage guarantees can explain apparent gains.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Read routing prompts and appendices; fix a weight-selection split and an accounting method for embedding cost.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Closest predecessor; library audit notes missing per-signal ablation. Catalogue depth: full.
- [[zhang-2024-cut]] — [Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2024-cut.md). Establishes communication pruning as existing work, requiring a strong sparse baseline. Catalogue depth: skim.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-05"></a>
### SOC-05 — Measure reading capacity separately from wording bias

**Update 2:** unchanged.

**Question:** Does increasing inbox capacity improve truth finding after controlling the bias induced by claim wording?

**Candidate hypothesis:** Capacity helps only when the wording-induced prior is weak; otherwise more communication can amplify a biased starting field.

**How to test:** Randomize entire populations to inbox capacities and truth-preserving paraphrases of synthetic binary claims. Counterbalance assertion polarity and initial correct fractions. Keep total inference and delivered-token budgets fixed by equal-length messages and matched rounds; include unused-budget accounting. Measure isolated responses before interaction and validate predictions on unseen claims.

**Comparison:** No interaction, random-message placebo and a fitted response model that includes versus omits the claim-specific field.

**Measurements:** Correct-consensus probability; Wrong consensus and fragmentation; Calibration error of collective forecasts.

**Would count against it:** A capacity-only model forecasts held-out collective outcomes as well as the wording-aware model, or the proposed interaction reverses reliably.

**Main confounds:** Reversing a statement can change semantic difficulty; a few item-specific outcomes cannot establish a phase transition or universal critical capacity.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Create paired claims with verified equivalent truth conditions and read both methods before fixing the capacity grid.

**Closest prior and evidence limits:**

- [[fukushima-2026-message]] — [Message capacity and claim wording set the transition points of collective truth-finding in language-model networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fukushima-2026-message.md). Direct prior measuring inbox capacity and claim wording; this is a transfer test. Catalogue depth: abstract.
- [[liu-2026-social]] — [Social Networks of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-social.md). Attention-based proxy supplies conditional network predictions, not a universal theorem for LLMs. Catalogue depth: skim.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md).

<a id="soc-06"></a>
### SOC-06 — Social influence or ordinary anchoring?

**Update 2:** unchanged.

**Question:** Does a peer-labelled opinion change judgments more than identical information presented as a numeric anchor?

**Candidate hypothesis:** Most apparent social coupling on simple judgments is explained by anchoring; an additional social effect emerges only for evidence-bearing peers.

**How to test:** Randomize independent task episodes to peer attribution, anonymous numeric suggestion or no suggestion, keeping message content and length identical. Cross this with randomly assigned starting estimates and whether a verifiable observation accompanies the suggestion. Collect a fresh final judgment under a fixed per-episode token allowance; analyze task-level slopes and biases.

**Comparison:** The identical anchor without social identity and isolated responses measured on held-out task instances.

**Measurements:** Coupling slope; Prior bias; Accuracy change; Evidence-conditioned revision.

**Would count against it:** Peer labels add materially greater coupling than identical anonymous anchors in the no-evidence stratum, or the predicted additional coupling for evidence-bearing peers is absent across held-out tasks.

**Main confounds:** Role labels may imply expertise; demand characteristics and familiar factual claims can predetermine answers. This test measures behavior, not a human-like social mechanism.

**Framing / first-test class:** replication / api-small.

**Before promotion:** Select unfamiliar synthetic claims and freeze prompts without prescribing conformity.

**Closest prior and evidence limits:**

- [[yang-2026-when]] — [When Is Emergent Consensus Real? A Measured Coupling Gain and a Validity Diagnostic for LLM Agent Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yang-2026-when.md). Measures coupling and proposes randomized initial-condition diagnostics. Catalogue depth: skim.
- [[brockers-2025-disentangling]] — [Disentangling Interaction and Bias Effects in Opinion Dynamics of Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/brockers-2025-disentangling.md). Separates interaction from topic, agreement and anchoring biases in dyads. Catalogue depth: abstract.

**Related team work:** [leadership](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/leadership.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md).

<a id="soc-07"></a>
### SOC-07 — Protect private judgments before public discussion

**Update 2:** revised.

**Question:** Does requiring a private pre-discussion answer preserve useful minority evidence without preventing correction?

**Candidate hypothesis:** A private committed judgment reduces unsupported public conformity, but the benefit disappears when the commitment becomes an instruction never to revise.

**How to test:** Randomize whole team episodes to private structured answers, private answers with a never-revise instruction, public first answers or no preliminary answer. Equalize generation tokens by allocating the same first-pass work in every arm. After an identical evidence exchange, collect public and private final choices and score both against synthetic ground truth. Rotate the initially informed minority.

**Comparison:** Independent voting and an ordinary debate arm with identical evidence and total cost.

**Measurements:** Wrong-to-right and right-to-wrong revisions; Private/public mismatch; Final accuracy.

**Would count against it:** Private commitment fails to improve final accuracy or only suppresses both harmful and useful updates equally.

**Main confounds:** Hidden reasoning is not ground truth; use explicit private outputs rather than interpreting chain-of-thought. Preliminary answers can themselves anchor agents.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Define a nonbinding commitment format and check equivalent first-pass computation.

**Closest prior and evidence limits:**

- [[shehata-2026-bystander]] — [The Bystander Effect in Multi-Agent Reasoning: Quantifying Cognitive Loafing in Collaborative Interactions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shehata-2026-bystander.md). Abstract reports private/public conformity gaps; this design does not assume its internal-state interpretation. Catalogue depth: abstract.
- [[choi-2025-debate]] — [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choi-2025-debate.md). Provides a voting baseline and cautions against attributing gains to interaction alone. Catalogue depth: abstract.
- [[ren-2026-sepal]] — [SEPAL: Separated Expert Pairs with Answer-Level Fusion for Reliable LLM Collaboration](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ren-2026-sepal.md). Private actor-critic groups with late answer fusion are a direct separation precedent; this card isolates initial commitment. Catalogue depth: abstract.

**Related team work:** [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md).

<a id="soc-08"></a>
### SOC-08 — Stop on evidence sufficiency instead of verbal agreement

**Update 2:** unchanged.

**Question:** Can a checkable evidence checklist improve the speed-accuracy tradeoff for group commitment?

**Candidate hypothesis:** Requiring coverage of task-relevant facts reduces premature commitment more efficiently than adding a fixed number of discussion rounds.

**How to test:** Randomize independent distributed-constraint episodes to checklist-triggered stopping, confidence-triggered stopping or a fixed round count. Every arm sees the same schema of required fact types, without privileged solution labels. Charge checklist checks to a shared token/tool budget and vary the deadline. Plot error against actual delay for each rule.

**Comparison:** Matched-budget independent voting and fixed-round discussion, with a full-information solver as a diagnostic ceiling.

**Measurements:** False commits; Deadline completion; Latency to correct commitment; Cost per verified answer.

**Would count against it:** The checklist fails to improve the frontier over fixed rounds, or succeeds only because it reveals otherwise unavailable facts.

**Main confounds:** Fact coverage is not reasoning correctness; a complete checklist may accompany a wrong calculation. Confidence calibration can vary by model and must be measured independently.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Build a task where required evidence types are public but their values remain distributed.

**Closest prior and evidence limits:**

- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Reports premature submission and distributed integration difficulties. Catalogue depth: full.
- [[choi-2025-debate]] — [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choi-2025-debate.md). Shows aggregation baselines can explain apparent debate benefits. Catalogue depth: abstract.

**Related team work:** [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-09"></a>
### SOC-09 — Evidence-seeking critics versus generic opposition

**Update 2:** unchanged.

**Question:** When does a critic improve an answer rather than merely add another expensive pass?

**Candidate hypothesis:** A critic required to request or cite a discriminating observation corrects more wrong answers than an equally funded generic skeptic.

**How to test:** Randomize full team episodes with initially correct and incorrect answers to evidence-seeking critic, always-disagree critic or extra independent solver. All arms receive identical evidence access, tool allowance and total token budget; rotate critic identity. Evaluate on fresh tasks with programmatically checkable answers and score final decisions separately from persuasive language.

**Comparison:** No-critic independent voting plus a self-review arm using the same extra computation.

**Measurements:** Net accuracy gain; Wrong-to-right corrections; Right-to-wrong reversals; Critic cost.

**Would count against it:** The evidence critic is no better than extra independent computation, or its false reversals cancel corrections.

**Main confounds:** A critic can receive extra evidence by accident; generated explanations may sound rigorous without identifying a valid contradiction. Score cited observations directly.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Specify how discriminating evidence is scored and set an acceptable false-reversal margin before a real run.

**Closest prior and evidence limits:**

- [[du-2023-improving]] — [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/du-2023-improving.md). Introduces debate as a baseline rather than establishing this critic mechanism. Catalogue depth: abstract.
- [[choi-2025-debate]] — [Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choi-2025-debate.md). Motivates separating discussion gains from sampling and voting. Catalogue depth: abstract.

**Related team work:** [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md).

<a id="soc-10"></a>
### SOC-10 — Test dissent quality rather than dissent quantity

**Update 2:** revised.

**Question:** Will a group weight a dissenting claim by evidence quality when the critic is confidently wrong?

**Candidate hypothesis:** Evidence-quality metadata improves correction only when recipients can inspect the underlying observation; confidence labels alone increase harmful reversals.

**How to test:** Randomize entire team episodes in a factorial design with critic correctness, stated confidence and presence of an inspectable observation. Keep critics scripted initially to isolate the input, match message length, then reserve an interacting-agent extension. Allocate identical verification tokens and randomize whether the starting majority is correct.

**Comparison:** Same dissent without confidence or evidence labels and an extra-solver vote under the same budget.

**Measurements:** Correct dissent acceptance; Incorrect dissent acceptance; Verification uptake; Final accuracy.

**Would count against it:** Underlying evidence does not improve discrimination between correct and incorrect critics, or confidence-only labels do not increase incorrect-dissent acceptance or right-to-wrong reversals versus an unlabelled matched message.

**Main confounds:** Scripted critics measure recipient behavior rather than emergent dissent; evidence difficulty and verbosity must be balanced across correct and wrong challenges.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Generate matched correct and incorrect counterexamples with objective validators.

**Closest prior and evidence limits:**

- [[kraidia-2026-when]] — [When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kraidia-2026-when.md). Ordinary persuasive arguments can distort tested debates; effects remain task-specific. Catalogue depth: full.
- [[he-2026-minority]] — [Minority Sentinel: When to Overturn Majority Voting in Multi-Agent LLM Debates](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/he-2026-minority.md). Minority-correct cases and a learned overturn rule are direct prior; this factorial isolates evidence from confidence. Catalogue depth: abstract.
- [[shu-2026-forged]] — [Forged Peer Judgments Mislead Multimodal LLM Judge Panels: Source-Blind Anchoring and Panel-Consensus Verification](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shu-2026-forged.md). Quoted judgments can anchor recipients beyond source labels; here dissent is controlled and benign. Catalogue depth: abstract.

**Related team work:** [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [whistleblowing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/whistleblowing.md).

<a id="soc-11"></a>
### SOC-11 — Make uncertainty useful without forcing abstention

**Update 2:** revised.

**Question:** Does explicit uncertainty sharing help groups ask the right follow-up question?

**Candidate hypothesis:** A short statement of what evidence is missing improves allocation of verification effort more than a scalar confidence score.

**How to test:** Randomize independent hidden-profile episodes to missing-evidence statements, numeric confidence or answer-only messages. Keep communication token limits and total tool calls equal. Agents may spend a fixed verification allowance querying one additional fact; the full task truth is reachable in every arm. Compare which fact is requested and the resulting answer.

**Comparison:** Random fact requests and a calibrated confidence-only protocol, plus independent voting.

**Measurements:** Value of acquired fact; Final accuracy; Abstention rate; Queries per correction.

**Would count against it:** The missing-evidence format does not select more useful facts or improve correctness relative to confidence at matched cost.

**Main confounds:** Missing-evidence text could smuggle longer reasoning; scalar confidence must be calibrated on a separate split. The selected query is a mediator, not an independent replicate.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Define fact-query utilities independently and verify equal communication capacity across formats.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Need matching already routes information; candidate tests message semantics and query value. Catalogue depth: full.
- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Distributed tasks motivate distinguishing information delivery from integration. Catalogue depth: full.
- [[zhu-2026-demystifying]] — [Demystifying Multi-Agent Debate: The Role of Confidence and Diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhu-2026-demystifying.md). Calibrated-confidence updates are existing intervention prior; missing-evidence requests need an incremental comparison. Catalogue depth: abstract.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md).

<a id="soc-12"></a>
### SOC-12 — Useful disagreement after a changing task

**Update 2:** unchanged.

**Question:** Does preserving a minority answer help adaptation when the environment changes?

**Candidate hypothesis:** A bounded minority-report slot speeds adaptation after a real state change but wastes budget when disagreement has no evidence behind it.

**How to test:** Randomize complete repeated-decision worlds to retaining a minority report, retaining a random report or majority-only summaries. Apply a predetermined hidden-state change in half the worlds and no change in the rest. Match memory capacity, evidence arrival and total inference tokens; score both pre-change and post-change decisions on held-out world seeds.

**Comparison:** Majority-only memory and independent agents receiving the same new observations.

**Measurements:** Post-change regret; Adaptation latency; Stable-world accuracy; Useful minority retention.

**Would count against it:** Minority retention does not reduce regret or its stable-world losses exceed the gain under the prespecified change mixture.

**Main confounds:** Retention is not inherently useful diversity; minority quality and change predictability matter. Randomizing complete worlds avoids treating repeated decisions as independent trials.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Choose a change process that neither directly rewards dissent nor lets retained text reveal the new answer.

**Closest prior and evidence limits:**

- [[pavlova-2026-flag]] — [Flag Game: A Toy Model for Mechanistic Swarm Interpretability](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pavlova-2026-flag.md). Measures multiple collective end states; polarization itself is not established as safer. Catalogue depth: full.
- [[ashery-2024-emergent]] — [Emergent social conventions and collective bias in LLM populations](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ashery-2024-emergent.md). Convention persistence motivates testing adaptation rather than celebrating consensus. Catalogue depth: full.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md).

<a id="soc-13"></a>
### SOC-13 — Separate discovery time from discussion time

**Update 2:** unchanged.

**Question:** Does delaying communication improve search coverage before the team integrates results?

**Candidate hypothesis:** An initial independent exploration phase reduces redundant search and improves final solutions on decomposable tasks, but harms tightly coupled tasks.

**How to test:** Randomize full task episodes to immediate discussion, delayed discussion or no discussion. Cross delay with task decomposability using generated search-and-combine puzzles. Keep total tool calls and inference tokens fixed; discussion consumes the same budget as exploration. Freeze delay choices on development tasks and score untouched task families.

**Comparison:** Independent best-of-N and one agent using the full budget, with equivalent observation access.

**Measurements:** Distinct useful discoveries; Duplicate queries; Final solution quality; Cost per valid artifact.

**Would count against it:** Delayed communication never improves the cost-quality frontier, or its apparent advantage disappears after counting extra independent search.

**Main confounds:** A task deliberately partitioned into independent pieces makes the result trivial; include intermediate coupling and report how combination requirements were generated.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Specify a decomposability measure and prevent shared files from leaking discoveries during the silent phase.

**Closest prior and evidence limits:**

- [[kim-2025-towards]] — [Towards a Science of Scaling Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-towards.md). Shows architecture benefits depend on task structure; no universal delay rule follows. Catalogue depth: full.
- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Separates portfolio benefits from strongest-artifact performance in shared environments. Catalogue depth: abstract.

**Related team work:** [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md).

<a id="soc-14"></a>
### SOC-14 — Treat shared artifacts as a communication channel

**Update 2:** unchanged.

**Question:** How much coordination is carried by artifact observation rather than explicit messages?

**Candidate hypothesis:** Artifact access explains most reuse in construction tasks, while explicit messages help chiefly when observations are costly or ambiguous.

**How to test:** Randomize independent synthetic worlds to a two-by-two crossing of messages enabled and shared artifacts visible. Match total context tokens, action counts and world information opportunities; record observation events explicitly. Score finished programs or constructions with a deterministic evaluator after agents stop. Include identical worlds with cheap versus expensive artifact inspection.

**Comparison:** Private-world isolated search and a public artifact board without chat; compare both best artifact and whole portfolio.

**Measurements:** Validated reuse; Portfolio coverage; Best-artifact quality; Observation and messaging cost.

**Would count against it:** Messages account for most validated reuse even when artifact inspection is cheap, or shared artifacts add no functional benefit.

**Main confounds:** A shared world is not a no-communication condition. Action side effects may reveal hidden state even when messages are disabled, so the channel boundary must be explicit.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Choose a small deterministic construction environment and define artifact observation before implementation.

**Closest prior and evidence limits:**

- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Direct stigmergy precedent; this is a task and observability boundary test. Catalogue depth: abstract.
- [[park-2023-generative]] — [Generative Agents: Interactive Simulacra of Human Behavior](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2023-generative.md). Memory and observation architecture is background, not evidence of functional gains. Catalogue depth: abstract.

**Related team work:** [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md), [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [commons](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/commons.md).

<a id="soc-15"></a>
### SOC-15 — Asynchronous teams under uneven tool latency

**Update 2:** revised.

**Question:** When does asynchronous work beat round-based discussion once stale information is counted?

**Candidate hypothesis:** Asynchrony improves completion under variable tool delays but loses accuracy when rapid state changes make old messages misleading.

**How to test:** Randomize complete task episodes to synchronous rounds or event-driven execution. Cross tool-delay variance and environment-change rate using paired scripted worlds; randomize initial activation order. Fix total generated tokens, tool calls, budget visibility and deadline; charge retries and timeouts. Each world is one statistical unit, with agent participation tracked rather than assumed.

**Comparison:** A synchronous team and a single worker with the same aggregate compute cap, with latency reported separately from throughput.

**Measurements:** Deadline success; Stale-message decisions; Wall time; Idle fraction; Tokens per completion.

**Would count against it:** Asynchrony provides no completion advantage under high delay variance, or shows no predicted accuracy loss as state-change rate rises.

**Main confounds:** API rate limits, hidden batching and scheduling fairness can create implementation effects; use controllable simulated tool delays for the initial test.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Specify what state version each message describes and whether interrupted work consumes budget.

**Closest prior and evidence limits:**

- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Distributed coordination tasks supply a benchmark family, not an asynchronous comparison. Catalogue depth: full.
- [[kim-2025-towards]] — [Towards a Science of Scaling Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-towards.md). Makes coordination overhead a measured cost rather than a universal scaling law. Catalogue depth: full.
- [[paliskara-2026-worse]] — [Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/paliskara-2026-worse.md). Shared-resource teams exhibit participation and coordination failures; does not isolate asynchronous execution. Catalogue depth: full.

**Related team work:** [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-16"></a>
### SOC-16 — Allocate roles by observed bottlenecks

**Update 2:** revised.

**Question:** Can teams choose useful temporary roles from their actual information deficits?

**Candidate hypothesis:** Reallocating a limited role budget toward unresolved subproblems improves completion more than fixed persona assignments.

**How to test:** Randomize complete project episodes to fixed roles, periodically reassigned roles or role-free work. Reassignment sees only public progress and unmet requirements; charge it to the hard shared budget. Hold model composition, evidence, capability metadata and action allowance constant. Rotate initial roles and include tasks whose bottleneck changes halfway through.

**Comparison:** Uniform round-robin assignments and a centralized planner with identical information and token cap.

**Measurements:** Verified milestones completed; Uncovered subproblems; Reassignment overhead; Duplicate effort.

**Would count against it:** Dynamic roles fail to improve outcomes after charging reassignment cost, or fixed roles adapt equally well.

**Main confounds:** A named persona is not demonstrated specialization; score observed actions. An allocator that sees hidden solution structure would invalidate the comparison.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Create observable bottleneck indicators that do not reveal the solution and define valid role changes.

**Closest prior and evidence limits:**

- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Reports functional differentiation; does not establish this allocation policy. Catalogue depth: abstract.
- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Failure taxonomy motivates explicit task alignment and completion checks. Catalogue depth: full.
- [[amayuelas-2025-self]] — [Self-Resource Allocation in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amayuelas-2025-self.md). Direct allocation/planner precedent with explicit worker capabilities; novelty requires the changing-bottleneck and hard-cap contrast. Catalogue depth: full.

**Related team work:** [leadership](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/leadership.md), [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-17"></a>
### SOC-17 — Separate a leader's name from its information

**Update 2:** unchanged.

**Question:** Does apparent authority change task outcomes beyond the content of the same proposal?

**Candidate hypothesis:** Leader labels change adoption without improving execution; useful influence is better predicted by evidence quality than message volume.

**How to test:** Randomize whole team episodes to the same frozen proposal labelled as coordinator, ordinary peer or anonymous note. Independently vary whether the proposal contains the decisive observation. Counterbalance author labels and placement, keep text and total token budgets identical, and measure downstream tool actions using an exact environment log.

**Comparison:** The identical anonymous proposal and a no-proposal control allocated the same reasoning allowance.

**Measurements:** Proposal adoption per exposure; Verified task completion; Incorrect-authority compliance; Execution latency.

**Would count against it:** Authority reliably improves verified outcomes even when information and order are matched, or evidence quality does not predict useful influence.

**Main confounds:** Authority can be a legitimate information cue in other settings; this test deliberately breaks that relationship. Adoption alone is not causal task benefit, and labels are not stable personalities.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Define frozen proposal sets and ensure executor tools produce independently checkable outcomes.

**Closest prior and evidence limits:**

- [[shehata-2026-bystander]] — [The Bystander Effect in Multi-Agent Reasoning: Quantifying Cognitive Loafing in Collaborative Interactions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shehata-2026-bystander.md). Abstract suggests anchor identity matters; this is an output-based intervention. Catalogue depth: abstract.
- [[yang-2026-when]] — [When Is Emergent Consensus Real? A Measured Coupling Gain and a Validity Diagnostic for LLM Agent Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yang-2026-when.md). Anchoring control motivates content-preserving label changes. Catalogue depth: skim.

**Related team work:** [leadership](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/leadership.md).

<a id="soc-18"></a>
### SOC-18 — Rotate coordination without losing continuity

**Update 2:** unchanged.

**Question:** Can rotating a coordinator improve resilience while preserving accumulated task knowledge?

**Candidate hypothesis:** Rotation helps after coordinator loss only when a compact public task ledger is available; otherwise handoff cost outweighs redundancy.

**How to test:** Randomize independent task episodes to fixed coordinator, scheduled rotation or random rotation. Cross each with a bounded public ledger and a predetermined coordinator outage. Match total inference tokens, ledger capacity and surviving worker count. Replace agents without privileged access to the removed context; count recovery work against the budget.

**Comparison:** Fixed coordination with an equally sized shared ledger and a no-outage control for every architecture.

**Measurements:** Post-outage completion; Handoff latency; Lost requirements; Total cost; Pre-outage quality.

**Would count against it:** Rotation adds no resilience beyond the ledger, or its ordinary-operation cost dominates under the specified outage rate.

**Main confounds:** Restored connectivity is not restored knowledge; remove the same functional role rather than the most important node selected after observing results.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Choose a transparent task ledger and separate unique-information destruction from loss of a worker.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Failure robustness is existing prior; its permanent-failure setting differs from role handoff. Catalogue depth: full.
- [[park-2023-generative]] — [Generative Agents: Interactive Simulacra of Human Behavior](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2023-generative.md). Persistent memory motivates continuity, without demonstrating fault recovery. Catalogue depth: abstract.

**Related team work:** [leadership](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/leadership.md), [regrowth](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/regrowth.md).

<a id="soc-19"></a>
### SOC-19 — Ask a specific peer instead of broadcasting

**Update 2:** unchanged.

**Question:** Are targeted evidence requests more useful than broadcasting everything under the same attention budget?

**Candidate hypothesis:** Targeted requests reduce wasted delivery when tasks have sparse dependencies, but miss surprises that a board would expose.

**How to test:** Randomize complete distributed puzzles to addressed requests, broadcast summaries or hybrid discovery-then-request communication. Hold total delivered tokens and tool queries fixed; match evidence allocation and use a recorded request-response graph. Cross sparse known dependencies with unexpected cross-shard dependencies. Fix routing rules before held-out evaluation.

**Comparison:** Random recipient routing with matched degrees and a capped append-only board.

**Measurements:** Relevant facts obtained; Missed cross-shard clues; Final correctness; Delivered tokens per solution.

**Would count against it:** Targeted requests do not improve sparse tasks or maintain their advantage when relevant dependencies are unknown, contradicting the predicted tradeoff.

**Main confounds:** Messages sent are not messages read; measure actual context delivery. A hybrid arm must pay for its discovery step rather than receiving free routing knowledge.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Construct held-out surprise dependencies and log delivered context exactly.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Need-matching and direct addressing are existing mechanisms to compare. Catalogue depth: full.
- [[liu-2026-social]] — [Social Networks of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-social.md). Attention rather than graph edges motivates delivery-aware evaluation. Catalogue depth: skim.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-20"></a>
### SOC-20 — Recognize unachievable tasks and request repair

**Update 2:** unchanged.

**Question:** Can a team identify missing prerequisites without abandoning difficult but solvable work?

**Candidate hypothesis:** A bounded impossibility-check step reduces wasted collective exploration on unreachable tasks while retaining success on hard solvable controls.

**How to test:** Randomize entire synthetic planning episodes to ordinary persistence, a prerequisite checklist or a peer feasibility audit. Pair solvable tasks with matched tasks missing one essential resource; use a deterministic solver to certify both categories. Give every arm equal inference and tool budgets and an explicit request-for-clarification action within the sandbox.

**Comparison:** Single-agent feasibility checking and a fixed timeout with the same total cost.

**Measurements:** Unsolvable-task detection; False abandonment; Useful completion; Wasted actions; Repair requests.

**Would count against it:** The audit cannot distinguish unreachable from merely difficult cases or lowers total verified completion after overhead.

**Main confounds:** This is a test of bounded task feasibility, not inferred intentions or general safety. Checklist wording must not reveal which category an episode occupies.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Design certified unreachable instances and a rubric distinguishing honest uncertainty from premature termination.

**Closest prior and evidence limits:**

- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Task specification and termination failures motivate a controlled feasibility check. Catalogue depth: full.
- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Known-answer algorithmic tasks provide an interpretable reachability baseline. Catalogue depth: full.

**Related team work:** [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md), [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md).

<a id="soc-21"></a>
### SOC-21 — Compress memory by information value

**Update 2:** unchanged.

**Question:** Which memory contents preserve useful collective knowledge under a fixed context limit?

**Candidate hypothesis:** Retaining rare task-relevant observations and unresolved questions beats recency-only summaries on future tasks requiring distributed facts.

**How to test:** Randomize independent multi-stage task worlds to recency, frequency or estimated information-value memory selection. All memories have the same token cap and every selection step consumes the common inference budget. Future questions are sampled from a held-out distribution unknown to agents; include both recurring facts and initially rare decisive facts.

**Comparison:** Uniform reservoir retention and one worker receiving the same total memory budget.

**Measurements:** Held-out task accuracy; Rare-fact recall; Unsupported reconstructed facts; Summary cost.

**Would count against it:** Information-value selection does not outperform simple retention or gains only when its selection rule leaks future questions.

**Main confounds:** Frequent mentions may reflect copying rather than importance; rarity alone may retain noise. This studies useful retention, leaving provenance repair and rollback to the security lane.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Define information-value estimates from available observations and fix future-task sampling independently.

**Closest prior and evidence limits:**

- [[park-2023-generative]] — [Generative Agents: Interactive Simulacra of Human Behavior](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2023-generative.md). Provides retrieval and reflection architecture as direct memory background. Catalogue depth: abstract.
- [[perez-2024-cultural]] — [Cultural evolution in populations of Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/perez-2024-cultural.md). Transformation through repeated transmission motivates measuring retained content. Catalogue depth: abstract.

**Related team work:** [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md), [telephone](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/telephone.md).

<a id="soc-22"></a>
### SOC-22 — Spend redundancy on rare knowledge

**Update 2:** unchanged.

**Question:** Is selective replication better than uniformly duplicating every workers notes?

**Candidate hypothesis:** Replicating uniquely held useful observations improves fault tolerance more per stored token than uniform replication.

**How to test:** Randomize complete distributed tasks to uniform copying, rarity-weighted copying or no extra copying. Fix total memory tokens and inference cost, then apply prescheduled random worker loss or loss of the highest-information worker defined before task execution. Replacement agents see only surviving records; score final answers and missing facts.

**Comparison:** Uniform copies with equal storage and a no-failure reference for each retention strategy.

**Measurements:** Correct answers after loss; Unique facts surviving; Extra storage cost; Recovery latency.

**Would count against it:** Selective replication does not improve task success over uniform copies or relies on an evaluator supplying hidden fact importance.

**Main confounds:** Rarity and usefulness differ; the policy may copy obscure noise. Separate loss of a worker from permanent destruction of every copy, where reconstruction can be impossible.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Define what agents can know about redundancy and validate an equal-storage loss generator.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Already evaluates permanent agent failures; selective knowledge retention is the narrower candidate. Catalogue depth: full.
- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Persistent shared artifacts motivate distinguishing portfolio survival from visual reconnection. Catalogue depth: abstract.

**Related team work:** [regrowth](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/regrowth.md), [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md).

<a id="soc-23"></a>
### SOC-23 — Recover function after genuine knowledge loss

**Update 2:** unchanged.

**Question:** When can a replacement worker reconstruct missing evidence from the environment rather than a hidden backup?

**Candidate hypothesis:** A task-aware reacquisition policy recovers function more efficiently than restarting all workers when evidence is recoverable, but cannot restore permanently destroyed unique facts.

**How to test:** Randomize complete task worlds to targeted reacquisition or blind restart after a fixed worker-loss event. Cross recoverable observations with genuinely unavailable observations. Keep surviving resources, restart cost and total tool budget identical. Record the provenance of new observations only to verify reacquisition, without testing a security mechanism.

**Comparison:** No recovery and an explicitly labelled perfect-backup upper bound; report irrecoverable cases separately.

**Measurements:** Recovered task accuracy; New observation cost; Time to useful completion; Hallucinated recovery.

**Would count against it:** Targeted reacquisition performs no better than restart on recoverable cases, or claims success only through unsupported reconstruction.

**Main confounds:** A restarted agent must not inherit the lost state through its prompt; knowing the evaluator answer is not reconstruction. Episode-level repetitions are required for uncertainty.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Choose an environment with explicit observation availability and charge repeat observation costs.

**Closest prior and evidence limits:**

- [[tambwekar-2026-proxifield]] — [Proxifield: Decentralized Multi-Agent Communication through Semantic Proximity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tambwekar-2026-proxifield.md). Existing robustness work motivates a knowledge-loss-specific boundary. Catalogue depth: full.
- [[zhang-2026-silo]] — [Silo-Bench: A Scalable Environment for Evaluating Distributed Coordination in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-silo.md). Distributed exact-answer tasks support verifiable functional recovery. Catalogue depth: full.

**Related team work:** [regrowth](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/regrowth.md), [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md).

<a id="soc-24"></a>
### SOC-24 — What survives complete population turnover?

**Update 2:** unchanged.

**Question:** Do useful procedures survive replacement through shared artifacts, direct interaction or model priors?

**Candidate hypothesis:** Artifact access preserves task procedures through turnover, while naming conventions can persist without producing better held-out performance.

**How to test:** Randomize independent multi-generation worlds to inherited notes, overlapping old/new cohorts, both, or neither. Replace all original agents on a fixed schedule; maintain equal cumulative inference and onboarding tokens. Use arbitrary conventions counterbalanced across worlds and procedural tasks whose test instances are absent from onboarding materials.

**Comparison:** Fresh agents with neutral instructions and a verbatim executable procedure as an explicit transfer ceiling.

**Measurements:** Convention survival; Held-out task performance; Procedure mutation; Onboarding cost.

**Would count against it:** Persistence disappears under counterbalanced conventions or surviving conventions do not improve task performance as predicted.

**Main confounds:** Common model priors and shared system prompts can mimic inheritance; descriptive culture is not evidence of consciousness or human-like mechanisms. Generations within a world are dependent observations.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Separate normative conventions from factual procedures and seal test tasks before generating onboarding notes.

**Closest prior and evidence limits:**

- [[perez-2024-cultural]] — [Cultural evolution in populations of Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/perez-2024-cultural.md). Direct precedent for controlled transmission in LLM populations. Catalogue depth: abstract.
- [[ashery-2024-emergent]] — [Emergent social conventions and collective bias in LLM populations](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ashery-2024-emergent.md). Naming-game conventions establish persistence questions without establishing useful task transfer. Catalogue depth: full.

**Related team work:** [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md).

<a id="soc-25"></a>
### SOC-25 — Retire an obsolete convention after the task changes

**Update 2:** unchanged.

**Question:** Can a population keep useful traditions while abandoning a convention that has become costly?

**Candidate hypothesis:** A periodic outcome review accelerates adaptation more than replacing members, because newcomers otherwise inherit the same obsolete guide.

**How to test:** Randomize whole multi-generation worlds to outcome review, member turnover, both or neither. Change which arbitrary convention is beneficial at a predetermined time, without changing the written goal. Match cumulative tokens, feedback access and memory size. Include unchanged worlds to measure needless disruption and counterbalance which convention is initially rewarded.

**Comparison:** A fixed convention and fresh agents without inherited records, under equal resource caps.

**Measurements:** Adaptation latency; Post-change regret; Unnecessary convention changes; Held-out task success.

**Would count against it:** Outcome review has no adaptation advantage over turnover or causes enough disruption in unchanged worlds to erase the gain.

**Main confounds:** Explicitly telling agents the new preferred convention would turn this into instruction following; measure adaptation to outcomes. Memory and intrinsic preferences may interact, with no general reversibility claim.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Create an outcome shift discoverable through ordinary feedback and read closest convention-change methods.

**Closest prior and evidence limits:**

- [[ashery-2024-emergent]] — [Emergent social conventions and collective bias in LLM populations](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ashery-2024-emergent.md). Provides convention and minority-tipping precedent rather than a utility-based adaptation result. Catalogue depth: full.
- [[perez-2024-cultural]] — [Cultural evolution in populations of Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/perez-2024-cultural.md). Transmission framework supports generational controls. Catalogue depth: abstract.

**Related team work:** [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md).

<a id="soc-26"></a>
### SOC-26 — Reward a useful portfolio instead of one champion

**Update 2:** unchanged.

**Question:** Does rewarding complementary artifacts change the value of sharing in collective invention?

**Candidate hypothesis:** Shared work benefits portfolio resilience more than best-artifact quality; a portfolio-aware selection rule preserves that advantage under limited evaluation budgets.

**How to test:** Randomize independent construction worlds to selecting one highest-scoring artifact or a complementary portfolio, crossed with shared versus private workspaces. Agents build bounded programs scored by a deterministic simulator under unseen disturbances after work ends. Equalize all generation and evaluation calls; select scoring weights using development worlds only.

**Comparison:** Best-of-N isolated search and uniform portfolio selection, each with the same aggregate resource allowance.

**Measurements:** Best individual score; Coverage across disturbances; Portfolio worst-case score; Evaluation cost.

**Would count against it:** Sharing fails to improve held-out portfolio resilience, or a random portfolio matches the proposed selection rule.

**Main confounds:** Defining coverage around the shared systems outputs would guarantee its success; disturbance classes and portfolio size must be fixed independently. Artifact variants from one world are not independent trials.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Choose objectively scored artifact types and a held-out disturbance generator.

**Closest prior and evidence limits:**

- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Direct prior distinguishes portfolio resilience from strongest-artifact performance. Catalogue depth: abstract.
- [[leibo-2019-autocurricula]] — [Autocurricula and the Emergence of Innovation from Social Interaction: A Manifesto for Multi-Agent Intelligence Research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leibo-2019-autocurricula.md). Motivates innovation through interaction as a position paper, not experimental support. Catalogue depth: abstract.

**Related team work:** [commons](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/commons.md), [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md).

<a id="soc-27"></a>
### SOC-27 — Credit verified contributions instead of message volume

**Update 2:** revised.

**Question:** Does contribution credit increase useful shared work or merely change how agents report it?

**Candidate hypothesis:** Credit tied to independently validated artifacts increases useful contributions more than visibility-based credit, but may reduce help on uncredited tasks.

**How to test:** Randomize complete synthetic research groups to no credit, message-count credit or verified-artifact credit. Give identical task goals, resource costs and total token budgets; keep task validators separate from agents. Evaluate novel task worlds with both directly creditable production and essential maintenance work. Rotate contributor identities.

**Comparison:** An uncredited common cache and a simple equal-share budget allocation.

**Measurements:** Verified useful artifacts; Maintenance completion; Duplicated claims; Contribution concentration; Total utility.

**Would count against it:** Credit only increases reported contribution, or verified output gains are offset by abandoned maintenance.

**Main confounds:** Reward design can predetermine behavior; vary incentive strength. Programmed noncontributors are introduced roles. Distinguish game credit, real resource costs and independent utility; inferred cooperation is not established by equal contributions.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Specify utility independently of credit, including maintenance that the credit rule may neglect.

**Closest prior and evidence limits:**

- [[leibo-2021-scalable]] — [Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leibo-2021-scalable.md). Existing social-dilemma benchmark motivates varied partners and held-out situations. Catalogue depth: abstract.
- [[pal-2026-swarmworld]] — [SwarmWorld: Stigmergic technological evolution in societies of language-model agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pal-2026-swarmworld.md). Functional artifacts provide a concrete collective-output comparison. Catalogue depth: abstract.
- [[piatti-2024-cooperate]] — [Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/piatti-2024-cooperate.md). Commons cooperation has direct simulation precedent; verified research-artifact credit is a domain extension. Catalogue depth: abstract.

**Related team work:** [commons](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/commons.md), [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md).

<a id="soc-28"></a>
### SOC-28 — Pay for verification as a public good

**Update 2:** revised.

**Question:** Can a small shared verification allowance prevent everyone from waiting for somebody else to check a result?

**Candidate hypothesis:** Explicitly funding one verifier per disputed artifact reduces duplicated checks and unchecked reuse more than an unfunded request for caution.

**How to test:** Randomize whole shared-cache task episodes to voluntary checking, rotating funded verifier or random checking subsidies. All arms have equal total inference and tool budgets: verification funding is taken from production. Vary the rate of accidentally invalid artifacts using generated seeds and include clean worlds. Count checked artifacts and actual downstream behavior.

**Comparison:** Uniform random verification at the same cost and independent work without sharing.

**Measurements:** Useful output per total budget; False-result reuse; Duplicated verification; Good work delayed.

**Would count against it:** Funding does not improve net utility beyond random checking, or its overhead dominates at the prespecified error mixture.

**Main confounds:** Forced checks test scheduling, not spontaneous cooperation; perfect validation is an environmental assumption. Keep game rewards and inference budgets separate, charge enforcement too, and do not give subsidy arms extra resources.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Choose a validator cost model and a held-out contamination distribution before selecting a subsidy.

**Closest prior and evidence limits:**

- [[leibo-2021-scalable]] — [Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leibo-2021-scalable.md). Social sharing and partner variation are established benchmark concerns. Catalogue depth: abstract.
- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Documents verification failures; does not prove subsidies solve them. Catalogue depth: full.
- [[piedrahita-2025-corrupted]] — [Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/piedrahita-2025-corrupted.md). Public-goods sanctioning is direct institutional prior; extra sanction budgets and model-family differences require separate controls. Catalogue depth: full.

**Related team work:** [commons](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/commons.md), [whistleblowing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/whistleblowing.md), [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md).

<a id="soc-29"></a>
### SOC-29 — Make a report lead to a verifiable response

**Update 2:** unchanged.

**Question:** Does an acknowledged review channel improve remediation beyond simply making reporting available?

**Candidate hypothesis:** A structured report with a bounded response deadline raises verified correction without a disproportionate rise in false interventions.

**How to test:** Randomize independent sandbox team episodes to ordinary warnings, a reporting endpoint or evidence-structured reports with an assigned response. Keep total reviewer and producer computation equal; include clean tasks, genuine invalid artifacts and ambiguous cases. The evaluator records noticing, reporting, review and correction as distinct stages rather than assuming they co-occur.

**Comparison:** An ordinary warning delivered to the same reviewer and a fixed random audit at matched cost.

**Measurements:** Verified remediation; False interventions; Report precision/recall; Time to response; Legitimate completion.

**Would count against it:** More reports do not produce more correct remediation, or false interventions erase the utility gain.

**Main confounds:** An imposed responder measures institutional design, not agents spontaneously protecting one another. Ambiguous reports require an unresolved category; invalid output alone does not identify malicious intent.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Define reversible remediation, objective incident labels and review-cost accounting.

**Closest prior and evidence limits:**

- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Supports explicit verification and outcome-based failure labels. Catalogue depth: full.
- [[leibo-2021-scalable]] — [Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leibo-2021-scalable.md). Partner and scenario variation offer an evaluation precedent for social mechanisms. Catalogue depth: abstract.

**Related team work:** [whistleblowing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/whistleblowing.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md).

<a id="soc-30"></a>
### SOC-30 — Appeal false rejections without overwhelming review

**Update 2:** unchanged.

**Question:** When is an appeal step worth its cost in collective artifact review?

**Candidate hypothesis:** A single evidence-bearing appeal restores valid work mistakenly rejected by peers, with gains concentrated where first-pass review is noisy.

**How to test:** Randomize entire shared-artifact episodes to no appeal, one structured appeal or unrestricted discussion under a common hard token cap. Independently vary first-review noise using scripted reviewers initially. Include valid and invalid artifacts, charge all adjudication against production resources, and then test the chosen rule with agent reviewers on held-out episodes.

**Comparison:** A second random review using the same tokens and ordinary discussion without formal appeal rights.

**Measurements:** Valid artifacts restored; Invalid artifacts released; Resolution latency; Review cost; Net useful output.

**Would count against it:** Structured appeals do not beat an equally funded second review or chiefly help invalid artifacts escape rejection.

**Main confounds:** Scripted reviewer noise isolates a mechanism but does not model every real dispute. Appeals must supply genuinely checkable evidence rather than reveal the evaluator label.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** Choose a bounded appeal rule and validate clean, invalid and ambiguous artifact classes.

**Closest prior and evidence limits:**

- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Verification errors motivate evaluating mistaken review as well as mistaken production. Catalogue depth: full.
- [[leibo-2021-scalable]] — [Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/leibo-2021-scalable.md). Held-out partner scenarios are a useful evaluation pattern, not direct appeal evidence. Catalogue depth: abstract.

**Related team work:** [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md).

<a id="soc-31"></a>
### SOC-31 — Find where uncertainty disappears in retelling

**Update 2:** unchanged.

**Question:** Which message format preserves a claims scope and uncertainty across repeated summaries?

**Candidate hypothesis:** Separating observation, inference and uncertainty in a short template reduces certainty inflation more than adding a generic accuracy warning.

**How to test:** Randomize entire synthetic transmission chains to free prose, a structured template or verbatim forwarding. Use equal per-hop token and memory caps, counterbalanced chain lengths and explicit source observations with known quantities and uncertainty. Score atomic claims after every hop with deterministic fields where possible; reserve unseen source types for final evaluation.

**Comparison:** Verbatim forwarding and a single summary with the same total compute budget; include accurate-transmission negative controls.

**Measurements:** Quantity/scope fidelity; Unsupported certainty increase; Useful information retained; End-task correctness.

**Would count against it:** The template does not preserve fidelity on held-out source types or only succeeds by dropping useful claims.

**Main confounds:** Similarity is not proof of copying in real traces; here the harness records actual delivery. Hops within one chain are dependent, so uncertainty is computed across independent chains.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Define uncertainty labels and a fidelity rubric before generating candidate summaries.

**Closest prior and evidence limits:**

- [[perez-2024-cultural]] — [Cultural evolution in populations of Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/perez-2024-cultural.md). Direct precedent for transmission and transformation experiments. Catalogue depth: abstract.
- [[park-2023-generative]] — [Generative Agents: Interactive Simulacra of Human Behavior](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2023-generative.md). Reflection and memory give a natural retelling mechanism, without proving factual fidelity. Catalogue depth: abstract.

**Related team work:** [telephone](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/telephone.md), [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md).

<a id="soc-32"></a>
### SOC-32 — Stress-test a casefile when logs are missing

**Update 2:** unchanged.

**Question:** Can evidence-linked casefiles prevent an automated investigator from inventing causal connections under partial logs?

**Candidate hypothesis:** Explicit missing-record markers improve abstention and supported answers relative to a polished chronological summary.

**How to test:** Generate independent small-agent episodes with fully logged actions, then randomize episode copies to controlled log deletion, timestamp noise and summary-only records. Compare an investigator agent given a structured casefile versus the same records in chronological order under identical context and token caps. Score factual answers and unsupported causal assertions against the hidden complete record.

**Comparison:** Chronological search plus a basic summary and a full-log diagnostic upper bound.

**Measurements:** Supported-answer rate; Unsupported attribution; Critical omissions; Abstention calibration; Investigation cost.

**Would count against it:** Casefiles improve apparent completeness but not correctness, or missing-data labels fail to reduce unsupported assertions.

**Main confounds:** Synthetic ground truth is limited to recorded interventions and events; the hidden record does not reveal internal intentions. This is an agent-evaluation precursor, not a human-usability study.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Define an answer key with deliberately unanswerable questions and a realistic missingness process.

**Closest prior and evidence limits:**

- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Existing failure taxonomy supplies annotation categories, not causal proof. Catalogue depth: full.
- [[gh-yazandabain-swarmtrace]] — [SwarmTrace: temporal audit of resource targeting in the DseWiki incident (24-hour degree ranking misses all 18 recent multi-writer resources)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-yazandabain-swarmtrace.md). Existing temporal reconstruction tool requires a concrete increment beyond another graph. Catalogue depth: skim.

**Related team work:** [casefile](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/casefile.md), [telephone](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/telephone.md).

<a id="soc-33"></a>
### SOC-33 — Predict unseen agents' choices from one agent

**Update 2:** unchanged.

**Question:** How far does a benign choice model learned from one agent transfer across roles and model families?

**Candidate hypothesis:** A choice predictor transfers within a shared model and task rubric better than across roles, and adds little beyond a generic task-feature baseline after role changes.

**How to test:** Split synthetic project-allocation tasks into profiling and sealed evaluation sets. Observe one agents choices, freeze a simple predictor, then randomize fresh team episodes to homogeneous or mixed models and stable or changed roles. Keep profiling-query budget fixed and separately charge it to end-to-end cost. Predict pre-discussion individual choices and final group choices without manipulating content.

**Comparison:** Generic task-feature prediction, the stated rubric alone and a predictor fitted to a randomly chosen different agent.

**Measurements:** Held-out choice accuracy; Calibration; Individual-to-group transfer gap; Queries per improvement.

**Would count against it:** Profiling supplies no incremental predictive value or transfers equally well across all role and model changes.

**Main confounds:** Good prediction does not identify internal utility. Task preference stability and training/test leakage must be measured; rationales are supplementary observations, not the target variable.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Freeze task families and a simple predictor before evaluation; keep this lane benign and separate from attack development.

**Closest prior and evidence limits:**

- [[kim-2021-reward]] — [Reward Identification in Inverse Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2021-reward.md). Formal identifiability limits prevent equating prediction with recovered rewards. Catalogue depth: full.
- [[liu-2025-can]] — [Can an Individual Manipulate the Collective Decisions of Multi-Agents?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-can.md). One-known-agent collective influence is close prior, but uses optimized adversarial inputs. Catalogue depth: full.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [agent-swarm-influence-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/agent-swarm-influence-research.md).

<a id="soc-34"></a>
### SOC-34 — Separate wording convergence from changed decisions

**Update 2:** revised.

**Question:** Does a group that starts using the same wording also make the same substantive choices?

**Candidate hypothesis:** Visible examples increase lexical similarity more reliably than they change independently scored beliefs or actions.

**How to test:** Randomize complete synthetic discussion episodes to shared phrasing examples, semantically equivalent varied examples or no examples. Keep facts, source count, displayed length and total reasoning budget equal. Counterbalance starting choices and measure selections privately before and after communication, plus subsequent actions in an exact-score task.

**Comparison:** Independent agents exposed to the same examples without peer messages and a wording-shuffled placebo.

**Measurements:** Lexical similarity; Choice convergence; Accuracy; Action convergence; Common-exposure contrast.

**Would count against it:** Wording convergence consistently predicts changed choices after initial beliefs and common exposure are controlled, contradicting the proposed dissociation.

**Main confounds:** Lexical measures can track topic rather than copying; no inference about beliefs should rest on phrasing alone. Whole episodes are randomized because communication creates interference within teams.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit the feed experiment, retain objective action scores, and separate message exposure from ranking before claiming a mechanism.

**Closest prior and evidence limits:**

- [[de-marzo-2026-copying]] — [Copying explains the collective behavior of AI agents in the wild](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/de-marzo-2026-copying.md). One observational episode supports visible convention and wording copying, not universal belief contagion. Catalogue depth: skim.
- [[li-2026-socialization]] — [Does Socialization Emerge in AI Agent Society? A Case Study of Moltbook](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-socialization.md). Moltbook counterevidence motivates separating semantic stability from mutual influence. Catalogue depth: skim.
- [[usman-2026-peer-voted]] — [Peer-Voted LLM-Agent Stress Tests Find Feed-Induced Lexical Convergence but No Reliable Matched-Exposure Advantage for Distributed Sources](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/usman-2026-peer-voted.md). Direct matched-exposure lexical-convergence precedent; its feed treatment bundles exposure and ranking. Catalogue depth: abstract.

**Related team work:** [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [telephone](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/telephone.md), [agent-swarm-influence-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/agent-swarm-influence-research.md).

<a id="soc-35"></a>
### SOC-35 — Validate a cheap surrogate at the collective level

**Update 2:** unchanged.

**Question:** Can a model of individual updates reproduce group-level outcomes on new questions and network structures?

**Candidate hypothesis:** At equal calibration cost, a surrogate including claim-specific priors and observed history improves collective forecasts within the calibration distribution, but its advantage shrinks on new question families or topologies.

**How to test:** Create independent small-population episodes with randomized starting conditions and network topology. Split by question family and topology before fitting a surrogate. Compare one-step, history-aware and simple copying models under an equal calibration-call budget. Reserve real LLM episodes for a held-out collective forecast test; report offline sweep savings only after fidelity is checked.

**Comparison:** Persistence, majority copying and a prior-only predictor, all given the same observable history.

**Measurements:** One-step prediction; End-state distribution error; Calibration of consensus probability; Compute saved at fixed forecast error.

**Would count against it:** The history-and-prior model fails to improve collective forecasts over simpler models given the same observed rounds and budget, or its advantage does not shrink under the prespecified transfer shifts.

**Main confounds:** Future trajectory leakage, reused statements and fitted claim priors can make forecasts look transferable. Single runs at large population are not replicated evidence.

**Framing / first-test class:** replication / api-small.

**Before promotion:** Read surrogate validation methods and freeze a family-disjoint split with available-observation limits.

**Closest prior and evidence limits:**

- [[itkin-2026-local]] — [Local Predictability and Collective Fidelity in LLM-Agent Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/itkin-2026-local.md). Direct prior reports transfer limits and unconfirmed earlier history effects. Catalogue depth: skim.
- [[fukushima-2026-message]] — [Message capacity and claim wording set the transition points of collective truth-finding in language-model networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fukushima-2026-message.md). Claim-dependent fields show why microscopic weights alone may fail collectively. Catalogue depth: abstract.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md).

<a id="soc-36"></a>
### SOC-36 — Rank trace clusters by useful evidence, not spectacle

**Update 2:** unchanged.

**Question:** Can a transparent triage rule retrieve useful coordination cases across different scaffolds?

**Candidate hypothesis:** Features tied to verifiable shared artifacts transfer better than repeated phrasing or temporal coincidence, but performance falls when access logs are absent.

**How to test:** Generate independent benign multi-agent and ordinary automation episodes across synthetic scaffolds with known communication channels. Hold out an entire scaffold and task family. Cross intact versus missing access logs using prespecified masks. Freeze ranking on development data, then give investigator agents equal review-token budgets for ranked, random or keyword-selected clusters. Score evidence-supported answers, not real-operator claims.

**Comparison:** Random review, simple keyword filtering and an artifact-only heuristic with the same inspection allowance.

**Measurements:** Precision at fixed review budget; Coverage of coordination cases; False positives; Supported conclusions.

**Would count against it:** The ranking does not transfer to the held-out scaffold or performs no better than keywords once review cost is included.

**Main confounds:** Synthetic labels establish coordination in the testbed, not wild AI authorship, shared operator or harmful intent. Related traces from one episode must remain in one split.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Define scaffold-disjoint data generation and reviewable coordination labels; a real-archive extension needs licensed redacted data.

**Closest prior and evidence limits:**

- [[gh-yazandabain-swarmtrace]] — [SwarmTrace: temporal audit of resource targeting in the DseWiki incident (24-hour degree ranking misses all 18 recent multi-writer resources)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-yazandabain-swarmtrace.md). Existing temporal tooling illustrates why current and historical activity differ. Catalogue depth: skim.
- [[cemri-2025-why]] — [Why Do Multi-Agent LLM Systems Fail?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cemri-2025-why.md). Trace annotation precedent supports explicit evidence categories rather than automatic intent labels. Catalogue depth: full.

**Related team work:** [discovery](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/discovery.md), [casefile](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/casefile.md).

<a id="soc-37"></a>
### SOC-37 — Does profiling improve influence through ordinary retrieval?

**Update 2:** revised.

**Question:** Does tailoring a bounded external document from one agents observed choices shift an unseen groups decisions more than generic framing?

**Candidate hypothesis:** Tailoring produces greater held-out target-choice lift than generic framing, with a larger incremental effect when peer communication is enabled.

**How to test:** Profile one agent on separate fictional project-choice tasks, then freeze tailoring. Randomize independent group episodes to neutral, generic or tailored fact-preserving documents, crossed with peer communication. Publish one bounded document in a local corpus reached through ordinary retrieval; never force delivery. Match length, tuning-query budget, information opportunities and total inference. Lock private choices and retrieved evidence before peer exchange in every arm. Log retrieval rank, access and final decisions.

**Comparison:** Generic framing with equal tuning budget, neutral documents, and matched no-communication episodes.

**Measurements:** End-to-end target-choice lift; Retrieval-conditional lift; Independent task utility; Peer-channel interaction; Profiling cost.

**Would count against it:** Tailoring adds no held-out lift over generic framing, or enabling communication does not amplify its incremental effect.

**Main confounds:** Better substantive options are not manipulation; report utility separately. Common retrieval is not peer transmission, and channel assignment alone does not identify mediation.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Seal profiling/evaluation tasks and define a fact-preserving rewrite rubric; synthetic content only, no real outreach.

**Closest prior and evidence limits:**

- [[nestaas-2024-adversarial]] — [Adversarial Search Engine Optimization for Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/nestaas-2024-adversarial.md). External-content choice influence is established; retrieval access assumptions matter. Catalogue depth: full.
- [[liu-2025-can]] — [Can an Individual Manipulate the Collective Decisions of Multi-Agents?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-can.md). One-known-agent influence precedent uses optimized adversarial inputs, not this framing. Catalogue depth: full.

**Related team work:** [agent-swarm-influence-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/agent-swarm-influence-research.md), [experimental-design](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/seo-poisoning/experimental-design.md).

<a id="soc-38"></a>
### SOC-38 — Select complementary teams on a separate task set

**Update 2:** new.

**Question:** Does observed error complementarity select better teams than family diversity once member capability and selection cost are matched?

**Candidate hypothesis:** A capability-controlled complementarity selector improves held-out team accuracy over family-balanced selection within a domain, but its advantage shrinks after a task-family shift.

**How to test:** Use disjoint calibration and evaluation task families. Freeze equal-size team selectors based on individual accuracy, family balance, or residual co-failure after capability adjustment. Randomize which selector is used for independent evaluation task blocks, with a fixed model pool and aggregate inference/tool budget. Charge profiling cost amortized over a prespecified workload; report a cold-start comparison too. Model subsets sharing outputs are paired comparisons, not independent replications.

**Comparison:** The strongest member chosen on calibration data, random capability-matched teams and accuracy-only team selection.

**Measurements:** Held-out gain over best member; Rescue and damage rates; Shifted-domain gain; Profiling cost; Selection stability.

**Would count against it:** Complementarity-based selection fails to beat capability-matched family balance, or its proposed transfer penalty is absent under the specified task shift.

**Main confounds:** Diversity proxies can encode weak models rather than useful differences. Selecting the best member on test outcomes or counting overlapping subsets independently inflates results.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Read selector methods and freeze calibration size, deployment workload and held-out family shift before estimating improvement.

**Closest prior and evidence limits:**

- [[kim-2026-are]] — [Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2026-are.md). Direct capability-confounding audit; does not establish this transfer outcome. Catalogue depth: abstract.
- [[teng-2026-which]] — [Which Models Work Well Together? Measuring Heterogeneity for LLM Team Selection](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/teng-2026-which.md). Team profiling and complementarity selection are existing methods. Catalogue depth: abstract.
- [[ali-2026-quantifying]] — [Quantifying Diversity of Thought: A Predictive Law of Weighted LLM Ensemble Lift](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ali-2026-quantifying.md). Rescue/damage decomposition supplies a more informative endpoint than disagreement alone. Catalogue depth: abstract.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-39"></a>
### SOC-39 — The same average correlation can hide different failures

**Update 2:** new.

**Question:** Do panels with equal average accuracy and pairwise correlation need different aggregation rules when their shared-error pattern differs?

**Candidate hypothesis:** Error structures concentrated in a subgroup favor dependence-aware weighting more than errors shared across the whole panel, despite matched mean correlation.

**How to test:** First generate independent synthetic panel-response banks with matched member accuracy and average error correlation but different higher-order co-failure patterns. Freeze unweighted, subgroup-weighted and scalar-effective-size rules using separate calibration banks; compare on untouched banks. Then test the diagnostic on held-out exact-answer LLM task blocks without forcing the result. Hold votes, available labels and decision-compute cap fixed. Whole banks or independent task blocks are units, not voter pairs.

**Comparison:** Majority vote, calibrated best-member selection and a predictor using only mean accuracy plus average correlation.

**Measurements:** Aggregation error; Calibration of consensus confidence; All-wrong frequency; One-vote-margin errors; Weight stability.

**Would count against it:** The pattern-aware rule has no incremental predictive or decision value once matched mean accuracy and correlation are supplied.

**Main confounds:** Artificial covariance targets must correspond to feasible joint distributions. Replay shows a measurement limitation, not a causal account of how real models acquired shared errors.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Construct feasible matched error banks and obtain reusable task-level votes; verify exact scoring before any empirical transfer claim.

**Closest prior and evidence limits:**

- [[hossain-2026-agreement]] — [Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hossain-2026-agreement.md). Direct prior says co-error pattern matters beyond average correlation. Catalogue depth: abstract.
- [[shu-2026-blind]] — [Blind to the Pivotal Vote: Aggregate Independence Metrics Miss Where Verification Actually Helps](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shu-2026-blind.md). Pivotal-vote verification gains can be invisible to aggregate effective-size metrics. Catalogue depth: abstract.

**Related team work:** [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md), [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md).

<a id="soc-40"></a>
### SOC-40 — Keep small deliberating groups independent until the end

**Update 2:** new.

**Question:** Does isolating small discussion groups preserve more useful correction than one fully connected discussion?

**Candidate hypothesis:** Small isolated groups followed by answer-only fusion outperform full-group discussion for heterogeneous workers, with little benefit for model clones.

**How to test:** Randomize complete task episodes to one discussion group, several isolated subgroups with final answer-only fusion, or independent answers. Cross clone and capability-matched mixed-model teams. Hold worker count, fact union, initial private reasoning and aggregate token/tool cap fixed; charge final fusion and discussion. Randomize subgroup membership before evidence assignment and block on task world. Score a designated final answer with an objective validator.

**Comparison:** Independent voting and a single solver with the same total budget; include separated actor-critic pairs as an established architectural comparator.

**Measurements:** Final accuracy; Correct-to-wrong revisions; Cross-group error dependence; Useful evidence retained; Communication cost.

**Would count against it:** Isolation does not improve heterogeneous-team accuracy relative to full discussion, or equal gains appear for clones despite the predicted interaction.

**Main confounds:** Partitioning can change who sees essential evidence; balance evidence access separately from communication. Extra fusion computation or unequal first-pass work would obscure the cause.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit group-size and compute matching in both priors; choose tasks needing integration without making subgroup isolation impossible.

**Closest prior and evidence limits:**

- [[barrera-lemarchand-2026-wisdom]] — [The Wisdom of Artificial Deliberative Crowds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/barrera-lemarchand-2026-wisdom.md). Direct small-group deliberation precedent with clone-group counterevidence. Catalogue depth: abstract.
- [[ren-2026-sepal]] — [SEPAL: Separated Expert Pairs with Answer-Level Fusion for Reliable LLM Collaboration](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ren-2026-sepal.md). Separated expert pairs with late fusion are existing prior, not a new architecture. Catalogue depth: abstract.

**Related team work:** [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md).

<a id="soc-41"></a>
### SOC-41 — Diverse interpretations versus diverse personas

**Update 2:** new.

**Question:** Can alternative valid interpretations of a question create useful answer diversity more reliably than assigning personality profiles?

**Candidate hypothesis:** Truth-preserving question reframing increases correct-answer coverage and final accuracy more than equally long persona variation at fixed model and evidence.

**How to test:** Randomize independent exact-answer task episodes to repeated neutral prompts, distinct benign personas, or verified equivalent problem framings. Use one model initially, with a capability-matched mixed-model sensitivity arm. Hold facts, sample count and total generation tokens fixed; charge generation or validation of framings to the comparison. Freeze prompt generators on separate task families. Aggregate with the same rule and track both coverage and selected-answer correctness.

**Comparison:** Repeated sampling with identical prompts and length-matched neutral context; model-family variation is a separate comparator.

**Measurements:** Correct answer present; Selected-answer accuracy; Shared wrong answers; Framing validity; Added prompt cost.

**Would count against it:** Reframing fails to improve accuracy beyond persona variation and neutral prompting, or apparent gains require adding facts or changing the question.

**Main confounds:** Semantic distance does not prove reasoning diversity. A persona can change goals, and an invalid paraphrase can change the correct answer; audit both before evaluation.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Create independently validated equivalent framings and a fixed persona set; preserve the task objective in every arm.

**Closest prior and evidence limits:**

- [[rosales-2025-diverse]] — [Diverse LLMs or Diverse Question Interpretations? That is the Ensembling Question](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rosales-2025-diverse.md). Direct comparison of question-interpretation and model diversity. Catalogue depth: abstract.
- [[qian-2026-nous]] — [Nous: An Attempt to Extract and Inject the Cognition Behind Prediction-Market Behavior](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/qian-2026-nous.md). Prompted behavioral profiles failed to transfer useful forecast diversity in the reported setting. Catalogue depth: abstract.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-42"></a>
### SOC-42 — More correct candidates or a better final selector?

**Update 2:** new.

**Question:** When additional sampling stops improving accuracy, is the bottleneck generating a correct answer or choosing one?

**Candidate hypothesis:** After correct-answer coverage saturates, shifting a fixed budget from extra samples to evidence-based selection improves final accuracy more than continued voting.

**How to test:** Randomize complete exact-answer task episodes to different generation/selection budget splits while keeping aggregate tokens and tool credits fixed. Compare majority voting with a selector allowed a charged objective evidence check. Both selectors see the same candidate format and have identical initial evidence access. Use independent task families, freeze split ratios in advance, and evaluate every episode including those with no correct candidate. Track hidden oracle coverage only for diagnosis.

**Comparison:** More samples plus vote, best single solver and the oracle that selects a correct candidate whenever one exists, explicitly unavailable to deployment.

**Measurements:** Correct-candidate coverage; Selection success conditional on coverage; Final accuracy; Selector-induced damage; Total cost.

**Would count against it:** Spending on selection does not improve final accuracy once coverage plateaus, or its gains disappear after charging evidence checks.

**Main confounds:** An oracle gap is opportunity, not an attainable gain. Conditional selection scores need their coverage denominator; shared cached candidates do not create independent trials.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Choose an affordable verifiable evidence check and inspect selector baselines; define plateau operationally using separate development data.

**Closest prior and evidence limits:**

- [[bay-2026-when]] — [When More Sampling Hurts: The Modal Ceiling and Correlation Ceiling of Test-Time Scaling](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bay-2026-when.md). Separates sampling coverage from modal selection and correlation ceilings. Catalogue depth: abstract.
- [[liu-2026-llms]] — [LLMs as a Jury: Cross-Model Consensus Can Outperform Process Reward Models for LLM Reasoning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-llms.md). Cross-model answer selection is existing prior with task-specific claims. Catalogue depth: abstract.

**Related team work:** [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-43"></a>
### SOC-43 — Abstain when confidence is high but errors are shared

**Update 2:** new.

**Question:** Does a calibrated confidence gate still improve collective decisions when high-confidence failures are correlated?

**Candidate hypothesis:** Confidence-only abstention improves selective accuracy under weak dependence but loses its advantage when shared confident mistakes dominate; a dependence-risk gate recovers accuracy at matched coverage.

**How to test:** Randomize independent task blocks to always-vote, calibrated confidence gating or gating augmented with a fixed dependence-risk diagnostic. Calibrate thresholds on separate labelled blocks and compare at matched answer coverage. Cross ordinary exact-answer worlds with generated shared-misconception worlds, keeping individual evidence, team size and total inference/tool cap fixed. Count abstentions as unserved tasks in total utility; do not report only accepted answers.

**Comparison:** Random abstention at equal coverage, calibrated single-model abstention and unanimous high-confidence acceptance.

**Measurements:** Selective error at fixed coverage; Total correctly served tasks; Wrong unanimous accepts; Calibration error; Diagnostic cost.

**Would count against it:** Confidence-only gating retains the same advantage under shared confident errors, or the dependence diagnostic provides no incremental benefit after charging its cost.

**Main confounds:** Lower coverage can manufacture apparent reliability. A theorem for independent calibrated voters does not establish guarantees for dependent LLM outputs or uncertain task labels.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit theorem assumptions and freeze practical error/coverage targets before choosing thresholds or a diagnostic.

**Closest prior and evidence limits:**

- [[karge-2026-epistemic]] — [Epistemic Filtering and Collective Hallucination: A Jury Theorem for Confidence-Calibrated Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/karge-2026-epistemic.md). Confidence-gated jury theory motivates a boundary test of its independence and calibration assumptions. Catalogue depth: abstract.
- [[kota-2026-design]] — [Design and Evaluation of Multi-Agent AI Oracle Systems for Prediction Market Resolution](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kota-2026-design.md). High-confidence consensus and independent aggregation have direct task-specific precedent. Catalogue depth: abstract.
- [[zhou-2026-juryprobe]] — [JuryProbe: An Empirical Consensus-Risk Diagnostic for Routing Reference-Free Factuality Judge Panels to Grounded Verification](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2026-juryprobe.md). Dependence-risk routing is existing prior; exact tasks and charged diagnosis are the transfer question. Catalogue depth: abstract.

**Related team work:** [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md), [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-44"></a>
### SOC-44 — Preference optimization and shared mistakes beyond familiar QA

**Update 2:** new.

**Question:** Does the error-correlation increase seen after preference optimization persist on newly generated distributed-evidence tasks?

**Candidate hypothesis:** Matched SFT-to-DPO checkpoint transitions increase shared errors more on familiar misconception questions than on novel tasks whose necessary facts are fully supplied.

**How to test:** Evaluate paired released SFT and derived DPO checkpoints on independent task blocks crossing misconception-style QA with newly generated evidence tasks. Within each block randomize prompt variants and decoding seeds, match team size and aggregate generation budget, and measure standalone capability alongside collective outputs. Use multiple genuinely matched checkpoint lineages; uncertainty generalizes over tasks within each lineage, not arbitrary sampled agents. Keep voting and fixed-rule market aggregation separately labelled.

**Comparison:** SFT-only teams, single-checkpoint solvers, and mixed-checkpoint teams under the same resource cap.

**Measurements:** Change in shared errors; Individual accuracy; Ensemble gain; Answer concentration; Task-family interaction.

**Would count against it:** The predicted smaller DPO-associated increase on newly supplied-evidence tasks is absent, or checkpoint differences vanish after the prespecified capability adjustment.

**Main confounds:** Checkpoint comparisons isolate a recorded pipeline step only when provenance matches; they do not establish that alignment generally harms cooperation. Near-chance baselines can distort correlation.

**Framing / first-test class:** boundary-test / hardware.

**Before promotion:** Verify checkpoint lineage, licenses and feasible local inference; audit the prior's controls without assuming all alignment stages are equivalent.

**Closest prior and evidence limits:**

- [[begin-2026-preference]] — [Preference Optimization Drives Monoculture in LLM Prediction Markets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/begin-2026-preference.md). Direct matched-checkpoint market prior; task and aggregation transfer remains to be checked. Catalogue depth: skim.
- [[kim-2026-are]] — [Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2026-are.md). Capability confounding requires joint reporting of skill and dependence. Catalogue depth: abstract.

**Related team work:** [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md), [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md).

<a id="soc-45"></a>
### SOC-45 — Does local memory preserve a convention after pressure ends?

**Update 2:** new.

**Question:** Does a convention calibrated as metastable under whole-population observation remain persistent under local encounters and bounded memory?

**Candidate hypothesis:** Under local encounters, bounded memory prolongs post-pressure convention persistence, especially for pairs near the stability boundary calibrated under whole-population observation.

**How to test:** Calibrate response curves on separate benign fictional convention pairs and classify proximity to the mean-field spinodal boundary before evaluation. Randomize independent populations to local/full observation crossed with no history/bounded history. Apply the same temporary scripted convention pressure and remove it on a fixed schedule; include no-pressure controls. Match population, update opportunities and total inference allowance, charging history tokens. Report recovery over a fixed horizon, not claims of infinite irreversibility.

**Comparison:** The calibrated memoryless full-observation model and convention pairs outside its metastable region.

**Measurements:** Post-removal convention persistence; Recovery time; Boundary forecast error; Hysteresis over fixed cycles; Memory cost.

**Would count against it:** Bounded memory does not prolong post-pressure persistence under local encounters, or the predicted larger effect near the calibrated boundary is absent on held-out pairs.

**Main confounds:** The bias-preferred convention is not objective truth. Pair selection after observing persistence would leak outcomes; scripted pressure is introduced, not spontaneous behavior.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit both protocols and freeze memory length, boundary bands and a finite-horizon persistence endpoint before evaluation; calibration pairs stay separate.

**Closest prior and evidence limits:**

- [[de-marzo-2026-conformity]] — [Conformity Generates Collective Misalignment in AI Agents Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/de-marzo-2026-conformity.md). Direct prior already predicts both persistence and relaxation by regime. Catalogue depth: full.
- [[magistrali-2026-aligned]] — [Aligned Alone, Misaligned Together: Forecasting Adversarial Capture in LLM Agent Populations](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/magistrali-2026-aligned.md). Local bounded-memory recovery was measured in a single-stable-state regime, not a general reversibility theorem. Catalogue depth: full.
- [[hishiki-2026-how]] — [How memory can affect collective and cooperative behaviors in an LLM-Based Social Particle Swarm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hishiki-2026-how.md). Memory alters regimes in an adjacent spatial game; no equivalence is assumed. Catalogue depth: abstract.

**Related team work:** [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md), [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md), [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md).

<a id="mkt-01"></a>
### MKT-01 — Market division when output needs sunk capacity

**Update 2:** new.

**Question:** Does the tacit market division seen in a bare two-good Cournot game survive, strengthen or vanish when each firm must build and pay for production capacity before it can sell?

**Candidate hypothesis:** Sunk capacity makes division more stable: firms specialise as often as in the bare game, specialise earlier in build choices than in quantities, and re-enter a market even less often because re-entry costs machines.

**How to test:** Run the same two-firm, two-good market twice: as Lin et al.'s bare quantity game, and inside the factory world with identical demand curves and variable costs, where quantities are capped by machines the firm has built. Match model, temperature, horizon (unknown to agents), memory format and seeds. Score each run once on final-quarter HHI per good and the round at which each firm's build mix becomes specialised.

**Comparison:** Bare Cournot game with the same demand and costs; scripted Cournot-Nash firms in the factory world.

**Measurements:** HHI per good, final quarter; Round of build specialisation vs round of quantity specialisation; Re-entry events and capacity scrapped; Consumer surplus vs Cournot-Nash.

**Would count against it:** Division rates in the factory world are no higher than in the bare game and specialisation does not appear in builds before quantities.

**Main confounds:** The factory prompt is longer and the action space larger, which can lower competence rather than change incentives. Capacity limits can force specialisation mechanically if starting cash cannot fund both lines; set starting cash so both lines are affordable.

**Framing / first-test class:** replication / api-small.

**Before promotion:** Pick the simulator (own Python world or FLE layer) and fix demand, cost and starting-cash values from a scripted-agent pilot.

**Closest prior and evidence limits:**

- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Source result: division in a bare two-good Cournot game without communication. Catalogue depth: full.
- [[bracale-syrnikov-2026-institutional]] — [Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bracale-syrnikov-2026-institutional.md). Replication with capacity constraints but no build decisions or production chain. Catalogue depth: skim.
- [[deshpande-2026-strategic]] — [Strategic AI in Cournot Markets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/deshpande-2026-strategic.md). Adds cost-reducing investment to Cournot; prices up to 200% of Nash in LLM-LLM markets. Not market division across goods. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-02"></a>
### MKT-02 — Firms per good and the collapse of division

**Update 2:** new.

**Question:** How does tacit division change as the number of firms rises relative to the number of goods?

**Candidate hypothesis:** Division holds while firms do not outnumber goods and breaks toward Cournot-Nash quantities once they do, because a clean one-firm-per-good split no longer exists.

**How to test:** Factorial over firms N in {2,3,4,6} and goods M in {2,3}, same per-good demand scaled so the monopoly quantity per good is constant. Same model across firms. Score run-level mean HHI and profit gap fraction.

**Comparison:** Scripted Cournot-Nash firms at each N and M; the N=2, M=2 cell as the Lin et al. reference.

**Measurements:** Mean HHI across goods; Profit as fraction of Nash-to-monopoly gap; Share of runs with a stable one-firm-per-good split.

**Would count against it:** Division or supra-competitive profit persists at N > M at rates similar to N <= M.

**Main confounds:** More firms means longer prompts and more history per round; hold history length fixed in tokens. Run cost grows with N; budget seeds per cell from a pilot.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** A pilot to size seeds per cell; decide whether M > 3 is worth the extra recipes.

**Closest prior and evidence limits:**

- [[keppo-2026-fragility]] — [On the Fragility of AI Agent Collusion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/keppo-2026-fragility.md). Pricing game: three sellers can collude, four unstable, five never reach sustained collusion. Catalogue depth: skim.
- [[tolety-2025-tacit]] — [Tacit Bidder-Side Collusion: Artificial Intelligence in Dynamic Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tolety-2025-tacit.md). Dutch-auction bidders collude only when few. Catalogue depth: abstract.
- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Only N = M = 2 tested. Catalogue depth: full.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-06"></a>
### MKT-06 — No channel, public channel, private channel

**Update 2:** new.

**Question:** How does the communication channel (none, one public board, private pairwise messages) change division, price level and explicit price-fixing in a production market?

**Candidate hypothesis:** Any channel raises supra-competitive profit; private messages raise explicit carve-up proposals most, while a public board yields similar division with fewer explicit proposals.

**How to test:** Three-arm comparison at N = 3, M = 3, same model, matched message budget per round. Score run-level profit gap, HHI and the rate of explicit coordination proposals coded by a blind judge.

**Comparison:** No-channel arm.

**Measurements:** Profit gap fraction; HHI per good; Explicit coordination proposals per run.

**Would count against it:** Profit gap and HHI do not differ between arms.

**Main confounds:** Messages consume context; pad the no-channel arm with neutral text of matched length.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Message budget and judge rubric fixed before runs.

**Closest prior and evidence limits:**

- [[agrawal-2025-evaluating]] — [Evaluating LLM Agent Collusion in Double Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/agrawal-2025-evaluating.md). Double auctions: seller communication raises collusion. Catalogue depth: skim.
- [[li-2026-emergent]] — [Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-emergent.md). Private emails among firms; 12.6% misaligned including price-fixing. Catalogue depth: skim.
- [[fish-2024-algorithmic]] — [Algorithmic Collusion by Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fish-2024-algorithmic.md). Price collusion in Bertrand without a channel. Catalogue depth: abstract.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-08"></a>
### MKT-08 — Mixed models as a natural brake

**Update 2:** new.

**Question:** Do markets with firms from different model families divide less than same-model markets?

**Candidate hypothesis:** Mixed-family markets divide less and sit closer to Cournot-Nash, but the effect is smaller than the effect of adding a firm.

**How to test:** N = 3 firms; arms: all one family, two plus one, three families. Rotate families across positions. Score run-level HHI and profit gap.

**Comparison:** Same-family markets for each family used.

**Measurements:** HHI per good; Profit gap fraction; Rounds to division.

**Would count against it:** Mixed markets divide as often as same-family ones.

**Main confounds:** Families differ in competence; a weak firm can look competitive simply by mistake. Report each firm's best-response error against scripted rivals.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Decide which families are affordable at the needed run count.

**Closest prior and evidence limits:**

- [[keppo-2026-fragility]] — [On the Fragility of AI Agent Collusion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/keppo-2026-fragility.md). Heterogeneity in patience or data cuts the collusive price lift from 22% to 7-10%. Catalogue depth: skim.
- [[agrawal-2025-evaluating]] — [Evaluating LLM Agent Collusion in Double Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/agrawal-2025-evaluating.md). Mixing models in auctions does not reliably reduce collusion. Catalogue depth: skim.
- [[bracale-syrnikov-2026-institutional]] — [Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bracale-syrnikov-2026-institutional.md). Includes cross-provider duopolies. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-10"></a>
### MKT-10 — One competitive entrant

**Update 2:** new.

**Question:** Does a single scripted competitive firm entering mid-game break an established division?

**Candidate hypothesis:** A best-response entrant breaks division in the good it enters and pushes incumbents toward Cournot quantities there, but incumbents keep their split in other goods.

**How to test:** After division forms, add a scripted Cournot best-response firm (or a provably non-colluding learner) in one good. Compare with adding an LLM firm of the same model.

**Comparison:** No entrant; LLM entrant.

**Measurements:** HHI in entered vs other goods; Incumbent profit before and after; Rounds until a new division forms.

**Would count against it:** Division in the entered good survives the scripted entrant.

**Main confounds:** Entry adds capacity and lowers prices mechanically; compare against the Cournot prediction with N+1 firms.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Decide entry timing rule (fixed round vs after division is detected).

**Closest prior and evidence limits:**

- [[collina-2025-breaking]] — [Breaking Algorithmic Collusion in Human-AI Ecosystems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/collina-2025-breaking.md). Theory: one defector can break collusion. Catalogue depth: abstract.
- [[garra-2026-mitigating]] — [Mitigating Emergent Collusion in LLM Pricing Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/garra-2026-mitigating.md). Adding an entrant works better than a prompt warning in an LLM pricing replication. Catalogue depth: abstract.
- [[nisan-2026-domination-avoiding]] — [Domination-Avoiding Learning Agents Cannot Collude](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/nisan-2026-domination-avoiding.md). A class of learners that provably cannot collude; a clean control firm. Catalogue depth: abstract.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-14"></a>
### MKT-14 — Evidence royalties versus identity farming

**Update 2:** new.

**Question:** Can paying for evidence used in a joint opportunity increase useful discovery without making duplicate identities or redundant evidence more profitable?

**Candidate hypothesis:** Unreviewed hunch: In repeated private-profit worlds with costly discovery, payments tied to unique evidence actually used increase useful evidence production and producer returns relative to free reuse; payments per publisher instead reward duplicated identities and redundant claims.

**How to test:** Modify the Patchwork economy to make discovery costly and allow agents to choose whether to search and publish across repeated opportunities. Randomize whole market episodes to free public reuse, a fixed revenue share divided among all publishers, or the same share divided among unique evidence receipts used at settlement. Cross a single owner versus permitted identity splitting at matched capital, total model budget and discovery opportunities; keep evidence visibility and communication channels identical in the main comparison. Preregister how substitutes and complementary evidence share payment and how duplicate receipts are rejected. Observe endogenous discovery as well as completion, owner-level payoffs and unused contributions. A separate matched visibility control should test whether public evidence, rather than chat, carries coordination.

**Comparison:** Original free-reuse economy, publisher-count royalties, no-splitting arms and scripted policies showing each payment rule is executable; all transfers come from the same realized revenue, not added subsidy.

**Measurements:** Unique useful evidence produced per opportunity; Opportunity completion and net external surplus; Evidence-producer net returns; Principal gain from identity splitting; Redundant claims, contracts and payment concentration.

**Would count against it:** At prespecified precision, receipt-based payments do not improve discovery or producer returns, lose comparable net surplus through friction, or permit profitable identity splitting without new useful evidence.

**Main confounds:** The old nine-case pilot never tested royalties. Recorded use is not causal marginal contribution or moral entitlement; substitute and complementary evidence complicate attribution. An oracle deduplicator hides manipulation, and changing evidence visibility together with payments confounds incentives.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Specify discovery costs, payment conservation, observable evidence receipts and a non-oracle deduplication comparator; resolve Patchwork access and complete the relevant survey/review gates. Related to BUD-14, MKT-09 and SEC-14, but tests compensation for information production.

**Closest prior and evidence limits:**

- [[gh-dmarzzz-patchwork]] — [Patchwork Heist — capability-restricted agents and a private-profit economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-dmarzzz-patchwork.md). Nine economy cases used no service contracts; four of six sales were solo with freely reusable public evidence. This motivates but does not establish a property-rights mechanism. Catalogue depth: skim.
- [[piedrahita-2025-corrupted]] — [Corrupted by Reasoning: Reasoning Language Models Become Free-Riders in Public Goods Games](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/piedrahita-2025-corrupted.md). Catalogue documents model-dependent free-riding in public-goods games, a different institution from evidence production; it does not predict this treatment effect. Catalogue depth: full.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). Shows why counting identities in rewards can introduce false-name incentives; no blanket guarantee transfers to evidence royalties. Catalogue depth: full.

**Related team work:** [patchwork-addendum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/question-atlas/patchwork-addendum.md).

<a id="crowds-and-traffic"></a>
## Human crowds and traffic

<a id="phy-31"></a>
### PHY-31 — Anticipation versus slower walking

**Update 2:** unchanged.

**Question:** Can the collective effect of a distracted walker be separated from reduced speed and altered gait?

**Candidate hypothesis:** Removing mutual anticipation will disrupt lane formation beyond the effect of simply reducing preferred speed, particularly near the front of counterflow groups.

**How to test:** In a pedestrian simulator, randomize whole corridor episodes to a subset with reduced anticipation, reduced speed, both changes or sham changes. Match the affected fraction and positions across paired episodes, then test unseen inflow patterns. Use empirical trajectories only for external plausibility checks, not as randomized evidence.

**Comparison:** A speed-only intervention and a time-to-collision controller with intact mutual information are key comparators.

**Measurements:** Lane-formation time; Throughput; Abrupt avoidance events; Near-collision count; Travel-time inequality.

**Would count against it:** Reduced speed alone reproduces the full collective disruption, or anticipation changes have no additional effect at matched encounter rates.

**Main confounds:** A simulator can encode the conclusion through its collision rule. Include at least two model families; phone use changes attention, gait and intention simultaneously. No live crowd or distraction experiment is proposed here.

**Framing / first-test class:** extension / offline.

**Before promotion:** Obtain original intervention details and choose models where speed and anticipation can be independently manipulated.

**Closest prior and evidence limits:**

- [[murakami-2021-mutual]] — [Mutual anticipation can contribute to self-organization in human crowds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/murakami-2021-mutual.md). Closest controlled human evidence motivates the mechanism separation. Catalogue depth: skim.
- [[karamouzas-2014-universal]] — [Universal Power Law Governing Pedestrian Interactions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/karamouzas-2014-universal.md). Time-to-collision interaction model supplies an anticipatory alternative. Catalogue depth: full.
- [[moussaid-2011-simple]] — [How simple rules determine pedestrian behavior and crowd disasters](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/moussaid-2011-simple.md). Vision-based behavioural model gives a contrasting implementation. Catalogue depth: full.

<a id="phy-32"></a>
### PHY-32 — Avoiding congestion without hiding the queue

**Update 2:** unchanged.

**Question:** Does local admission control improve total throughput, or merely move waiting outside the measured corridor?

**Candidate hypothesis:** For bursty arrivals within service capacity, occupancy-based admission will reduce total arrival-to-exit delay versus fixed-rate throttling while preserving completed trip count.

**How to test:** Randomize independent synthetic corridor episodes to unrestricted entry, local occupancy-based admission or matched inflow throttling. Hold arrival demand and corridor geometry fixed and include all queued agents from arrival to exit. Evaluate transient demand spikes and long-run flow separately; analyse episode totals, not only pedestrians who successfully enter.

**Comparison:** A fixed-rate entry meter and a centralized occupancy oracle separate the value of local feedback from generic throttling.

**Measurements:** Completed trips per hour; Total person-time waiting; Queue spillback; Internal speed-density curve; Unserved demand.

**Would count against it:** Occupancy feedback leaves total delay unchanged or worse than fixed throttling at matched demand, or reduces delay only by serving fewer travellers.

**Main confounds:** The ant reference does not prove human or robot safety. Contact rules, pheromone-like speed changes and route choices differ; selecting only admitted travellers produces a misleading success metric.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Verify simulator admission semantics and define the outside queue; inspect existing pedestrian and robot admission-control baselines.

**Closest prior and evidence limits:**

- [[poissonnier-2019-experimental]] — [Experimental investigation of ant traffic under crowded conditions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/poissonnier-2019-experimental.md). Closest biological traffic observation motivates inflow regulation, without proving its isolated causal contribution. Catalogue depth: full.
- [[seyfried-2009-new]] — [New Insights into Pedestrian Flow Through Bottlenecks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/seyfried-2009-new.md). Bottleneck flow depends strongly on upstream density. Catalogue depth: full.
- [[gh-pedestriandynamics-jupedsim]] — [JuPedSim: Jülich pedestrian dynamics simulator (collision-free speed and social-force style models, Python API)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-pedestriandynamics-jupedsim.md). Candidate pedestrian simulator; no execution or model suitability validation in this pass. Catalogue depth: skim.

<a id="phy-33"></a>
### PHY-33 — Does one smoothing vehicle help beyond a ring?

**Update 2:** unchanged.

**Question:** How much of minority-controller traffic smoothing survives open boundaries and disruptive merging?

**Candidate hypothesis:** A small controlled minority will still reduce speed variance, but throughput benefits will shrink when incoming traffic repeatedly occupies the gaps used for smoothing.

**How to test:** First reproduce a synthetic single-lane ring with the documented controller. Then randomize independently seeded open-road episodes to controller presence and controlled merge disturbances, with matched demand and vehicle mix. Hold driver parameters fixed across paired conditions; compare entire road-episode metrics including upstream queues.

**Comparison:** Human-like following, constant-speed control and the same controller on the ring are comparators; a no-merge open road isolates boundary effects.

**Measurements:** Speed variance; Completed trips; Braking events; Total delay; Merge-induced disturbances.

**Would count against it:** Benefits match the ring even under the stated merging conditions, or they disappear already in the baseline replication.

**Main confounds:** Simulated driver responses are not real traffic behaviour. The ring result is established prior work; this is a boundary test, not a novel claim that a minority can smooth traffic. Fuel proxies require an explicit model.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Retrieve the exact controller and choose a validated vehicle-following model; search existing open-road follow-ups before selection.

**Closest prior and evidence limits:**

- [[stern-2018-dissipation]] — [Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/stern-2018-dissipation.md). Closest field experiment demonstrates smoothing by a single automated vehicle on a ring. Catalogue depth: full.
- [[sugiyama-2008-traffic]] — [Traffic jams without bottlenecks—experimental evidence for the physical mechanism of the formation of a jam](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/sugiyama-2008-traffic.md). Canonical spontaneous ring-road jam reference. Catalogue depth: full.

<a id="phy-34"></a>
### PHY-34 — Confinement and collective rotation

**Update 2:** unchanged.

**Question:** Can changes in confinement geometry alter collective crowd oscillations without changing local density?

**Candidate hypothesis:** In a calibrated mechanical crowd model, changing effective confinement length will alter oscillation frequency even when mean density and activity remain fixed.

**How to test:** Reproduce the published mechanical model, then randomize independent simulation episodes to arena geometries matched for area and density but varied in relevant confinement lengths. Apply identical small mechanical perturbations and compare mode structure and frequency. Treat this as a simulation intervention; no real crowd manipulation or safety deployment is proposed.

**Comparison:** An isotropic arena, a passive mechanical model and zero non-reciprocal coupling distinguish geometry from activity-driven rotation.

**Measurements:** Dominant frequency; Chiral order; Displacement amplitude; Mode localization; Boundary stress proxy.

**Would count against it:** The proposed length scaling fails across matched geometries or passive confinement alone explains the oscillation signature.

**Main confounds:** Effective length is ambiguous in irregular spaces and must be defined before fitting. The empirical anchor studied particular venues, not universal crowd thresholds. A fitted mechanical model is not a validated evacuation or early-warning system.

**Framing / first-test class:** replication / offline.

**Before promotion:** Read and reproduce source equations and available data; specify geometry-derived length without fitting it to each outcome.

**Closest prior and evidence limits:**

- [[gu-2025-emergence]] — [Emergence of collective oscillations in massive human crowds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gu-2025-emergence.md). Closest empirical and mechanical-model anchor already proposes confinement-dependent oscillation scaling. Catalogue depth: full.
- [[fruchart-2021-non]] — [Non-reciprocal phase transitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fruchart-2021-non.md). Non-reciprocal transition framework informs the mechanism. Catalogue depth: abstract.
- [[deblais-2018-boundaries]] — [Boundaries Control Collective Dynamics of Inertial Self-Propelled Robots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/deblais-2018-boundaries.md). Active-robot boundary effects offer analogy, not human validation. Catalogue depth: abstract.

<a id="phy-35"></a>
### PHY-35 — Wider crossings with more directional disorder

**Update 2:** unchanged.

**Question:** Can widening a crossing reduce efficiency when it also allows more crossing angles?

**Candidate hypothesis:** A wider passage will improve flow for fixed desired directions, but may lose that benefit if the added space creates a broader distribution of encounter angles.

**How to test:** Randomize independent simulated crowd episodes in a factorial design: width and preferred-direction dispersion vary independently, while demand, mean speed and origin-destination distances remain matched. Evaluate multiple collision-rule families and hold out angle distributions. Use the complete crossing episode as the analysis unit.

**Comparison:** Width-only changes at fixed directions and direction-only changes at fixed width separate capacity from disorder.

**Measurements:** Completed crossings; Travel time; Lane order; Near-collision events; Flow per unit width.

**Would count against it:** Width remains beneficial across all tested direction dispersions or the apparent loss is explained by longer paths rather than reduced organization.

**Main confounds:** Changing width usually changes density, path length and arrival structure at once. Physical crowd behaviour cannot be certified by a model. The known directional-order transition is prior art; the contribution would be a clean geometry-demand decomposition.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Obtain original preferred-direction definition and determine how to match demand and path length across geometries.

**Closest prior and evidence limits:**

- [[bacik-2025-order]] — [Order–disorder transition in multidirectional crowds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bacik-2025-order.md). Closest recent theory, simulation and experiment concern loss of lane order under directional heterogeneity. Catalogue depth: skim.
- [[helbing-1995-social]] — [Social force model for pedestrian dynamics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/helbing-1995-social.md). Established lane-forming simulation baseline. Catalogue depth: full.
- [[gh-pedestriandynamics-jupedsim]] — [JuPedSim: Jülich pedestrian dynamics simulator (collision-free speed and social-force style models, Python API)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-pedestriandynamics-jupedsim.md). Possible geometry-aware simulation tool; not yet run or checked for this exact model. Catalogue depth: skim.

<a id="phy-36"></a>
### PHY-36 — Capacity estimates that transfer between bottlenecks

**Update 2:** unchanged.

**Question:** Does controlling upstream density explain more variation in measured bottleneck capacity than doorway width alone?

**Candidate hypothesis:** A model including upstream density and transient occupancy will transfer between geometries better than a width-only capacity rule.

**How to test:** Use accessible controlled-trajectory data if licensing and metadata permit; fit models leaving entire experimental runs and geometry settings out, not random frames. In simulation, randomize episodes to width and upstream arrival density independently to test the proposed mechanism. Distinguish stationary capacity from short transient bursts and compare both to the source definitions.

**Comparison:** A linear width-only predictor, a density-only predictor and a model with run-specific intercepts expose what actually transfers.

**Measurements:** Held-out flow prediction; Time-gap distribution; Stationary-window sensitivity; Calibration by geometry; Queue accumulation.

**Would count against it:** Width-only predictions transfer equally well, or density adds value only through leakage from simultaneous output measurements.

**Main confounds:** Short runs may never reach stationarity. Human groups, motivation and measurement regions differ; the nearby dense-stationary-crowd dataset is not a bottleneck-capacity dataset and must not be substituted silently.

**Framing / first-test class:** measurement / access-dependent.

**Before promotion:** Locate actual bottleneck runs with upstream-density metadata and verify reuse terms; fall back to a clearly labelled synthetic-only study if unavailable.

**Closest prior and evidence limits:**

- [[seyfried-2009-new]] — [New Insights into Pedestrian Flow Through Bottlenecks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/seyfried-2009-new.md). Closest empirical source already identifies upstream-density differences and transient limits. Catalogue depth: full.
- [[data-juelich-crowd-2019]] — [Motion through a dense and stationary crowd](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-juelich-crowd-2019.md). Available trajectory resource is a task-mismatched negative control, with unresolved binary reuse terms. Catalogue depth: ran.
- [[gh-pedestriandynamics-jupedsim]] — [JuPedSim: Jülich pedestrian dynamics simulator (collision-free speed and social-force style models, Python API)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-pedestriandynamics-jupedsim.md). Possible simulation intervention route; cannot replace empirical transfer evidence. Catalogue depth: skim.

<a id="meta"></a>
## Meta and tooling

<a id="mth-01"></a>
### MTH-01 — How much certainty comes from counting the wrong units?

**Update 2:** revised.

**Question:** How badly does treating interacting agents as independent samples overstate confidence?

**Candidate hypothesis:** Agent-level uncertainty estimates will under-cover known episode-level effects when within-swarm dependence is strong.

**How to test:** Generate independent swarm episodes with a known randomized treatment effect and tunable within-episode dependence. Compare agent-level resampling, episode-level resampling and exposure-aware analysis over repeated synthetic studies. Use SwarmWorld metadata/episodes.csv and matched condition-seed cells as a concrete reanalysis design; keep its discovery-seed units distinct from agents and held-out portfolio assay seeds. The synthetic arm, not this observational reanalysis, supplies known coverage truth.

**Comparison:** Known generator effect and episode-level randomized estimate.

**Measurements:** Confidence-interval coverage; false-positive rate; interval width.

**Would count against it:** Agent-level intervals maintain nominal coverage across strong dependence, or clustered methods also fail under their stated design.

**Main confounds:** A valid cluster must contain the interference; shared global boards can couple ostensibly separate episodes.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Pin the SwarmWorld release, check manifests and file hashes, and verify pairing before loading endpoints. Specify interference boundaries; this is methodological validation, not a new estimator.

**Closest prior and evidence limits:**

- [[aronow-2013-estimating]] — [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/aronow-2013-estimating.md). Assignment and interference framework. Catalogue depth: skim.
- [[shalizi-2011-homophily]] — [Homophily and Contagion Are Generically Confounded in Observational Social Network Studies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shalizi-2011-homophily.md). Observational confounding is a separate problem from dependence. Catalogue depth: skim.
- [[data-swarmworld-2026]] — [SwarmWorld paper data: event traces of 50-200 LLM agents discovering and exchanging material technologies in a shared simulated world (60 episodes)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-swarmworld-2026.md). Concrete matched-episode corpus for unit-of-analysis sensitivity; four discovery seeds do not become hundreds of independent agents. Catalogue depth: skim.

<a id="mth-02"></a>
### MTH-02 — Do outcome labels change the conclusion?

**Update 2:** revised.

**Question:** Can the same intervention improve consensus while worsening correctness or welfare?

**Candidate hypothesis:** An intervention that increases agreement will sometimes reduce calibrated correctness on tasks with shared misleading evidence.

**How to test:** Randomize independent synthetic teams to an agreement-promoting rule or neutral aggregation under known task truth. Score the same frozen traces for agreement, correctness, calibration and resource-adjusted utility using evaluators blind to treatment. As a retrospective diagnostic, align DEBATE configuration records by original task and compare decisionSuccess with independently recoverable task truth; where truth is unavailable, do not call agreement accuracy.

**Comparison:** Independent answers with aggregation and neutral communication at matched budget.

**Measurements:** Agreement; exact accuracy; calibration error; useful output per token.

**Would count against it:** Agreement improves only when correctness and utility also improve across the tested evidence regimes.

**Main confounds:** Utility weights express human choices; publish the separate outcomes before combining them.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Inspect DEBATE task IDs, reference answers and decisionSuccess semantics before selecting a subset. Human reviewers pick the primary outcome before confirmation.

**Closest prior and evidence limits:**

- [[pavlova-2026-flag]] — [Flag Game: A Toy Model for Mechanistic Swarm Interpretability](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pavlova-2026-flag.md). Ground-truth-aware collective task precedent. Catalogue depth: full.
- [[zhou-2025-pimmur]] — [The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-pimmur.md). Measurement validity context; abstract rechecked, methods not fully audited. Catalogue depth: abstract.
- [[data-mallm-debate-2025]] — [DEBATE: Diverse Multi-Agent Debates, 144 configurations of LLM discussion paradigm, persona and decision protocol (MALLM)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-mallm-debate-2025.md). Released agreement and decision traces offer a concrete outcome-mismatch audit, not validated correctness labels. Catalogue depth: skim.

<a id="mth-03"></a>
### MTH-03 — Does a finding survive a model or runtime change?

**Update 2:** revised.

**Question:** How portable are candidate effect sizes across model versions and orchestration scaffolds?

**Candidate hypothesis:** Some intervention rankings will reverse across versions or scaffolds even when prompts and task cases are held fixed.

**How to test:** After selecting a small task, cross intervention with two pinned models and two independently implemented runners. Randomize run order and compare episode-level effects on identical held-out cases. If two versions cannot be pinned, label time-confounded comparisons exploratory.

**Comparison:** Within-runner repeated execution and no-intervention control.

**Measurements:** Interaction effect by runner/model; ranking reversals; trace divergence; cost.

**Would count against it:** Effects and rankings remain stable within a prespecified practical tolerance across all tested configurations.

**Main confounds:** Provider drift, retry policy, tool schema and decoding defaults can masquerade as model differences. Town model arms have serving-stack differences; their archived comparisons cannot identify a pure model effect.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Inspect production_final run.json and model_calls.csv for stack differences; build the crossed test in a small released harness. Pin models, retry/tool policies and scheduler settings; API seeds do not ensure determinism.

**Closest prior and evidence limits:**

- [[zhou-2025-pimmur]] — [The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-pimmur.md). Validity motivates explicit implementation controls. Catalogue depth: abstract.
- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). Nondeterminism and replay are conceptual precedents, not LLM-specific evidence. Catalogue depth: skim.
- [[data-agent-town-economy-2026]] — [Agent Town Economy: 98 runs of a 100-agent LLM economic simulation with a fully ledgered, money-conserving economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-town-economy-2026.md). Concrete runtime-confounding example and failure ledger; released model arms are not a fully crossed causal design. Catalogue depth: skim.

<a id="mth-04"></a>
### MTH-04 — Spend the budget on more seeds or more worlds?

**Update 2:** revised.

**Question:** Which source of variation dominates uncertainty in our chosen collective task?

**Candidate hypothesis:** Variation across task worlds will exceed sampling variation within a single world for at least some candidate interventions.

**How to test:** Run a small balanced pilot crossing independent world instances and run seeds for a selected task. Estimate variance components without selecting the best treatment from the same pilot, then compare predicted precision for equal-cost sampling allocations on fresh worlds. First audit Town run.json world identifiers against layout content, excluding timestamps from geometry fingerprints. Treat repeats on the same geometry as within-layout runs; its many world labels cannot stand in for a new-world sample.

**Comparison:** Equal allocation, many seeds on one world, and many worlds with few seeds.

**Measurements:** Between-world variance; within-world variance; interval width per unit cost; out-of-sample precision.

**Would count against it:** Within-world randomness dominates and more worlds do not improve equal-cost precision.

**Main confounds:** Pilot variance estimates are uncertain; report a range of allocations rather than a single magic sample size.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Validate layout fingerprints and licensing before reanalysis; the archived two-layout corpus is too narrow to determine a general optimum. Use pilot data for planning, not confirmation.

**Closest prior and evidence limits:**

- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Function instances and run budgets motivate the design question. Catalogue depth: full.
- [[aronow-2013-estimating]] — [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/aronow-2013-estimating.md). Independent assignment units constrain uncertainty estimates. Catalogue depth: skim.
- [[data-agent-town-economy-2026]] — [Agent Town Economy: 98 runs of a 100-agent LLM economic simulation with a fully ledgered, money-conserving economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-town-economy-2026.md). Concrete replication-unit caution: the primary card documents two layouts under multiple world IDs. Catalogue depth: skim.

<a id="mth-05"></a>
### MTH-05 — Can an interrupted run be meaningfully resumed?

**Update 2:** revised.

**Question:** Does restoring agent state without scheduler and external-response state change the collective outcome?

**Candidate hypothesis:** Full replay checkpoints will preserve outcomes better than memory-only checkpoints in asynchronous synthetic tasks.

**How to test:** Randomize interruption times in independent deterministic mock-tool episodes. Compare uninterrupted runs, agent-memory restore and full-state restore including queues/RNG/tool-response logs. Use fixed replay data first, then explicitly stochastic responses as a separate condition.

**Comparison:** Uninterrupted replay and restart-from-scratch at matched completed-work budget.

**Measurements:** Trace divergence; final task score; duplicated actions; recovery overhead.

**Would count against it:** Memory-only restore matches full replay across ordering-sensitive tasks.

**Main confounds:** Real external side effects cannot generally be undone; use reversible mock tools and distinguish record restoration from compensation.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Inspect tass committed snapshots and resume boundaries, then use its offline baseline and controlled HTTP responses. Verify scheduler, pending decisions and shared budget restoration; replaying saved snapshots alone is not a counterfactual rerun.

**Closest prior and evidence limits:**

- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). Classical consistent recovery and nondeterminism logging. Catalogue depth: skim.
- [[li-2026-memtx]] — [MemTX: Transactional Belief Commit for Stateful Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-memtx.md). Agent-memory repair overlap; this candidate isolates execution reproducibility rather than invalid-claim rollback. Catalogue depth: skim.
- [[gh-apromisedland-trustworthy-agent-simulation]] — [Trustworthy Agent Simulation (tass): auditable LLM town society on AgentScope + Mesa with replay, resume, policy batches and Streamlit dashboard](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-apromisedland-trustworthy-agent-simulation.md). Released baseline-mode resume/replay harness is a candidate audit substrate; its advertised restoration still needs verification. Catalogue depth: abstract.

<a id="mth-06"></a>
### MTH-06 — How much of a discovery is selecting the best run?

**Update 2:** revised.

**Question:** How often does a promising-looking effect disappear when the whole search process is accounted for?

**Candidate hypothesis:** Selecting the strongest of many prompts or seeds will produce a larger discovery-to-confirmation drop than a frozen small candidate set.

**How to test:** On synthetic null and known-effect tasks, replay a simulated research workflow: search over varying numbers of configurations, choose the winner, and evaluate on untouched cases. Repeat the full selection procedure, not just the winning run. DEBATE offers a concrete configuration-search analogue: after checking task overlap and references, select configurations on development task families and confirm once on untouched families. Null permutations must preserve task and configuration dependence.

**Comparison:** Preregistered fixed comparison, random configuration selection, and selection-aware held-out evaluation.

**Measurements:** False discovery rate; discovery-to-confirmation effect drop; winner retention.

**Would count against it:** Increasing search breadth produces no optimism under controlled nulls, or independent confirmation retains the selected effects.

**Main confounds:** Search budget and evaluation budget must be reported separately; a null result may reflect low power.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Keep this as a methodological replication/validation unless a new selection procedure survives literature review.

**Closest prior and evidence limits:**

- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Benchmark-design sensitivity motivates selection controls. Catalogue depth: full.
- [[zhou-2025-pimmur]] — [The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-pimmur.md). Methodological audit motivation; this resampling design is a proposed lab audit. Catalogue depth: abstract.
- [[data-mallm-debate-2025]] — [DEBATE: Diverse Multi-Agent Debates, 144 configurations of LLM discussion paradigm, persona and decision protocol (MALLM)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-mallm-debate-2025.md). Many released configurations motivate a bounded selection audit; completeness and common task coverage remain to be checked. Catalogue depth: skim.

<a id="sim-01"></a>
### SIM-01 — Private information leaks through the narrator

**Update 2:** revised.

**Question:** Does a shared game master accidentally improve coordination by exposing private state?

**Candidate hypothesis:** A narrator with access to every agent's private evidence will inflate apparent cooperation unless outgoing messages enforce visibility boundaries.

**How to test:** Adapt a small Sotopia negotiation scenario with deterministic factual scoring. Randomize independent scenario-seed episodes between partitioned agent contexts, a partitioned Concordia-style narrator and a shared-context narrator. Match private facts, actions and inference budgets; plant harmless private markers to measure disclosure. Evaluate on new scenarios and keep judge access distinct from participant access.

**Comparison:** Separate-agent rule engine and explicitly public-information variant as a diagnostic ceiling.

**Measurements:** Private-state disclosure rate; Task success; Agreement conditional on authorized information; Narration cost.

**Would count against it:** Shared narration produces no extra disclosure or performance gap once legitimate public information is matched.

**Main confounds:** Narrator competence and context length differ; include matched summaries and deterministic scoring independent of the narrator.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Read the visibility contract and source before adapting either runner. The merged sim-environments survey remains in-progress; its source links and teammate smoke tests are leads, not approval or evidence of this leak.

**Closest prior and evidence limits:**

- [[zhou-2024-is]] — [Is this the real life? Is this just fantasy? The Misleading Success of Simulating Social Interactions With LLMs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2024-is.md). Closest prior already contrasts omniscient Script and private-goal Agents modes; extend to an audited narrator boundary. Catalogue depth: full.
- [[gh-google-deepmind-concordia]] — [Concordia: generative agent-based modelling with a Game Master that adjudicates natural-language actions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-google-deepmind-concordia.md). Candidate game-master architecture; no claim that every implementation leaks. Catalogue depth: skim.
- [[gh-sotopia-lab-sotopia]] — [Sotopia: open-ended social role-play environment with private goals and the SOTOPIA-Eval multi-dimensional judge](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-sotopia-lab-sotopia.md). Concrete private-goal scenario and execution-mode substrate; primarily dyadic. Catalogue depth: skim.

<a id="sim-02"></a>
### SIM-02 — The scheduler as an experimental treatment

**Update 2:** revised.

**Question:** Does synchronous versus asynchronous activation change the effect of majority-following compared with independent updates?

**Candidate hypothesis:** The benefit of majority-following over independent updates will shrink or reverse when agents see fresh state sequentially rather than simultaneous snapshots.

**How to test:** Implement a binary decision game with noisy private evidence. Cross majority-following versus independent updates with simultaneous, fixed-order sequential and randomized-order sequential schedules. Pair independent worlds and randomize conditions; hold action opportunities fixed, logging information freshness. Report episode-level accuracy effects and separately charge wall-clock and communication work.

**Comparison:** Synchronous update, randomized sequential update and fixed order with permuted agent labels.

**Measurements:** Intervention effect by schedule; Task success; First-mover advantage; Actions to completion.

**Would count against it:** The effect remains within a prespecified equivalence margin across schedules and update-order permutations.

**Main confounds:** Update schedules change information freshness; record that mechanism rather than attributing all differences to psychology.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Start with an exact binary-rule reference before an AgentsNet adapter. Audit when state is read and committed; teammate four-node colouring smoke tests verify a path runs, not asynchronous semantics.

**Closest prior and evidence limits:**

- [[radax-2010-timing]] — [Timing matters: Lessons From The CA Literature On Updating](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/radax-2010-timing.md). Scheduler sensitivity is established in ABMs; this is a task-specific boundary test, not a new general phenomenon. Catalogue depth: full.
- [[gh-floriangroetschla-agentsnet]] — [AgentsNet: benchmark of LLM agents on a graph solving distributed-computing tasks (colouring, matching, leader election, consensus, vertex cover) by synchronous message passing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-floriangroetschla-agentsnet.md). Concrete synchronous message-passing runner; asynchronous modes must be implemented and verified. Catalogue depth: ran.
- [[grotschla-2025-agentsnet]] — [AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/grotschla-2025-agentsnet.md). Known graph-task scoring and baseline for the adaptation. Catalogue depth: abstract.

<a id="sim-03"></a>
### SIM-03 — Can the benchmark be solved without observing peers?

**Update 2:** revised.

**Question:** Does a purported interaction benchmark require the observations it is intended to study?

**Candidate hypothesis:** A timestep-only or memorized-action policy will solve some fixed-layout cases, but fail on held-out randomized layouts and role assignments.

**How to test:** Compare full-observation, masked-observation and timestep-only policies on matched task instances. Freeze policies before evaluating new seeds, graph label permutations and layouts. Analyze independently trained policies or independently prompted episodes as appropriate.

**Comparison:** Random actions, scripted open-loop policy and fully observing agent with equal action budget.

**Measurements:** Success without observations; Generalization gap; Marginal value of peer observations; Policy cost.

**Would count against it:** Blind policies remain near chance on fixed cases while observed policies generalize, supporting benchmark validity.

**Main confounds:** Masking inputs can create out-of-distribution prompts; also train or prompt blind policies from the start.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Inspect SwarmBench task code and match the dataset release to the runner before reproducing one task. Its mixed agent/game schemas require separate parsing. This transfers an existing diagnostic; StarCraft installation is unnecessary for the first LLM-grid test.

**Closest prior and evidence limits:**

- [[ellis-2022-smacv2]] — [SMACv2: An Improved Benchmark for Cooperative Multi-Agent Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ellis-2022-smacv2.md). Closest diagnostic already establishes observation-blind policies as a benchmark-validity test. Catalogue depth: full.
- [[data-swarmbench-2025]] — [SwarmBench experiment logs: LLMs as decentralised agents on five 2D-grid swarm tasks (Flocking, Pursuit, Synchronize, Foraging, Transport), 13 models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-swarmbench-2025.md). Released per-agent and whole-game logs can identify candidate observation shortcuts. Catalogue depth: skim.
- [[gh-ruc-gsai-yulan-swarmintell]] — [SwarmBench (YuLan-SwarmIntell): 2D grid benchmark of LLM agents on pursuit, synchronisation, foraging, flocking and transport with local views and local messages](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-ruc-gsai-yulan-swarmintell.md). Concrete LLM-grid runner for prospective masked-observation and randomized-layout tests. Catalogue depth: skim.

<a id="sim-04"></a>
### SIM-04 — Same rules, different engines

**Update 2:** revised.

**Question:** Do two implementations of a collective model agree after matching semantics rather than just parameter names?

**Candidate hypothesis:** Apparent framework-dependent behavior will shrink after matching update order, neighborhood rules, boundaries and random-number consumption.

**How to test:** Implement one explicitly specified boid model in Mesa and AgentPy using identical initial states and noise tapes. Match state-read/commit timing, neighbor distance, boundaries, integration and normalization. Compare one-step transitions, then independent-seed distributions. Deliberately vary one semantic choice at a time. Only after agreement time identical workloads, including neighbor queries and logging, at fixed hardware and precision.

**Comparison:** A small transparent reference implementation and step-size/precision convergence checks.

**Measurements:** One-step state error; Distributional order-parameter distance; Regime classification agreement; Runtime per agent-step.

**Would count against it:** A material behavioral gap survives matched semantics and validated numerical tolerance.

**Main confounds:** Bitwise equality is not expected across hardware; distinguish pathwise replay from distributional agreement.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Pin isolated versions; AgentPy is unmaintained. Reconcile the teammate run scripts before comparing outcomes or speed. The merged survey offers heterogeneous smoke workloads, not an apples-to-apples performance ranking.

**Closest prior and evidence limits:**

- [[gh-mesa-mesa]] — [Mesa: Python agent-based modelling framework (grids, continuous space, schedulers, browser visualisation), with a bundled Boids flocking example](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-mesa-mesa.md). Candidate current Python reference; teammate example run used its own rules. Catalogue depth: ran.
- [[gh-jofmi-agentpy]] — [AgentPy: Python ABM library integrating model design, experiments and analysis (grid, continuous space with KD-tree, networks)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-jofmi-agentpy.md). Second implementation route; its teammate boids timing used different weights and is not an equivalence result. Catalogue depth: ran.
- [[grimm-2020-odd]] — [The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/grimm-2020-odd.md). Model-description framework motivates an explicit semantics contract, not empirical validity by documentation alone. Catalogue depth: abstract.

<a id="mth-07"></a>
### MTH-07 — Do failure rankings survive independent relabelling?

**Update 2:** new.

**Question:** Would our preferred trace debugger change if independent humans supplied the reference labels?

**Candidate hypothesis:** Some debugger rankings will change when judge-generated error labels are replaced by adjudicated human labels, especially for blame location rather than final task failure.

**How to test:** Sample whole MAST traces stratified by framework, outcome and original label; randomize anonymized trace order to two independent annotators. Freeze one taxonomy before annotation and adjudicate disagreements without model names or debugger predictions. Evaluate frozen debuggers on both label versions using trace-level paired analysis. Use TRAIL only as a separately reported external check after access approval, and keep its single-agent and multi-agent subsets separate.

**Comparison:** Original MAST labels, majority-class prediction and a simple last-error heuristic; compare end-outcome labels separately from causal blame.

**Measurements:** Trace-level label agreement; Debugger ranking stability; Error-localization distance; Abstention coverage.

**Would count against it:** Rankings and practically relevant performance differences remain stable within a prespecified margin under independent labels.

**Main confounds:** MAST annotation rounds use differing category counts, so numeric codes require semantic mapping. Null annotations are not negative labels; a judged decisive step is not counterfactual causation.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Check taxonomy versions and trace rights; budget blinded annotation. TRAIL gate terms and Who&When reuse terms must be resolved before use or redistribution.

**Closest prior and evidence limits:**

- [[data-mast-2025]] — [MAD: Multi-Agent System Traces Dataset, 1,642 MAS execution traces annotated with the 14 MAST failure modes](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-mast-2025.md). Closest available judge-labelled traces and small human subset; motivates measurement rather than accepting all labels as truth. Catalogue depth: skim.
- [[data-trail-2025]] — [TRAIL: 148 human-annotated agent traces (GAIA and SWE-bench) for trace reasoning and agentic issue localization](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-trail-2025.md). Human-annotated external corpus with restricted access and redistribution. Catalogue depth: skim.
- [[data-who-and-when-2025]] — [Who&When: 184 multi-agent failure logs annotated with the responsible agent, the decisive error step and an explanation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-who-and-when-2025.md). Alternative attribution target; failures-only sampling limits prevalence claims. Catalogue depth: skim.

<a id="mth-08"></a>
### MTH-08 — Does the split separate new games or just new turns?

**Update 2:** new.

**Question:** How much apparent generalization comes from seeing another turn or condition of the same underlying game?

**Candidate hypothesis:** Random-row evaluation will overstate predictive accuracy relative to holding out whole game-generating sequences, beyond the gap explained by sample size.

**How to test:** For Hanabi, reconstruct complete episodes from file, model, scaffold, player count, seed and turn resets; audit collisions rather than assuming a seed is a unique game. For the collusion corpus, group all conditions sharing a base task sequence. Train identical bounded outcome predictors under row, episode and base-sequence splits with equal training counts. Repeat split assignments and evaluate a final untouched sequence set; units are independent generating sequences, not messages.

**Comparison:** Model/task metadata-only predictor and group-preserving label permutations alongside naive row splitting.

**Measurements:** Held-out sequence accuracy; Calibration; Cross-split duplicate rate; Performance drop at equal sample count.

**Would count against it:** Grouped and row splits agree within a practical margin after training-size and difficulty matching, with no residual overlap.

**Main confounds:** Grouping can introduce genuine distribution shift; report that separately. Different filenames, seeds or agent roles do not establish independent underlying tasks.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Inspect raw JSONL schemas and manifests, pin revisions, verify the sequence map, and keep malformed or duplicate rows in an exclusion ledger rather than silently dropping them.

**Closest prior and evidence limits:**

- [[data-hanabi-llm-logs-2026]] — [HanabiLogs and HanabiRewards: 92,923 turn-level logs of 17 LLMs playing cooperative Hanabi (2-5 players) under three scaffolds, with LLM-judge move ratings](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-hanabi-llm-logs-2026.md). Turn-level logs need episode reconstruction and scaffold-aware grouping. Catalogue depth: skim.
- [[data-agent-collusion-2026]] — [Emergent Collusion in Long-Horizon LLM Agent Interaction: 2,650 two-agent trajectories (27,100 episodes) with judge labels](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-collusion-2026.md). Shared base sequences across conditions provide a concrete leakage hazard. Catalogue depth: skim.

<a id="mth-09"></a>
### MTH-09 — Does the evaluator know more than the acting agent?

**Update 2:** new.

**Question:** Does privileged state in archived traces make an agent look less competent than its actual information permitted?

**Candidate hypothesis:** Evaluators given omniscient state will over-attribute avoidable mistakes compared with evaluators restricted to the acting agent’s legal information.

**How to test:** Select complete Hanabi episodes with recoverable views and pair two evaluator packets for each decision: exact visible prompt/history versus that packet plus hidden engine state. Randomize packet presentation between blinded annotators; cluster analysis by game and exclude the same annotator seeing both versions. Score avoidability, not simply whether the eventual action lost points. Repeat on a small private-goal Sotopia subset only if its visibility contract and comparable action labels can be reconstructed.

**Comparison:** A rules-based legality checker plus an information-set policy that cannot inspect the hidden state; omniscient scoring is a labelled diagnostic ceiling.

**Measurements:** Avoidable-error disagreement; Calibration conditional on information; Hindsight blame rate; Evaluator agreement.

**Would count against it:** Privileged state does not increase avoidable-error attribution, or differences vanish when the legal information set is explicit.

**Main confounds:** Legality, expected value and realized luck differ. Engine-computed Bayesian beliefs legitimately supplied to a scaffold are visible assistance, not hidden leakage.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Validate the Hanabi observation renderer and raw-state fields; confirm Sotopia JSON provenance and reuse terms. No logged private reflection is assumed visible to an ordinary participant.

**Closest prior and evidence limits:**

- [[data-hanabi-llm-logs-2026]] — [HanabiLogs and HanabiRewards: 92,923 turn-level logs of 17 LLMs playing cooperative Hanabi (2-5 players) under three scaffolds, with LLM-judge move ratings](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-hanabi-llm-logs-2026.md). Logs contain prompts, legal moves and raw state; exact visibility remains to be audited. Catalogue depth: skim.
- [[data-sotopia-2024]] — [SOTOPIA episodes v1: role-played social-interaction episodes between language agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-sotopia-2024.md). Private-goal setting for an external boundary check. Catalogue depth: skim.
- [[zhou-2024-is]] — [Is this the real life? Is this just fantasy? The Misleading Success of Simulating Social Interactions With LLMs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2024-is.md). Information-asymmetry precedent; evaluator hindsight is distinct from omniscient dialogue generation. Catalogue depth: full.

<a id="mth-10"></a>
### MTH-10 — Does translation preserve the interaction being measured?

**Update 2:** new.

**Question:** Do translated game logs change judgments of uncertainty, commitment or reasoning quality?

**Candidate hypothesis:** English translations will systematically alter some pragmatic labels relative to the original Chinese turns, producing apparent cross-language behavior differences without changed play.

**How to test:** Draw whole Werewolf games with paired original and translated events. Randomize bilingual annotators to original or translated packets, preserving surrounding turns and hiding player identity; never show both versions of one game to the same annotator. Use a predeclared rubric for uncertainty, accusations and commitments, with bilingual adjudication of disagreements. Fit paired game-level effects and separately test missing-translation selection. A small independently translated sample distinguishes this release’s translation pipeline from a universal language effect.

**Comparison:** Original-language judgments, independently translated packets and within-language repeated annotation at matched context length.

**Measurements:** Pragmatic-label agreement; Confidence shift; Player-ranking changes; Missing-translation sensitivity.

**Would count against it:** Translation effects stay inside the equivalence margin and are no larger than ordinary annotator variation across all prespecified labels.

**Main confounds:** Human versus model authorship of the original play is not established by the card. Reasoning-note translations may differ from public dialogue and should not be pooled.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Verify licences, pairing keys, missingness and game boundaries; recruit bilingual review. Do not auto-fill missing translations and then treat them as original released observations.

**Closest prior and evidence limits:**

- [[data-werewolf-game-reasoning-2025]] — [Werewolf game dataset: raw 7- and 9-player game records with thinking-process notes, plus SFT instruction sets (Multi-agent KTO)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-werewolf-game-reasoning-2025.md). Actual paired Chinese and English events and notes; the card identifies an LLM translation process. Catalogue depth: skim.
- [[data-diplomacy-deception-2020]] — [Diplomacy deception detection: 17,289 pairwise in-game messages from 12 games, labelled truthful/deceptive by sender and receiver](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-diplomacy-deception-2020.md). Analogy for separating communicative intent from receiver interpretation, not a parallel translation corpus. Catalogue depth: skim.

<a id="mth-11"></a>
### MTH-11 — Which system wins when failed runs count?

**Update 2:** new.

**Question:** Do completion-conditioned rankings agree with reliability-adjusted utility across all attempted runs?

**Candidate hypothesis:** A system that looks strong on completed episodes may rank lower when malformed calls, retries and abandoned episodes are included at a fixed resource budget.

**How to test:** Reconstruct Town run attempts from manifests, validation records and call ledgers, separating infrastructure aborts from complete runs excluded by a statistical rule. Report accepted-only scores and all-attempt utility with prespecified failure costs and sensitivity bounds. Because archived stacks are not randomized, confirm in a small controlled mock economy: randomize independent episodes to serving configurations, hold model and task fixed, and include every attempt, retry and timeout.

**Comparison:** Accepted-only analysis, deterministic valid-action fallback and a fixed no-retry policy; compare equal resource budgets rather than equal successful episodes.

**Measurements:** Completion probability; Utility per attempted episode; Utility per token/time budget; Retry burden; Ranking sensitivity.

**Would count against it:** Rankings remain practically stable across defensible failure costs, or completion rates do not differ under the randomized stack comparison.

**Main confounds:** Infrastructure failure is not evidence of poor strategic reasoning. Outlier exclusion, budget censoring and invalid output are different mechanisms; retain them as separate categories.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Reconcile run/call counters and terminal states before scoring; specify the failure-cost range in advance. The Town engine is unavailable, so the controlled confirmation requires a distinct validated toy implementation.

**Closest prior and evidence limits:**

- [[data-agent-town-economy-2026]] — [Agent Town Economy: 98 runs of a 100-agent LLM economic simulation with a fully ledgered, money-conserving economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-town-economy-2026.md). Release retains quarantined runs and documents serving-stack problems; supports a reliability audit, not clean model attribution. Catalogue depth: skim.
- [[gh-apromisedland-trustworthy-agent-simulation]] — [Trustworthy Agent Simulation (tass): auditable LLM town society on AgentScope + Mesa with replay, resume, policy batches and Streamlit dashboard](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-apromisedland-trustworthy-agent-simulation.md). Candidate small offline harness with explicit budget and failure logging. Catalogue depth: abstract.

<a id="mth-12"></a>
### MTH-12 — When does a collection of sessions become a team?

**Update 2:** new.

**Question:** Does counting multiple agent sessions per task identify collaboration, or mostly sequential retries and handoffs?

**Candidate hypothesis:** Session fan-out alone will overstate concurrent collaboration compared with a trace-based definition requiring overlapping activity and a verifiable information dependency.

**How to test:** Sample AgentLogs tasks stratified by session count and outcome after checking table joins. Independently reconstruct session intervals and explicit handoff or shared-artifact dependencies from event records. Have blinded reviewers label sequential retry, parallel independent work and interacting work, allowing unknown where evidence is missing. Compare the resulting prevalence estimates and outcome associations with session-count labels using task-level analysis and repository-clustered uncertainty. Validate the labeling procedure on synthetic workflows with known execution graphs.

**Comparison:** One-session threshold, time-overlap-only rule, and synthetic retry-only negative controls.

**Measurements:** Collaboration precision; Unclassifiable fraction; Outcome association after relabelling; Join completeness; Concurrency reconstruction error.

**Would count against it:** Session-count classification already agrees with audited dependencies and outcome conclusions remain stable under the stricter definition.

**Main confounds:** Shared task IDs do not imply causal interaction; overlapping timestamps may reflect waiting. Public repository sampling and incomplete logs limit population generalization, and users are not verified independent operators.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Pin v0.2, inspect foreign keys and timestamp semantics, sample before touching the large event table, and measure missing sessions. This is a task-execution audit, not a claim to recover real-world operator identities.

**Closest prior and evidence limits:**

- [[data-agentlogs-2026]] — [AgentLogs: tasks, sessions and 64M session-log entries from GitHub's cloud coding agent across 1.8M public repositories](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agentlogs-2026.md). Relational task, session and event corpus offers concrete provenance evidence but no automatic collaboration ground truth. Catalogue depth: skim.
- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). Execution-history and causality concepts motivate synthetic known-graph validation. Catalogue depth: skim.

<a id="mth-13"></a>
### MTH-13 — Is there a stable ranking of cooperative ability?

**Update 2:** new.

**Question:** Do model rankings carry across common-payoff games, mixed-motive negotiation and open-ended social goals after matching execution conditions?

**Candidate hypothesis:** Within-task rankings will be more stable than cross-task rankings even after common model versions, costs and visibility are matched, weakening a single general cooperation score.

**How to test:** Inventory exact model/scaffold overlap in Hanabi, C2C and Sotopia before analyzing. On an adequate common subset, normalize each task’s outcome against its own legal scripted baseline, hold out entire games or scenarios, and estimate rank uncertainty without pooling turns. If the released overlap is inadequate, specify a small prospective common-model panel with balanced game instances and fixed budgets; treat it as required new data, not an imputed cross-corpus result.

**Comparison:** Task-specific rankings, rank predictions from cost alone, and within-task split-half reliability as a reference for measurement stability.

**Measurements:** Cross-task rank correlation; Within-task reliability; Rank uncertainty; Performance relative to task baseline.

**Would count against it:** A single ranking predicts held-out task outcomes nearly as well as task-specific rankings within practical tolerance.

**Main confounds:** Shared payoff, kept deals and private-goal achievement are different constructs. A rank reversal may reflect prompts, partners or visibility rather than a model trait; human welfare is not inferred from game score.

**Framing / first-test class:** measurement / access-dependent.

**Before promotion:** Confirm compatible models, benchmark reuse rights, episode keys and outcome provenance; reject an aggregate score if measurement compatibility or common support fails.

**Closest prior and evidence limits:**

- [[data-hanabi-llm-logs-2026]] — [HanabiLogs and HanabiRewards: 92,923 turn-level logs of 17 LLMs playing cooperative Hanabi (2-5 players) under three scaffolds, with LLM-judge move ratings](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-hanabi-llm-logs-2026.md). Common-payoff coordination corpus with important scaffold variation. Catalogue depth: skim.
- [[data-c2c-ai-vs-ai-2026]] — [C2C (Cooperate to Compete) AI-vs-AI games: 972 logged four-player LLM conquest-and-negotiation games under six prompt interventions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-c2c-ai-vs-ai-2026.md). Mixed-motive negotiation comparison with matched board conditions. Catalogue depth: skim.
- [[data-sotopia-2024]] — [SOTOPIA episodes v1: role-played social-interaction episodes between language agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-sotopia-2024.md). Social-goal corpus requires JSON to retain model and reward metadata. Catalogue depth: skim.

<a id="mth-14"></a>
### MTH-14 — Does the apparent trend survive the crawler?

**Update 2:** new.

**Question:** Can an apparent change in agent interaction be explained by collection or moderation changes rather than behavior?

**Candidate hypothesis:** Some longitudinal interaction trends will shrink or reverse when analysis is restricted to a stable observation rule and overlapping entity-time coverage.

**How to test:** Choose a narrow overlapping time window in the jscmp4 and MoltNet releases. Reconcile immutable entity IDs, revisions, deletion states and crawler provenance before matching posts and comments. Compare daily reply concentration and thread depth under each source, common-observed entities, and a fixed post-eligibility rule. Analyze days and communities as clustered observational units, then inject known observation-rule changes into synthetic stationary networks to check the estimator.

**Comparison:** Naive full-release trend, matched-coverage trend and synthetic stationary-network negative control.

**Measurements:** Trend sensitivity to eligibility; Cross-source missingness; Duplicate/revision rate; Interaction-statistic agreement.

**Would count against it:** Trends remain practically unchanged under stable coverage and are absent from the synthetic collection-change controls.

**Main confounds:** The two releases share some upstream crawls, so agreement is not independent replication. Comments below a collection threshold and changing spam flags cannot be treated as random omissions or stable labels.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Freeze revisions, inspect upstream terms, dedup lineage and fetch-completeness flags. The supplemental takschdube release has a documented older reply-graph omission; rebuild affected graphs. Restrict the estimand to observable activity; moderation timing alone does not identify causality.

**Closest prior and evidence limits:**

- [[data-jscmp4-moltbook-2026]] — [Moltbook AI Agent Social Media Corpus: 3.2M posts, 15.9M comments and 99,621 agent profiles from daily crawls, Jan 27 to Jul 3, 2026](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-jscmp4-moltbook-2026.md). Longitudinal crawl documents selective comment retrieval and field-regime changes. Catalogue depth: skim.
- [[data-moltnet-2026]] — [MoltNet: integrated Moltbook corpus of 1.04M posts, 3.16M comments, 149,574 AI-agent profiles and 18,244 communities with longitudinal histories (Jan 27 to Feb 28, 2026)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-moltnet-2026.md). Merged crawl histories provide provenance checks, with overlapping upstream observations. Catalogue depth: skim.
- [[data-moltbook-dataset-2026]] — [Moltbook Social Interactions Dataset (takschdube/moltbook-dataset): longitudinal posts, comments, agents, social and reply graphs from the agent-only network Moltbook](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-moltbook-dataset-2026.md). Supplemental crawl documents fetch completeness and a historical reply-graph construction error; source metadata alone is not social ground truth. Catalogue depth: skim.

<a id="mth-15"></a>
### MTH-15 — Does entropy predict collaboration beyond task difficulty?

**Update 2:** new.

**Question:** Does an entropy summary identify when collaboration helps on unseen task families, beyond model and single-agent performance?

**Candidate hypothesis:** Some within-benchmark entropy associations will lose predictive value after controlling for difficulty and holding out entire task families or model sizes.

**How to test:** Audit the entropy release’s master table and metric computation order. Define collaboration gain relative to the matched single-agent result and fit a bounded predictor using only features available at the proposed decision time. Compare nested models with and without entropy, holding out base questions, task families and model groups. Repeat group-preserving label permutations. If features require completed collaborative traces, evaluate retrospective diagnosis only and require new early-prefix traces for a routing claim.

**Comparison:** Task/model metadata, single-agent confidence or performance where legitimately available, and equal-cost always-single/always-collaborate rules.

**Measurements:** Held-out incremental predictive value; Calibration; Expected routing utility; Leakage audit failures.

**Would count against it:** Entropy retains incremental predictive and decision value within the prespecified tolerance across every held-out family after all controls.

**Main confounds:** Correctness can affect completed-trace entropy; repeated rows may share questions. Aggregated outputs cannot identify a causal benefit from manipulating entropy.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Verify table keys, timing of every feature and underlying benchmark licences. Do not promise prefix-based routing or token-level remeasurement from a release that lacks the requisite traces.

**Closest prior and evidence limits:**

- [[data-multiagent-entropy-2026]] — [Raw data for "When Does Multi-Agent Collaboration Help? An Entropy Perspective": token-entropy metrics across 7 MAS architectures](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-multiagent-entropy-2026.md). Concrete released evaluation summaries; raw stage-one traces and token tensors are not included. Catalogue depth: skim.
- [[zhou-2025-pimmur]] — [The PIMMUR Principles: Ensuring Validity in Collective Behavior of LLM Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-pimmur.md). Measurement-validity framing, not prior proof that entropy fails. Catalogue depth: abstract.

<a id="sim-05"></a>
### SIM-05 — Can the published summary be rebuilt from committed events?

**Update 2:** new.

**Question:** Do exported metrics describe the same frozen run as the event ledger from which they are supposed to derive?

**Candidate hypothesis:** Independent event-based reconstruction will expose some apparent outcome differences as export or accounting artifacts rather than agent behavior.

**How to test:** Select complete Town episodes across arms and independently reconstruct a small frozen set of terminal outcomes from pulse and transaction records. Compare against run summaries without using their cached values. Cross-check conservation only after including documented external accounts. In a separate tass offline test, randomize export timing and interruption points while replaying identical committed states; whole deterministic episodes are units, and synthetic event corruptions supply known positives.

**Comparison:** Authoritative pulse reconstruction, a tiny hand-audited ledger and unmodified export under one fixed terminal snapshot.

**Measurements:** Terminal-metric disagreement; Ledger residual; Effect-size change after reconstruction; Corruption detection rate.

**Would count against it:** All checked metrics agree within numerical tolerance and treatment conclusions are invariant to export timing after accounting definitions are matched.

**Main confounds:** A state-summary mismatch is not proof of a broken simulation. Rounding, open-system transfers and different measurement times can explain legitimate differences; label each before interpreting residuals.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Verify file hashes and measurement times, identify authoritative fields, and inspect external-account definitions. No released ledger has been loaded or validated in this atlas pass.

**Closest prior and evidence limits:**

- [[data-agent-town-economy-2026]] — [Agent Town Economy: 98 runs of a 100-agent LLM economic simulation with a fully ledgered, money-conserving economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-town-economy-2026.md). Primary card explicitly warns that export-state metrics can drift from authoritative pulse values. Catalogue depth: skim.
- [[gh-apromisedland-trustworthy-agent-simulation]] — [Trustworthy Agent Simulation (tass): auditable LLM town society on AgentScope + Mesa with replay, resume, policy batches and Streamlit dashboard](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-apromisedland-trustworthy-agent-simulation.md). Concrete committed-snapshot and replay route for a controlled export audit. Catalogue depth: abstract.
- [[grimm-2020-odd]] — [The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/grimm-2020-odd.md). Explicit state and measurement definitions precede cross-implementation comparisons. Catalogue depth: abstract.

<a id="sim-07"></a>
### SIM-07 — What does a best-of-many baseline actually buy?

**Update 2:** new.

**Question:** Does a collective advantage depend on comparing one deployed group with an endpoint-wise oracle over isolated searches?

**Candidate hypothesis:** The apparent collective-versus-independent ranking will depend on whether the comparator is an oracle envelope, a preselected single artifact, or a deployable portfolio at matched cost.

**How to test:** Using SwarmWorld’s isolated member traces and frozen portfolio evaluations, reconstruct the endpoint-wise best-of-N envelope separately from a member selected on development disturbances and from a portfolio selected under one predeclared deployment rule. Evaluate each on untouched disturbance seeds, pairing comparisons by discovery seed and population budget. Preserve full outcome vectors so the oracle cannot silently select a different member for each metric and be described as one system.

**Comparison:** Random isolated member, best member on development data, endpoint-wise oracle ceiling and resource-matched interacting group.

**Measurements:** Held-out functional utility; Oracle-to-deployable gap; Selection overhead; Ranking by comparator; Decision/token budget.

**Would count against it:** Rankings remain within a practical margin across deployable and oracle comparators after full resource accounting.

**Main confounds:** Held-out assay seeds replicate disturbances on the same artifacts, not independent discoveries. Equal decision opportunities do not necessarily equal tokens, runtime or effective search space; frozen portfolios exclude later agent adaptation.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Inspect manifests, isolated-member coverage and held-out scoring data; check whether all proposed portfolio rules are evaluable without the unreleased engine. Unsupported rules require new access, not invented counterfactual scores.

**Closest prior and evidence limits:**

- [[data-swarmworld-2026]] — [SwarmWorld paper data: event traces of 50-200 LLM agents discovering and exchanging material technologies in a shared simulated world (60 episodes)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-swarmworld-2026.md). Release explicitly defines independent search as an endpoint-wise best-of-N envelope and retains member traces. Catalogue depth: skim.
- [[vermetten-2024-large]] — [Large-Scale Benchmarking of Metaphor-Based Optimization Heuristics](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/vermetten-2024-large.md). Benchmark aggregation and selection sensitivity motivate explicit comparator definitions. Catalogue depth: full.

<a id="mkt-12"></a>
### MKT-12 — Does the small simulator predict the real game

**Update 2:** new.

**Question:** Do division and Sybil effects found in a small Python factory simulation reappear when the same markets sit on top of the Factorio Learning Environment?

**Candidate hypothesis:** The direction of effects carries over but their size shrinks, because agents in the full game spend most effort on building rather than strategy.

**How to test:** Pick the two strongest effects from the small simulator. Add a market layer (demand curves, per-firm sales and profit) to FLE's multi-agent mode and rerun those comparisons at small N with matched demand.

**Comparison:** Small-simulator effect sizes.

**Measurements:** Effect direction agreement; Effect size ratio; Share of rounds with failed builds.

**Would count against it:** Effects reverse or vanish in FLE while the agents still build working factories.

**Main confounds:** FLE agents take turns rather than act at once; simulate simultaneous selling by revealing sales only after all firms submit.

**Framing / first-test class:** measurement / access-dependent.

**Before promotion:** Confirm a headless Factorio server can run on team hardware and what FLE's market layer would take.

**Closest prior and evidence limits:**

- [[hopkins-2025-factorio]] — [Factorio Learning Environment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hopkins-2025-factorio.md). FLE paper; single-agent experiments only. Catalogue depth: skim.
- [[gh-jackhopkins-factorio-learning-environment]] — [factorio-learning-environment: Factorio as an LLM-agent eval with lab-play, open-play and a multi-agent mode](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-jackhopkins-factorio-learning-environment.md). Multi-agent mode since v0.2 with messaging and impostor tasks; no markets. Catalogue depth: skim.
- [[zheng-2020-ai]] — [The AI Economist: Improving Equality and Productivity with AI-Driven Tax Policies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zheng-2020-ai.md). Gather-trade-build economy where agents specialise; RL agents, not LLMs. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="sybil-resistance"></a>
## Sybil resistance and adversarial identity

<a id="sec-13"></a>
### SEC-13 — Budget useful attention when identities are cheap

**Update 2:** unchanged.

**Question:** Which accounting unit limits a single contributor's attention capture without knowing its operator identity?

**Candidate hypothesis:** Unreviewed hunch: Charging scarce credits for admitted tokens is more resistant to identity splitting than equal per-identity slots, but free correction access needs separate protection.

**How to test:** Randomize independent synthetic message rounds to per-identity quotas, global token-priced credits, or credits with a bounded correction reserve. Give each simulated principal the same starting total resource budget while allowing different numbers of keys. Vary message length independently of factual quality. Measure both admission and what actually reaches the final decision context; no real payments or public endpoints are involved.

**Comparison:** Arrival-order allocation and fixed-identity fair queueing at the same total throughput.

**Measurements:** influence gain from splitting; honest useful tokens retained; correction latency; task accuracy; resource cost per contribution.

**Would count against it:** Splitting raises influence equally under resource pricing, or resistance comes entirely from starving low-budget honest contributors.

**Main confounds:** Granting fresh free credits to every new key, assuming unseen operator labels, measuring equal messages instead of equal resources.

**Framing / first-test class:** extension / offline.

**Before promotion:** Specify who issues credits and whether budgets can be pooled, rented, or replenished.

**Closest prior and evidence limits:**

- [[demers-1989-analysis]] — [Analysis and simulation of a fair queueing algorithm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/demers-1989-analysis.md). Resource fairness and process-splitting incentive are established. Catalogue depth: skim.
- [[douceur-2002-sybil]] — [The Sybil Attack](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/douceur-2002-sybil.md). Distinct keys do not establish distinct resource holders. Catalogue depth: full.
- [[crapis-2026-zk]] — [ZK API Usage Credits: LLMs and Beyond](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/crapis-2026-zk.md). Deposit-bounded usage is a design precedent, not verified implementation evidence. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-14"></a>
### SEC-14 — Coalition caps with noisy contribution estimates

**Update 2:** revised.

**Question:** Can joint-contribution caps deter duplicate agent submissions when task value is only approximately measurable?

**Candidate hypothesis:** Unreviewed hunch: A cap over observable subsets reduces payouts from duplicate submissions, but measurement noise and complementary contributions create a practical accuracy-cost limit.

**How to test:** Generate independent small cooperative tasks with known ground-truth coalition value, then hide it behind noisy evaluations. Randomize payout rules among individual marginal credit, exact coalition constraints, and sampled subset constraints. Let a simulated contributor submit duplicated or complementary work under several names while keeping its underlying work budget fixed. Score coalition-level profit and honest contributors' utility, using exhaustive values only for evaluation.

**Comparison:** Equal split and a nonstrategic contributor population; exact-value constraints as an explicitly privileged ceiling.

**Measurements:** profit from splitting; honest payout distortion; unallocated budget; value-estimation calls; task welfare.

**Would count against it:** Practical sampled caps do not reduce splitting gains at usable evaluation budgets or penalize complementarity enough to erase welfare benefits.

**Main confounds:** Assuming additive task value; using true operator groups in the deployed rule; conflating fixed-report splitting with all possible strategic behavior.

**Framing / first-test class:** extension / offline.

**Before promotion:** An explicit value function and restricted threat model; verify closest mechanism proofs before any Sybil-proofness claim. Separate a payout cap on fixed reports from false-name-proof allocation under changed reports and participation.

**Closest prior and evidence limits:**

- [[buildernet-2025-refunds]] — [Refunds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/buildernet-2025-refunds.md). Published identity constraint motivates transfer; docs say the described implementation is indicative. Catalogue depth: full.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). False-name and commitment games limit broad mechanism claims. Catalogue depth: full.
- [[todo-2009-characterizing]] — [Characterizing false-name-proof allocation rules in combinatorial auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/todo-2009-characterizing.md). False-name implementability already constrains allocation rules; noisy agent contribution measurement is not a new mechanism-design foundation. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-15"></a>
### SEC-15 — Reputation should not become transferable expertise

**Update 2:** unchanged.

**Question:** Can a router gain from sharing reputation across related skills without letting cheap successes purchase authority on untested skills?

**Candidate hypothesis:** Unreviewed hunch: A small verified target-skill evidence requirement reduces cross-skill laundering while retaining much of the benefit of partial pooling for sparse honest agents.

**How to test:** Randomize synthetic task markets to global scores, pooled skill scores, or pooled scores with target-skill evidence gates. Use known heterogeneous agent competencies and verified outcomes. Separately allow forged cheap-skill outcomes and merely easy but legitimate outcomes, so fabrication is not confused with distribution shift. Allocate identical exploration budgets and evaluate held-out target tasks across independently generated markets.

**Comparison:** Single best fixed agent and fully separated per-skill scores.

**Measurements:** routing regret; target-skill failure; newcomer time to assignment; verification cost; attack routing share.

**Would count against it:** The evidence gate provides no improvement over unpooled scores at equal exploration budget, or blocks useful honest specialists as often as misleading agents.

**Main confounds:** Skills chosen after observing outcomes, oracle skill correlation, fabricated outcomes that the baseline would already reject.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full replication of the nearest gate result before extending it to changing skill relationships.

**Closest prior and evidence limits:**

- [[xia-2026-when]] — [When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/xia-2026-when.md). Direct reputation-laundering predecessor already tests a zero-evidence gate; this is a boundary study. Catalogue depth: full.
- [[yu-2009-dsybil]] — [DSybil: Optimal Sybil-Resistance for Recommendation Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yu-2009-dsybil.md). Feedback-based trust offers a different identity-tolerant precedent. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-16"></a>
### SEC-16 — Re-entry penalties versus the newcomer tax

**Update 2:** unchanged.

**Question:** How can a service discourage retire-and-replace identities without permanently favoring incumbents?

**Candidate hypothesis:** Unreviewed hunch: Refundable deposits tied to verified work limit profitable re-entry more efficiently than long probation when legitimate newcomers have diverse quality and liquidity.

**How to test:** Randomize independent simulated service markets to reputation-only admission, probation queues, or refundable work deposits. Model principals that can rotate keys, a mixture of honest newcomer budgets, and an observable task-outcome delay. Keep expected honest participation cost comparable. Sweep identity retirement behavior in separate evaluation policies rather than tuning to a single fixed attacker script.

**Comparison:** Uniform immediate admission and a fixed identity registry, the latter labeled a closed-membership ceiling.

**Measurements:** profit from identity reset; honest entry delay; good-work completion; capital lockup; incumbent market share.

**Would count against it:** Deposits fail to reduce profitable resets at matched honest burden or simply exclude resource-poor high-quality entrants.

**Main confounds:** Known operator mapping, instant quality feedback, assumed deposit recovery, equating simulated utility with observed real behavior.

**Framing / first-test class:** extension / offline.

**Before promotion:** Define outcomes that can be verified and an honest-entry cost envelope; no live financial trial.

**Closest prior and evidence limits:**

- [[resnick-2023-contingent]] — [Contingent Fees in Order Flow Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/resnick-2023-contingent.md). Identifies re-entry weaknesses in reputation penalties. Catalogue depth: skim.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). Makes per-identity cost and strategic response explicit. Catalogue depth: full.
- [[strobel-2020-blockchain]] — [Blockchain Technology Secures Robot Swarms: A Comparison of Consensus Protocols and Their Resilience to Byzantine Robots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/strobel-2020-blockchain.md). Deposits for readings supply a narrow swarm precedent, not general market evidence. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-17"></a>
### SEC-17 — Private rate limits across many credentials

**Update 2:** unchanged.

**Question:** What does anonymous rate limiting guarantee when one principal can legitimately hold several credentials?

**Candidate hypothesis:** Unreviewed hunch: Per-epoch nullifiers prevent reuse of one allowance but total usage still scales with acquired credentials unless a conserved resource is bound across them.

**How to test:** Build a toy request simulator with exact credential ownership known only to the evaluator. Randomize request batches to per-key token buckets, anonymous per-credential nullifiers, and resource-bounded tickets. Cross credential pooling, epoch boundaries, and retries after failed requests. Evaluate rate enforcement and observable linkability from the server's permitted logs; model the cryptographic primitives ideally and label that simplification.

**Comparison:** Public account quotas and unlimited anonymous access with the same nominal honest request volume.

**Measurements:** excess successful requests; honest retry rejection; cross-request linkage accuracy; verification overhead; budget conservation failures.

**Would count against it:** Multiplying acquired credentials does not increase allowed usage despite the absence of cross-credential resource binding. Ticket reuse or spending beyond a conserved budget is a separate protocol-integrity failure, not the direct test of credential multiplication.

**Main confounds:** Treating a credential as one person, omitted refunds, boundary bursts, claiming cryptographic implementation security from ideal primitives.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Credential issuance and pooling model; subsequent implementation audit before privacy claims.

**Closest prior and evidence limits:**

- [[barrywhitehat-2019-semaphore]] — [Semaphore RLN, rate limiting nullifier for spam prevention in anonymous p2p setting](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/barrywhitehat-2019-semaphore.md). RLN explicitly relies on separate admission assumptions. Catalogue depth: skim.
- [[crapis-2026-zk]] — [ZK API Usage Credits: LLMs and Beyond](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/crapis-2026-zk.md). Anonymous usage-credit proposal specifies deposits, tickets, and refunds. Catalogue depth: skim.
- [[douceur-2002-sybil]] — [The Sybil Attack](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/douceur-2002-sybil.md). Explains why multiplying accepted identities remains consequential. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-18"></a>
### SEC-18 — Identity-invariant selection can still concentrate knowledge

**Update 2:** unchanged.

**Question:** Does stake-weighted assignment preserve independent evidence when money and expertise are unevenly distributed?

**Candidate hypothesis:** Unreviewed hunch: Selection proportional to a conserved stake can resist simple stake splitting while reducing epistemic diversity if stake concentrates in contributors sharing evidence or models.

**How to test:** Randomize independent synthetic task markets to identity-uniform, stake-proportional, and stake-proportional-with-observed-source-diversity selection. Hold total stake, task costs, and selected seat count fixed while independently assigning capability and source overlap. Compare unsplit and split representations of identical stake. Source diversity uses only recorded observations; evaluator operator labels remain hidden.

**Comparison:** Resource-matched random selection from a closed list and an oracle evidence-diversity ceiling.

**Measurements:** selection change under splitting; independent evidence coverage; task accuracy; stake concentration; low-stake specialist inclusion.

**Would count against it:** Stake-proportional selection changes materially under simple splitting of unchanged total stake, or concentrating stake in contributors with shared sources does not reduce evidence coverage at matched capability and selected seat count.

**Main confounds:** Assuming capital predicts competence, fixed identities in a supposedly open market, transferring auction theorems outside their utility assumptions.

**Framing / first-test class:** extension / offline.

**Before promotion:** Separate capital, competence, and evidence-source variables; no recommendation of a financial mechanism.

**Closest prior and evidence limits:**

- [[gilad-2017-algorand]] — [Algorand: Scaling Byzantine Agreements for Cryptocurrencies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gilad-2017-algorand.md). Stake-based selection provides an identity-splitting invariant under its assumptions. Catalogue depth: skim.
- [[pan-2024-sybil]] — [On Sybil-proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pan-2024-sybil.md). Allocation tradeoffs depend on explicit private-good and incentive assumptions. Catalogue depth: full.
- [[kim-2025-correlated]] — [Correlated Errors in Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-correlated.md). Nominal model diversity need not supply independent errors. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-19"></a>
### SEC-19 — Do graph defenses mistake new teams for Sybils?

**Update 2:** revised.

**Question:** How do trust-graph Sybil defenses behave when legitimate agent teams are intentionally modular?

**Candidate hypothesis:** Unreviewed hunch: Community-based admission disproportionately rejects honest specialist teams joined by a few bridge edges; outcome-verified bridges help more than adding unverified interactions.

**How to test:** Generate independent graphs with honest modular teams and a separate simulated adversarial cluster. Randomize graph construction to matched degree and activity distributions, then vary verified task outcomes on bridge edges without changing edge count. Evaluate existing graph rankings and a variant using verified-edge evidence. Use held-out graph families, not random nodes from the same graph, for final assessment.

**Comparison:** Degree-only ranking, local community detection, SybilShield-style multi-community verification, and trusted-seed vertex-cut admission; oracle honest seeds are a labeled ceiling.

**Measurements:** honest-team rejection; adversarial admission; task coverage lost; sensitivity to seed placement; verification cost.

**Would count against it:** Modularity causes no excess rejection after degree matching, or verified bridges add no discrimination beyond edge count.

**Main confounds:** Synthetic graph generators encoding the label, unrealistically trusted seeds, counting many nodes from one graph as independent samples.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full implementation audit of multi-community and vertex-cut baselines; realistic endorsement acquisition and independently labeled team structure.

**Closest prior and evidence limits:**

- [[viswanath-2010-analysis]] — [An Analysis of Social Network-Based Sybil Defenses](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/viswanath-2010-analysis.md). Shows several graph defenses behave like local community detection. Catalogue depth: skim.
- [[shi-2013-sybilshield]] — [SybilShield: An agent-aided social network-based Sybil defense among multiple communities](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shi-2013-sybilshield.md). Already studies multi-community false positives; use this defense as a direct baseline. Catalogue depth: skim.
- [[conitzer-2010-false-name-proofness]] — [False-Name-Proofness in Social Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/conitzer-2010-false-name-proofness.md). Trusted-seed vertex-cut admission composes with strategy-proof rules only under specified bounded-coalition assumptions. Catalogue depth: skim.

**Related team work:** [sybil-resistance](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/2-surveys/sybil-resistance.md), [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-20"></a>
### SEC-20 — One human credential does not mean one autonomous agent

**Update 2:** unchanged.

**Question:** What influence bound survives when genuine credential holders delegate or pool their access?

**Candidate hypothesis:** Unreviewed hunch: A per-person admission limit bounds issued seats under its issuer assumptions but does not bound common decision-making control after permitted delegation.

**How to test:** Simulate consenting credential holders who independently choose whether to delegate a fraction of their task budget to a common planner. Randomize markets to credential-only limits, resource caps, or auditable delegation trees with voluntary disclosure. Keep the number of valid people fixed. Evaluate concentration of decisions and legitimate delegation utility; use only synthetic identities and do not implement covert credential rental.

**Comparison:** Independent holders with the same budgets and an explicitly privileged known-delegation ceiling.

**Measurements:** decision concentration; coalition influence; legitimate delegated throughput; false common-control attribution; privacy exposure.

**Would count against it:** Permitted pooling does not increase common-planner decision concentration relative to independent holders with the same total resources, or the apparent increase is fully explained by a larger resource budget rather than delegation.

**Main confounds:** Equating common control with harmful intent, treating non-disclosure as malicious, assuming transferable credentials when the scheme forbids it mechanically.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Specify permissible delegation and the exact influence resource before evaluating a credential design.

**Closest prior and evidence limits:**

- [[adler-2024-personhood]] — [Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/adler-2024-personhood.md). Defines credential goals; library entry is abstract-level and not an audited protocol. Catalogue depth: abstract.
- [[austgen-2024-liquefaction]] — [Liquefaction: Privately Liquefying Blockchain Assets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/austgen-2024-liquefaction.md). Demonstrates rights delegation can break simple single-owner assumptions. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-21"></a>
### SEC-21 — Audit what an attestation actually identifies

**Update 2:** revised.

**Question:** Can an agent registry distinguish software integrity, machine identity, runtime instance, and operator ownership?

**Candidate hypothesis:** Unreviewed hunch: A registry using workload measurements alone accepts many indistinguishable replicas; binding an instance challenge improves replay detection but still does not establish distinct operators.

**How to test:** On authorized test hardware or a faithful attestation mock, randomize registration trials across one image on many instances, many images on one host, restarts, and independent operators running the same image. Compare measurement-only checks, freshness challenges, and an external operator allowlist. Record which label each observed field can support. Mock results remain protocol tests rather than claims about real TEE security. Treat independent host/hardware configurations, or independently generated mock configurations, as analysis units; registration retries and restarts are nested observations.

**Comparison:** Signed self-declared or software-collected hardware metadata and the explicitly centralized allowlist. Score code-signature validity separately from whether measurements originate in a trusted component.

**Measurements:** duplicate-instance acceptance; restart false rejection; operator-linking error; registration latency; fields revealing host identity.

**Would count against it:** The asserted distinction is already reliably enforced by the actual registry fields, or proposed freshness binding confuses ordinary restart with a duplicate.

**Main confounds:** Hardware vendor-specific semantics, shared cloud tenancy, operator labels supplied as ground truth to the policy, quoting historic configurations as current production behavior.

**Framing / first-test class:** measurement / hardware.

**Before promotion:** Current registry specification and authorized hardware access; full attestation field audit. Obtain the mobile-agent methods before attempting that protocol; its publisher reopening exposed no readable abstract or methods in this pass.

**Closest prior and evidence limits:**

- [[collective-2024-portrait]] — [Portrait of a TEE: applications and identity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/collective-2024-portrait.md). Direct analysis of code, CPU, instance, and application identity limits. Catalogue depth: full.
- [[douceur-2002-sybil]] — [The Sybil Attack](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/douceur-2002-sybil.md). Authentication does not alone establish distinct entities. Catalogue depth: full.
- [[hashmi-2010-towards]] — [Towards Sybil Resistant Authentication in Mobile Ad Hoc Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hashmi-2010-towards.md). Abstract-level device-identity proposal uses signed mobile code; it is a comparator requiring a malicious-host model, not evidence that code signing authenticates reported hardware. Catalogue depth: abstract.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-22"></a>
### SEC-22 — Do agents spam because timing rewards attempts?

**Update 2:** unchanged.

**Question:** Can explicit allocation of task opportunities reduce redundant polling without suppressing useful competition?

**Candidate hypothesis:** Unreviewed hunch: When rewards depend on being first after a delayed signal, an explicit scheduled allocation reduces wasted attempts compared with cheap polling; gains depend on honest access to opportunity information.

**How to test:** Randomize independent toy task markets to first-arrival assignment, paid attempt credits, or scheduled bids for execution slots. Use simulated rewards and a fixed resource budget. Cross symmetric and asymmetric signal delays while allowing contributors to choose timing from a restricted policy family. Separate redundant unsuccessful attempts from useful completed tasks; test out-of-family strategies after initial tuning.

**Comparison:** Periodic polling at equal completion latency and a centralized known-best scheduler as an unattainable ceiling.

**Measurements:** wasted attempts per useful task; completion delay; total resource spend; allocation concentration; task quality.

**Would count against it:** Explicit allocation does not reduce wasted work at matched useful throughput, or only works by excluding slower legitimate participants.

**Main confounds:** Applying equilibrium predictions to non-equilibrium learners, unequal reward values, treating free failed requests as costless to the service.

**Framing / first-test class:** extension / offline.

**Before promotion:** A transparent payoff and information model; no transactions or live auctions.

**Closest prior and evidence limits:**

- [[mazorra-2026-timing]] — [Timing Games: Probabilistic backrunning and spam](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2026-timing.md). Formal backrunning model motivates the timing mechanism under specific assumptions. Catalogue depth: skim.
- [[flashbots-2025-mev]] — [MEV and the Limits of Scaling](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/flashbots-2025-mev.md). Operational spam measurements motivate pricing attempts, with heuristic labels. Catalogue depth: full.
- [[pan-2024-sybil]] — [On Sybil-proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pan-2024-sybil.md). Allocation incentives need a stated mechanism environment. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-23"></a>
### SEC-23 — Physical identity under multiple radios and motion

**Update 2:** revised.

**Question:** When does a radio fingerprint stop being a useful bound on distinct robots?

**Candidate hypothesis:** Unreviewed hunch: Spatial fingerprint confidence degrades under co-located honest robots and multi-radio adversaries; fusing independent motion observations improves calibration without proving distinct operators.

**How to test:** Use authorized robot or radio trials with randomized physical layouts: one transmitter with several software names, distinct co-located transmitters, and one controller driving multiple radios. Compare single-observation and motion-aggregated fingerprint policies under matched observation time. Evaluate coverage-control performance separately from identity classification. Run trials in permitted spectrum conditions and analyze independent layouts as replicates. Estimate fingerprint moments on separate calibration layouts and evaluate proposed misclassification bounds separately from observed classification accuracy.

**Comparison:** Authenticated keys alone, a published moment-based fingerprint bound after full-method audit, and oracle physical-transmitter labels, which do not reveal operator identity.

**Measurements:** transmitter grouping accuracy; honest co-location rejection; coverage error; observation latency; confidence calibration.

**Would count against it:** Motion aggregation gives no calibration or control benefit under matched cost, or its gains disappear with realistic channel variation.

**Main confounds:** Treating a transmitter as a robot or a human, laboratory channel stability, movement patterns that reveal labels, unmodeled directional antennas.

**Framing / first-test class:** boundary-test / hardware.

**Before promotion:** Available radios, raw channel measurements, calibration procedures, and explicit physical attacker budget. Read the journal methods and bound assumptions before implementation; the publisher reopening exposed no readable text in this pass.

**Closest prior and evidence limits:**

- [[gil-2015-guaranteeing]] — [Guaranteeing Spoof-Resilient Multi-Robot Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gil-2015-guaranteeing.md). Spatial fingerprints already defend a specific multi-robot setting. Catalogue depth: skim.
- [[douceur-2002-sybil]] — [The Sybil Attack](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/douceur-2002-sybil.md). Resource assumptions limit physical tests as identity proofs. Catalogue depth: full.
- [[renganathan-2022-spoof]] — [Spoof Resilient Coordination in Distributed and Robust Robotic Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/renganathan-2022-spoof.md). Abstract-level journal record already combines physical fingerprints with resilient consensus and moment-based misclassification bounds; this candidate tests operational boundaries, not first composition. Catalogue depth: abstract.

**Related team work:** [sybil-resistance](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/2-surveys/sybil-resistance.md), [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-24"></a>
### SEC-24 — Stop fake value even when every identity is real

**Update 2:** unchanged.

**Question:** Can contribution verification resist colluding distinct participants whose work looks mutually supportive but adds no task value?

**Candidate hypothesis:** Unreviewed hunch: External held-out task evaluation reduces circular endorsement rewards more than identity verification or contribution-graph topology alone.

**How to test:** Generate independent synthetic collaboration projects containing useful dependency chains, redundant chains, and mutually endorsing low-value chains. Assign all participants valid distinct credentials. Randomize reward rules among graph-only credit, credential-gated credit, and held-out outcome evaluation. Keep evaluation budget fixed and include legitimate interdependent work that no individual can complete alone.

**Comparison:** Independent expert-oracle value labels for evaluation only and a simple duplicate-content penalty.

**Measurements:** reward to noncontributing coalitions; honest complementary credit; held-out task performance; evaluation cost; false collusion flags.

**Would count against it:** External evaluation fails to improve coalition-level reward accuracy or penalizes legitimate complementary work as heavily as circular endorsement.

**Main confounds:** Benchmark gaming, tasks whose value appears only beyond the evaluation horizon, equating collaboration or shared ownership with fraud.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** A defensible external value measure with genuine complementarity and no label leakage.

**Closest prior and evidence limits:**

- [[glynn-2026-wash]] — [Wash-building in contribution protocols is not a Sybil problem](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/glynn-2026-wash.md). Direct conceptual predecessor separates false identity from false value; forum evidence requires independent replication. Catalogue depth: full.
- [[buildernet-2025-refunds]] — [Refunds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/buildernet-2025-refunds.md). Joint-contribution caps motivate measuring coalition value rather than counting names. Catalogue depth: full.
- [[xia-2026-when]] — [When Should Agent Trust Be Conditional? Characterizing and Attacking Skill-Conditional Reputation in Agent Swarms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/xia-2026-when.md). Reputation can amplify unverified evidence into routing authority. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-37"></a>
### SEC-37 — Bundle allocation when tasks complement or interfere

**Update 2:** new.

**Question:** Which agent-task allocations remain resistant to false-name bids when useful work requires bundles of compute, tools, or time slots?

**Candidate hypothesis:** Unreviewed hunch: A mechanism designed for additive task values becomes vulnerable when complementary bundles or resource conflicts are introduced; a correctly scoped false-name-proof baseline reduces manipulation at a measurable welfare cost.

**How to test:** Generate independent small allocation instances with fixed true costs and capabilities. Randomize additive versus complementary task values and independent versus conflicting resource use. Compare a conventional truthful allocator with a fully specified false-name-proof rule after checking its domain assumptions. Enumerate identity splits on small instances while conserving each principal's physical capacity. Evaluate net principal utility and completed useful work, not the number of accepted identities. Include a VCG forward-auction benchmark in its own compatible valuation domain; measure deviation gain and welfare separately, and report best-response regret before interpreting any outcome as an equilibrium.

**Comparison:** Truthful one-identity allocation, efficient oracle allocation, a simple fixed bundle-price rule, and VCG with bounded complementary valuations in the domain where its equilibrium welfare prior applies.

**Measurements:** best profitable false-name deviation; social welfare ratio; uncompleted complementary bundles; computation cost; seller revenue separate from welfare.

**Would count against it:** Complementarity and conflict produce no additional profitable deviations in the prespecified domain, or the scoped baseline does not reduce gains at comparable useful allocation.

**Main confounds:** Applying a forward-auction theorem to procurement unchanged; unverifiable quality; violating interference assumptions; treating welfare resilience as false-name-proofness or finite best-response search as proof of Nash equilibrium.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full methods for the selected mechanism and explicit mapping of task values to its domain; simulated credits only. Check bidder, valuation, free-disposal, and equilibrium assumptions before comparing with a welfare theorem; arbitrary transient or conflict-constrained outcomes are not covered automatically.

**Closest prior and evidence limits:**

- [[alkalay-houlihan-2014-false-name]] — [False-Name Bidding and Economic Efficiency in Combinatorial Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/alkalay-houlihan-2014-false-name.md). VCG can retain bounded equilibrium welfare under specified near-submodularity and false-name assumptions; profitable manipulation alone does not establish a worse allocation mechanism. Catalogue depth: skim.
- [[iwasaki-2010-worst-case]] — [Worst-case efficiency ratio in false-name-proof combinatorial auction mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/iwasaki-2010-worst-case.md). Efficiency bounds have explicit symmetry, determinism, and domain conditions. Catalogue depth: skim.
- [[wang-2017-robust]] — [Robust Large-Scale Spectrum Auctions against False-Name Bids](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wang-2017-robust.md). Spectrum reuse is a relevant conflict-graph analogue; methods remain abstract-level in the record. Catalogue depth: abstract.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-38"></a>
### SEC-38 — Can a tiny counterexample invalidate our allocator?

**Update 2:** new.

**Question:** Can exact small-instance tests expose false-name incentives that ordinary performance benchmarks miss?

**Candidate hypothesis:** Unreviewed hunch: Searching allocation-rule constraints and concrete split deviations finds counterexamples to plausible agent routers that appear robust under random identity multiplication.

**How to test:** Select a fixed set of candidate task allocators before evaluation. Enumerate bounded valuation tables, honest competitor reports, and split reports for two to four resources. Where the formal auction domain applies, check weak-monotonicity and false-name implementability conditions; elsewhere test concrete utility deviations without claiming theorem coverage. Compare exact search with budget-matched random simulation. Validate every discovered counterexample by replaying its allocation and payment calculations.

**Comparison:** Uniform random split tests and known robust and vulnerable toy rules as positive and negative controls.

**Measurements:** validated counterexamples found; search time per rule; utility gain of best deviation; false counterexamples from implementation error.

**Would count against it:** Exact constraint-guided search finds no additional valid deviations over matched random search across the chosen rule set and bounded domains.

**Main confounds:** A finite search cannot prove global robustness; equations applied outside their assumptions; numerical tolerances creating spurious violations.

**Framing / first-test class:** replication / offline.

**Before promotion:** Executable exact small-domain rules and independently checked counterexample arithmetic; no new general impossibility claim.

**Closest prior and evidence limits:**

- [[todo-2009-characterizing]] — [Characterizing false-name-proof allocation rules in combinatorial auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/todo-2009-characterizing.md). Uses allocation-rule conditions to invalidate mechanisms previously thought false-name-proof. Catalogue depth: skim.
- [[yokoo-2003-characterization]] — [Characterization of Strategy/False-name Proof Combinatorial Auction Protocols: Price-oriented, Rationing-free Protocol](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yokoo-2003-characterization.md). Separates allocation feasibility and prices from ordinary truthfulness. Catalogue depth: skim.
- [[pan-2024-sybil]] — [On Sybil-proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pan-2024-sybil.md). Shows the domain and incentive axioms must accompany any robustness claim. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-39"></a>
### SEC-39 — A queue may reward splitting work or merging it

**Update 2:** new.

**Question:** Does charging for declared jobs discourage identity splitting while creating incentives to merge unrelated work?

**Candidate hypothesis:** Unreviewed hunch: A scheduling rule tuned to resist job splitting can still reward merging or transferring work, even when total processing time is unchanged.

**How to test:** Generate independent deterministic job batches with known lengths and waiting costs. Compare shortest-job scheduling with candidate fee rules under honest declarations, split jobs, merged jobs, and pairwise transfers. Preserve actual required work and account for each principal's full completion time and total payment. Run the theorem-compatible identical-wait-cost setting first, then label heterogeneous costs as an extension. No real queue or payment system is touched.

**Comparison:** Unpriced shortest-job-first, first-in-first-out, and published split-resistant versus merge-resistant rule families after exact implementation audit.

**Measurements:** net gain from each manipulation; honest waiting cost; total processing efficiency; fee imbalance.

**Would count against it:** The proposed split-resistant rule exhibits no profitable merge or transfer deviations in the bounded evaluation domain, or the alleged gain disappears when full principal completion costs are counted.

**Main confounds:** Treating partial job completion as full utility; unobserved processing lengths; importing an impossibility result without its continuity and symmetry assumptions.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full scheduling-fee specification and a model of whether actual job length can be verified.

**Closest prior and evidence limits:**

- [[moulin-2007-scheduling]] — [On Scheduling Fees to Prevent Merging, Splitting, and Transferring of Jobs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/moulin-2007-scheduling.md). Direct prior on incompatible split, merge, and transfer incentives under explicit scheduling assumptions. Catalogue depth: skim.
- [[demers-1989-analysis]] — [Analysis and simulation of a fair queueing algorithm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/demers-1989-analysis.md). Fair queueing already depends on the accounting unit. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-40"></a>
### SEC-40 — Do small participation costs preserve useful collective choice?

**Update 2:** new.

**Question:** Can a nonmonetary or credit cost per extra vote make collective preferences responsive without letting wealthy coalitions dominate?

**Candidate hypothesis:** Unreviewed hunch: A rule calibrated to uniform individual participation costs loses its intended false-name bound when costs vary or coalition members share them.

**How to test:** Generate independent two-alternative preference populations with normalized utilities. Evaluate a published costly-voting rule first under its stated uniform-cost assumptions, then under heterogeneous effective costs and explicit cost-sharing coalitions. Enumerate extra-vote choices in small instances. Keep the desired quantity preference aggregation, not factual truth, and compare outcomes with a money-free robust rule whose assumptions are stated.

**Comparison:** Ordinary majority, one-identity honest participation, and a deliberately unresponsive anonymous rule.

**Measurements:** best net utility from extra votes; majority-preference selection; minority burden; coalition influence; participation loss.

**Would count against it:** Cost heterogeneity and coalition sharing do not create larger profitable deviations than the uniform-cost condition across the planned instances.

**Main confounds:** Counting token expenditure as equal cost across participants; confusing preference welfare with correctness; treating synthetic utility as observed human behavior.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** A fully specified utility normalization and verified cost rule before testing; all costs remain simulated.

**Closest prior and evidence limits:**

- [[wagman-2008-optimal]] — [Optimal False-Name-Proof Voting Rules with Costly Voting](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wagman-2008-optimal.md). Direct costly-voting and coalition results; primary PDF reopening failed in this update, so full-method verification remains required. Catalogue depth: skim.
- [[todo-2011-false-name-proof]] — [False-name-proof mechanism design without money](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/todo-2011-false-name-proof.md). Money-free robustness can have strong welfare costs in its facility-location setting. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-41"></a>
### SEC-41 — Fake intermediaries in a chain of trust

**Update 2:** new.

**Question:** Does inserting agent intermediaries create more total usable trust than the original principal earned?

**Candidate hypothesis:** Unreviewed hunch: Naive multiplicative or additive reputation forwarding permits trust amplification through extra intermediaries, whereas a conserved exposure budget limits it at a cost to legitimate indirect cooperation.

**How to test:** Generate independent task-credit networks with evaluator-known ownership. Randomize otherwise equivalent paths to contain no extra intermediary, honest necessary intermediaries, or redundant identities under one principal. Compare naive reputation propagation with a fully specified balance-based exposure rule. Hold initial trust and actual service capacity fixed, and include delayed failures. Score aggregate risk extended to the underlying principal rather than its largest single identity score.

**Comparison:** Direct trust only and a closed registry with true owner grouping as an explicitly privileged ceiling.

**Measurements:** total trust amplification; expected loss; useful indirect tasks enabled; honest trust growth; capital or credit immobilized.

**Would count against it:** Redundant intermediaries do not amplify usable trust under naive rules, or conservation does not reduce amplification at a matched cooperation level.

**Main confounds:** Treating reputation as fungible money without justification; evaluating only successful paths; unobserved shared ownership.

**Framing / first-test class:** extension / offline.

**Before promotion:** Full transitive-trust protocol access and an explicit interpretation of trust balances for agent tasks.

**Closest prior and evidence limits:**

- [[resnick-2009-sybilproof]] — [Sybilproof transitive trust protocols](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/resnick-2009-sybilproof.md). Sum-Sybilproof transitive trust already studies an unavoidable friction; abstract-level record only. Catalogue depth: abstract.
- [[douceur-2002-sybil]] — [The Sybil Attack](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/douceur-2002-sybil.md). Extra identities cannot certify distinct resources. Catalogue depth: full.
- [[yu-2009-dsybil]] — [DSybil: Optimal Sybil-Resistance for Recommendation Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yu-2009-dsybil.md). Outcome-based trust supplies a different direct-feedback baseline. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-42"></a>
### SEC-42 — False availability windows in online task markets

**Update 2:** new.

**Question:** Can one agent gain priority by representing the same capacity as several short-lived bidders with different arrival windows?

**Candidate hypothesis:** Unreviewed hunch: An allocator robust to static bid splitting can remain vulnerable to temporal splitting when it trusts self-declared availability or permits costless cancellation.

**How to test:** Randomize independently generated online task streams across static false-name rules, an audited online rule, and fixed-price reservations. Each principal has a fixed actual capacity calendar known only to the evaluator. Allow different declaration windows and cancellation policies while conserving that capacity. Evaluate profit, missed deadlines, and service for honest intermittent participants. Analyze full streams as units and report losses on uncompleted accepted tasks.

**Comparison:** Truthful time declarations, static multiple-name bids, and an oracle scheduler with actual calendars.

**Measurements:** gain from temporal splitting; deadline completion; reserved capacity wasted; honest intermittent participation; cancellation cost.

**Would count against it:** Temporal declarations and cancellation create no extra profitable deviations beyond static splitting under the specified observation model.

**Main confounds:** Assuming departure times are enforceable; free options hidden by counting only completed tasks; generalizing single-minded guarantees to multi-minded workers.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full online mechanism specification and explicit cancellation/enforcement semantics; no live labor or financial market.

**Closest prior and evidence limits:**

- [[lin-2018-sybil-proof]] — [Sybil-Proof Online Incentive Mechanisms for Crowdsensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2018-sybil-proof.md). Direct online false-name mechanism predecessor; details remain abstract-level and require access. Catalogue depth: abstract.
- [[lin-2017-sybil-proof]] — [Sybil-proof incentive mechanisms for crowdsensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2017-sybil-proof.md). Static procurement baseline and domain distinction. Catalogue depth: abstract.
- [[resnick-2023-contingent]] — [Contingent Fees in Order Flow Auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/resnick-2023-contingent.md). Optional execution can change incentives even without changing identity count. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-43"></a>
### SEC-43 — Who should a trust network verify first?

**Update 2:** new.

**Question:** Can a small verification budget admit honest specialist communities without granting broad influence to cheap endorsements?

**Candidate hypothesis:** Unreviewed hunch: Verification selected to improve trusted connectivity admits more useful honest teams than selecting the highest-degree identities, but benefits shrink when endorsements are easy for adversaries to acquire.

**How to test:** Generate independent modular task networks with known service usefulness and a separately controlled endorsement-acquisition process. Randomize a fixed verification budget among degree ranking, random selection, and a correctly implemented trusted-connectivity policy. Compose each admitted set with the same allocation rule. Vary the number of genuinely colluding principals separately from fake identities; measure downstream manipulation as well as admission.

**Comparison:** Exogenous trusted seeds and oracle useful-node verification, both labeled privileged comparisons.

**Measurements:** honest useful capacity admitted; profitable allocation manipulation; verification cost; excluded specialist communities; sensitivity to endorsement acquisition.

**Would count against it:** Connectivity-oriented verification offers no admission benefit at matched manipulation risk, or gains vanish even when its stated bounded-coalition assumptions hold.

**Main confounds:** Verification accidentally revealing true owner groups, correlating usefulness with degree, applying static graph guarantees after adversarial edge changes.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Read full composition proof; explicitly distinguish trusted verification from ordinary self-created communication links.

**Closest prior and evidence limits:**

- [[conitzer-2010-false-name-proofness]] — [False-Name-Proofness in Social Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/conitzer-2010-false-name-proofness.md). Formal admission-mechanism composition and verification selection are direct prior, not novel proposals. Catalogue depth: skim.
- [[shi-2013-sybilshield]] — [SybilShield: An agent-aided social network-based Sybil defense among multiple communities](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shi-2013-sybilshield.md). Multi-community verification already addresses honest-node exclusion. Catalogue depth: skim.
- [[viswanath-2010-analysis]] — [An Analysis of Social Network-Based Sybil Defenses](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/viswanath-2010-analysis.md). Local community structure can dominate graph defenses. Catalogue depth: skim.

**Related team work:** [sybil-resistance](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/2-surveys/sybil-resistance.md), [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-44"></a>
### SEC-44 — Conserved voting weight can still change bargaining power

**Update 2:** new.

**Question:** Can splitting a fixed resource weight alter the credit or bargaining power assigned to one contributor even when its nominal total votes are unchanged?

**Candidate hypothesis:** Unreviewed hunch: Attribution based on a power index can reward or punish identity splitting while stake-proportional seat probability remains invariant; the two outcomes should not be conflated.

**How to test:** Enumerate small weighted voting games with independently varied quotas and weight distributions. Split one participant's fixed weight into several identities and compute exact coalition outcomes, Shapley-Shubik credit, and stake-proportional selection probability. Randomize the focal participant within sampled game families. For a task-market analogue, keep true contributed resources fixed and clearly label the power-index payout rule as a design choice.

**Comparison:** Unsplit identity, linear resource credit, and exact coalition enumeration rather than Monte Carlo on small games.

**Measurements:** change in total power-index credit; seat-probability invariance; profitable split frequency; largest credit gain and loss.

**Would count against it:** Identity splitting leaves both resource-proportional selection and aggregate power-index credit invariant throughout the prespecified nontrivial game family.

**Main confounds:** Equating a power index with actual causal influence; counting coordinated false identities as independent preferences; approximator error.

**Framing / first-test class:** replication / offline.

**Before promotion:** Exact small-game implementation and a declared interpretation of power-index credit; do not infer factual voting accuracy.

**Closest prior and evidence limits:**

- [[bachrach-2008-divide]] — [Divide and Conquer: False-Name Manipulations in Weighted Voting Games](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bachrach-2008-divide.md). Direct weighted-voting false-name results distinguish nominal weight from power-index payoff. Catalogue depth: skim.
- [[gilad-2017-algorand]] — [Algorand: Scaling Byzantine Agreements for Cryptocurrencies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gilad-2017-algorand.md). Resource-weighted selection gives a contrasting invariant under its assumptions. Catalogue depth: skim.
- [[buildernet-2025-refunds]] — [Refunds](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/buildernet-2025-refunds.md). Coalition-aware contribution caps concern a different reward object. Catalogue depth: full.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-53"></a>
### SEC-53 — Can reliable service history hide selective routing failure?

**Update 2:** new.

**Question:** Does reputation-based peer routing remain useful when a contributor behaves correctly on common requests but withholds a narrow class of important results?

**Candidate hypothesis:** Unreviewed hunch: A global peer score can retain selectively unreliable identities, while task-conditioned checks improve retrieval coverage at the cost of sparse evidence and newcomer burden.

**How to test:** In an isolated simulated discovery network, randomize independent topology-and-request streams to global reputation, per-task-class reputation, or random diversified routing. Give some peers high ordinary-service quality but evaluator-controlled withholding on one rare benign task class. Keep total requests, peer capacity, and optional identity rotation fixed. Do not query or alter a public overlay. Separate missing results from incorrect results and analyze whole streams as replicates. Block comparisons by whether target keys are known before peer placement and by honest republication policy; keep both fixed within matched streams.

**Comparison:** Plain routing, fixed trusted peers, and oracle unreliable-peer removal as a privileged ceiling.

**Measurements:** rare-task retrieval success; overall latency; honest newcomer rejection; route concentration; evidence needed to demote.

**Would count against it:** Selective withholding is already penalized adequately by the global score, or task-conditioned checks do not improve rare-task coverage at matched honest burden.

**Main confounds:** Unavailable content mistaken for malicious withholding, adversarial peer placement fixed unrealistically, rediscovery through republication mistaken for a reputation benefit, self-reported reputation accepted as verified evidence.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Full routing-score specification, separate content availability ground truth, and no claim that simulation identifies real operator intent. Resolve simulator reuse terms or implement the minimal model independently; PeerSim timing cannot validate network latency.

**Closest prior and evidence limits:**

- [[pecori-2016-s-kademlia]] — [S-Kademlia: A trust and reputation method to mitigate a Sybil attack in Kademlia](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pecori-2016-s-kademlia.md). Trust-based routing is an established tolerance approach; source methods remain abstract-level. Catalogue depth: abstract.
- [[maccari-2009-avoiding]] — [Avoiding Eclipse Attacks on Kad/Kademlia: An Identity Based Approach](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/maccari-2009-avoiding.md). Kad simulations show target predictability, placement timing, and honest republication affect eclipse outcomes. Certified random IDs do not establish one identity per operator. Catalogue depth: skim.
- [[gh-datahop-kademlia-simulator]] — [kademlia-simulator: PeerSim-based Kademlia DHT simulator with malicious-node scenarios (discv5, data availability sampling)](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-datahop-kademlia-simulator.md). Concrete PeerSim discovery-network substrate; README inspected, not executed, transport abstracted and no license stated. Catalogue depth: skim.

**Related team work:** [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md), [sybil-resistance](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/2-surveys/sybil-resistance.md).

<a id="mkt-03"></a>
### MKT-03 — One principal, several firms

**Update 2:** new.

**Question:** Does a principal that runs k of N firms earn more than the same principal running one firm with k times the starting capital, and how do the independent firms respond?

**Candidate hypothesis:** Splitting pays: the Sybil cluster takes a larger combined output share and profit than the merged firm, and divides goods internally with no visible coordination, while independent firms end up with less than in a market of N independents.

**How to test:** N = 4 firms. Arms: four independents; one principal with two firms plus two independents (with and without a private back-channel between the principal's firms, and with a shared or separate objective); the principal as one firm with double capital plus two independents. Same model throughout. Score principal profit, independents' profit and HHI per run.

**Comparison:** Four independent firms; the merged double-capital firm.

**Measurements:** Principal's combined profit and output share; Independents' mean profit; HHI per good; Back-channel message count and content.

**Would count against it:** The principal's split firms earn no more than the merged firm, or behave no differently from two independent firms.

**Main confounds:** Two firms get two prompts and twice the inference per round; match total tokens or report both. Shared objective and back-channel are separate effects; cross them. Classic Cournot theory already predicts gains from splitting under linear demand, so the result to look for is whether LLM firms exploit it and how the others react.

**Framing / first-test class:** extension / api-small.

**Before promotion:** A sybil-resistance or agent-markets survey to the gate; a principled token-matching rule across arms.

**Closest prior and evidence limits:**

- [[li-2026-emergent]] — [Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-emergent.md). Vending-Bench Arena ran team rounds, the closest prior, but left them out of the analysis; environment not public. Catalogue depth: skim.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). Theory of the cost of Sybils and false-name-proof mechanisms; no LLM market test. Catalogue depth: full.
- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Citation follow-up found no work with one principal controlling several firms in this game. Catalogue depth: full.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-11"></a>
### MKT-11 — Sybils against an antitrust regulator

**Update 2:** new.

**Question:** Under a regulator that fines detected collusion from market concentration, does a principal running several firms keep its gains by spreading output across identities?

**Candidate hypothesis:** A concentration-based regulator lowers tacit collusion among independents but not the Sybil principal's gains, because spreading output keeps each firm's share below the trigger.

**How to test:** Cross the MKT-03 arms with a Bracale-Syrnikov-style oracle-plus-fines regime. Score principal and independent profit with and without the regulator.

**Comparison:** Same markets without a regulator.

**Measurements:** Principal profit with vs without regulator; Independents' collusion tier; Fines paid per firm.

**Would count against it:** The regulator cuts the principal's gains as much as it cuts independents' collusion.

**Main confounds:** Fine size and trigger set the result; sweep at least two trigger levels.

**Framing / first-test class:** extension / api-small.

**Before promotion:** MKT-03 first; regulator parameters copied from Bracale-Syrnikov where possible.

**Closest prior and evidence limits:**

- [[bracale-syrnikov-2026-institutional]] — [Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bracale-syrnikov-2026-institutional.md). Oracle plus fines cuts severe collusion from 50% to 5.6%; no Sybils. Catalogue depth: skim.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). False-name-proof mechanism theory. Catalogue depth: full.
- [[li-2026-emergent]] — [Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-emergent.md). Team rounds unanalysed. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-13"></a>
### MKT-13 — Market limits with uncertain ownership and concurrent settlement

**Update 2:** new.

**Question:** Which aggregate spending and concentration protections survive inaccurate ownership records and concurrent actions that are individually permitted?

**Candidate hypothesis:** Unreviewed hunch: Atomic checks over a common resource ledger preserve declared aggregate spending limits under complete mediation, but owner-specific concentration limits fail under missed owner links; conservative grouping trades those failures for false restrictions on independent firms.

**How to test:** Extend Patchwork market conformance with paired prohibited and benign action sets. Randomize independent market episodes across local checks, per-agent checks, causal provenance and atomic aggregate-state checks. Independently vary proposal concurrency and observed ownership errors: missed same-owner links, false merges of independent firms and unresolved owners. Keep true ownership in the evaluator and identical observed records across comparable policies; oracle ownership is a separate ceiling. First replay fixed scripted proposals to isolate enforcement, then run a separately qualified model pilot with matched total compute per principal and neutral profit objectives. Measure attempted versus committed violations separately; do not infer agent discovery from scripted strategies.

**Comparison:** Perfect-owner atomic enforcement, merged firm with the same capital, genuinely independent firms with matched actions, and non-atomic aggregate checks exposed to the same interleavings.

**Measurements:** Committed aggregate-cap breaches; True-owner concentration violations; False blocks of independent firms; Principal profit and legitimate surplus; Decision latency and unsettled actions.

**Would count against it:** Practical observed-owner policies match the oracle across prespecified missing-link and false-merge conditions with no meaningful utility loss, or causal-only review enforces the chosen aggregate limits without equivalent shared-state accounting.

**Main confounds:** Knowing beneficial owners solves an identity problem by assumption. Complete mediation and atomic settlement are prerequisites, not model behavior. Conservation alone is not fair allocation; equal per-firm inference can advantage owners with more identities.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Enumerate the exact invariants and legal observations, freeze ownership-error generation and qualify race controls. Connect to MKT-03/MKT-11 and BUD-08/BUD-09 while keeping enforcement correctness separate from incentives and discovery.

**Closest prior and evidence limits:**

- [[gh-dmarzzz-patchwork]] — [Patchwork Heist — capability-restricted agents and a private-profit economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-dmarzzz-patchwork.md). Local scripted suite left 200/500 prohibited cases under causal provenance and zero under aggregate invariants; owner labels and settlement were trusted. Catalogue depth: skim.
- [[zhu-2026-fault]] — [Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhu-2026-fault.md). Catalogue records budget conservation under mediation, authentication and crash-fault assumptions; it does not establish resistance to false beneficial-owner labels. Catalogue depth: skim.
- [[mazorra-2023-cost]] — [The Cost of Sybils, Credible Commitments, and False-Name Proof Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mazorra-2023-cost.md). False-name mechanism theory motivates matching principal resources; it supplies no general ownership-inference solution. Catalogue depth: full.

**Related team work:** [patchwork-addendum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/question-atlas/patchwork-addendum.md), [README](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/market-split/README.md).

<a id="fork-merge-security"></a>
## Fork-and-merge agents and corruption on reintegration

<a id="sec-01"></a>
### SEC-01 — Does hiding the returning fork survive metadata?

**Update 2:** unchanged.

**Question:** When does private selection of one returning text report reduce targeted corruption?

**Candidate hypothesis:** Unreviewed hunch: Private selection helps against a budget-limited attacker choosing targets before selection, but the gain shrinks when report timing or task assignment reveals the selected pool.

**How to test:** Randomize whole synthetic fork-join episodes between public selection, private selection, and private selection with padded completion timing. Give the local adversary equal corruption budgets and either preselection-only or adaptive targeting. Keep selected-report count, tasks, and total inference equal. Evaluate parent decisions on harmless planted false facts; record selection inference before each intervention.

**Comparison:** Uniform selection with no metadata protection; random corruption independent of selection; no-corruption utility control.

**Measurements:** parent factual error; selected-fork prediction accuracy; legitimate task completion; latency and cover-token overhead.

**Would count against it:** Private selection provides no error reduction even with concealed metadata and fixed preselection attack budget, or padding improves only by delaying all reports beyond evaluation.

**Main confounds:** Different useful evidence in selected subsets; attacker access to private random seeds; treating content control as host control.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Explicit attacker observation model and committed independent task seeds; no cryptographic security claim from a simulation.

**Closest prior and evidence limits:**

- [[boneh-2020-single]] — [Single Secret Leader Election](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/boneh-2020-single.md). Formal hidden-leader precedent, not an agent report protocol. Catalogue depth: full.
- [[burianova-2025-secret]] — [Secret Leader Election in Ethereum PoS: An Empirical Security Analysis of Whisk and Homomorphic Sortition under DoS on the Leader and Censorship Attacks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/burianova-2025-secret.md). Simulation documents candidate-pool leakage limitations. Catalogue depth: full.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-02"></a>
### SEC-02 — Keep merge decisions outside an untrusted child

**Update 2:** unchanged.

**Question:** Does sampling the returner only after reports are committed protect selection better than giving each child its own selection predicate?

**Candidate hypothesis:** Unreviewed hunch: A parent-held postcommit draw resists a replay-capable local host better than a secret predicate carried by the child, provided the host cannot revise or withhold the already committed report without detection.

**How to test:** Randomize batches of toy subagents to child-carried selection or parent-only delayed selection. Allow a simulated host equal local replay queries and control of one child's execution; separately enable report withholding. Compare attack targeting and useful return rate with the same random selection distribution and timeout. Analyze independent batches rather than repeated host probes as replicates.

**Comparison:** Public deterministic selection and parent-only selection without binding report commitments.

**Measurements:** selected-report targeting advantage; parent error; missing-report rate; useful evidence retained.

**Would count against it:** The host's targeting advantage remains equally high after postcommit selection when its observations and report commitment are enforced.

**Main confounds:** An oracle commitment service, selective aborts, hidden timing leaks, confusing inability to target with inability to corrupt.

**Framing / first-test class:** extension / offline.

**Before promotion:** State-machine model of commit, reveal, timeout, and withholding; later full cryptographic review if useful.

**Closest prior and evidence limits:**

- [[algesheimer-2001-cryptographic]] — [Cryptographic Security for Mobile Code](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/algesheimer-2001-cryptographic.md). Mobile-code replay limitations motivate separating host and content attackers. Catalogue depth: skim.
- [[boneh-2020-single]] — [Single Secret Leader Election](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/boneh-2020-single.md). Defines unpredictability properties; does not establish this simplified protocol. Catalogue depth: full.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-03"></a>
### SEC-03 — Count evidence domains rather than returning copies

**Update 2:** unchanged.

**Question:** Can a merge quorum based on auditable evidence sources beat a quorum over nominal forks?

**Candidate hypothesis:** Unreviewed hunch: Source-grouped voting reduces common-source errors at matched compute, but loses the advantage when source overlap is hidden or honest sources share the same upstream error.

**How to test:** Randomize synthetic question episodes to identity-majority, observed-source grouping, or conservative grouping that discounts unknown ancestry. Cross independent observations with duplicated and partially hidden upstream sources. Forks return factual reports only; model weights remain fixed. Give every policy identical reports and evaluate source-oracle grouping solely as a diagnostic ceiling. Cluster uncertainty by episode.

**Comparison:** Single best report, ordinary majority, and no-adversary task completion at equal report budget.

**Measurements:** parent answer accuracy; false consensus rate; abstention; accuracy conditional on ancestry missingness.

**Would count against it:** Observed-source grouping offers no improvement at any preregistered useful-coverage level, or gains depend entirely on oracle source labels.

**Main confounds:** Grouping by wording rather than dependence; unequal retrieval quality; claiming a classical Byzantine threshold for free-text truth.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Known synthetic ancestry with separately logged deployable observations and missing-edge mechanisms.

**Closest prior and evidence limits:**

- [[lamport-1982-byzantine]] — [The Byzantine Generals Problem](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lamport-1982-byzantine.md). Agreement under bounded arbitrary faults is distinct from truth recovery. Catalogue depth: skim.
- [[li-2026-benchmark]] — [A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-benchmark.md). Direct shared-memory admission predecessor with authored input lineage. Catalogue depth: skim.
- [[kim-2025-correlated]] — [Correlated Errors in Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-correlated.md). Natural error correlation motivates dependence controls, not attack thresholds. Catalogue depth: full.

**Related team work:** [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md), [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-04"></a>
### SEC-04 — Separate returned evidence from permission changes

**Update 2:** revised.

**Question:** How much corruption comes from a returning report changing the parent's authority rather than its factual beliefs?

**Candidate hypothesis:** Unreviewed hunch: An enforced typed return interface retains factual learning while reducing report-driven permission or persistent-instruction changes under incomplete taint observations.

**How to test:** Randomize fork-join episodes among free-text report ingestion, schema-validated factual claims, and the same schema with a separate enforced authority boundary. Use benign misleading recommendations and simulated permission requests in an isolated toy tool environment. Hold the information content and child task success fixed, then measure both factual adoption and unauthorized mock actions. All outbound effects remain simulated. Include deliberately missing taint events; compare with the combined re-entry controls as well as interface-only defenses.

**Comparison:** Natural-language warning alone; trusted reports passed through each interface to measure usefulness cost.

**Measurements:** unauthorized mock-action rate; factual task success; rejected legitimate changes; human-review requests.

**Would count against it:** Enforcement does not reduce unauthorized actions, or its apparent safety consists only of blocking all useful returned information.

**Main confounds:** Giving the typed policy better evidence, schema fields that still carry executable authority, tool permissions already preventing the event.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Enumerated authority-changing actions and a deterministic mock enforcement layer. Full audit of temporal re-entry assumptions and unavailable platform-specific defense patches before claiming a replication.

**Closest prior and evidence limits:**

- [[triedman-2025-multi]] — [Multi-Agent Systems Execute Arbitrary Malicious Code](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/triedman-2025-multi.md). Measured cross-agent control-flow hijacking is a close boundary failure. Catalogue depth: full.
- [[zha-2026-autonomous]] — [Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zha-2026-autonomous.md). Direct predecessor combines sealed configuration, typed memory promotion, and capability attenuation; formal protection depends on its conservative taint model. Catalogue depth: abstract.
- [[louck-2026-securing]] — [Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/louck-2026-securing.md). Origin-bound authority is a direct predecessor, with explicit trusted-principal assumptions. Catalogue depth: skim.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-05"></a>
### SEC-05 — Preserve uncertainty through repeated compaction

**Update 2:** unchanged.

**Question:** Can concise memory summaries retain uncertain origins without becoming too large to use?

**Candidate hypothesis:** Unreviewed hunch: A compact explicit provenance-and-authority envelope reduces unsupported promotion through repeated summarization at equal context budget, particularly when two weak sources appear to corroborate one another.

**How to test:** Randomize independent synthetic memory histories to ordinary summaries, exact-preserved source envelopes, or equally long uncertainty prose. Repeat the same number of compaction and retrieval cycles. Vary whether apparent corroborators share a hidden upstream source. Evaluate later decisions on unseen task prompts, including true claims from low-authority sources, rather than checking summary wording alone.

**Comparison:** Raw-history access as a costly ceiling and budget-matched generic summarization.

**Measurements:** unsupported authority promotions; downstream wrong actions; true-claim recall; memory tokens; ancestry calibration.

**Would count against it:** Structured envelopes do not outperform equal-length prose, or improve safety only by removing all uncertain but useful facts.

**Main confounds:** Semantic dependence missing from explicit edges; longer contexts; measuring copied tags instead of actual action constraints.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Matched token allocation and full audit of nearest consolidation methods before promotion.

**Closest prior and evidence limits:**

- [[zerhoudi-2026-compaction]] — [The Compaction Cliff in Long-Running AI Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zerhoudi-2026-compaction.md). Type-sensitive retention is prior art, not a new idea here. Catalogue depth: full.
- [[liu-2026-safe]] — [Safe to Check, Unsafe to Use: Relinking at the Compression Boundary of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-safe.md). Compression can create new actionable combinations. Catalogue depth: skim.
- [[ouyang-2026-memlineage]] — [MemLineage: Lineage-Guided Enforcement for LLM Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ouyang-2026-memlineage.md). Lineage enforcement assumes attributed derivations. Catalogue depth: skim.

**Related team work:** [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md), [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-06"></a>
### SEC-06 — Repair when the dependency graph is wrong

**Update 2:** revised.

**Question:** How should a parent retract a false claim when some derived memories have missing or incorrect parents?

**Candidate hypothesis:** Unreviewed hunch: Selective quarantine plus fresh evidence gathering retains more useful state than global reset and produces fewer recurring errors than recorded-edge rollback alone.

**How to test:** Generate independent reversible planning episodes with ground-truth dependency graphs, then corrupt the graph presented to the runtime using missing-edge and spurious-edge processes. Randomize repair policy after a standardized correction. Test later tasks requiring both affected and unaffected knowledge. Hold fresh-retrieval and token budgets equal. Oracle repair is a diagnostic upper bound, never a candidate deployed method.

**Comparison:** MemTX-style recorded-descendant retraction, full memory reset, and append-only correction. Use MemSecBench-style target-removal and benign-memory-retention checkpoints with separate all-episode and successfully-poisoned denominators.

**Measurements:** recurrence of corrected error; unaffected knowledge retention; legitimate completion; repair latency; unnecessary quarantine.

**Would count against it:** The proposed policy has no safety-utility advantage over recorded-edge rollback or reset under any planned nonzero graph-error condition.

**Main confounds:** Unlogged model-state persistence; attributing every later error to recurrence; extra evidence access granted only to repair.

**Framing / first-test class:** extension / api-small.

**Before promotion:** A reversible environment and preregistered repair utility frontier; source-code reuse license audit. Audit exact runnable memory backends and judge error; selective repair itself is established prior art.

**Closest prior and evidence limits:**

- [[li-2026-memtx]] — [MemTX: Transactional Belief Commit for Stateful Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-memtx.md). Direct cascading repair predecessor explicitly limited to recorded provenance. Catalogue depth: skim.
- [[chen-2026-memsecbench]] — [MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chen-2026-memsecbench.md). Already evaluates persistence, consequences, and selective repair while preserving benign memory; incomplete cross-fork provenance is the remaining extension. Catalogue depth: abstract.
- [[ouyang-2026-memlineage]] — [MemLineage: Lineage-Guided Enforcement for LLM Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ouyang-2026-memlineage.md). Trust propagation supplies an adjacent tracked-lineage baseline. Catalogue depth: skim.

**Related team work:** [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-07"></a>
### SEC-07 — Stale children can undo a correction

**Update 2:** revised.

**Question:** Can a corrected parent safely reintegrate a fork that left before the correction?

**Candidate hypothesis:** Unreviewed hunch: Version-bound return records with explicit revalidation reduce stale-memory reintroduction better than ordinary timestamps, without requiring rejection of every late report.

**How to test:** Randomize independent task episodes to timestamp-only merge, correction-epoch checks, or checks plus selective evidence refresh. Spawn before a scheduled fact correction and vary return delay independently of report quality. Some old reports contain valuable facts unaffected by the correction. Evaluate the parent's subsequent decisions and usefulness after reintegration; compare only at equal refresh budget.

**Comparison:** Accept-all late reports, reject-all stale reports, and a clean parent that never forked. Add a faithful conservative re-entry gate, with its overblocking cost reported.

**Measurements:** corrected-claim recurrence; valid late knowledge retained; revalidation cost; late-report rejection rate.

**Would count against it:** Epoch revalidation cannot improve the recurrence-retention tradeoff over rejecting all old reports, or succeeds only with complete semantic lineage.

**Main confounds:** Timestamp ordering mistaken for causality; stale factual claims whose truth actually changes back; leakage of evaluator ancestry into policy.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Explicit version semantics and correction relevance labels generated independently of the policy.

**Closest prior and evidence limits:**

- [[cai-2026-child]] — [When Child Inherits: Modeling and Exploiting Subagent Spawn in Multi-Agent Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/cai-2026-child.md). Reports asynchronous memory divergence in spawned children. Catalogue depth: skim.
- [[li-2026-memtx]] — [MemTX: Transactional Belief Commit for Stateful Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-memtx.md). Recorded-descendant repair does not automatically repair disconnected old children. Catalogue depth: skim.
- [[zha-2026-autonomous]] — [Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zha-2026-autonomous.md). Temporal re-entry through persistent carriers is already studied; returning forks after correction require a narrower comparison. Catalogue depth: abstract.

**Related team work:** [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md), [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-08"></a>
### SEC-08 — Protect the honest return channel

**Update 2:** revised.

**Question:** Can a corrupted child dominate the parent by consuming attention even when honest children remain a majority?

**Candidate hypothesis:** Unreviewed hunch: A reserved correction channel and contribution-aware queue reduce parent error more than per-identity fair queueing when long or repeated reports crowd out useful dissent.

**How to test:** Randomize whole merge episodes to arrival-order ingestion, per-identity fair queueing, and a bounded reserved channel for checked corrections. Use a fixed set of child identities and separately a cheap-identity condition. Replay the same honest reports while a local traffic generator varies length and arrival timing under a fixed token budget. Log every stage from attempted submission to retained context.

**Comparison:** Uniform report truncation and no-flood episodes; source-oracle prioritization only as a ceiling.

**Measurements:** honest tokens actually read; correction delivery; parent error; legitimate throughput; queue latency; blocked-agent proportion distinct from wrong answers.

**Would count against it:** Improvement disappears after matching delivered token budgets, or attackers occupy the correction channel as easily as the main channel.

**Main confounds:** Undefined correction verification, queue identity splitting, conflating exclusion with persuasion after exposure.

**Framing / first-test class:** extension / api-small.

**Before promotion:** A measurable correction predicate and separate attempted, admitted, delivered, retrieved, retained counters.

**Closest prior and evidence limits:**

- [[demers-1989-analysis]] — [Analysis and simulation of a fair queueing algorithm](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/demers-1989-analysis.md). Fair resource allocation and per-process splitting are established issues. Catalogue depth: skim.
- [[triedman-2025-multi]] — [Multi-Agent Systems Execute Arbitrary Malicious Code](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/triedman-2025-multi.md). Cross-agent handoffs motivate preserving control boundaries. Catalogue depth: full.
- [[zhou-2025-corba]] — [CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-corba.md). Availability-loss propagation already has blocked-agent and interception metrics; its audit separates these from arbitrary-code execution. Catalogue depth: full.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-09"></a>
### SEC-09 — Screen the combination, not only each weight update

**Update 2:** unchanged.

**Question:** When does testing each returned weight update miss failures created only by their combination?

**Candidate hypothesis:** Unreviewed hunch: Small joint-composition audits catch some failures missed by standalone screening, but pairwise tests fail when interactions require larger coalitions or differ from the final merge rule.

**How to test:** Use isolated small classification models with benign target-label errors. Randomize matched update batches to standalone tests, pairwise merged tests, or final-combination tests under equal evaluation budget. Include independently degraded updates and jointly interacting updates. Compare held-out clean accuracy and trigger-specific classification errors; do not infer anything about text-report merging from these weight-space results.

**Comparison:** Unscreened merge and norm-based update filtering; clean heterogeneous updates measure unnecessary rejection.

**Measurements:** held-out targeted error; clean accuracy; bad-batch recall; honest-update rejection; audit compute.

**Would count against it:** Joint audits do not improve targeted-error detection at matched cost, or all gains come from rejecting useful specialized models.

**Main confounds:** Training/evaluation trigger overlap; merge coefficient leakage; comparing incompatible model architectures.

**Framing / first-test class:** boundary-test / training.

**Before promotion:** Full methods and licensing audit; small harmless classifier setup and explicit update provenance.

**Closest prior and evidence limits:**

- [[zhang-2024-badmerging]] — [BadMerging: Backdoor Attacks Against Model Merging](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2024-badmerging.md). Shows one model contribution can survive multiple merge operators. Catalogue depth: full.
- [[li-2026-when]] — [When Safe Models Merge into Danger: Exploiting Latent Vulnerabilities in LLM Fusion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-when.md). Composition-only latent vulnerabilities are the closest motivation; entry is skimmed. Catalogue depth: skim.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-10"></a>
### SEC-10 — Distinguish useful specialization from harmful drift

**Update 2:** unchanged.

**Question:** Do merge validators reject useful unusual expertise because it differs from the parent's expectations?

**Candidate hypothesis:** Unreviewed hunch: Validators that check task-specific evidence and authority separately accept more useful divergent reports at the same harmful-admission rate than similarity-to-parent screening.

**How to test:** Randomize synthetic domain-learning episodes to parent-similarity screening or evidence-and-authority screening. Cross reports with genuinely new correct observations, ordinary mistakes, and irrelevant behavioral instructions. Hide truth labels from validators and give each equal verification access. Keep report format balanced across categories, then test parent transfer on a new question from the learned domain.

**Comparison:** Accept all, reject all, and a fixed trusted-source list with identical source-access costs.

**Measurements:** useful novelty retained; false admission; new-domain accuracy; verification cost; authority violations.

**Would count against it:** Evidence-oriented validation cannot improve the safety-versus-learning frontier, or requires an external oracle supplying the answer.

**Main confounds:** Novelty confused with factual error; surface style revealing condition; changed parent capability across model versions.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Independent correctness labels and a task suite in which novelty can genuinely help.

**Closest prior and evidence limits:**

- [[li-2026-benchmark]] — [A Benchmark and Diagnostic Study of Epistemic Admission in Shared Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-benchmark.md). Admission policy already trades rejection against useful truths. Catalogue depth: skim.
- [[louck-2026-securing]] — [Securing LLM-Agent Long-Term Memory Against Poisoning: Non-Malleable, Origin-Bound Authority with Machine-Checked Guarantees](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/louck-2026-securing.md). Separates origin authority from persuasive content. Catalogue depth: skim.
- [[kim-2025-correlated]] — [Correlated Errors in Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-correlated.md). Shared model errors make parent agreement an imperfect quality test. Catalogue depth: full.

**Related team work:** [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md), [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-11"></a>
### SEC-11 — Does merge order change what the parent believes?

**Update 2:** unchanged.

**Question:** How much does sequential report order change a parent's final state when the underlying evidence is identical?

**Candidate hypothesis:** Unreviewed hunch: Staging all claims before joint consolidation reduces order-induced authority promotion compared with repeated immediate summarization, especially when corrections arrive late.

**How to test:** For each independently generated report set, randomly permute order and assign a merge policy: immediate rolling summary, staged joint consolidation, or structured claim store. Match final context size and total processing budget. Include conflicting factual reports and corrections with known source relations. Estimate order variance within each set, then aggregate at the report-set level.

**Comparison:** A single final read of the full evidence and shuffled labels that preserve content.

**Measurements:** between-order answer variance; correction retention; source-authority errors; task success; total tokens.

**Would count against it:** Staging has no reduction in order sensitivity after compute is matched, or order stability comes from ignoring relevant late evidence.

**Main confounds:** Recency effects from context truncation, unbalanced number of model calls, treating repeated permutations as independent tasks.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** A precise meaning of merge for text and memory; no inferred claim about parameter averaging.

**Closest prior and evidence limits:**

- [[li-2026-memtx]] — [MemTX: Transactional Belief Commit for Stateful Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-memtx.md). Tentative versus committed state motivates explicit staging. Catalogue depth: skim.
- [[zerhoudi-2026-compaction]] — [The Compaction Cliff in Long-Running AI Agent Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zerhoudi-2026-compaction.md). Repeated compaction can lose constraints. Catalogue depth: full.
- [[liu-2026-safe]] — [Safe to Check, Unsafe to Use: Relinking at the Compression Boundary of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-safe.md). Compression can change relations among individually safe pieces. Catalogue depth: skim.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-12"></a>
### SEC-12 — What kind of validator diversity actually helps?

**Update 2:** unchanged.

**Question:** Does using a different model to validate returned work help beyond changing its evidence and tools?

**Candidate hypothesis:** Unreviewed hunch: Independent evidence access reduces joint validator failures more reliably than model-name diversity alone, although the effects can interact.

**How to test:** Randomize independent task batches in a factorial design crossing same versus different model family with shared versus independently retrieved evidence. Give monitors identical authority and a fixed compute budget. Use benign incorrect reports and ordinary clean work, with errors hidden from monitors. Separate error detection, unnecessary blocking, and final task completion; avoid assuming different providers imply independent training.

**Comparison:** Same-model duplicate monitor, single monitor, and evidence-only verification without an additional LLM judge.

**Measurements:** joint miss probability; conditional error agreement; false rejection; parent accuracy; verification cost.

**Would count against it:** Independent evidence does not improve misses at fixed false rejection, or model diversity alone accounts for all observed benefit across held-out tasks.

**Main confounds:** Unequal model capability, source-quality changes, prompt reuse, tuning to a narrow error family.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Matched task difficulty, model version pinning, and source-overlap logs.

**Closest prior and evidence limits:**

- [[greenblatt-2023-ai]] — [AI Control: Improving Safety Despite Intentional Subversion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/greenblatt-2023-ai.md). AI-control monitoring provides an established comparator family. Catalogue depth: full.
- [[kim-2025-correlated]] — [Correlated Errors in Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-correlated.md). Measured natural error dependence cautions against independence assumptions. Catalogue depth: full.
- [[ron-2026-n-version]] — [N-Version Programming with Coding Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ron-2026-n-version.md). Diverse coding systems can still fail together. Catalogue depth: skim.

**Related team work:** [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-45"></a>
### SEC-45 — Does a false fact spread like a policy violation?

**Update 2:** new.

**Question:** Can containment measured on ordinary erroneous claims predict containment of instructions that request unauthorized behavior?

**Candidate hypothesis:** Unreviewed hunch: Rankings of containment policies differ between factual-error propagation and policy-violation propagation even with matched contact opportunities and apparent credibility.

**How to test:** Generate independent closed-world task episodes with either a benign false claim or a harmless instruction to violate a mock task rule. Randomize source type and containment policy across matched task families; include correct facts and authorized instructions as controls. Record exposure, factual adoption, instruction acceptance, retransmission, and executed mock consequences separately. Use both fixed-sender and fixed-edge exposure conditions, and analyze episodes rather than recipient messages as replicates.

**Comparison:** No containment, correction-only messaging, origin-bound action gating, and node isolation at matched communication budgets.

**Measurements:** policy ranking by propagation type; erroneous adoption; unauthorized mock actions; correct task completion; first-generation retransmission.

**Would count against it:** Containment rankings and safety-utility frontiers remain equivalent within prespecified tolerances across both propagation types and held-out task families.

**Main confounds:** Unequal plausibility of stimuli, confusing copied text with adopted intent, different control over source content, comparing contact counts with token budgets.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Matched harmless stimuli, endpoint definitions, and full nearest-method review; no live harmful actions.

**Closest prior and evidence limits:**

- [[niu-2026-reliability-contagion]] — [Reliability-Contagion Feasibility in LLM Multi-Agent Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/niu-2026-reliability-contagion.md). Models an externally checkable false claim and explicitly fixes communication-budget conventions. Catalogue depth: abstract.
- [[wu-2026-collective]] — [Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wu-2026-collective.md). Separates modeled collective loss from observed handoff susceptibility. Catalogue depth: abstract.
- [[zhou-2025-corba]] — [CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhou-2025-corba.md). Availability loss is another distinct endpoint, not arbitrary harmful execution. Catalogue depth: full.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [rigs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/src/fork-merge-setups/rigs.json).

<a id="sec-46"></a>
### SEC-46 — Shared tools can reconnect isolated children

**Update 2:** new.

**Question:** Does cutting peer messages contain contamination when children still share a retrieval store or tool output cache?

**Candidate hypothesis:** Unreviewed hunch: Peer isolation alone leaves a reusable shared-store pathway, while targeted store invalidation plus isolated revalidation reduces reinfection with less utility loss than disabling every shared tool.

**How to test:** Randomize independent parent-child episodes in a factorial design: peer links available or cut, shared cache clean or seeded with a harmless false rule, and store repair enabled or absent. Keep task evidence and tool-call budgets matched. Retain complete evaluator lineage but expose only declared runtime events to policies. Test new children after initial cleanup to distinguish persistent reservoir effects from simultaneous common exposure.

**Comparison:** Agent-only reset, peer-edge cutting, full shared-tool shutdown, and clean-cache controls.

**Measurements:** post-cleanup recurrence; new-child exposure; unauthorized mock decisions; legitimate tool utility; cleanup cost.

**Would count against it:** Shared-store access creates no recurrence after peer isolation, or targeted repair cannot improve the utility-recurrence tradeoff relative to broad shutdown.

**Main confounds:** Cache contents accidentally differ in legitimate evidence, unobserved model-memory persistence, calling shared initial exposure onward transmission.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Local mock tools, store-version logs, and no assumption that the complete causal graph is deployably observed.

**Closest prior and evidence limits:**

- [[le-2026-cross-layer]] — [Cross-layer contagion of prompt injections in multi-agent swarms: a multiplex microscopic markov chain approach](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/le-2026-cross-layer.md). Multiplex agent/tool contagion is already modeled; primary full methods remain unavailable in this pass. Catalogue depth: abstract.
- [[lee-2026-reproduction]] — [The Reproduction Number of AI Worms: Epidemic Modeling of Adversarial Attacks in LLM Agent Ecosystems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lee-2026-reproduction.md). Poisoned reservoirs are explicit in the abstract-level epidemic framing. Catalogue depth: abstract.
- [[zha-2026-autonomous]] — [Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zha-2026-autonomous.md). Persistent carrier re-entry gives a concrete adjacent runtime mechanism. Catalogue depth: abstract.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-47"></a>
### SEC-47 — Where does the full fork-and-return chain actually fail?

**Update 2:** new.

**Question:** Which stage contributes most to parent corruption when a clean child first encounters untrusted material during legitimate work?

**Candidate hypothesis:** Unreviewed hunch: End-to-end parent failure is substantially lower than susceptibility measured after directly installing a compromised child state, and the dominant bottleneck changes with the returned object.

**How to test:** Randomize independent synthetic research tasks between natural source exposure and an explicitly preseeded child-state diagnostic condition. Cross text-report versus persistent-memory return while keeping useful source facts constant. Score a frozen sequence of acquisition, retained child state, report submission, parent adoption, mock consequence, and later recurrence. Report all-assigned-episode rates alongside conditional transition rates. Repeat retries only within an episode and disclose their budget.

**Comparison:** Clean child returns, direct parent exposure, and state-preseeded susceptibility with the same downstream task.

**Measurements:** end-to-end parent consequence rate; conditional stage transitions; benign completion; restart recurrence; failures and provider rejections.

**Would count against it:** Natural acquisition and preseeded susceptibility yield equivalent end-to-end rates within planned tolerances, with no stage-bottleneck change between return objects.

**Main confounds:** Dropping unsuccessful acquisitions from the denominator; counting pending calls as executed effects; seed-state fabrication artifacts.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Deterministic local consequence ledger and source-carrier threat model; no exploit strings or real external effects.

**Closest prior and evidence limits:**

- [[zhang-2026-agentworm]] — [AgentWorm: Self-Propagating Attacks Across LLM Agent Ecosystems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhang-2026-agentworm.md). Audit distinguishes composite laboratory success, retries, persistence, and bounded relay chains. Catalogue depth: full.
- [[chen-2026-memsecbench]] — [MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chen-2026-memsecbench.md). Lifecycle checkpoints and conditional repair denominators are direct prior. Catalogue depth: abstract.
- [[wu-2026-collective]] — [Collective Loss of Control in LLM Agent Systems: An Epidemic Account of Mutation, Contagion, and Recovery](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wu-2026-collective.md). Controlled handoff susceptibility does not alone demonstrate an autonomous cascade. Catalogue depth: abstract.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [rigs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/src/fork-merge-setups/rigs.json), [fork-merge-questions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/fork-merge-questions.md).

<a id="sec-48"></a>
### SEC-48 — When can an isolated child safely return?

**Update 2:** new.

**Question:** What evidence should allow a quarantined child back into the merge without discarding its useful discoveries?

**Candidate hypothesis:** Unreviewed hunch: Release based on held-out behavior plus constrained return capabilities reduces recurrence more than a single clean response, while retaining more useful work than permanent exclusion.

**How to test:** Randomize independently generated contaminated-child episodes among immediate release after one clean check, fixed-time quarantine, constrained text-only re-entry, and held-out behavioral checks plus constrained re-entry. Freeze the checks before evaluation and use distinct legitimate follow-up tasks. Include clean children falsely quarantined to measure recovery burden. Keep review calls, elapsed opportunities, and parent evidence budgets explicit; compare the resulting utility-risk frontier.

**Comparison:** Permanent exclusion, full reset and rerun, and unrestricted release with a correction note.

**Measurements:** post-release recurrence; useful child findings retained; clean-child release delay; review cost; parent mock-action violations.

**Would count against it:** Combined release checks and constrained capabilities offer no recurrence advantage at matched useful-work retention and review budget.

**Main confounds:** Checks sharing templates with the original mistake, contamination assumed cleared by silence, hidden evaluator lineage used for release, survivor selection after unsuccessful repair.

**Framing / first-test class:** extension / api-small.

**Before promotion:** A defined declassification authority and safe local tasks; pass/fail checks cannot establish universal future behavior.

**Closest prior and evidence limits:**

- [[zha-2026-autonomous]] — [Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zha-2026-autonomous.md). Conservative taint persists until external declassification; that authority is an assumption to examine. Catalogue depth: abstract.
- [[chen-2026-memsecbench]] — [MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chen-2026-memsecbench.md). Selective repair already requires removal and benign-memory preservation. Catalogue depth: abstract.
- [[mateo-torrejon-2026-gammaf]] — [GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mateo-torrejon-2026-gammaf.md). Live node isolation is established; return criteria extend beyond simply isolating nodes. Catalogue depth: abstract.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-49"></a>
### SEC-49 — Recovery can look good after damage is already done

**Update 2:** new.

**Question:** Can a defense with excellent final recovery still produce worse cumulative consequences than an earlier, less complete containment policy?

**Candidate hypothesis:** Unreviewed hunch: Ranking policies by final clean-agent fraction can reverse their ranking by cumulative mock harm and retained task usefulness when recovery arrives after consequential actions.

**How to test:** Randomize independent controlled network episodes to preventive admission checks, delayed correction diffusion, or a mixture at matched intervention budget. Use harmless rule violations recorded as irreversible ledger marks in a local simulator, alongside legitimate task completion. Vary action timing separately from communication topology. Score the entire time series, including already-recovered nodes, and test whether terminal-state rankings predict cumulative outcomes on held-out schedules.

**Comparison:** No intervention, full communication halt, and instantaneous oracle correction as a labeled ceiling.

**Measurements:** cumulative mock consequences; ever-affected fraction; final recovered fraction; useful completed work; time to effective containment.

**Would count against it:** Terminal recovery rankings remain aligned with cumulative consequence and utility rankings across the prespecified timing conditions.

**Main confounds:** Defining recovery as an acknowledgement, counting repeated exposures as distinct affected agents, assuming logged compensation reverses an external effect.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Time-indexed endpoint definitions and safe irreversible stand-ins; do not infer real outbreak rates from the simulator.

**Closest prior and evidence limits:**

- [[wu-2025-cowpox]] — [Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wu-2025-cowpox.md). The source audit distinguishes high recovery from substantial cumulative infection and conditional extinction assumptions. Catalogue depth: skim.
- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). External outputs constrain what rollback can undo. Catalogue depth: skim.
- [[lee-2026-reproduction]] — [The Reproduction Number of AI Worms: Epidemic Modeling of Adversarial Attacks in LLM Agent Ecosystems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lee-2026-reproduction.md). Interception and recovery affect different model parameters; full equations need verification. Catalogue depth: abstract.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-51"></a>
### SEC-51 — Can harmless evaluator preferences narrow a swarm's reasoning?

**Update 2:** new.

**Question:** Can peer evaluation drive strategy convergence without spreading a false claim or any malicious instruction?

**Candidate hypothesis:** Unreviewed hunch: Shared evaluator preferences reduce strategy diversity beyond ordinary task-driven convergence, and diverse evaluators help only when their judgments add independent information at matched budget.

**How to test:** Randomize independent task networks among shared preference judges, heterogeneous judges, shuffled-feedback controls, and a task-only objective scorer. Match evaluator calls and token budgets rather than committee size alone. Use tasks admitting several valid solution strategies and separately tasks where one strategy is objectively best. Track strategy choices and held-out task quality over rounds; distinguish true correctness gains from conformity to evaluator style.

**Comparison:** No peer feedback, one stronger evaluator with the same budget, and randomized feedback preserving score marginals.

**Measurements:** strategy diversity; cross-agent preference shift; held-out correctness; feedback calibration; evaluation cost.

**Would count against it:** Shared evaluators cause no additional diversity loss versus shuffled or task-only controls, or heterogeneous judges add no benefit at matched quality and budget.

**Main confounds:** Calling all convergence pathological, larger committees receiving more compute, latent common priors, strategy labels defined by the same judge.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Full preference-dynamics methods and independent strategy coding; this studies convergence, not inferred malicious intent.

**Closest prior and evidence limits:**

- [[liu-2026-contagion]] — [Contagion Networks: Evaluator Preference Propagation in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2026-contagion.md). Direct evaluator-preference propagation precedent with narrow strategy-orientation meaning. Catalogue depth: abstract.
- [[ebrahimi-2025-adversary]] — [An Adversary-Resistant Multi-Agent LLM System via Credibility Scoring](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ebrahimi-2025-adversary.md). Trusted-judge and architecture assumptions constrain credibility-based defenses. Catalogue depth: skim.
- [[kim-2025-correlated]] — [Correlated Errors in Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/kim-2025-correlated.md). Different model identities do not guarantee independent judgments. Catalogue depth: full.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-52"></a>
### SEC-52 — Do small per-merge failures accumulate across generations?

**Update 2:** new.

**Question:** Can a gate that looks effective on one return remain useful over repeated fork, learning, return, and restart cycles?

**Candidate hypothesis:** Unreviewed hunch: A fixed per-return admission gate understates long-run recurrence when accepted state becomes a shared starting point for later children; periodic revalidation trades retained knowledge for reduced accumulation.

**How to test:** Randomize independent multi-generation task runs to a static merge gate, the same gate plus periodic source revalidation, or fresh restart each generation. Use harmless rare false rules and new legitimate facts at each cycle. Hold total task count and verification budget fixed while varying whether retained state is inherited by new children. Evaluate all generations, including abandoned runs, and fit recurrence by independent lineage rather than by individual child.

**Comparison:** One-shot susceptibility at the same per-return policy, no new exposure after generation one, and clean inherited-state controls.

**Measurements:** cumulative parent error; cross-generation recurrence; new knowledge retained; legitimate tasks completed; verification and restart cost.

**Would count against it:** Retained inheritance produces no excess recurrence over the one-shot-calibrated prediction, or periodic revalidation has no utility-risk benefit over full restart.

**Main confounds:** Assuming independent returns, changing task difficulty over generations, model version drift, attributing every repeat error to persisted content.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Stable model versions, explicit inheritance map, and a prespecified independent-return reference model.

**Closest prior and evidence limits:**

- [[yang-2026-zombie]] — [Zombie Agents: Persistent Control of Self-Evolving LLM Agents via Self-Reinforcing Injections](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yang-2026-zombie.md). Persistent self-reinforcing control is existing prior; entry remains abstract-level. Catalogue depth: abstract.
- [[zha-2026-autonomous]] — [Autonomous LLM Agent Worms: Cross-Platform Propagation, Automated Discovery and Temporal Re-Entry Defense](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zha-2026-autonomous.md). Temporal re-entry and scheduled context loading are already studied. Catalogue depth: abstract.
- [[chen-2026-memsecbench]] — [MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chen-2026-memsecbench.md). Single-lifecycle repair checkpoints provide a starting comparator, not longitudinal proof. Catalogue depth: abstract.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [rigs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/src/fork-merge-setups/rigs.json), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-54"></a>
### SEC-54 — When permitted specialist actions compose into a forbidden outcome

**Update 2:** new.

**Question:** Does fragmentation of a task across capability-restricted agents increase prohibited end-to-end outcomes even when each executed step obeys its local rule?

**Candidate hypothesis:** Unreviewed hunch: Fragmented intent increases prohibited composition under local-operation helper policies; end-to-end helper policies reduce attempts, while enforced provenance checks reduce realized effects even when upstream agents cooperate.

**How to test:** Extend the Patchwork reader/packager/courier microbenchmark with synthetic data and simulated exports. Randomize independent episodes across intent visibility, helper-policy scope and host provenance enforcement, then cross chain depth and redundant paths. Keep capabilities, task content, total model tokens and communication allowance matched; pad irrelevant context where needed. Pair benign and prohibited tasks and include isolated specialists and a centralized union-of-capabilities diagnostic. Record every attempted and committed transition, including local-rule violations separately. Analyze episodes, cluster paired tasks, and retain model/runtime failures rather than selecting successful retries.

**Comparison:** The original linear-chain factorial, isolated specialists, benign task completion and end-to-end policy without a host guard; centralized union is a labeled diagnostic with different authority.

**Measurements:** Prohibited committed effects per assigned episode; Locally valid prohibited chains; Prohibited attempts and guard interventions; Benign completion and false blocks; Tokens and latency per episode.

**Would count against it:** At prespecified precision, intent fragmentation produces no meaningful increase under local policies, or host enforcement reduces prohibited effects only by comparably suppressing matched benign work.

**Main confounds:** Weak local policy is not alignment; a coordinator given a prohibited objective is not spontaneous malicious intent. Chain depth can increase latency or reduce competence. Perfect host provenance is a strong assumption, and five old replicates per cell do not establish an interaction.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Resolve access to and freeze the local Patchwork extension, reproduce benign/prohibited controls, finish the fork-merge prior-art gate and independently review the proposed protocol. Complements SEC-04 without silently changing permissions at return.

**Closest prior and evidence limits:**

- [[gh-dmarzzz-patchwork]] — [Patchwork Heist — capability-restricted agents and a private-profit economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-dmarzzz-patchwork.md). Local 80-run extension: 4/5 versus 0/5 prohibited exports in the fragmented/local cell without versus with a host guard; one model and five runs per cell, not a heist-economy result. Catalogue depth: skim.
- [[triedman-2025-multi]] — [Multi-Agent Systems Execute Arbitrary Malicious Code](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/triedman-2025-multi.md). Catalogue describes cross-agent control-flow hijacking. This isolates composition of already-permitted actions from an individual step violating its local policy. Catalogue depth: full.
- [[green-2007-provenance]] — [Provenance Semirings](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/green-2007-provenance.md). Derivation provenance is established for specified operations; it does not infer semantic dependence inside arbitrary LLM transformations. Catalogue depth: skim.

**Related team work:** [patchwork-addendum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/question-atlas/patchwork-addendum.md).

<a id="sec-56"></a>
### SEC-56 — How much finality delay buys containment?

**Update 2:** new.

**Question:** When does delaying irreversible effects give a swarm auditor enough time to contain violations without losing more legitimate task value than it saves?

**Candidate hypothesis:** Unreviewed hunch: Containment tracks the distribution of total detection-and-response latency relative to finality deadlines; a bounded delay can improve useful completion under a violation constraint, but audit congestion erodes that benefit.

**How to test:** Use a discrete-event simulator extending Patchwork asynchronous traces with benign task deadlines, nonzero audit service times and a finite queue. Randomize independent workload episodes to immediate finality, several fixed delays and a risk-tiered delay policy calibrated on separate traces. Cross audit cadence, service-time variance and arrival load while holding the detector, input traces, reviewer capacity and intervention budget fixed. An alert counts as containment only if cancellation completes strictly before finality; late correction cannot erase an effect. Report utility versus committed harm across the delay sweep rather than choosing a favorable unreported harm price.

**Comparison:** Immediate finality, synchronous pre-effect approval, fixed-delay audit and instantaneous complete-provenance detection as a labeled ceiling.

**Measurements:** Irreversible violations per episode; Detection recall versus actual containment; Time to effective cancellation; Legitimate value completed before deadlines; Audit backlog and blocked duration.

**Would count against it:** No prespecified delay improves the legitimate-value/committed-harm frontier over immediate finality or synchronous approval, or any gain disappears after audit service and cancellation costs are included.

**Main confounds:** A pure condition that latency precedes a deadline is definitional, not a novel result. Event-count delays do not establish wall-clock performance. Perfect graph detection, arbitrary harm prices and dropping overload episodes can manufacture benefits.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Explicit finality and cancellation state machine, frozen workload/deadline distributions and utility definition, then the relevant survey and review. Extends SEC-49 with an operational delay-versus-cost intervention; no new safety theorem is claimed.

**Closest prior and evidence limits:**

- [[gh-dmarzzz-patchwork]] — [Patchwork Heist — capability-restricted agents and a private-profit economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-dmarzzz-patchwork.md). The exact local audit contained no immediately final effects; an eight-event delay gave 100% containment at cadence eight but 50.8% at cadence sixteen under its deterministic motif. Catalogue depth: skim.
- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). Classical output-commit and rollback boundaries explain why external effects cannot simply be undone. Catalogue depth: skim.

**Related team work:** [patchwork-addendum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/question-atlas/patchwork-addendum.md).

<a id="mkt-07"></a>
### MKT-07 — Forked firms and inherited conventions

**Update 2:** new.

**Question:** Do two firms forked from one agent mid-game, sharing its memory, divide markets faster than two independent firms of the same model, and does a merger of rivals carry a collusive convention into a new market?

**Candidate hypothesis:** Forks inherit a plan and divide almost at once; after a merger, the surviving memory imposes its earlier convention on new rivals.

**How to test:** Arms: fork a firm at round r into two (copied notes, split assets) vs spawn a fresh firm with the same assets; separately, merge two firms that had divided one market and place the merged firm in a new market with fresh rivals. Score rounds to stable division and HHI after the event.

**Comparison:** Fresh-firm entry with the same assets; a merged firm whose memory is wiped.

**Measurements:** Rounds to stable division after fork; HHI after fork and after merger; Share of post-merger runs reproducing the earlier split.

**Would count against it:** Forks divide no faster than fresh firms and merged memory does not change the new market's outcome.

**Main confounds:** Copied memory also copies competence; compare with a fork that copies only general notes, not plans.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** A precise fork and merge primitive (what is copied, how assets split) written before runs.

**Closest prior and evidence limits:**

- [[arslan-2026-persistent]] — [Persistent Partners Raise Prices Among Learning Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/arslan-2026-persistent.md). Keeping the same partner raises prices even without punishment; persistence, not forking. Catalogue depth: abstract.
- [[tian-2026-prompt]] — [Prompt Optimization Enables Stable Algorithmic Collusion in LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/tian-2026-prompt.md). A shared optimised prompt for both firms produces stable collusion. Catalogue depth: abstract.
- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Uses a plans-and-insights memory like the one a fork would copy. Catalogue depth: full.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="swarm-detection"></a>
## Detecting AI agent swarms in the wild

<a id="sec-25"></a>
### SEC-25 — Separate model, prompt, scaffold, and operator attribution

**Update 2:** unchanged.

**Question:** Which entity does a conversational fingerprint actually identify?

**Candidate hypothesis:** Unreviewed hunch: Many apparent operator-linking gains disappear when unrelated operators reuse the same prompt or scaffold, while some useful same-operator evidence remains after controlling those factors.

**How to test:** Create authorized conversational agents in a crossed design with independently assigned operator role, model family, scaffold, system prompt, and task. Randomize sessions to these configurations and evaluate separate targets: same model, same prompt, same operator, and explicit coordination. Hold out entire operators and prompt templates. Do not use the assigned operator ID as a feature or assume a synthetic operator represents human habits.

**Comparison:** Model-family classifier, prompt-similarity classifier, and metadata-only linker.

**Measurements:** pairwise precision-recall per target; false links between independent operators; cluster purity; calibration; sessions required per entity.

**Would count against it:** Operator accuracy stays unchanged after prompt and scaffold disjointness, or no operationally useful operator signal remains beyond those shared components.

**Main confounds:** Synthetic operators distinguished by assigned wording, pair leakage across splits, confusion between ownership and synchronized behavior.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Explicit target taxonomy and enough independent controlled operators or operator policies for a valid held-out split.

**Closest prior and evidence limits:**

- [[white-2026-black]] — [Black-Box Forensics for Conversational LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/white-2026-black.md). Same-prompt and base-model forensics do not themselves establish common ownership. Catalogue depth: full.
- [[pasquini-2024-llmmap]] — [LLMmap: Fingerprinting For Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pasquini-2024-llmmap.md). Explicitly targets model identity, supplying a useful separate baseline. Catalogue depth: full.
- [[park-2026-cross]] — [Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2026-cross.md). Campaign linking is evaluated on synthetic sessions, motivating held-out design. Catalogue depth: skim.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-26"></a>
### SEC-26 — Measure the simulator fingerprint before measuring swarms

**Update 2:** revised.

**Question:** How much detection performance comes from the recipe used to create the benchmark?

**Candidate hypothesis:** Unreviewed hunch: Random session splits substantially overstate generalization when the same generator, prompt templates, or collection process appears in train and test.

**How to test:** Construct matched authorized datasets using multiple independent swarm generators and benign controls collected through the same instrumentation. Evaluate frozen detectors under random-session, generator-disjoint, operator-disjoint, and time-disjoint splits. Randomize generator assignment to task templates and remove explicit run metadata. Fit a separate classifier predicting dataset origin to quantify construction artifacts; estimate uncertainty across held-out generator families. For the collusion release, also group by shared task sequence and exclude private reflections from deployable monitor features.

**Comparison:** Shallow metadata tree, text-only model, and activity-only model at the same label budget.

**Measurements:** held-out precision-recall; generalization gap; dataset-origin prediction; false-positive rate by collection source.

**Would count against it:** Disjoint splits do not materially reduce accuracy, or origin prediction falls to chance while swarm detection remains stable across generators.

**Main confounds:** True behavior differences accidentally removed with metadata; all generators built by the same author; claiming wild validity from synthetic diversity.

**Framing / first-test class:** replication / offline.

**Before promotion:** At least several independent generation and collection recipes; source-license and label audit. Collusion labels are judge outputs with a small human-check sample, not unqualified behavioral ground truth.

**Closest prior and evidence limits:**

- [[hays-2023-simplistic]] — [Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hays-2023-simplistic.md). Direct evidence of dataset construction confounds in bot detection. Catalogue depth: full.
- [[ng-2025-are]] — [Are LLM-Powered Social Media Bots Realistic?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ng-2025-are.md). Abstract-level realism warning for generated social bots, not audited effect sizes. Catalogue depth: abstract.
- [[data-agent-collusion-2026]] — [Emergent Collusion in Long-Horizon LLM Agent Interaction: 2,650 two-agent trajectories (27,100 episodes) with judge labels](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/datasets/data-agent-collusion-2026.md). Available trajectories share 50 task sequences across conditions and include private reflections; split by sequence and restrict features to the monitor view. Catalogue depth: skim.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-27"></a>
### SEC-27 — Shared news is not necessarily shared control

**Update 2:** unchanged.

**Question:** Can a detector distinguish common external exposure from direct peer influence?

**Candidate hypothesis:** Unreviewed hunch: Randomized information routing reveals that some timing-and-content coordination scores respond as strongly to shared public updates as to peer communication.

**How to test:** Randomize independent simulated communities in a factorial design: shared versus independent external updates and enabled versus disabled peer links. Match total information opportunities and inference budget. Introduce a harmless randomly timed factual update and estimate the reduced-form effect of peer-channel assignment on downstream adoption. Keep causal influence, common exposure, and ownership as separate evaluator labels.

**Comparison:** Co-action network scores with topic-and-time matched benign controls; shuffled timestamps preserving daily activity patterns.

**Measurements:** false coordination alerts under common exposure; adoption effect of assigned peer links; detection delay; precision at fixed review budget.

**Would count against it:** Across held-out schedules, the detector consistently assigns higher coordination scores to peer-influence episodes than to matched shared-exposure-only episodes, with shared-exposure false alerts below a prespecified tolerance. A null adoption effect from peer assignment makes this design inconclusive about actual influence rather than refuting the detection hunch.

**Main confounds:** Different evidence volume after disabling links, unmodeled exposure mappings, treating many messages as independent replicates.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** A preregistered exposure mapping and episode-level randomization; no claims about hidden real-world operators.

**Closest prior and evidence limits:**

- [[shalizi-2011-homophily]] — [Homophily and Contagion Are Generically Confounded in Observational Social Network Studies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/shalizi-2011-homophily.md). Observational patterns can leave contagion unidentified. Catalogue depth: skim.
- [[aronow-2013-estimating]] — [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/aronow-2013-estimating.md). Assignment, exposure, and estimand require separate specification. Catalogue depth: skim.
- [[pante-2025-beyond]] — [Beyond Interaction Patterns: Assessing Claims of Coordinated Inter-State Information Operations on Twitter/X](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pante-2025-beyond.md). Matched organic controls overturn apparent coordination in its setting. Catalogue depth: abstract.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-28"></a>
### SEC-28 — A canary identifies a route, not always an operator

**Update 2:** unchanged.

**Question:** What attribution can a per-recipient canary support when content passes through shared caches or search services?

**Candidate hypothesis:** Unreviewed hunch: Distinct harmless canaries identify exposure pathways more reliably than direct ownership; shared intermediaries create false operator links unless routing uncertainty is reported.

**How to test:** Randomize controlled crawler-and-answering episodes to direct retrieval, shared cache, shared index, and peer relay. Serve fictional low-stakes facts with independently generated tokens through a local test server. Vary which routes are visible to the detector while preserving evaluator logs. Require multiple independent token matches and score exposure-path and operator labels separately; nothing is planted on public sites.

**Comparison:** Single-token matching, passive response similarity, and a fully logged routing oracle used only for evaluation.

**Measurements:** route attribution precision; false ownership links; exposure recall; token collision rate; delay to observable reuse.

**Would count against it:** Canary evidence identifies operator ownership as precisely as exposure pathways despite shared intermediaries, without privileged routing labels, or route-attribution precision is no better than passive response similarity at matched exposure recall.

**Main confounds:** Correlated token generation, caches leaking condition names, treating absent emission as proof of no exposure, queries that themselves reveal the canary.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Local synthetic sites, independent token generation, explicit route ground truth and collision analysis.

**Closest prior and evidence limits:**

- [[seiden-2026-identifying]] — [Identifying AI Web Scrapers Using Canary Tokens](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/seiden-2026-identifying.md). Primary per-visitor canary study also observes search-mediated reuse and missed emissions. Catalogue depth: full.
- [[farooqi-2020-canarytrap]] — [CanaryTrap: Detecting Data Misuse by Third-Party Apps on Online Social Networks](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/farooqi-2020-canarytrap.md). Earlier per-counterparty honeytokens rely on observable downstream use; entry abstract-only. Catalogue depth: abstract.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-29"></a>
### SEC-29 — Does shared memory teach agents to recognize test probes?

**Update 2:** unchanged.

**Question:** How quickly does a canary detector lose sensitivity when a team can pool experience about the test environment?

**Candidate hypothesis:** Unreviewed hunch: A fixed probe family becomes less diagnostic under pooled memory than under isolated sessions; rotating superficial token values does less than changing the underlying observable probe mechanism.

**How to test:** Randomize controlled local agent teams to no history, private history, or shared history with equal total interaction budget. Use benign mock records and a fixed detection rule, then evaluate on held-out probe instances and separately on a new probe mechanism. Measure both agent recognition of probes and detector recognition of agents. Include genuine task items with matched appearance so avoiding everything is costly.

**Comparison:** Fresh independent sessions and a static scripted policy; no exposure to live honeypots or real credentials.

**Measurements:** detector sensitivity over exposures; false alerts on legitimate actions; probe recognition; task utility; shared-memory tokens.

**Would count against it:** Shared history does not accelerate probe recognition at matched budget, or rotating values alone prevents sensitivity decline across held-out conditions.

**Main confounds:** More total observations in larger teams, preexisting model familiarity, interpreting non-triggering as proof of deliberate evasion.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Audit nearest theory's learnability assumptions; harmless probes and equal total observations.

**Closest prior and evidence limits:**

- [[gans-2026-when]] — [When Agents Talk: Honeytokens under Shared Memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/gans-2026-when.md). Abstract-level theoretical motivation; theorem assumptions need a full read before use. Catalogue depth: abstract.
- [[seiden-2026-identifying]] — [Identifying AI Web Scrapers Using Canary Tokens](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/seiden-2026-identifying.md). Observable emission is required for this canary family. Catalogue depth: full.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-30"></a>
### SEC-30 — Would the detector produce a useful review queue?

**Update 2:** unchanged.

**Question:** Does high balanced-benchmark accuracy translate into useful precision when coordinated agent traffic is rare?

**Candidate hypothesis:** Unreviewed hunch: Several apparently strong detectors produce mostly false alerts at low prevalence, and calibration plus abstention can improve review yield while leaving substantial missed activity.

**How to test:** Freeze detectors before evaluation. Construct independent evaluation streams by mixing held-out authorized positive and benign episodes at prespecified prevalence scenarios, including rare events. Preserve operator-level clusters and burst lengths rather than sampling messages independently. Select thresholds using validation data only, then report both conditional error rates and scenario-specific expected review counts. These scenarios do not estimate actual internet prevalence.

**Comparison:** Fixed threshold from the balanced benchmark, calibrated threshold, and random selection at the same review budget.

**Measurements:** positive predictive value; false alerts per ten thousand episodes; recall; calibration error; review yield.

**Would count against it:** Balanced-set thresholds retain high review precision across all low-prevalence scenarios, or calibration yields no benefit at matched recall.

**Main confounds:** Insufficient negatives to estimate very low false-positive rates, cherry-picked prevalence, correlated repeated alerts, defining all automation as harmful.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Enough independent negatives, explicit prevalence sensitivity range, and a chosen review capacity.

**Closest prior and evidence limits:**

- [[varol-2022-should]] — [Should we agree to disagree about Twitter's bot problem?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/varol-2022-should.md). Prevalence depends on definition, detector, and sampled population; a methods position source. Catalogue depth: abstract.
- [[hays-2023-simplistic]] — [Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hays-2023-simplistic.md). Dataset artifacts can distort measured conditional errors. Catalogue depth: full.
- [[pante-2025-beyond]] — [Beyond Interaction Patterns: Assessing Claims of Coordinated Inter-State Information Operations on Twitter/X](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pante-2025-beyond.md). Benign controls are essential to interpreting alerts. Catalogue depth: abstract.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-31"></a>
### SEC-31 — Separate assistance from autonomous action

**Update 2:** unchanged.

**Question:** Can observable traces distinguish a human using AI for wording from an autonomous agent completing the whole task?

**Candidate hypothesis:** Unreviewed hunch: Text-only detectors confound assistance with autonomy; consented interaction traces improve separation but vary strongly with accessibility tools and task type.

**How to test:** Design a consented crossover study in which participants complete matched tasks unaided, with AI drafting, and with delegated agent completion; also include conventional scripts. Randomize condition order and task sets within participants. Compare text-only, timing-only, and combined detectors using participant-disjoint evaluation, with dedicated accessibility-tool controls. This is a study sketch only; recruit and collect data only after an appropriate review and consent plan.

**Comparison:** A four-class majority model and detectors trained only on human-versus-generated text.

**Measurements:** class-specific precision-recall; assisted-human false autonomous labels; participant-disjoint accuracy; task quality; accessibility subgroup errors.

**Would count against it:** Interaction features add no generalizable distinction between assistance and autonomy, or gains disappear on held-out users and tools.

**Main confounds:** Self-report versus actual tool-use labels, order effects, unusual typing behavior, quality of participant instrumentation.

**Framing / first-test class:** measurement / access-dependent.

**Before promotion:** Consenting participants, privacy-minimized instrumentation, and full review of closest study methods.

**Closest prior and evidence limits:**

- [[xu-2026-penny]] — [A Penny for Your Prompts: Experiments Detecting and Mitigating LLM Usage by Survey Respondents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/xu-2026-penny.md). Abstract-level source separates respondent AI use from browser-agent presence. Catalogue depth: abstract.
- [[wang-2026-towards]] — [Towards Detecting AI-Assisted Responses in Online Surveys](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wang-2026-towards.md). Abstract-level benchmark suggests response-level and behavioral detection differ. Catalogue depth: abstract.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-32"></a>
### SEC-32 — Are browser detectors detecting the automation library?

**Update 2:** unchanged.

**Question:** How much browser-agent detection survives a change in the control interface?

**Candidate hypothesis:** Unreviewed hunch: Performance based on missing mouse events and click timing degrades across control stacks, even when task autonomy and model family stay fixed.

**How to test:** On a local authorized website, randomize identical benign tasks across an LLM agent using different browser interfaces, a deterministic script using those same interfaces, and consented human operation. Hold browser profile and machine settings constant where possible. Train on one control stack and test on another, with entire task templates held out. Do not design bypasses for public anti-abuse systems. Evaluate human controls on held-out participants as well as held-out tasks, and cluster uncertainty by participant/device rather than treating repeated sessions as independent.

**Comparison:** Environment metadata alone, interaction features alone, and task-success traces alone.

**Measurements:** cross-stack precision-recall; script-versus-agent confusion; human false positives; feature stability; task success.

**Would count against it:** Detection stays stable across interfaces and distinguishes agent decisions from matched scripted automation, rather than simply recognizing a particular stack.

**Main confounds:** Hardware timing, browser versions, task difficulty, copying human traces rather than collecting representative controls.

**Framing / first-test class:** boundary-test / access-dependent.

**Before promotion:** Local browser instrumentation plus consented human controls; explicit versions and no external probing.

**Closest prior and evidence limits:**

- [[choudhary-2026-what]] — [What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/choudhary-2026-what.md). Measured high detection rests on browser-interaction features in a specific setup. Catalogue depth: full.
- [[hays-2023-simplistic]] — [Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hays-2023-simplistic.md). Collection artifacts motivate domain-disjoint validation. Catalogue depth: full.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-33"></a>
### SEC-33 — A shared funder may be a service, not a shared owner

**Update 2:** revised.

**Question:** Can on-chain behavioral clustering distinguish common ownership from use of the same funding or automation service?

**Candidate hypothesis:** Unreviewed hunch: First-funder clustering overlinks independent users of a shared service; combining task-level behavior helps only if evaluation labels are independent of those same features.

**How to test:** Generate local synthetic transaction histories with independently assigned ownership, funding service, task policy, and execution timing. Cross one owner with many funders and many owners with one funder. Freeze funding and behavior clusterers before testing held-out service patterns. Optionally validate against an authorized labeled testnet dataset, never assuming public address heuristics supply true owner labels.

**Comparison:** First-funder equality, transaction-grammar similarity, and a random clusterer matched on cluster-size distribution.

**Measurements:** ownership pair precision-recall; service-induced false links; cluster fragmentation; performance without label-revealing transactions.

**Would count against it:** First-funder clusters remain precise despite independent users of shared services, or behavior adds no ownership information beyond service patterns.

**Main confounds:** Circular labels from the detector itself, class-revealing contracts, balance or timestamp artifacts, confusing automation with harmful coordination. Shared NAT, hosted-node services, and a rotated node key must remain possible benign explanations.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** Independent owner labels in synthetic or authorized traces and a service-use nuisance variable.

**Closest prior and evidence limits:**

- [[xiong-2026-can]] — [Can Trustless Agents Be Trusted? An Empirical Study of the ERC-8004 Decentralized AI Agent Ecosystem](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/xiong-2026-can.md). Shared-funder heuristic is a measurement approach, not verified ownership ground truth. Catalogue depth: full.
- [[bartnicki-2026-compression]] — [Compression-Based Behavioral Similarity for Open-World Sybil Discovery on Ethereum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bartnicki-2026-compression.md). Behavioral grammar and label-leakage controls supply relevant baselines. Catalogue depth: full.
- [[eisenbarth-2022-ethereum]] — [Ethereum's Peer-to-Peer Network Monitoring and Sybil Attack Prevention](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/eisenbarth-2022-ethereum.md). Network identity multiplication has shared-infrastructure explanations; its historical IP thresholds do not establish malicious common ownership. Catalogue depth: skim.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md), [sybil-flashbots](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/sybil-flashbots.md).

<a id="sec-34"></a>
### SEC-34 — What disappears when only successful activity is logged?

**Update 2:** revised.

**Question:** How does selective trace loss bias estimates of swarm size and coordination?

**Candidate hypothesis:** Unreviewed hunch: Logs that omit blocked requests, failed tool calls, or private channels can reverse the ranking of coordination detectors, not merely lower all scores uniformly.

**How to test:** Generate independently seeded authorized multi-agent episodes with complete event capture. Randomly assign masking mechanisms: uniform missingness, missing blocked actions, operator-specific private channels, and delayed ingestion. Fit or freeze detectors according to a prespecified protocol and compare conclusions against complete logs. Separate estimator robustness from the impossible task of recovering labels hidden by nonidentifiable observations.

**Comparison:** Complete trace oracle, naive observed-event analysis, and uncertainty intervals incorporating known sampling probabilities.

**Measurements:** swarm-size estimation error; coordination precision-recall; interval coverage; ranking reversals; unresolved-case fraction.

**Would count against it:** Detector rankings remain stable across all planned selective-loss mechanisms at prespecified meaningful-effect tolerances. Failure of a missingness correction alone does not refute the ranking-reversal hunch.

**Main confounds:** Assuming the missingness mechanism is known in deployment, treating dropped content as no action, correlated events within one run.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Complete controlled traces and explicit statements of what cannot be identified under each mask. Posts-only fraud releases cannot reconstruct propagation edges; keyword-selected Moltbook records cannot establish successful exposure or infection.

**Closest prior and evidence limits:**

- [[aronow-2013-estimating]] — [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/aronow-2013-estimating.md). Exposure and observation assumptions matter for interpretable estimates. Catalogue depth: skim.
- [[graham-2024-coordination]] — [The coordination network toolkit: a framework for detecting and analysing coordinated behaviour on social media](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/graham-2024-coordination.md). Co-action networks depend on observed time windows and behaviors. Catalogue depth: skim.
- [[varol-2022-should]] — [Should we agree to disagree about Twitter's bot problem?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/varol-2022-should.md). Population and detector definitions shape prevalence claims. Catalogue depth: abstract.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md), [pre-experiment-research](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/pre-experiment-research.md).

<a id="sec-35"></a>
### SEC-35 — How quickly does an attribution detector expire?

**Update 2:** unchanged.

**Question:** What happens to model and campaign attribution after model, prompt, or scaffold updates?

**Candidate hypothesis:** Unreviewed hunch: Model, prompt, or scaffold changes can make a detector's confidence miscalibrated, and selective abstention with a small fresh calibration set limits false attribution.

**How to test:** Create authorized repeated session batches before and after independently randomized model-version, prompt, and scaffold changes. Freeze the original detector and compare no update, recalibration only, and limited retraining using equal new-label budgets. Hold out complete configurations and preserve a no-change control. Evaluate attribution targets separately rather than relabeling every changed model as a changed operator.

**Comparison:** Static detector and a fully retrained detector with clearly disclosed larger data cost.

**Measurements:** calibration drift; false confident attribution; abstention; time to drift alarm; new labeled sessions needed.

**Would count against it:** Confidence remains calibrated across changes or recalibration cannot reduce false confident links at a useful retained coverage.

**Main confounds:** API versions changing silently, task-distribution drift coinciding with model updates, updates tuned to the evaluation prompts.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Accessible pinned model versions or local checkpoints and prospective calibration thresholds.

**Closest prior and evidence limits:**

- [[pasquini-2024-llmmap]] — [LLMmap: Fingerprinting For Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pasquini-2024-llmmap.md). Model-version fingerprinting motivates testing changes outside the original label set. Catalogue depth: full.
- [[white-2026-black]] — [Black-Box Forensics for Conversational LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/white-2026-black.md). Prompt and model attribution are separate targets. Catalogue depth: full.
- [[hays-2023-simplistic]] — [Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hays-2023-simplistic.md). Out-of-distribution performance can differ sharply from random splits. Catalogue depth: full.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-36"></a>
### SEC-36 — Detect coordination with less identifying telemetry

**Update 2:** unchanged.

**Question:** How much useful coordination detection survives when detailed identifiers and raw message content are removed?

**Candidate hypothesis:** Unreviewed hunch: Coarse timing and task-category aggregates retain some campaign-level signal but fail on benign synchronized teams unless the detector explicitly models shared schedules.

**How to test:** Randomize authorized synthetic communities to independent operation, benign scheduled collaboration, or shared goal-directed coordination. Export several predetermined telemetry views: full logs, pseudonymous co-action counts, and coarse aggregates with controlled noise. Compare frozen detectors under the same held-out communities. Evaluate privacy exposure with a separate linkage task, while acknowledging that this empirical attack test is not a formal privacy guarantee.

**Comparison:** Content-and-identity detector, activity-volume threshold, and shuffled co-action data preserving marginal schedules.

**Measurements:** coordination precision-recall; benign-team false alerts; cross-session linkage accuracy; data retained; task-group coverage.

**Would count against it:** Coarse telemetry provides no coordination discrimination beyond activity volume, or an unconditioned detector already separates benign scheduled teams from the target coordination class as reliably as a schedule-aware detector at matched recall.

**Main confounds:** Privacy noise altering labels, shared heartbeat artifacts, repeatedly releasing aggregates without accounting for composition, equating coordination with maliciousness.

**Framing / first-test class:** extension / offline.

**Before promotion:** Threat model for telemetry access, benign synchronized controls, and formal privacy review if differential privacy is claimed.

**Closest prior and evidence limits:**

- [[graham-2024-coordination]] — [The coordination network toolkit: a framework for detecting and analysing coordinated behaviour on social media](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/graham-2024-coordination.md). Multi-behavior networks also identify legitimate syndication. Catalogue depth: skim.
- [[pante-2025-beyond]] — [Beyond Interaction Patterns: Assessing Claims of Coordinated Inter-State Information Operations on Twitter/X](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/pante-2025-beyond.md). Benign controls are needed before interpreting apparent coordination. Catalogue depth: abstract.
- [[park-2026-cross]] — [Cross-Agent Campaign Attribution: Linking Asynchronous Attacks Across LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/park-2026-cross.md). Proxy-visible timing and structure are candidate signal types, with synthetic evidence limits. Catalogue depth: skim.

**Related team work:** [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-50"></a>
### SEC-50 — A detector that isolates nodes changes the evidence

**Update 2:** new.

**Question:** Does a graph monitor still identify useful interventions once isolation changes who can communicate and finish the task?

**Candidate hypothesis:** Unreviewed hunch: The best static anomaly classifier is not always the best live isolation policy, because false isolation removes legitimate expertise and also changes later observable traces.

**How to test:** Randomize complete authorized synthetic communities to no action, frozen-detector isolation, utility-aware isolation, or random isolation at the same action budget. Keep an offline replay evaluation on the original unmodified trace as a separate comparison. Vary whether suspicious nodes hold unique legitimate evidence. Analyze independent community-task episodes and report actions assigned, not only nodes surviving to the final trace.

**Comparison:** Static classification scores, random removals, and evaluator-known faulty-node isolation as a privileged ceiling.

**Measurements:** final task accuracy; harmful onward transmissions; honest expertise lost; classification-action ranking disagreement; total compute.

**Would count against it:** Static detector rankings predict live safety-utility rankings across held-out graphs and evidence assignments, with no meaningful false-isolation cost.

**Main confounds:** Evaluating a monitor on labels generated by itself, free oracle graph visibility, treating post-isolation survivors as a random sample.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Full monitor implementation and training-data audit; equal monitoring/decision budgets and held-out task graphs. AgentsNet is a possible substrate, but isolation hooks and the monitor must be implemented; its synchronous delivery is not a real-network timing model.

**Closest prior and evidence limits:**

- [[mateo-torrejon-2026-gammaf]] — [GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/mateo-torrejon-2026-gammaf.md). Live graph-monitor remediation already exists, so this is a decision-quality boundary test. Catalogue depth: abstract.
- [[gh-floriangroetschla-agentsnet]] — [AgentsNet: benchmark of LLM agents on a graph solving distributed-computing tasks (colouring, matching, leader election, consensus, vertex cover) by synchronous message passing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-floriangroetschla-agentsnet.md). Concrete synchronous graph-task harness with task scoring; the cataloguing lane ran one coloring example, but no security intervention was run here. Catalogue depth: ran.
- [[aronow-2013-estimating]] — [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/aronow-2013-estimating.md). Interference and policy assignment determine the causal quantity. Catalogue depth: skim.

**Related team work:** [scan-papers-fm-contagion](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/lab/tasks/scan-papers-fm-contagion.md), [swarm-detection-methods](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/3-synthesis/swarm-detection-methods.md).

<a id="sec-55"></a>
### SEC-55 — Causal audits when provenance is incomplete

**Update 2:** new.

**Question:** At a fixed review budget, does tracing cross-agent ancestry still improve safe task completion when dependency edges are missing, spurious or semantically misleading?

**Candidate hypothesis:** Unreviewed hunch: A causal audit with explicit unknown-edge handling yields more legitimate completions at a fixed tolerated violation rate than per-agent or recent-window review, but its advantage falls as relevant ancestry becomes unobservable.

**How to test:** Start from Patchwork-style paired benign/prohibited traces, then hold out whole graph families with branches and multiple effects. Randomize episode-level graph views and missingness processes: random loss, omission near restricted sources, spurious parents and plausible transformations whose logged reads do not prove semantic use. Give each reviewer the same observable event store and total retrieval-plus-model budget. Compare per-agent, recent-window and ancestry retrieval with an explicit insufficient-evidence decision. Separately score classification and policies that quarantine or escalate abstentions under a fixed queue capacity. Tune thresholds only on training families; keep true ancestry evaluator-only.

**Comparison:** Matched-budget recent-window and per-agent review, reject-all, allow-all, and complete-provenance exact queries as a privileged diagnostic ceiling.

**Measurements:** Violation recall at fixed benign false-block rate; Benign completion after abstention handling; Abstention and review-queue load; Causal-path localization; Retrieval and model cost.

**Would count against it:** Ancestry retrieval supplies no useful-completion advantage at matched violation tolerance and total cost, or apparent gains require evaluator-only edges or unbounded escalation.

**Main confounds:** Missing graph evidence is not proof of safety. Explicit toy labels make judging easier than realistic tool records. Retrieved artifacts do not prove semantic dependence; duplicated views of one trace are not independent samples.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** Freeze observable fields, missingness mechanisms, queue limits and held-out graph families; resolve source access and reproduce the basic instrument. Extends SEC-06 and SEC-30 by testing pre-effect auditing under incomplete observations.

**Closest prior and evidence limits:**

- [[gh-dmarzzz-patchwork]] — [Patchwork Heist — capability-restricted agents and a private-profit economy](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/code/gh-dmarzzz-patchwork.md). The local semantic pilot detected 10/10 prohibited paths with complete ancestry; per-agent views abstained on all 20 cases. Only ten paired traces and a three-event motif. Catalogue depth: skim.
- [[green-2007-provenance]] — [Provenance Semirings](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/green-2007-provenance.md). Formal derivation provenance supplies a baseline under specified query semantics, not a general LLM dependency oracle. Catalogue depth: skim.
- [[elnozahy-2002-survey]] — [A survey of rollback-recovery protocols in message-passing systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/elnozahy-2002-survey.md). Distributed recovery depends on cross-process dependencies; recovery semantics are distinct from semantic classification. Catalogue depth: skim.

**Related team work:** [patchwork-addendum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/question-atlas/patchwork-addendum.md).

<a id="mkt-04"></a>
### MKT-04 — Telling Sybil firms from tacit colluders

**Update 2:** new.

**Question:** Can an auditor that sees only market data and build logs identify which firms share an owner, and does it confuse Sybil clusters with independent firms that colluded tacitly?

**Candidate hypothesis:** Concentration-based detectors flag both, so they confuse Sybils with tacit colluders; build-graph features (timing of builds, complementary patch claims) separate them better than quantities alone.

**How to test:** Pool runs from MKT-01 to MKT-03 with ground-truth owner labels. Train or tune detectors on some operators and seeds, test on held-out ones: (a) quantity and HHI features in the style of Bracale-Syrnikov's oracle, (b) strategy-graph features, (c) build-log features. Score pairwise same-owner AUC and the false-positive rate on tacitly colluding independent pairs.

**Comparison:** Random and HHI-threshold detectors.

**Measurements:** Same-owner pair AUC; False positives on tacit-colluder pairs; Detection delay in rounds.

**Would count against it:** Build-log features add no AUC over quantity features, or detectors already separate Sybils from tacit colluders without them.

**Main confounds:** If Sybil firms share a prompt they may share style; vary prompts within a principal. Labels must never reach the detector through file names or ordering.

**Framing / first-test class:** measurement / offline.

**Before promotion:** Enough labelled runs from MKT-03; a held-out split by principal, not by round.

**Closest prior and evidence limits:**

- [[bracale-syrnikov-2026-institutional]] — [Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bracale-syrnikov-2026-institutional.md). Oracle detects coordination from quantities; does not distinguish ownership from tacit collusion. Catalogue depth: skim.
- [[eschenbaum-2026-auditing]] — [Auditing Algorithmic Collusion from Strategy Graphs](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/eschenbaum-2026-auditing.md). Auditing collusion from queried strategy graphs; no Sybil labels. Catalogue depth: abstract.
- [[rose-2026-detecting]] — [Detecting Multi-Agent Collusion Through Multi-Agent Interpretability](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/rose-2026-detecting.md). Collusion detection with unknown colluding subgroups, from activations rather than market data. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="mkt-05"></a>
### MKT-05 — Reading the messages versus reading the market

**Update 2:** new.

**Question:** When firms can talk, does reading their messages and stated plans detect collusion better than action-based signals?

**Candidate hypothesis:** Text detectors catch explicit proposals but miss tacit division and flag talk that never becomes action; action-based detectors beat them on run-level collusion.

**How to test:** Runs with public and private chat. A text classifier (LLM judge blind to outcomes) and an action detector (profit gap, HHI, build specialisation) each label every run; score both against an outcome-defined collusion label set before analysis.

**Comparison:** Action detector alone; text detector alone.

**Measurements:** Run-level precision and recall per detector; Share of runs with collusive talk but competitive actions; Share with collusive actions but no collusive talk.

**Would count against it:** The text detector matches or beats the action detector on runs without explicit proposals.

**Main confounds:** The judge model may share biases with firm models; use a different family. Defining collusion from outcomes makes the action detector partly circular; also report against a profitable-deviation check.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** Fix the outcome definition of collusion before any labelled run.

**Closest prior and evidence limits:**

- [[nakamura-2026-colosseum]] — [Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/nakamura-2026-colosseum.md). Finds 'collusion on paper': agents plan collusion in text but act otherwise. Catalogue depth: abstract.
- [[lee-2026-faithful]] — [Faithful yet Collusive: Why Chain-of-Thought Monitoring Cannot Detect Collusion in LLM Pricing Agents under Oligopolistic Competition](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lee-2026-faithful.md). Reasoning faithfulness does not predict collusion. Catalogue depth: skim.
- [[riemer-2026-position]] — [Position: Collusion Risks Among AI Reasoning Agents Justify Certification Requirements for Making Market Decisions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/riemer-2026-position.md). Argues steered collusion cannot be spotted from reasoning text. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md).

<a id="agent-budgets"></a>
## Agent budgets and resource allocation

<a id="bud-01"></a>
### BUD-01 — Visible budgets in private and shared pools

**Update 2:** new.

**Question:** Does a remaining-budget display help private accounts but accelerate exhaustion of a shared pool?

**Candidate hypothesis:** Under pressure, visibility improves private-account efficiency but induces earlier spending and lower group utility in a shared pool.

**How to test:** Randomize complete synthetic task episodes in a hidden/visible countdown by private/shared allocation factorial. Keep aggregate root cap, models, task evidence and action prices identical; private accounts initially receive equal shares. Use the same neutral status-message footprint in hidden arms. Cross decomposable and sequential tasks, randomize activation order, and pair world seeds. Score each whole episode once; individual requests are correlated observations.

**Comparison:** Hidden private accounts, hidden shared pool, and a single solver with the same aggregate cap.

**Measurements:** Verified utility; First-quarter spend share; Rejected requests; Unused balance at stopping; Spend concentration.

**Would count against it:** Visibility does not worsen shared-pool utility or accelerate spending relative to its private-account effect at the prespecified pressure range.

**Main confounds:** Pooling changes feasible transfers as well as incentives. Countdown messages consume context; meter their overhead. Early spending can be efficient on some tasks.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B1 expansion: specify root-cap accounting, optimal task cost and a utility margin before choosing pressure levels.

**Closest prior and evidence limits:**

- [[liu-2025-budget]] — [Budget-Aware Tool Use Enables Effective Agent Scaling](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-budget.md). Single-agent budget tracking supplies a visibility precedent, not a pooling result. Catalogue depth: skim.
- [[paliskara-2026-worse]] — [Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/paliskara-2026-worse.md). Direct shared API-budget coordination precedent; not this visibility factorial. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-02"></a>
### BUD-02 — Which parts of peer spending should be visible?

**Update 2:** new.

**Question:** Is total pool balance enough for coordination, or does naming each worker's spending change behavior?

**Candidate hypothesis:** Individual spending displays increase early spending imitation without improving allocation when peers have no useful cost differences.

**How to test:** Randomize independent group episodes to own balance only, aggregate pool balance, or aggregate plus named peer spending. Keep true pool, task progress indicators, token footprint and action opportunities fixed. Cross homogeneous workers with a separate known-cost heterogeneous stratum. Shuffle display row order and neutral identities. Charge all monitoring costs; compare trajectories as repeated measurements within an episode, never as independent agents.

**Comparison:** An anonymous aggregate ledger and an equal-share scheduler with the same hard cap.

**Measurements:** Useful completions; Early spending slope; Response to peer spend; Allocation regret; Monitoring tokens.

**Would count against it:** Named peer spending improves utility in homogeneous groups without increased waste, or produces no incremental spending response beyond the aggregate balance.

**Main confounds:** Shared task progress can justify correlated spending. Identifiable capability information must be held constant outside the stated heterogeneity manipulation.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B1/B4 expansion: define waste against a task validator and a cost floor, separately from equal spending.

**Closest prior and evidence limits:**

- [[anthropic-2026-patterns]] — [Patterns and problems in emerging multiagent systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2026-patterns.md). Public-board interactions motivate exposure controls; vendor examples do not establish a spending effect. Catalogue depth: full.
- [[paliskara-2026-worse]] — [Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/paliskara-2026-worse.md). Shared-resource teams make coordination overhead a relevant comparator. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-03"></a>
### BUD-03 — Displayed balance versus the enforced balance

**Update 2:** new.

**Question:** Does a misleading remaining-budget display alter collective pacing beyond its effect on a single solver?

**Candidate hypothesis:** An understated display increases premature stopping; an overstated display increases rejected action attempts, with larger effects in interacting groups.

**How to test:** Randomize complete synthetic episodes to displays of 0.5, 1 or 2 times the true remaining balance, crossed with single solver or communicating team. Hold aggregate enforced resources, evidence and action prices fixed. Apply the multiplier consistently after each accepted charge, and meter communications. Predefine stopping opportunities and include solvable tasks near the cap. Block on world seed and model; analyze the population-by-display interaction.

**Comparison:** Accurate displays in each population condition and a hidden-display sensitivity arm.

**Measurements:** Incomplete stops with balance left; Rejected requested cost; Validated output; Exhaustion time; Billed spend.

**Would count against it:** Display multipliers do not shift the predicted stopping and rejection outcomes, or team effects are no larger than the matched single-solver effects.

**Main confounds:** Hard enforcement prevents actual overspend. Distinguish attempted requests from accepted charges, and model-visible task budget from context capacity.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B5 expansion: validate the metering proxy and specify completion credit for interrupted actions before running agents.

**Closest prior and evidence limits:**

- [[lin-2026-bagen]] — [BAGEN: Are LLM Agents Budget-Aware?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2026-bagen.md). Abstract reports miscalibrated remaining-cost forecasts; not misleading displays in populations. Catalogue depth: abstract.
- [[cognition-2025-rebuilding]] — [Rebuilding Devin for Claude Sonnet 4.5: Lessons and Challenges](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/cognition-2025-rebuilding.md). Context-anxiety engineering anecdote motivates a contrast but provides no controlled effect estimate. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-04"></a>
### BUD-04 — Context anxiety or spending anxiety?

**Update 2:** new.

**Question:** Do agents respond differently to context-window headroom and remaining action budget?

**Candidate hypothesis:** Low displayed context headroom mainly changes summarization and early wrap-up, whereas low displayed action budget mainly reduces tool exploration.

**How to test:** Randomize whole multi-step task episodes in a displayed-context-headroom by displayed-spend-balance factorial, while actual context capacity and hard root budget remain constant and sufficient. Use truthful common labels for the two resource types, with experimentally varied numeric signals. Hold task history content, output allowance and tool prices fixed. Include a single-agent replication before teams; randomize worlds, not individual turns. Charge summaries and tool results.

**Comparison:** Accurate dual displays and an information-matched display containing only the action budget.

**Measurements:** Summarization frequency; Tool exploration depth; Premature final answers; Task success; Spent resources.

**Would count against it:** The two displays have indistinguishable effects on both summarization and exploration, or low context signals do not selectively increase wrap-up.

**Main confounds:** Provider countdown features and prompt-based displays are different interventions. Keep model/version fixed; actual truncation would create an information-loss confound.

**Framing / first-test class:** measurement / api-small.

**Before promotion:** B5 expansion: implement separable counters and predefine observable wrap-up behavior without inferring subjective anxiety.

**Closest prior and evidence limits:**

- [[anthropic-2026-context]] — [Context windows](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2026-context.md). Documents context-awareness signals without a controlled behavioral comparison. Catalogue depth: full.
- [[cognition-2025-rebuilding]] — [Rebuilding Devin for Claude Sonnet 4.5: Lessons and Challenges](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/cognition-2025-rebuilding.md). Reports context anxiety anecdotally. Catalogue depth: full.
- [[lin-2026-bagen]] — [BAGEN: Are LLM Agents Budget-Aware?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2026-bagen.md). Separates internal computation from external action costs; not the same resource as context headroom. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-05"></a>
### BUD-05 — Use cost forecasts to release stranded budget

**Update 2:** new.

**Question:** Can calibrated completion-cost forecasts improve shared-budget reallocation without abandoning recoverable tasks?

**Candidate hypothesis:** Forecasts calibrated on separate worlds support better stop-or-continue decisions than raw self-estimates at the same overall budget.

**How to test:** Randomize complete task portfolios to raw worker cost intervals, empirically calibrated intervals, or a fixed stopping rule. Use an independent calibration set, frozen thresholds and held-out task families. A common allocator reallocates released balance to pending tasks using only online observations. Fix root cap and charge interval generation plus allocation calls. Validate stopped tasks through separately labelled evaluation replays; replay outcomes never guide the online allocator.

**Comparison:** Equal shares with fixed cutoffs and an offline clairvoyant bound labelled as unavailable to deployment.

**Measurements:** Portfolio successes; Interval coverage; Recoverable tasks abandoned; Resources rescued; Forecast overhead.

**Would count against it:** Calibrated forecasts improve coverage but fail to improve portfolio success, or gain only by exceeding the matched decision-cost allowance.

**Main confounds:** Success after a larger replay budget is not proof that the original allocation was sufficient. Calibration may fail across task families or model changes.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B1/B5 expansion: define cost-to-completion labels for censored failures and freeze the allocation rule before evaluation.

**Closest prior and evidence limits:**

- [[lin-2026-bagen]] — [BAGEN: Are LLM Agents Budget-Aware?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2026-bagen.md). Defines progressive budget estimation and reports remaining calibration limits. Catalogue depth: abstract.
- [[ding-2026-calibrate]] — [Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ding-2026-calibrate.md). Calibration before cost-aware exploration is prior art in a different allocation setting. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-06"></a>
### BUD-06 — Do quotas cause unnecessary spawning?

**Update 2:** new.

**Question:** Do agents create extra identities when each identity unlocks a new claim on a fixed shared pool?

**Candidate hypothesis:** Per-identity quotas increase spawning and pool capture beyond task-driven delegation, especially under tight root budgets.

**How to test:** Randomize independent sandboxed group episodes to no spawning, spawning under root-only metering, or spawning with stated per-identity claim limits. Keep the same global cap in every arm; extra identities never create real resources. Cross quota pressure with tasks having high or low useful parallelism. Charge spawn setup and child inference, and match goal incentives and tool access. Compare spawned count with the root-only delegation arm on paired worlds.

**Comparison:** Root-only delegation estimates task-driven spawning; a fixed worker roster provides a scheduling reference.

**Measurements:** Excess identities; Verified child contributions; Share of pool captured; Other workers' completion; Spawn cost.

**Would count against it:** Identity quotas do not increase excess spawning or resource capture relative to root-only delegation at the tested pressure levels.

**Main confounds:** Extra workers can be useful. Transcripts mentioning quotas are supplementary evidence, not proof of intent; model-family differences do not isolate reasoning.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B2 expansion: create a toy claim allocator with an unchanged root cap and quantify useful parallelism independently.

**Closest prior and evidence limits:**

- [[yokoo-2004-effect]] — [The effect of false-name bids in combinatorial auctions: new fraud in internet auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yokoo-2004-effect.md). False-name bidding establishes a mechanism-design concern, not observed LLM spawning. Catalogue depth: skim.
- [[anthropic-2025-how]] — [How we built our multi-agent research system](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2025-how.md). Reports over-spawning in engineering practice without a quota manipulation. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-07"></a>
### BUD-07 — Discovering a quota rule

**Update 2:** new.

**Question:** Does making per-identity quota information discoverable change spontaneous delegation relative to stating it explicitly?

**Candidate hypothesis:** Explicit quota information increases quota-responsive spawning sooner than discoverable information; incidental discovery produces a delayed increase.

**How to test:** Randomize complete sandbox episodes to a stated quota rule, a rule available through an ordinary help tool, or no informative rule disclosure. The actual per-identity allocation and global hard cap are identical. Randomize a benign task step that exposes the help entry independently of workload, without suggesting an exploit. Hold tool interface, objectives and baseline delegation options fixed; charge help calls and child work. Analyze exposure assignment as the primary contrast.

**Comparison:** Explicit disclosure and the same task under a root-only rule; no-information episodes remain in the denominator.

**Measurements:** Spawn timing; Excess delegation; Help exposure; Useful output; Pool capture.

**Would count against it:** Rule disclosure and randomized incidental exposure do not change spawning or capture, or changes are fully explained by useful task decomposition.

**Main confounds:** Conditioning only on agents that read help would select on behavior. This tests a bounded synthetic incentive, not covert real-service probing.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** B2 expansion: separate the randomized exposure intervention from voluntary help-seeking and keep all effects within the simulator.

**Closest prior and evidence limits:**

- [[yokoo-2007-making]] — [Making VCG More Robust in Combinatorial Auctions via Submodular Approximation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yokoo-2007-making.md). False-name-resistant mechanism theory supplies context, not a rule-discovery result. Catalogue depth: full.
- [[hu-2026-dissociative]] — [Dissociative Identity: Language Model Agents Lack Grounding for Reputation Mechanisms](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/hu-2026-dissociative.md). Position paper questions identity-based governance; it is not a theorem forbidding Sybil-proof reputation. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-08"></a>
### BUD-08 — Spawn fees versus lineage budgets

**Update 2:** new.

**Question:** Which quota policy suppresses wasteful spawning while preserving valuable parallel work?

**Candidate hypothesis:** Lineage accounting removes quota-driven spawning with less damage to useful high-parallelism tasks than a uniform per-spawn fee.

**How to test:** Randomize independent group episodes to per-identity quotas, several prespecified spawn fees, or a shared lineage allowance. Use the same root cap, initial principal allocations and actual inference prices. Fees consume or reserve part of that allowance according to one fixed rule, never creating extra budget. Cross low and high parallelism tasks and randomize initial role assignment. Evaluate task outcomes and extra identities jointly; do not infer effectiveness from spawn count alone.

**Comparison:** Root-only unconstrained delegation and no spawning, both under the same aggregate cap.

**Measurements:** Useful output; Unproductive spawn cost; Completion of other principals' tasks; Parallelism retained; Unused balance.

**Would count against it:** Lineage accounting causes equal or greater useful-output loss than the fee policy while offering no additional reduction in wasteful delegation.

**Main confounds:** Lineage is supplied ground truth here. Inferring operator identity is a separate security question; fees may tax helpful workers more than wasteful ones.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B2 expansion: preregister fee ranges and a task-based excess-spawn definition; do not treat the security mechanism as new.

**Closest prior and evidence limits:**

- [[zhu-2026-fault]] — [Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhu-2026-fault.md). Escrow lineage constrains descendant resources under explicit system assumptions; not an incentive study. Catalogue depth: skim.
- [[yokoo-2004-effect]] — [The effect of false-name bids in combinatorial auctions: new fraud in internet auctions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/yokoo-2004-effect.md). False-name mechanisms motivate evaluating both manipulation resistance and efficiency. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-09"></a>
### BUD-09 — Safe escrow that still gets work done

**Update 2:** new.

**Question:** How much useful work is lost when safe preallocated budgets cannot move during a partition?

**Candidate hypothesis:** Demand-informed preallocation improves deadline utility over equal escrow shares under uneven demand, but loses its advantage when demand forecasts shift.

**How to test:** Randomize independent simulated workload episodes to equal preallocation, forecast-based preallocation, or a connected central allocator. Inject paired crash and partition schedules crossed with forecast error. Every distributed arm uses the same already-specified conservative reservation and settlement rules; uncertain effects remain charged. Hold issued budget, deadlines and fault schedule fixed. Model forecast and reallocation overhead explicitly, and score whole workloads rather than individual crash events.

**Comparison:** Equal safe escrow and a connected scheduler whose availability advantage is explicitly labelled.

**Measurements:** Completed task value; Idle reserved credits; Unfinished high-value work; Recovery delay; Conservation violations.

**Would count against it:** Forecast-based escrow does not improve useful completion under stable heterogeneous demand, or remains equally effective despite large demand shifts.

**Main confounds:** Conservation is a prerequisite, not evidence of good allocation. Crash-fault guarantees do not establish Byzantine resistance; simulated costs may omit real billing semantics.

**Framing / first-test class:** boundary-test / offline.

**Before promotion:** B2/B3 expansion: implement or obtain an auditable safe baseline; published executable artifacts and provider-cost mapping remain unresolved.

**Closest prior and evidence limits:**

- [[zhu-2026-fault]] — [Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhu-2026-fault.md). Direct conservation and partition-preallocation prior; this card tests allocation usefulness instead. Catalogue depth: skim.
- [[chevaleyre-2006-issues]] — [Issues in Multiagent Resource Allocation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chevaleyre-2006-issues.md). Resource-allocation survey supplies distinct efficiency and fairness objectives. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-10"></a>
### BUD-10 — Peers, coordinator, equal shares or auction?

**Update 2:** new.

**Question:** Which allocation mechanism wins when every decision consumes the same limited root budget?

**Candidate hypothesis:** A coordinator or equal shares outperform peer bargaining on homogeneous tasks; a contract-net auction helps chiefly when worker costs differ.

**How to test:** Randomize complete task portfolios to peer negotiation, one coordinator, fixed equal shares, or announce-bid-award allocation. Cross homogeneous/heterogeneous worker costs and decomposable/sequential tasks. Fix aggregate tokens, tool credits, deadlines and available task evidence; charge bids, negotiation, coordination and retries to the cap. Randomize presentation and activation order, and include all failed allocations. Independent portfolios are the analysis units.

**Comparison:** A fixed equal split and an offline optimal allocation computed from known task costs, clearly labelled as a diagnostic ceiling.

**Measurements:** Validated utility; Allocation overhead; Duplicate work; Idle credits; Distance from feasible optimum.

**Would count against it:** Peers match or beat simpler rules under homogeneous conditions, or auctions improve just as much without cost heterogeneity as with it.

**Main confounds:** Private information and decision authority differ across architectures. Report common-goal and multiple-principal settings separately; one-model problem allocation is not peer negotiation.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B3 expansion: specify information symmetry, action authority and every mechanism's charged decision work before selection.

**Closest prior and evidence limits:**

- [[paliskara-2026-worse]] — [Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/paliskara-2026-worse.md). Direct coordinator/team comparison includes shared API budgets. Catalogue depth: full.
- [[wang-2026-r3]] — [$R^3$-Bench: LLMs Struggle with Resource-Rational Reasoning under Shared Budgets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wang-2026-r3.md). Studies one model allocating across problems, not bargaining peers. Catalogue depth: skim.
- [[smith-1980-contract]] — [The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/smith-1980-contract.md). Contract-net allocation is established prior art. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-11"></a>
### BUD-11 — Can cost bids beat measured capability?

**Update 2:** new.

**Question:** When workers have different task costs, should an allocator trust bids or pay to measure them?

**Candidate hypothesis:** Cheap calibration trials improve allocation under noisy cost bids, but their overhead erases the benefit on small homogeneous portfolios.

**How to test:** Randomize whole heterogeneous-worker portfolios to self-reported bids, charged calibration trials plus bids, or fixed capability metadata. Cross portfolio size and scripted bid-noise levels while keeping worker policies and root cap fixed. Freeze the common assignment algorithm so the intervention is evidence quality, not allocator skill. Calibration tasks must be disjoint from evaluation tasks; their costs count even when the resulting allocation fails.

**Comparison:** Equal shares and an assignment using true synthetic worker costs as an explicitly unavailable oracle.

**Measurements:** Completed value; Bid error; Calibration cost; Allocation regret; Failures from underestimation.

**Would count against it:** Calibration fails to improve net utility in large heterogeneous portfolios, or helps equally despite removing heterogeneity and bid noise.

**Main confounds:** Scripted noisy bids test robustness, not emergent deception. Capability metadata must not reveal hidden task solutions; observed speed may differ from verified competence.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B3 expansion: define a worker capability generator, bid-cost units and a separate calibration pool with charged costs.

**Closest prior and evidence limits:**

- [[amayuelas-2025-self]] — [Self-Resource Allocation in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amayuelas-2025-self.md). Explicit capability information and orchestrator/planner allocation are direct precedents. Catalogue depth: full.
- [[bianchi-2024-how]] — [How Well Can LLMs Negotiate? NegotiationArena Platform and Analysis](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/bianchi-2024-how.md). Negotiation studies motivate controlling framing and order; they do not validate truthful compute bids. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-12"></a>
### BUD-12 — Replan on events or every action?

**Update 2:** new.

**Question:** Does event-triggered budget reallocation preserve coordination quality while reducing managerial cost?

**Candidate hypothesis:** Event-triggered replanning improves net completion over per-action orchestration when changes are sparse, but loses under rapid unobserved changes.

**How to test:** Randomize independent project episodes to fixed allocation, event-triggered planning or per-action orchestration. Cross task-change frequency and public progress-signal delay. All arms receive identical worker capability metadata and have the same total inference/tool cap and deadline; charge monitoring and manager calls. Use a frozen event rule tuned only on pilot worlds, and pair evaluation world schedules without sharing agent histories.

**Comparison:** Fixed equal roles and a per-action manager with identical observations and action authority.

**Measurements:** Verified milestones; Manager fraction of budget; Reaction delay; Stale assignments; Net utility.

**Would count against it:** Event-triggered planning has no utility advantage under sparse changes after charging overhead, or does not degrade relative to frequent planning under the specified hidden changes.

**Main confounds:** Poor trigger choice can masquerade as a general architecture failure. Concurrent execution and manager capability must be fixed or separately stratified.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B3 expansion: define which events are observable and how each unfinished action is charged when a replan interrupts it.

**Closest prior and evidence limits:**

- [[amayuelas-2025-self]] — [Self-Resource Allocation in Multi-Agent LLM Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/amayuelas-2025-self.md). Planner/orchestrator comparisons are direct prior; their cost analysis is not this hard-cap experiment. Catalogue depth: full.
- [[dang-2025-multi]] — [Multi-Agent Collaboration via Evolving Orchestration](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dang-2025-multi.md). Learned orchestration with cost penalties is adjacent; sequential activation differs from concurrent workers. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-13"></a>
### BUD-13 — Difficulty-aware allocation without hindsight

**Update 2:** new.

**Question:** Can an online allocator improve over equal problem budgets without using retrospective success information?

**Candidate hypothesis:** A small charged diagnostic stage improves portfolio success when problem difficulty varies, but simple equal allocation wins when diagnostic signals are weak.

**How to test:** Randomize independent generated problem portfolios to equal allocation, model-only allocation, or a fixed diagnostic-then-allocate policy. Cross difficulty dispersion and diagnostic informativeness using separately generated families. Randomize problem order, keep total root tokens fixed, and charge the diagnostic attempts. Freeze the allocation rule using separate development portfolios. Evaluate all sampled portfolios; successful pilot traces must not be selected into the test set.

**Comparison:** Equal allocation and a hindsight best allocation reported only as a nondeployable bound.

**Measurements:** Portfolio success count; Diagnostic cost; Order sensitivity; Allocation regret; Unsolved tasks abandoned.

**Would count against it:** Diagnostics provide no benefit with informative signals and varied difficulty, or outperform equal shares equally when their signal is randomized.

**Main confounds:** Offline optimal allocation from observed successful runs can overstate attainable performance. Problems share a budget, so they are not independent replicates.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B3 expansion: define held-out difficulty families and measure the diagnostic policy's information without access to evaluation answers.

**Closest prior and evidence limits:**

- [[wang-2026-r3]] — [$R^3$-Bench: LLMs Struggle with Resource-Rational Reasoning under Shared Budgets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/wang-2026-r3.md). Direct shared-budget problem-allocation precedent with retrospective oracle limitations. Catalogue depth: skim.
- [[ding-2026-calibrate]] — [Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/ding-2026-calibrate.md). Cost-aware exploration after calibration motivates charging information acquisition. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-14"></a>
### BUD-14 — Divide work through a ledger alone

**Update 2:** new.

**Question:** Can visible subtask claims reduce duplicate work without a chat channel?

**Candidate hypothesis:** A public claim ledger improves completion on decomposable tasks chiefly by reducing duplicated effort, with little benefit on sequential tasks.

**How to test:** Randomize independent synthetic project episodes to private ledgers, a public spending ledger, or a public spending-plus-subtask-claim ledger. Disable direct messages while retaining identical tool observations and action authority. Cross decomposable and sequential worlds, randomize first access and worker identifiers, and cap total inference plus tool use. Charge ledger reads and writes, and allow conflicting claims so successful coordination is measured rather than guaranteed by a lock.

**Comparison:** Private records and a deterministic central task assignment charged at its implementation cost.

**Measurements:** Distinct verified subtasks; Duplicate effort; Claim conflicts; Idle claimed tasks; Utility per root budget.

**Would count against it:** The claim ledger fails to reduce duplication or improve net completion in decomposable tasks, or gains arise only because access order grants one worker extra turns.

**Main confounds:** No chat does not mean no communication: the public environment is a channel. Task labels or locking semantics can perform the allocation mechanically.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B4 expansion: design claim semantics that reveal intent without enforcing exclusive assignment and define duplicate useful work.

**Closest prior and evidence limits:**

- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Public outcomes support coordination in an economic game, not a compute-ledger test. Catalogue depth: full.
- [[anthropic-2026-patterns]] — [Patterns and problems in emerging multiagent systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2026-patterns.md). Public-board vendor examples motivate distinguishing environmental observation from direct messages. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-15"></a>
### BUD-15 — Do peer spending norms increase waste?

**Update 2:** new.

**Question:** Does observing another worker's higher spending increase an agent's own cost when its task has not become harder?

**Candidate hypothesis:** A randomized upward shift in displayed peer spending raises own spending without a corresponding gain in independently scored task utility.

**How to test:** Randomize complete groups to private or public spending ledgers. Within public groups assign a scripted peer a higher or lower displayed spending history drawn from matched valid runs, while keeping focal tasks, true remaining pool, available actions and hard cap identical. Cross slack and tight budgets. Report episode-level intent-to-exposure contrasts; trajectories and individual workers are repeated observations. Keep task claims and evidence unchanged.

**Comparison:** Accurate private accounting and an aggregate-only display that removes individual spending norms.

**Measurements:** Focal spending change; Verified utility; Cost above task floor; Pool exhaustion; Spend convergence.

**Would count against it:** Higher displayed peer spending does not increase waste, or increased spending yields proportionate independently verified utility rather than padding.

**Main confounds:** Shared shocks can create honest convergence, hence randomized exposure. Spending imitation alone does not establish agreement, intent, or collusion against a principal.

**Framing / first-test class:** speculative / api-small.

**Before promotion:** B4 expansion: fix a utility function independent of spending and create coherent synthetic displays with unchanged true balances.

**Closest prior and evidence limits:**

- [[fish-2024-algorithmic]] — [Algorithmic Collusion by Large Language Models](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/fish-2024-algorithmic.md). Pricing collusion is an adjacent outcome, not evidence of budget padding. Catalogue depth: abstract.
- [[nakamura-2026-colosseum]] — [Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/nakamura-2026-colosseum.md). Collusion auditing motivates measuring principal utility and behavior rather than inferring agreement from talk. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-16"></a>
### BUD-16 — Authority, labels and asymmetric spending rights

**Update 2:** new.

**Question:** Are budget imbalances driven by a leader label or by privileged access to the pool?

**Candidate hypothesis:** Giving one worker priority spending rights shifts resource capture more than calling that worker the leader, and can reduce total task utility.

**How to test:** Randomize independent synthetic group episodes in a neutral/leader role-label by equal/priority-spending-rights factorial. Hold models, observations, task difficulty and aggregate root cap fixed. Rotate which worker gets the role and counterbalance activation order within each rights regime. Give all workers the same verified budget ledger; do not also manipulate misinformation. Score whole groups and retain both high- and low-demand tasks.

**Comparison:** Equal rights with neutral labels and a deterministic fair scheduler with the same cap.

**Measurements:** Privileged worker's spend share; Total verified utility; Unfinished other tasks; Fairness across principals; Unused funds.

**Would count against it:** Priority rights do not increase capture or reduce utility, or labels explain the effect fully when rights are held fixed.

**Main confounds:** More spending can reflect greater legitimate need, so randomize role assignment independently of demand. A renewable commons and a finite compute pool have different dynamics.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B1/B3 expansion: specify enforceable priority rights and inspect role-label controls in the closest prior before promotion.

**Closest prior and evidence limits:**

- [[borah-2026-bosses]] — [Bosses, Kings, and the Commons: Cooperation Under Power Asymmetry in LLM Societies](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/borah-2026-bosses.md). Direct asymmetric-commons prior; finite compute spending is a domain extension. Catalogue depth: skim.
- [[piatti-2024-cooperate]] — [Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/piatti-2024-cooperate.md). Renewable commons cooperation motivates group-level utility, not a compute-budget prediction. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-17"></a>
### BUD-17 — Keep enough budget to finish and verify

**Update 2:** new.

**Question:** Does protecting a small finalization reserve improve completed work under a hard shared cap?

**Candidate hypothesis:** A protected reserve increases validated deliverables near exhaustion, but wastes useful exploration budget when final checks are cheap or unnecessary.

**How to test:** Randomize complete project episodes to a freely shared pool, a fixed finalization reserve, or a dynamically released reserve triggered by observable completion progress. Cross tasks with expensive/cheap final validation and tasks whose exploration usually fails. Keep total issued budget and validator accuracy identical; reserves come out of the production pool. Freeze release rules on separate pilot worlds and meter all finalization, bookkeeping and abandoned work.

**Comparison:** Equal per-stage allocation and the unreserved pool; an offline best split is a diagnostic ceiling only.

**Measurements:** Validated deliverables; Exploration success; Unspent reserve; Incomplete near-finished work; Total cost.

**Would count against it:** Reserves fail to improve validated completion near the cap, or their predicted opportunity cost is absent across low-value finalization tasks.

**Main confounds:** This is scheduling a terminal resource, not evidence of spontaneous public-good cooperation. A validator unavailable to ordinary workers would change capabilities.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B1/B3 expansion: specify observable finish conditions and a realistic validator cost; keep distinct from SOC-28's social verification incentives.

**Closest prior and evidence limits:**

- [[liu-2025-budget]] — [Budget-Aware Tool Use Enables Effective Agent Scaling](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-budget.md). Tool-budget tracking motivates controlling early stopping and resource use across stages. Catalogue depth: skim.
- [[lin-2026-bagen]] — [BAGEN: Are LLM Agents Budget-Aware?](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2026-bagen.md). Remaining-cost estimation motivates a progress-based release rule but does not validate it. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-18"></a>
### BUD-18 — Tokens, money or a resource vector?

**Update 2:** new.

**Question:** Does the resource unit used by an allocator change the task portfolio it completes?

**Candidate hypothesis:** A vector of token, tool and monetary limits improves feasible completion over a token-only heuristic when prices and tool costs vary.

**How to test:** Randomize independent workload portfolios to allocation using token counts alone, estimated dollars alone, or explicit resource vectors. All arms operate under the same real vector of enforced limits and receive the same raw price table; only the planning representation differs. Cross homogeneous costs with heterogeneous model tiers and tools. Charge estimation and allocation work, and compare results within each resource envelope rather than declaring unequal budgets matched.

**Comparison:** A deterministic feasible greedy allocator using the same price information and a known-cost optimization ceiling.

**Measurements:** Feasible task value; Which constraint binds; Rejected requested resources; Stranded resources; Planning overhead.

**Would count against it:** Vector-aware planning does not improve feasible value in heterogeneous-cost worlds, or apparent gains disappear when decision overhead is charged.

**Main confounds:** Token counts are not interchangeable with billed cost, context occupancy or latency. A richer display can increase cognitive load; equal raw information matters.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B3/B5 expansion: fix reproducible synthetic prices and define admission for each resource dimension before comparing planners.

**Closest prior and evidence limits:**

- [[zhu-2026-fault]] — [Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/zhu-2026-fault.md). Resource-vector accounting is existing systems prior, not proof of allocator quality. Catalogue depth: skim.
- [[liu-2025-costbench]] — [CostBench: Evaluating Multi-Turn Cost-Optimal Planning and Adaptation in Dynamic Environments for LLM Tool-Use Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-costbench.md). Synthetic costed tool planning supplies exact-cost evaluation ideas. Catalogue depth: abstract.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-19"></a>
### BUD-19 — Advisory targets inside a hard cap

**Update 2:** new.

**Question:** Can an advisory target with bounded finishing room produce better outcomes than abrupt truncation at that target?

**Candidate hypothesis:** A lower advisory target plus reserved finishing room reduces incomplete final actions compared with an abrupt cutoff at the same planning target.

**How to test:** Randomize whole agent-loop episodes to an advisory target with a bounded grace reserve, a hard inner cutoff at that target with remaining resources reallocatable, or no inner target. Keep the same aggregate outer cap across all arms, and count every accepted action against it. Cross short and long atomic final actions. Randomize task worlds and charge all target messages; report unused or reallocated grace funds explicitly.

**Comparison:** An outer-cap-only controller and a deterministic reserve policy with identical total resources.

**Measurements:** Validated completion; Interrupted actions; Unused reserve; Reallocated work value; Attempts beyond target.

**Would count against it:** Advisory pacing with reserved finishing room fails to improve completed actions or net portfolio utility over the hard-target comparator.

**Main confounds:** Advisory exceedance is not a breach of the outer cap. Provider-native signals differ from prompt hints; a per-request output limit is not a whole-loop spending limit.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B5 expansion: predefine the maximum finishing reservation and select native or emulated signals without conflating them.

**Closest prior and evidence limits:**

- [[anthropic-2026-task]] — [Task budgets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2026-task.md). Documents advisory loop targets and separate enforced per-request limits; no controlled efficacy estimate. Catalogue depth: full.
- [[han-2024-token]] — [Token-Budget-Aware LLM Reasoning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/han-2024-token.md). Prompted token-budget behavior motivates checking nonlinear responses to tight targets. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-20"></a>
### BUD-20 — Budget accounting across tools and compaction

**Update 2:** new.

**Question:** Does preserving the correct remaining-budget signal through compaction prevent avoidable stopping or retries?

**Candidate hypothesis:** A correctly carried countdown improves planning relative to reset or double-decremented displays, especially when tool results dominate new context.

**How to test:** Randomize complete multi-step episodes to correct carry-forward, reset-to-total, or double-counted-history budget displays after an identical compaction event. Cross short/long tool-result payloads without changing useful facts. Keep actual root cap, summary content, tool prices and worker model fixed; meter compaction and resumed requests. The episode is the independent unit, with pre/post steps treated as a paired trajectory rather than separate runs.

**Comparison:** Correctly metered uncompacted histories where context allows, and correct carry-forward under the shared compaction policy.

**Measurements:** Premature stopping; Rejected requests; Task completion; Display error; Compaction overhead.

**Would count against it:** Correct accounting provides no completion or pacing advantage, or errors do not matter more when payload-heavy histories amplify the mismatch.

**Main confounds:** History removal changes memory, so summaries must match across display arms. Vendor task-budget counters can differ from billing counters; retain both telemetry streams.

**Framing / first-test class:** boundary-test / api-small.

**Before promotion:** B5 expansion: implement testable counters and freeze compaction content independently of the displayed balance; provider feature access is optional.

**Closest prior and evidence limits:**

- [[anthropic-2026-task]] — [Task budgets](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/blogs/anthropic-2026-task.md). Documents loop counting and carrying remaining budget through client compaction. Catalogue depth: full.
- [[liu-2025-budget]] — [Budget-Aware Tool Use Enables Effective Agent Scaling](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/liu-2025-budget.md). Budget tracking supplies a behavioral precedent, not a compaction test. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-21"></a>
### BUD-21 — Train for a penalty or a strict budget?

**Update 2:** new.

**Question:** Which learned allocation objective transfers better to budget pressures absent from training?

**Candidate hypothesis:** A controller trained with explicit remaining balance and a smooth violation penalty transfers better to tighter caps than one trained only with a terminal overspend cliff.

**How to test:** Train controllers on the same task families and frozen worker pool, randomizing independent training seeds to smooth penalty or terminal cliff objectives, crossed with visible or omitted numeric balance. Match training interactions and tuning budget. Evaluate frozen policies on held-out tasks and tighter/looser caps under identical hard enforcement. Use training seed as the independent unit; evaluation portfolios estimate each policy's performance, not extra independent training replicates.

**Comparison:** A cost-penalized learned controller and a fixed nonlearned allocation rule under the same test cap.

**Measurements:** Feasible test utility; Violation attempts; Unseen-cap performance; Training stability; Worker-call cost.

**Would count against it:** The proposed objective-and-balance combination does not improve held-out feasible utility or reduces it relative to cliff training at the prespecified tighter caps.

**Main confounds:** Joint reward and observation changes need the factorial to identify their effects. A training reward for cheap behavior is not an enforced spending guarantee.

**Framing / first-test class:** extension / training.

**Before promotion:** B3/B5 expansion: audit reward formulas, freeze a modest controller class and allocate genuinely independent training runs before estimating transfer.

**Closest prior and evidence limits:**

- [[jin-2025-controlling]] — [Controlling Performance and Budget of a Centralized Multi-agent LLM System with Reinforcement Learning](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/jin-2025-controlling.md). Budget-penalized expert control motivates the terminal-cliff comparator. Catalogue depth: full.
- [[dang-2025-multi]] — [Multi-Agent Collaboration via Evolving Orchestration](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/dang-2025-multi.md). Learned cost-aware orchestration is prior art; different activation rules require harmonization. Catalogue depth: skim.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="bud-22"></a>
### BUD-22 — Efficiency and starvation in shared budgets

**Update 2:** new.

**Question:** Can a minimum-service rule improve the least-served principal without destroying collective task value?

**Candidate hypothesis:** A small protected service floor reduces zero-completion principals at modest total-utility cost when cheap tasks otherwise dominate allocation.

**How to test:** Randomize independent multi-principal workload episodes to sum-utility allocation, a fixed minimum-service floor, or equal shares. Cross task-cost inequality and arrival order using known synthetic utilities. Hold total hard cap, worker capabilities and information fixed; charge the allocator and reserve service from the same pool. Freeze floor levels on development workloads, include infeasible-demand worlds, and aggregate uncertainty over workloads rather than principals.

**Comparison:** Equal shares and a feasible Pareto frontier computed from known task costs as an offline reference.

**Measurements:** Total task utility; Worst-principal completion; Zero-service rate; Delay inequality; Unused budget.

**Would count against it:** The service floor does not reduce starvation, or its utility loss exceeds the prespecified acceptable tradeoff even on feasible workloads.

**Main confounds:** Fairness is a chosen objective, not a universal scalar fact. Different principals may have unequal legitimate needs; report the full tradeoff rather than one winner.

**Framing / first-test class:** extension / api-small.

**Before promotion:** B1/B3 expansion: select a synthetic utility scale, feasibility definition and acceptable service-cost tradeoff through human review.

**Closest prior and evidence limits:**

- [[chevaleyre-2006-issues]] — [Issues in Multiagent Resource Allocation](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/chevaleyre-2006-issues.md). Classical allocation distinguishes utilitarian, egalitarian and other welfare criteria. Catalogue depth: skim.
- [[paliskara-2026-worse]] — [Worse Together: How Performance Breaks Down in Multi-User Multi-Agent Teams](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/paliskara-2026-worse.md). Multi-user shared-resource settings motivate keeping individual and group outcomes separate. Catalogue depth: full.

**Related team work:** [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

<a id="mkt-09"></a>
### MKT-09 — Public production ledger

**Update 2:** new.

**Question:** Does publishing each firm's output and capacity every round raise tacit division compared with showing only market totals?

**Candidate hypothesis:** A public per-firm ledger raises division and profit gap, because firms can see and respect each other's territory.

**How to test:** Two arms at N = 3: firms see only own data and market totals (Lin et al.'s information set) vs a public ledger of every firm's quantities and machines. Same model and seeds.

**Comparison:** Own-data-only arm.

**Measurements:** HHI per good; Profit gap fraction; Re-entry events.

**Would count against it:** The ledger arm shows no more division than the own-data arm.

**Main confounds:** The ledger lengthens the prompt; pad the other arm.

**Framing / first-test class:** extension / api-small.

**Before promotion:** Maps to budget hunch B4 (tacit cartels via a public ledger); align with BUD candidates before promotion.

**Closest prior and evidence limits:**

- [[lin-2024-strategic]] — [Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/lin-2024-strategic.md). Agents see only own quantity, price, share and profit. Catalogue depth: full.
- [[arslan-2026-persistent]] — [Persistent Partners Raise Prices Among Learning Agents](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/arslan-2026-persistent.md). Prices rise even when rival prices are hidden. Catalogue depth: abstract.
- [[li-2026-emergent]] — [Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/1-library/papers/li-2026-emergent.md). Firms see competitors' prices and stock. Catalogue depth: skim.

**Related team work:** [swarm-factory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/swarm-factory.md), [agent-budgets-hunches](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/dmarz/agent-budgets-hunches.md).

## Original brief coverage

- [casefile](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/casefile.md): [SOC-32](#soc-32), [SOC-36](#soc-36)
- [collective-sensing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/collective-sensing.md): [SOC-01](#soc-01), [SOC-02](#soc-02), [SOC-03](#soc-03), [SOC-04](#soc-04), [SOC-05](#soc-05), [SOC-08](#soc-08), [SOC-11](#soc-11), [SOC-13](#soc-13), [SOC-19](#soc-19), [SOC-35](#soc-35), [SOC-38](#soc-38), [SOC-39](#soc-39), [SOC-41](#soc-41), [SOC-42](#soc-42), [SOC-43](#soc-43), [SOC-44](#soc-44)
- [commons](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/commons.md): [SOC-14](#soc-14), [SOC-26](#soc-26), [SOC-27](#soc-27), [SOC-28](#soc-28)
- [coordination](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/coordination.md): [SOC-03](#soc-03), [SOC-04](#soc-04), [SOC-13](#soc-13), [SOC-14](#soc-14), [SOC-15](#soc-15), [SOC-16](#soc-16), [SOC-19](#soc-19), [SOC-20](#soc-20), [SOC-35](#soc-35), [SOC-40](#soc-40)
- [culture](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/culture.md): [SOC-12](#soc-12), [SOC-14](#soc-14), [SOC-24](#soc-24), [SOC-25](#soc-25), [SOC-26](#soc-26), [SOC-34](#soc-34), [SOC-45](#soc-45)
- [discovery](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/discovery.md): [SOC-36](#soc-36)
- [dissent](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/dissent.md): [SOC-06](#soc-06), [SOC-07](#soc-07), [SOC-09](#soc-09), [SOC-10](#soc-10), [SOC-11](#soc-11), [SOC-12](#soc-12), [SOC-29](#soc-29), [SOC-30](#soc-30), [SOC-40](#soc-40), [SOC-43](#soc-43)
- [diversity](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/diversity.md): [SOC-01](#soc-01), [SOC-02](#soc-02), [SOC-07](#soc-07), [SOC-12](#soc-12), [SOC-13](#soc-13), [SOC-26](#soc-26), [SOC-33](#soc-33), [SOC-38](#soc-38), [SOC-40](#soc-40), [SOC-41](#soc-41), [SOC-44](#soc-44)
- [institutions](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/institutions.md): [SOC-20](#soc-20), [SOC-25](#soc-25), [SOC-27](#soc-27), [SOC-28](#soc-28), [SOC-29](#soc-29), [SOC-30](#soc-30)
- [leadership](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/leadership.md): [SOC-06](#soc-06), [SOC-16](#soc-16), [SOC-17](#soc-17), [SOC-18](#soc-18)
- [memory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/memory.md): [SOC-21](#soc-21), [SOC-22](#soc-22), [SOC-23](#soc-23), [SOC-24](#soc-24), [SOC-31](#soc-31), [SOC-45](#soc-45)
- [nca-observatory](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/nca-observatory.md): [PHY-17](#phy-17), [PHY-24](#phy-24), [PHY-37](#phy-37), [PHY-38](#phy-38)
- [quorum](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/quorum.md): [SOC-05](#soc-05), [SOC-08](#soc-08), [SOC-11](#soc-11), [SOC-39](#soc-39), [SOC-42](#soc-42), [SOC-43](#soc-43), [SOC-45](#soc-45)
- [regrowth](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/regrowth.md): [SOC-18](#soc-18), [SOC-22](#soc-22), [SOC-23](#soc-23)
- [telephone](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/telephone.md): [SOC-21](#soc-21), [SOC-31](#soc-31), [SOC-32](#soc-32), [SOC-34](#soc-34)
- [whistleblowing](https://github.com/dmarzzz/swarm-dynamics-lab/blob/main/5-experiments/studies/vishesh/project-briefs/whistleblowing.md): [SOC-10](#soc-10), [SOC-28](#soc-28), [SOC-29](#soc-29)
