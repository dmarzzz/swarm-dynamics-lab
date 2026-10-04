# Landscape map: how the swarm-lab topics connect

Owner: shadow/sol-atlas, holding task `synthesis-landscape-map`. Written 2026-10-04 against library snapshot
`10be71d5` (3,300 entries). Every count below is reproducible with
[landscape_counts.py](../researchers/shadow/notes/landscape-map/landscape_counts.py); the output is saved as
[counts.md](../researchers/shadow/notes/landscape-map/counts.md).

This is a map of the catalogue, not a survey. It has not been through the prior-art gate and proposes no
hypotheses. "Not tried" below means **not found in our library** by tag co-occurrence and text search; it is not a
claim about the wider literature. Read depths are shown as (abstract), (skim), (full) or (ran) next to an entry
whenever the claim leans on it.

## The short version

- The library has three regions. A **physics and biology core** (collective motion, active matter, criticality,
  collective decision, crowds), an **engineered-collectives ring** (swarm robotics, sync and consensus, swarm
  intelligence, MARL), and an **LLM and security region** (LLM agent swarms, Sybil resistance, fork-merge security,
  swarm detection, agent budgets, decision models, dissent). The LLM region holds 1,095 entries, 71% from 2025 and
  2026; the physics core is mostly older.
- The LLM community has imported **equilibrium statistical mechanics** (Ising, naming game, mean-field closures,
  Kuramoto order parameters) and **survey statistics** (design effect, effective team size). It has not imported
  the **measurement toolkit** of the collective-motion field (correlation length, topological interaction range,
  transfer entropy) or the **decision mechanisms** of social insects (quorum response, cross-inhibition,
  speed-accuracy tuning). Each of those has 0 mentions in LLM-tagged entries.
- The team's strongest completed results sit on one bridge: **more identities or more reports are not more
  evidence.** That idea appears independently in P2P security [[douceur-2002-sybil]], software reliability
  [[knight-1986-experimental]], survey statistics applied to LLM teams [[bertalanic-2026-ringelmann]] and an
  LLM-specific impossibility result [[bara-2026-epistemic]]. The dmarz Sybil cohorts and vishesh's Quorum of
  Mirrors are all instances of it.
- The security region and the physics core almost never cite each other (Sybil x active matter: 0 entries;
  Sybil x criticality: 1; fork-merge x collective motion: 2). The one working bridge into security from the
  engineered ring is robot Byzantine consensus (Sybil x sync-consensus: 79; Sybil x robotics: 49), and only two
  LLM-tagged entries carry it across.
- Recommended survey order (section 5): finish Sybil resistance and fork-merge (they carry the experiments), then
  agent budgets (an experiment is waiting on its gate), then collective decision and criticality-measurement
  (they supply the untried transfers).

## 1. The map

```
            PHYSICS AND BIOLOGY CORE                      ENGINEERED RING
   active-matter --124-- collective-motion --84-- swarm-robotics --69-- sync-consensus
        |                 |      \                     |      \            /     \
       34               111      77                   59       49 ------ 79      67
        |                 |        \                    |          \     /         \
 criticality-measurement  |   collective-decision --- marl-emergence  sybil-resistance
        |                 |        |   \                |               |    \
       45                34      105    65             29              104   125
        |                 |        |      \             |               |      \
   llm-agent-swarms <-----+----- llm-agent-swarms ----- fork-merge (254) ---- swarm-detection (200)
        |        crowds-and-traffic (9)          \
       41                                          20 -- decision-models -- 3 -- dissent
        |
   agent-budgets (0 with any physics topic)
```

Numbers are entries carrying both tags (co-tag matrix in counts.md). The drawing is a simplification: llm-agent-swarms
appears twice because it touches both the criticality corner (45) and the collective-decision corner (105).

### Corpus by topic

| topic | entries | relevance 5 | read full or ran | from 2025-2026 |
|---|---|---|---|---|
| collective-motion | 395 | 118 | 29% | 20% |
| collective-decision | 427 | 109 | 26% | 26% |
| swarm-robotics | 354 | 78 | 16% | 29% |
| swarm-intelligence | 126 | 27 | 17% | 26% |
| active-matter | 217 | 52 | 24% | 24% |
| sync-consensus | 337 | 88 | 28% | 26% |
| criticality-measurement | 248 | 82 | 32% | 33% |
| marl-emergence | 269 | 32 | 24% | 25% |
| llm-agent-swarms | 1,095 | 200 | 31% | 71% |
| crowds-and-traffic | 109 | 17 | 16% | 17% |
| sybil-resistance | 546 | 83 | 30% | 29% |
| fork-merge-security | 556 | 98 | 29% | 47% |
| swarm-detection | 755 | 77 | 37% | 55% |
| agent-budgets | 66 | 15 | 20% | 79% |
| decision-models | 25 | 24 | 4% | 72% |
| dissent | 5 | 3 | 0% | 40% |

Only one survey is complete (`llm-agent-swarms`; its three review files all say `revise`). Sybil resistance, fork-merge
security, simulation environments and decision models have in-progress surveys. The other eleven topics have none.

## 2. Each topic, placed

For each topic: where it sits, what it offers the others, and its 3 to 5 most important entries for this team.
"Most important" is a judgement weighted toward what the team's questions and experiments use, not citation count.

### Physics and biology core

**collective-motion.** The origin of most of the vocabulary: local alignment rules, order parameters, phase
transitions, and the first quantitative field data on real flocks. Feeds active matter (124 shared entries) and
criticality (111). Touches the LLM region in only 7 entries.
- [[vicsek-1995-novel]] (full): the self-propelled particle model; a noise-driven transition from disorder to
  collective motion. The reference model everyone else perturbs.
- [[couzin-2002-collective]] (full): zone model; four collective states from changing only orientation and
  attraction zone widths, with hysteresis between them. Hysteresis is the property the capture-memory work asks
  about in LLM populations.
- [[ballerini-2008-interaction]] (full): starlings interact with a fixed number of neighbours (about 6.5), not a
  fixed distance. The topological-versus-metric question.
- [[cavagna-2010-scale]] (full): correlation length of velocity fluctuations grows linearly with flock size, so
  correlations are scale-free.
- [[reynolds-1987-flocks]] (abstract): boids; the engineering ancestor.

**active-matter.** The continuum and statistical-physics theory of self-propelled systems. Offers hydrodynamic
theories, phase diagrams and the warning that apparent order-disorder transitions can be phase separation. No
shared entries with the LLM region (0).
- [[toner-1995-long]] (full): long-range order in 2D flocks, impossible in equilibrium XY models.
- [[cates-2015-motility]] (full): motility-induced phase separation; particles accumulate where they slow down.
- [[fily-2012-athermal]] (full): phase separation with no alignment rule at all.
- [[solon-2015-phase]] (abstract): the Vicsek transition reread as liquid-gas, not order-disorder.
- [[vicsek-2012-collective]] (skim): the review that ties motion, active matter and robotics together.

**criticality-measurement.** The measurement layer. Order parameters, criticality claims, maximum-entropy fits,
information-theoretic estimators. It is the topic with the highest share of full reads in the core (32%) and the
best-connected core topic to the LLM region (45 shared entries), almost all through Ising-style LLM opinion papers.
- [[mora-2011-biological]] (full): the inverse statistical-mechanics programme and what "poised at criticality"
  can and cannot mean.
- [[munoz-2018-colloquium]] (abstract): the criticality hypothesis for living systems and its toolkit.
- [[bialek-2012-statistical]] (abstract): maximum-entropy model of starling flight directions, no free parameters.
- [[lizier-2014-jidt]] (abstract): the transfer-entropy and active-information-storage toolkit.
- [[lord-2016-inference]] (abstract): causation entropy recovers direct influence channels from midge
  trajectories.

**collective-decision.** Biological group decisions: honeybee and ant house-hunting, quorum responses, informed
minorities. This is the core topic with the most traffic to the LLM region (105 shared entries) and to security
(Sybil 67, fork-merge 65), because "how should a group count votes it cannot verify" is the same question there.
- [[sumpter-2009-quorum]] (full): quorum responses as the common mechanism of consensus in insects and fish.
- [[seeley-2012-stop]] (abstract): stop signals give cross-inhibition, breaking deadlock between equal options.
- [[couzin-2005-effective]] (abstract): a small uninformed-to-informed ratio steers large groups without signalling.
- [[couzin-2011-uninformed]] (abstract): adding uninformed individuals returns control to the numerical majority
  and blunts an opinionated minority.
- [[pratt-2006-tunable]] (abstract), with [[franks-2003-speed]] (abstract): one algorithm, parameters tuned for
  speed or accuracy depending on urgency.

**crowds-and-traffic.** Human collectives as driven many-particle systems. Small (109 entries) and lightly read
(16% full). Offers the cleanest experimental demonstrations of instabilities and of a single controlled agent
removing them.
- [[helbing-1995-social]] (full): the social force model.
- [[helbing-2000-simulating]] (full): faster-is-slower at exits.
- [[sugiyama-2008-traffic]] (full): jams with no bottleneck on a ring road.
- [[stern-2018-dissipation]] (full): one automated car dissipates the human stop-and-go wave.
- [[gu-2025-emergence]] (full): 6,000-person crowd above a critical density self-organises into collective
  oscillations.

### Engineered ring

**swarm-robotics.** Physical and simulated robot swarms. Bridges the core (motion 84, active matter 69) to
consensus (69) and, through Byzantine robots, to Sybil resistance (49). Lightly read (16% full).
- [[brambilla-2013-swarm]] (abstract): the swarm-engineering review and taxonomy.
- [[rubenstein-2014-programmable]] (abstract): a thousand Kilobots self-assemble shapes.
- [[valentini-2017-best]] (full): best-of-n formalism for collective decisions in robot swarms.
- [[vasarhelyi-2018-optimized]] (full): Vicsek-style flocking on real outdoor drones, with 11 parameters tuned by CMA-ES.
- [[strobel-2020-blockchain]] (full): linear consensus, W-MSR and a blockchain contract compared against Byzantine
  robots.

**sync-consensus.** Consensus protocols, synchronisation and networked control. The formal backbone that both
robotics and the LLM opinion papers use, and the main bridge into security (Sybil 79, fork-merge 51).
- [[olfati-saber-2007-consensus]] (abstract): the consensus tutorial; dx/dt = -Lx.
- [[jadbabaie-2003-coordination]] (full): why noiseless Vicsek aligns, as a switched linear system.
- [[dorfler-2014-synchronization]] (skim): Kuramoto on networks, from the control side.
- [[okeeffe-2017-oscillators]] (full): swarmalators, coupling sync and motion.
- [[leblanc-2013-resilient]] (abstract): resilient consensus with local filtering; robustness, not connectivity, is
  the right graph measure.

**swarm-intelligence.** Optimisation metaheuristics inspired by insects and flocks. Weakly connected (126 entries,
17% full) and carries its own critique: much of the field renames old components.
- [[kennedy-1995-particle]] (abstract): particle swarm optimisation.
- [[dorigo-1996-ant]] (abstract): ant system.
- [[theraulaz-1999-brief]] (abstract): stigmergy, the coordination-through-environment idea that recurs in LLM
  message boards.
- [[sorensen-2015-metaheuristics]] (abstract) and [[camacho-villalon-2023-exposing]] (abstract): the metaphor
  critique.
- [[pinnau-2017-consensus]] (full): consensus-based optimisation, PSO's continuous mean-field cousin.

**marl-emergence.** Learned coordination. Offers mean-field approximations for large populations and methods that
learn interaction rules from data. Connects mainly to robotics (59); its 29 LLM co-tags are mostly benchmarks and
talks.
- [[yang-2018-mean]] (full): mean-field MARL; each agent sees the mean action of its neighbours.
- [[huttenrauch-2019-deep]] (full): permutation-invariant observation embeddings for swarms.
- [[durve-2020-learning]] (full): independent Q-learners rediscover Vicsek alignment.
- [[heras-2019-deep]] (abstract): attention networks recover zebrafish interaction rules from trajectories.
- [[li-2023-predator]] (abstract): survival pressure alone evolves swarming.

### LLM and security region

**llm-agent-swarms.** The largest and newest topic. Its centre of gravity is opinion and convention dynamics in
LLM populations, effective team size, and the 2026 in-the-wild incidents. Strongly linked to fork-merge (254),
detection (200), collective decision (105) and Sybil (104).
- [[de-marzo-2026-conformity]] (full): adoption probability fits tanh(beta(m+h)) across nine LLMs; inside the
  mean-field spinodal, misaligned states are metastable.
- [[ashery-2024-emergent]] (full): naming-game conventions, collective bias and committed-minority tipping in LLM
  populations.
- [[bertalanic-2026-ringelmann]] (full): effective team size via the Kish design effect; a hard ceiling when
  agreement does not fall with N.
- [[yang-2026-when]] (skim): coupling gain measured counterfactually; social coupling is about equal to numeric
  anchoring, so "emergent consensus" needs a control.
- [[de-marzo-2026-copying]] (skim): an unplanned 1,201-handle swarm on German wikis is explained by one
  proportional-copying rule.

**sybil-resistance.** Identity cost and false-name manipulation across P2P networks, mechanism design, robot swarms
and agent registries. Carries most of the team's completed experiments.
- [[douceur-2002-sybil]] (full): identity distinctness cannot be established without a trusted authority or
  unrealistic resource assumptions.
- [[conitzer-2010-using]] (full): false-name-proof mechanism design, the economics name for the same problem.
- [[mazorra-2023-cost]] (full): the price of identity when every player may clone.
- [[gil-2015-guaranteeing]] (skim): physical Wi-Fi fingerprints as a Sybil defence in robot networks.
- [[bara-2026-epistemic]] (full): no content-only aggregator can tell replication from corroboration; extra reports
  from one root collapse interval coverage from 0.940 to 0.263.

**fork-merge-security.** Agents that split and merge back, and how corruption returns on merge. Draws on Byzantine
fault tolerance, design diversity, federated poisoning, prompt and memory injection, and AI control.
- [[lamport-1982-byzantine]] (skim): the Byzantine generals problem.
- [[knight-1986-experimental]] (full): 27 independently written programs fail together far more than independence
  predicts (z = 100.51).
- [[kim-2025-correlated]] (full): LLM errors agree when both are wrong about twice the random rate, and more
  accurate models are more correlated.
- [[bagdasaryan-2020-how]] (full): one participant's scaled update replaces the federated model.
- [[dong-2025-memory]] (full) and [[greenblatt-2023-ai]] (full): query-only memory injection, and the control
  evaluation frame.

**swarm-detection.** Finding many automated identities acting for one operator, in the wild. Highest full-read
share in the library (37%). Its natural partner is Sybil resistance (125 shared entries).
- [[cao-2014-uncovering]] (skim): SynchroTrap; loosely synchronised actions on shared targets expose account groups.
- [[pacheco-2021-uncovering]] (full): the general unsupervised coordination-network recipe.
- [[gallwitz-2022-investigating]] (full): bot-score prevalence estimates are circular; audits find many false bots.
- [[liang-2024-monitoring]] (full): corpus-level, not document-level, estimation of LLM text.
- [[pasquini-2024-llmmap]] (full): eight probes identify the model behind an application.

**agent-budgets.** How agents perceive and divide compute, tokens, tool calls and money. Small (66 entries), new
(79% from 2025-2026), and isolated: 0 shared entries with any physics topic, 4 with MARL, 9 with Sybil.
- [[liu-2025-budget]] (skim): tool-call budgets saturate; an in-context budget tracker fixes it.
- [[wang-2026-r3]] (skim): six problems on one shared token budget; models misallocate against their own replay.
- [[lin-2026-bagen]] (abstract): budget-awareness as progressive interval estimation.
- [[anthropic-2026-task]] (full, vendor documentation): a model-visible task budget countdown.
- [[moulin-2007-scheduling]] (skim): merging and splitting jobs across identities to game a scheduler, the
  classical form of quota splitting.

**decision-models.** Typed classifiers such as Jev, calibration and provenance-aware decisions. 25 entries, 1 read
in full. Effectively a sub-area of llm-agent-swarms (20 shared entries).
- [[gh-dy-ma-jev-world]] (skim): Jev land/water renders; explicitly not an accuracy benchmark.
- [[deusser-2026-evaluating]] (abstract): Jev calibration on Choice versus binary thresholds.
- [[guo-2017-calibration]] (abstract): accuracy is not calibration.
- [[jin-2026-not]] (abstract): provenance partitions make evidence counts duplication-invariant.
- [[wang-2026-graphecho]] (full): redundant graph paths change LLM judgements.

**dissent.** Minority evidence and decision repair. 5 entries, none read in full. The thinnest topic with an active
experiment line (vishesh's Right Dissenter).
- [[seeley-2012-stop]] (abstract): stop signals as bounded challenge.
- [[mansuri-2026-multi]] (abstract): discussion gains shrink when dissent is withheld.
- [[hay-2012-selecting]] (skim): when a computation (a check) is worth its cost.
- [[tan-2016-honey]] (abstract): inhibitory signalling tuned to threat severity.
- [[he-2026-minority]] (abstract, not tagged dissent): the minority is right in about one in four divergent debates.

**meta.** Methods and validity. The entries the team cites most when judging its own work.
- [[larooij-2025-do]] (full): 35 generative agent-based modelling papers, mostly validated subjectively and from one
  run.
- [[zhou-2025-pimmur]] (abstract): LLMs identify the social experiment they are in 65.2% of the time.
- [[shalizi-2011-homophily]] (skim): homophily and contagion are confounded in observational networks.
- [[aronow-2013-estimating]] (skim): exposure mappings for interference.
- [[jansen-2021-once]] (full): one simulation per configuration is not enough.

## 3. Cross-community transfers

### 3.1 Transfers that have been tried

Each line: the source idea, the community it came from, the LLM or security work that imports it, and what came
back. Results are as reported in the entries; read depth matters.

1. **Ising and mean-field opinion dynamics** (statistical physics, sync-consensus) into LLM populations.
   [[de-marzo-2024-ai]] (full) fits Glauber dynamics of the Curie-Weiss model; [[de-marzo-2026-conformity]] (full)
   measures beta and h across nine models; [[el-2026-physics]] (full) fits an Ising-type model to about 10,000
   communities; [[okawa-2026-emergence]] (skim) models debate as tanh(beta(Jm + h)). Outcome: the closures fit and
   predict. Caveat from [[yang-2026-when]] (skim): the measured coupling equals numeric anchoring, so a fitted
   field does not by itself show a social mechanism.
2. **Naming game and committed-minority tipping** (sociophysics) into LLM populations. [[ashery-2024-emergent]]
   (full), [[flint-2026-group]] (full, cached policies up to N of about 10^4), [[flint-2026-indirect]] (skim,
   tipping through intermediate conventions), [[de-nobili-2026-microscopic]] (full, the listener check as a
   temperature-dependent YES/NO). Outcome: conventions, bias amplification and tipping all reproduce. Whether
   capture reverses after the minority leaves is contested between [[magistrali-2026-aligned]] (full) and
   [[de-marzo-2026-conformity]]; the team's capture-memory and capture-memory-mix notes test memory length as the
   deciding variable (see section 4).
3. **Kuramoto order parameters** (synchronisation) into LLM estimate panels. [[hirota-2026-collective]] (full)
   maps circular answers to phases and classifies regimes by global and local order. One study.
4. **Absorbing-state phase transitions** into multi-agent search. [[zheng-2026-absorbing]] (abstract) derives a
   critical communication degree; agreement with experiment is described as mixed.
5. **DeGroot and Friedkin-Johnsen consensus** (networked control) into LLM agents. [[chen-2023-multi]] (full):
   GPT-3.5 agents spontaneously average their neighbours, which is DeGroot consensus. [[yang-2026-when]] uses
   Friedkin-Johnsen with measured coefficients.
6. **Design effect and correlated failure** (survey statistics and software reliability) into LLM teams and
   judges. [[bertalanic-2026-ringelmann]] (full), [[kohli-2026-nine]] (skim: nine judges carry about two
   independent votes), [[begin-2026-preference]] (skim: ten same-model traders equal about 1.38 forecasters),
   [[kim-2025-correlated]] (full). The software antecedent is [[knight-1986-experimental]]. This transfer is the
   most consequential for the team (section 4).
7. **Classical swarm algorithms run by LLMs** (swarm intelligence, collective motion). [[rahman-2025-llm-powered]]
   (abstract): LLM boids took about 300 times the compute of classical boids. [[zomer-2026-unraveling]] (full):
   an LLM agent swarm against constriction PSO; individual ability does not become collective performance, and
   topology dominates. [[li-2024-challenges]] (abstract): LLM agents fail to flock. [[jimenez-romero-2025-multi-agent]]
   (abstract): NetLogo ant foraging and flocking with GPT-4o. Outcome: possible, costly, rarely better.
8. **Swarm-robotics task suites** into LLM evaluation. [[ruan-2025-benchmarking]] (full): SwarmBench, five grid
   tasks under local views; coordination is rudimentary and model-specific.
9. **Byzantine-resilient consensus** (robotics, distributed systems) into LLM agent graphs. [[lee-2026-robust]]
   (abstract) states (F+1)-robustness conditions for LLM peer-to-peer filtering; [[jo-2025-byzantine]] (full)
   uses Byzantine reliable broadcast and a geometric median over evaluator scores; [[liu-2026-consensus]] (full)
   shows majority voting collapses once injected agents are a majority of five.
10. **False-name-proof mechanism design** (economics) into LLM agents. [[gh-brunomazorra-llms-sybils]] (skim) is
    a harness asking whether agents discover extra identities unprompted; [[karten-2026-agent]] (skim) runs one
    deceptive principal with K seller identities. The team's market-split cohorts are a third instance (section 4).
11. **Mean-field approximations** (MARL) into LLM population simulation. [[mi-2025-mf-llm]] (skim) replaces
    all-to-all reading with a learned mean-field signal and matches Weibo trajectories better. One study, and it
    targets simulation fidelity, not control.
12. **Wisdom-of-crowds network experiments** (human collective decision) into LLM deliberation. Antecedents
    [[becker-2017-network]] (skim) and [[lorenz-2011-how]] (skim); LLM imports [[li-2026-diverse]] (abstract:
    identical evidence herds, partitioned evidence helps) and [[liu-2026-social]] (skim: bounded effective N under
    narrow attention).
13. **Stigmergy** (social insects) into LLM societies. [[pal-2026-swarmworld]] (abstract) and the sealed board of
    [[gh-killy-netsphere-sealed-swarm-transcripts]] (skim), where a shared board synchronised the swarm on one
    frontier and carried errors as efficiently as the one real invention.
14. **Information-theoretic emergence measures** (complex systems) into LLM groups. [[riedl-2025-emergent]] (full)
    uses higher-order information measures to separate a genuine collective from independent agents. This is the
    only catalogued LLM study that uses the information-decomposition side of the criticality-measurement
    toolkit.
15. **Learning interaction rules from trajectories** (MARL and animal behaviour, [[heras-2019-deep]]) into wild
    agent data. [[de-marzo-2026-copying]] (skim) fits one copying rule to three decisions per arriving wiki agent.

### 3.2 Transfers that have not been tried (in our library)

Evidence for absence: the concept counts in counts.md (0 or near-0 mentions in llm-agent-swarms entries), plus
targeted text searches of the library on 2026-10-04. A wider literature search might find work we have not
catalogued. Each item names the closest work we do have.

1. **Correlation length and scale-free correlations** ([[cavagna-2010-scale]], [[bialek-2012-statistical]]) applied
   to LLM populations. 23 mentions in natural-systems entries, 0 in LLM entries. The question it would answer: does
   a perturbation to one agent's belief decorrelate locally or span the whole population as N grows? Closest: the
   global and local Kuramoto order of [[hirota-2026-collective]], which measures order, not correlation range.
2. **Topological versus metric interaction range** ([[ballerini-2008-interaction]]) applied to how many messages
   an agent reads. 19 mentions in natural entries, 0 in LLM entries. [[bertalanic-2026-ringelmann]] finds that peer
   count k and rounds tau enter only through k tau, and [[liu-2026-social]] models attention width; neither frames
   it as a fixed-k versus fixed-radius comparison on a spatial or graph layout.
3. **Transfer entropy and causation entropy** ([[lizier-2014-jidt]], [[lord-2016-inference]]) to recover who
   influences whom from agent message traces. 14 natural mentions, 0 LLM. Swarm detection uses co-action similarity
   ([[cao-2014-uncovering]], [[pacheco-2021-uncovering]]) rather than directed information flow. The confounding
   warning of [[shalizi-2011-homophily]] applies to both.
4. **Quorum responses and speed-accuracy tuning** ([[sumpter-2009-quorum]], [[pratt-2006-tunable]],
   [[franks-2003-speed]]) as commit rules for LLM committees. 15 and 11 natural mentions, 0 LLM. The team's own
   attempt is vishesh's adaptive quorum (Antsy), where fixed and adaptive quorums tied on its evidence tapes
   ([experiments/EVIDENCE.md](../experiments/EVIDENCE.md), `antsy-v1`).
5. **Cross-inhibition and stop signals** ([[seeley-2012-stop]], [[reina-2017-model]]) as a bounded-dissent or
   anti-deadlock mechanism in LLM debate. 13 natural mentions, 0 LLM. The closest LLM work is
   [[mansuri-2026-multi]] (abstract) on withheld dissent; vishesh's Right Dissenter plan cites Seeley as biological
   motivation ([PLAN](../researchers/vishesh/notes/dissent/PLAN.md)).
6. **Uninformed individuals as a defence** ([[couzin-2011-uninformed]]): neutral members return control from an
   opinionated minority to the majority. Never tested against LLM committed minorities or Sybil coalitions. The
   sealed swarm reports exploit spread from 3 informed to 16 uninformed lineages
   ([[gh-killy-netsphere-sealed-swarm-transcripts]]), which is the opposite direction (uninformed agents as carriers).
7. **Physical and trust-side-channel Sybil defences** ([[gil-2015-guaranteeing]], [[yemini-2021-characterizing]],
   [[mallmann-trenn-2021-crowd]]) applied to software agents. Listed as a gap in the Sybil survey draft
   (`surveys/sybil-resistance.md`, Gaps). Their guarantees are stated over abstract trust observations, so a
   software analogue (attested runtime, metered compute) is a direct substitution.
8. **A single controlled damper agent** ([[stern-2018-dissipation]]): one automated car removed a stop-and-go wave.
   The analogous LLM question, whether one scripted stabilising agent can dissipate a belief cascade, is untested.
   The capture-memory-mix mixtures (a few full-memory agents among short-memory ones) are the nearest team result.
   This is a speculative bridge; the mechanism (velocity control on a ring) has no proven analogue.
9. **Mean-field games and market-based allocation for shared budgets.** Agent budgets has 0 shared entries with any
   physics topic and 4 with MARL. Classical task markets ([[smith-1980-contract]], abstract) and job splitting
   ([[moulin-2007-scheduling]]) are catalogued, but no entry applies mean-field allocation to LLM agents sharing a
   token pool. [[wang-2026-r3]] measures misallocation for one model, not a population.
10. **Correlated shared-input corruption in k-of-n merges.** Error-correlation figures are all for natural errors
    ([[kim-2025-correlated]]); the directed-corruption sweep is five agents ([[liu-2026-consensus]]). Listed as a gap
    in the fork-merge survey draft.
11. **Fission-fusion dynamics as a measured model for fork-and-merge** ([[aureli-2008-fission]], skim). The
    fork-merge survey draft notes there is no primary measurement of reunion behaviour beyond the framework.
12. **The metaheuristic metaphor critique** ([[sorensen-2015-metaheuristics]], [[camacho-villalon-2023-exposing]])
    applied to "LLM swarm" systems. Only [[rahman-2025-llm-powered]] checks swarm principles against an LLM
    framework. A component-level deconstruction of LLM "swarm" orchestrators has not been catalogued.
13. **Active-matter mechanisms of any kind.** 0 shared entries between active-matter and llm-agent-swarms.
    Density-dependent slowing ([[cates-2015-motility]]) has an obvious verbal analogue in agents crowding a shared
    resource, but that analogy is not supported by any catalogued measurement. Listed for completeness, not
    recommended.

## 4. Where the team's experiments sit on this map

Source: [experiments/EVIDENCE.md](../experiments/EVIDENCE.md) and dmarz's
[latest results review](../researchers/dmarz/notes/latest-results-review-2026-10-04/evidence.json). Numbers are as
reported by the owners; independent recomputation is a separate task (`review-dmarz-completed-xcheck`).

- **Sybil resistance and identity splitting (dmarz).** The densest experimental cluster. Examples: proportional
  checks raised Sonnet specialist accuracy by +52.8 pp at 972 identities
  ([sybil-scale-sonnet](../researchers/dmarz/notes/sybil-scale-sonnet/RESULTS.md)); splitting a fixed attacker
  budget across identities raised rare-skill wrong answers +41.0 pp more under degree-based than coverage-based
  admission ([sybil-split-opus](../researchers/dmarz/notes/sybil-split-opus/RESULTS.md)); cutting truthful carriers
  from 81 to 1 dropped accuracy by 95.8 pp
  ([sybil-scarcity-opus](../researchers/dmarz/notes/sybil-scarcity-opus/RESULTS.md)). Map position: Sybil x
  collective-decision x the N_eff transfer (3.1 item 6). The scripted identities feed one model synthesizer, so
  these are admission and aggregation results, not autonomous-swarm results.
- **Market splitting (dmarz).** A flexible LLM owner split into another firm in 6/6 firm-regulated markets and 0/6
  owner-regulated markets ([market-split-api](../researchers/dmarz/notes/market-split-api/RESULTS.md)). Map
  position: false-name-proof mechanism design (3.1 item 10) meeting agent budgets.
- **Quorum of Mirrors, Phantom Coast, Right Dissenter, Antsy (vishesh).** Collective decision under repeated or
  missing evidence. Quorum of Mirrors Q1-02: 0/8 graded full-lineage cases correct; choices tracked the copied
  majority. Map position: the same N_eff bridge from the decision-models side, plus the untried quorum and
  cross-inhibition transfers (3.2 items 4 and 5).
- **Discussion dose and compositional safety (dmarz), Theseus and Immune Response (vishesh).** Fork-merge and
  memory repair. Map position: fork-merge x llm-agent-swarms.
- **Capture-memory and capture-memory-mix (shadow).** Committed-minority capture and reversal versus memory length.
  Map position: the naming-game transfer (3.1 item 2) at the Magistrali-De Marzo disagreement. Scripted mixtures
  rescued return; the Qwen real-model run did not reproduce the mixture benefit (dmarz review verdict: "Mixture
  rescue does not generalize").
- **Not touched by any team experiment:** collective motion, active matter, crowds and traffic, swarm intelligence,
  and the criticality measurement toolkit beyond order parameters. Regrowth-200 (route repair) is the only study in
  the engineered ring and has one map.

The pattern: experiments cluster where the library is newest and most LLM-specific. The older core is catalogued
but unused, which is consistent with the hackathon's LLM framing; it also means the cheapest novelty for a later
round is a measurement transfer from the core onto data the team already has (sealed swarm transcripts, the wiki
corpus, its own run records).

## 5. Ranked survey priorities

Ranked by decision value for the team now: does a pending hypothesis or experiment need the gate, does the survey
supply an untried transfer, and how much of the corpus is already read. The first two are owned surveys; this list
recommends, it does not reassign.

0. **Answer the narrow llm-agent-swarms revise first.** It is the only complete survey and three hypotheses rest
   on it (`shadow-board-nsweep`, `shadow-capture-memory`, `shadow-neff-evidence-board`). All three review files
   say `revise`; the latest re-review ([llm-agent-swarms--dmarz-inbox](../reviews/llm-agent-swarms--dmarz-inbox.md))
   calls it "revise, narrowly" with the gate passing. This is owner repair work, not a new survey, but no
   hypothesis on it can reach `accepted` until a review passes.
1. **survey-sybil-resistance** (in progress, dmarz). The largest block of completed experiments depends on it, and
   its draft Gaps section already lists concrete openings. Finishing the gate turns the dmarz cohorts from notes into
   hypothesis-backed work. 546 entries, 30% full.
2. **survey-fork-merge-security** (in progress, dmarz). Discussion-dose, compositional safety, Theseus and Immune
   Response sit here. Its draft has ten specific gaps, the most of any survey. 556 entries, 29% full.
3. **survey-agent-budgets** (open). The quota-splitting experiment (`build-quota-splitting`, hunch B2) is waiting
   on this gate, and the task's Done-when asks the exact question the experiment needs: has anyone measured LLM
   agents spawning identities to claim per-identity quota. Small corpus (66 entries), so it is the fastest gate to
   pass, but only 20% is read in full and the isolation in section 3.2 item 9 means the search must reach into
   economics and operating-systems vocabulary.
4. **survey-collective-decision** (open). Supplies four of the untried transfers (quorum response, cross-inhibition,
   speed-accuracy, uninformed individuals) and is the prior art behind vishesh's quorum, dissent and Phantom Coast
   lines, none of which has a survey of its own. 427 entries, 26% full, strongest core link to the LLM region.
5. **survey-criticality-measurement** (open). The measurement toolkit for untried transfers 1 to 3 (correlation
   length, interaction range, transfer entropy) and the validity checks for the many LLM "phase transition" claims.
   Highest full-read share in the core (32%).
6. **survey-sync-consensus** (open). The formal bridge between robot Byzantine consensus and LLM agent graphs
   (Sybil co-tags: 79), and the DeGroot and Friedkin-Johnsen models the LLM opinion papers already use.
7. **survey-swarm-detection** (open). Large (755 entries) and well read (37% full), and dmarz's detection synthesis
   already organises it, so a survey is mostly conversion work. Lower rank because no detection experiment has run;
   the false-alarm cascade study is planned.
8. **survey-marl-emergence** (open). Mean-field RL and rule-learning methods (3.1 items 11 and 15). Useful once the
   team fits update rules to its own transcripts.
9. **survey-swarm-robotics** (open). Best-of-n and robot Sybil defences are the useful parts; much of it is
   covered from the Sybil and sync-consensus side. 16% full.
10. **survey-collective-motion** (open). Foundational and well read (29% full), but no team question currently
    depends on it beyond vocabulary.
11. **survey-crowds-and-traffic** (open). One concrete bridge (the single-damper idea, 3.2 item 8), otherwise
    remote from current work. 16% full.
12. **survey-active-matter** (open). No shared entries with the LLM region and no team question that needs it.
13. **survey-swarm-intelligence** (open). The catalogued LLM transfers (3.1 item 7) report weak or costly results,
    and the field's own critique argues against new metaphor-driven work.

Other survey-kind tasks: `heterogeneous-methods-review` and `quorum-mirrors-research-gates` (vishesh) slot in
beside items 4 and 2 respectively; `survey-avalon-swarm` (p2) is a testbed survey for Sybil and fork-merge work and
belongs after items 1 and 2.

## 6. Limits of this map

- Topic tags are assigned by whoever catalogued the entry and are uneven. Some relevant entries lack a tag
  ([[he-2026-minority]] is about dissent but not tagged with it). Co-tag counts undercount real overlap.
- Concept counts are regex hits over entry text, including notes and links, so a passing mention counts the same
  as a central one. They show what the catalogue discusses, not what the literature contains.
- Read depth is the cataloguer's claim. Most entries are abstract or skim; [[gh-dy-ma-jev-world]] and other
  decision-models entries are especially thin. I did not re-read sources for this map; summaries are taken from
  library entries.
- "Most important" entries are a judgement weighted toward this team's questions.
- Experiment numbers in section 4 are owner-reported; see the xcheck review task for recomputation.
