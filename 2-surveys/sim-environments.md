---
id: sim-environments
type: survey
title: 'Multi-agent and swarm simulation environments: what exists, what runs on a laptop today, and what is still missing before we build our own'
owner: dmarz
agents: [dmarz/sim-envs]
status: in-progress  # set to complete only when `python3 scripts/lab.py gate sim-environments` passes
started: 2026-10-03
topics: [llm-agent-swarms, marl-emergence, swarm-robotics, collective-motion, sybil-resistance, fork-merge-security, swarm-detection, meta]
questions:
  - Which simulation environments already exist for many interacting agents (LLM agents, RL agents, rule-based ABM agents, robots, network nodes), and what interaction model, scale and maintenance state does each have?
  - Which of them can host LLM-driven agents, an open population (agents joining, leaving, forking, merging mid-run), and adversarial identities (Sybils, impostors, compromised sub-agents) without rewriting the engine?
  - What has the literature already established about building such simulators (validity, update order, leakage, throughput, reproducibility) that a new environment must not rediscover?
  - For each research line in this lab (swarm dynamics, Sybil resistance, fork-and-merge security, swarm detection), what should we bootstrap from, and what genuinely has to be built?
seminal: [park-2023-generative, leibo-2021-scalable, grimm-2020-odd, yang-2024-oasis]
search_log:
  # One row per search round, in the order you ran them. `results` = relevant hits you looked at,
  # `new` = how many of those were not already in library/. The last rounds must show saturation.
  # Lanes ran in parallel on 2026-10-03; rows are grouped by lane in the order each lane ran them, then the
  # saturation pass in its run order. GitHub rounds in the saturation pass count only repos above the stated
  # star threshold, which flatters the last rounds: see ## Saturation.
  # Lane: LLM-agent societies
  - {where: github, query: "gh search: llm agent social simulation, multi-agent llm benchmark, llm werewolf, social deduction llm, llm social simulation", date: 2026-10-03, results: 55, new: 3}
  - {where: web, query: "github LLM agent social media simulation framework sybil bots 2025; survey benchmarks multi-agent LLM environments arena games", date: 2026-10-03, results: 30, new: 12}
  - {where: citations-backward, query: "GitHub links in the awesome-llm-social-simulation README", date: 2026-10-03, results: 29, new: 8}
  - {where: arxiv, query: "agent-based AND LLM AND (validation OR critical OR promising)", date: 2026-10-03, results: 14, new: 3}
  - {where: hn, query: "Algolia: LLM agent simulation", date: 2026-10-03, results: 20, new: 2}
  - {where: web, query: "arxiv 2025 open-source platform simulate thousands of LLM agents social network", date: 2026-10-03, results: 10, new: 4}
  # Lane: MARL suites and GPU engines
  - {where: github, query: "gh api repos/ on 33 named MARL and GPU-engine candidates", date: 2026-10-03, results: 30, new: 30}
  - {where: github, query: "gigastep, pufferlib, gpudrive, madrona escape room, multi-agent jax, neural mmo 3", date: 2026-10-03, results: 30, new: 3}
  - {where: github, query: "multiagent environment; MARL benchmark; marl environment; textarena", date: 2026-10-03, results: 52, new: 2}
  - {where: arxiv, query: "survey+environments; multi-agent+GPU+env/benchmark; massively multiagent", date: 2026-10-03, results: 33, new: 7}
  - {where: arxiv, query: "targeted titles: SMACv2, Gigastep, WarpDrive, NMMO 2.0, Gorsane, Papoudakis, open-ended multi-agent", date: 2026-10-03, results: 8, new: 2}
  - {where: web, query: "Gigastep paper; MA-Craftax repo; MARL environment survey 2024-25", date: 2026-10-03, results: 27, new: 5}
  - {where: arxiv, query: "POGEMA, Gorsane, ad hoc/open populations, LLM+MARL benchmark, Lux, Flatland", date: 2026-10-03, results: 5, new: 1}
  - {where: citations-backward, query: "related work of SMACv2, NMMO 2.0, Gigastep, GPUDrive; Table 6 of hu-2025-toward", date: 2026-10-03, results: 60, new: 15}
  # Lane: ABM frameworks and swarm robotics
  - {where: github, query: "agent-based modeling framework; swarm simulator; drone swarm simulation; agent-based simulation GPU; LLM agent-based modeling; kilobot simulator; multi-robot simulator; flocking boids", date: 2026-10-03, results: 70, new: 3}
  - {where: github, query: "gh api lookups of 29 seed ABM and robotics repos", date: 2026-10-03, results: 27, new: 18}
  - {where: arxiv, query: "FLAME GPU, Agents.jl, Repast4Py, gym-pybullet-drones, Aerial Gym, SwarmLab, AgentTorch, krABMaga, mesa+LLM, ABM comparisons, async updating", date: 2026-10-03, results: 20, new: 6}
  - {where: web, query: "Melodie JOSS; ODD 2020 JASSS; FLAME GPU 2 SPE; synchronous vs asynchronous updating artefacts", date: 2026-10-03, results: 37, new: 5}
  - {where: citations-backward, query: "Datseris 2022 references; README links of Agents.jl, gym-pybullet-drones, FLAME; Radax to Huberman", date: 2026-10-03, results: 15, new: 4}
  - {where: github, query: "agent-based rust; swarm-simulator python; agent-based jax; mesa llm agents", date: 2026-10-03, results: 32, new: 0}
  # Lane: network, market and adversarial substrates
  - {where: github, query: "direct API lookups of 24 named repos (Shadow, ns-3, Testground, PeerSim, SimBlock, BlockSim, cadCAD, radCAD, TokenSPICE, ABIDES, Inspect, Petri, attacknet)", date: 2026-10-03, results: 19, new: 19}
  - {where: github, query: "peersim, kademlia simulator, sybil attack simulator, botnet llm, mev ABM, PBS sim, llm market sim", date: 2026-10-03, results: 14, new: 4}
  - {where: web, query: "attacknet ethereum chaos; BotSim; MEV PBS auction ABM", date: 2026-10-03, results: 27, new: 6}
  - {where: web, query: "Magentic Marketplace; gossipsub hardening Sybil Testground; LLM Sybil sandbox arXiv", date: 2026-10-03, results: 27, new: 3}
  - {where: github, query: "honeypot, hive, assertoor, chaos-mesh, jepsen, maelstrom, madsim, TwinMarket, rbuilder", date: 2026-10-03, results: 18, new: 5}
  - {where: arxiv, query: "Once is Never Enough; Co-opting Linux Processes; Running Tor in a Box; BlockSim", date: 2026-10-03, results: 10, new: 2}
  - {where: citations-backward, query: "tornettools README to Jansen 2021; BotSim references (S3, Chirper, TwiBot)", date: 2026-10-03, results: 8, new: 1}
  - {where: semantic-scholar, query: "batch lookup of 9 simulator papers", date: 2026-10-03, results: 9, new: 0}
  - {where: web, query: "LLM agents P2P Sybil/eclipse reputation simulation arXiv 2025-2026", date: 2026-10-03, results: 9, new: 1}
  - {where: hn, query: "deterministic simulation testing: Shadow, Antithesis, madsim", date: 2026-10-03, results: 9, new: 1}
  # Saturation pass
  - {where: github, query: "lead resolution: 19 named forward-citation and leftover leads (arXiv + GitHub)", date: 2026-10-03, results: 19, new: 18}
  - {where: citations-forward, query: "Semantic Scholar citers of Melting Pot arXiv:2107.06857, title filter, top 25", date: 2026-10-03, results: 21, new: 16}
  - {where: citations-forward, query: "Semantic Scholar citers of OASIS arXiv:2411.11581, title filter, top 25", date: 2026-10-03, results: 22, new: 16}
  - {where: citations-forward, query: "Semantic Scholar citers of Concordia arXiv:2312.03664, title filter, top 25", date: 2026-10-03, results: 20, new: 19}
  - {where: citations-forward, query: "Semantic Scholar citers of Generative Agents arXiv:2304.03442 (first 3000), title filter, top 25", date: 2026-10-03, results: 9, new: 5}
  - {where: citations-forward, query: "Semantic Scholar citers of ODD 2020 doi:10.18564/jasss.4259, LLM/generative/agentic filter", date: 2026-10-03, results: 7, new: 7}
  - {where: hn, query: "multi-agent simulation", date: 2026-10-03, results: 19, new: 17}
  - {where: hn, query: "agent based simulation LLM", date: 2026-10-03, results: 5, new: 4}
  - {where: web, query: "A survey of social network simulation in the LLM era 2026", date: 2026-10-03, results: 8, new: 7}
  - {where: web, query: "Moltbook dataset github agent social network posts data release", date: 2026-10-03, results: 5, new: 5}
  - {where: semantic-scholar, query: "multi-agent simulation platform large language model agents", date: 2026-10-03, results: 16, new: 13}
  - {where: arxiv, query: "abs:artificial society AND abs:language model", date: 2026-10-03, results: 6, new: 3}
  - {where: arxiv, query: "abs:agent-based AND abs:social simulation AND abs:open-source AND abs:LLM", date: 2026-10-03, results: 0, new: 0}
  - {where: github, query: "multi-agent simulation (sort stars, top 30)", date: 2026-10-03, results: 25, new: 19}
  - {where: github, query: "agent-based modeling (sort stars, top 30)", date: 2026-10-03, results: 16, new: 11}
  - {where: github, query: "llm social simulation / agent society simulation / agent-based simulation framework / generative agents, >=100 stars", date: 2026-10-03, results: 12, new: 7}
  - {where: github, query: "multi-agent environment benchmark / multi-agent reinforcement learning environment, >=100 stars", date: 2026-10-03, results: 13, new: 9}
  - {where: github, query: "agent simulation, >=500 stars", date: 2026-10-03, results: 20, new: 6}
  - {where: github, query: "multi-agent environment / multi-agent reinforcement learning / multi-agent simulator / world simulator agents, >=500 stars", date: 2026-10-03, results: 33, new: 10}
  - {where: github, query: "agent-based model / agent-based / swarm simulation / social simulation / multi-robot simulation / llm agents simulation, >=500 stars", date: 2026-10-03, results: 19, new: 0}
  - {where: github, query: "simulation environment agents, >=1000 stars", date: 2026-10-03, results: 2, new: 0}
---

## Scope

In scope: software in which many agents act in a shared world and the world's state is the object of study.
Five families, because the lab's questions cut across all of them:

1. LLM-agent societies, arenas and multi-agent LLM benchmarks (shared feeds, game masters, text games, graph
   message passing).
2. Multi-agent RL environment suites and GPU-vectorised engines.
3. General agent-based modelling (ABM) frameworks and swarm-robotics or drone simulators.
4. Network, protocol and market simulators that supply the substrate for Sybil, partition and Byzantine
   experiments.
5. Evaluation harnesses that are not simulators but are what an LLM sim gets run inside.

Out of scope: single-agent environments (Craftax, Kinetix, XLand-MiniGrid, Brax), orchestration frameworks
used only to get a task done (covered by the `llm-agent-swarms` survey and the `scan-code-agent-orchestration` task),
and closed platforms with no code (Antithesis, Simile). In-the-wild corpora (AI Village, Moltbook, the wiki
swarm) are mentioned where they change what a simulator is for, but are surveyed in `surveys/llm-agent-swarms.md`.

The motivating decision: dmarz was about to build a multi-agent simulation environment from scratch. This
survey asks what that build can reuse, and which of its problems have already been written up.

## Search log

Seeds were the ~90 simulator and framework repos already in `library/code/` from the
`scan-code-collective-sims`, `scan-code-agent-orchestration` and MARL scans. The scan then ran as four
parallel lanes on 2026-10-03 (LLM societies, MARL and GPU engines, ABM and robotics, network/market/
adversarial), each doing direct GitHub API lookups of named candidates, `gh search repos` keyword rounds,
arXiv title and abstract queries, web searches, and backward citation trails through the related-work
sections and tables of the environment papers (notably Table 6 of [[hu-2025-toward]], which lists about 45
MARL environments, and the `awesome-llm-social-simulation` list). A fifth pass followed forward citations of
the seminal works through Semantic Scholar and ran fresh-vocabulary rounds to test saturation.

Dead ends: OpenAlex's daily budget was exhausted and Semantic Scholar rate-limited for most of the day, so
the scholarly-index rounds are thinner than the arXiv and GitHub rounds. Several candidates were checked and
deliberately not catalogued: archived or superseded repos (Nocturne, the original Neural MMO, repast.hpc),
single-agent suites, a Swarm-SLAM system that is not a simulator, and student flocking repos with no licence.
PufferLib was catalogued but failed to build on macOS.

Twelve environments were installed and run on an M1 Max CPU during the scan (radCAD, Inspect, MMASim and ABIDES among them, plus the eight LLM and RL engines in the throughput table below); their commands and outputs are
in each entry's Run notes and the scripts are in `src/sim-envs/`.

## Landscape

**LLM-agent societies.** The line starts with the 25-agent Smallville of [[park-2023-generative]]
([[gh-joonspk-research-generative-agents]]) and splits three ways. Social-feed simulators put agents on a
synthetic Twitter or Reddit with a recommender: [[gh-camel-ai-oasis]] ([[yang-2024-oasis]], up to one million
agents), [[gh-ysocialtwin-ysocial]] ([[rossetti-2024-y]]), [[gh-tsinghua-fib-lab-agentsociety]]
([[piao-2025-agentsociety]]) and the bot-injection sandbox [[gh-qqqqqqby-botsim]] ([[qiao-2025-botsim]]).
Game-master simulators keep the world in an LLM narrator: [[gh-google-deepmind-concordia]] and, in game form,
[[gh-google-werewolf-arena]], [[gh-goodstartlabs-ai-diplomacy]] and [[gh-mukobi-welfare-diplomacy]]
([[mukobi-2023-welfare]]). Arenas and benchmarks fix the rules in code and plug LLMs into seats:
[[gh-textarena-textarena]] ([[guertler-2025-textarena]]), [[gh-sotopia-lab-sotopia]] ([[zhou-2023-sotopia]]),
[[gh-giorgiopiatti-govsim]] ([[piatti-2024-cooperate]]), [[gh-ulab-uiuc-marble]] ([[zhu-2025-multiagentbench]]),
[[gh-ruc-gsai-yulan-swarmintell]] ([[ruan-2025-benchmarking]]), [[gh-floriangroetschla-agentsnet]]
([[grotschla-2025-agentsnet]]), [[zhang-2026-silo]] and the market environments
[[gh-microsoft-multi-agent-marketplace]] ([[bansal-2025-magentic]]) and [[gh-freedomintelligence-twinmarket]].
At the population end, [[gh-agenttorch-agenttorch]] ([[chopra-2024-limits]]) trades per-agent LLM calls for
archetypes broadcast over tensors, and [[gh-stanfordhci-genagents]] ([[park-2024-llm]]) supplies 1,000+
interview-grounded personas without a world.

**MARL suites and GPU engines.** Particle worlds ([[lowe-2017-multi]], [[gh-openai-multiagent-particle-envs]],
now in [[gh-farama-foundation-pettingzoo]] and vectorised in [[gh-proroklab-vectorizedmultiagentsimulator]]),
social-dilemma substrates ([[leibo-2021-scalable]], [[gh-google-deepmind-meltingpot]]), open worlds
([[gh-neuralmmo-environment]], [[suarez-2023-neural]]; [[gh-baselomari-ma-craftax]]; [[gh-metta-ai-mettagrid]]),
grids at scale ([[gh-cognitive-ai-systems-pogema]], [[skrynnik-2024-pogema]];
[[gh-farama-foundation-magent2]]), the emergent-tool-use hide-and-seek world ([[baker-2020-emergent]]), and
the SMAC line ([[gh-oxwhirl-smac]], [[gh-oxwhirl-smacv2]], [[ellis-2022-smacv2]]). Throughput engines
([[gh-shacklettbp-madrona]] / [[shacklett-2023-extensible]], [[gh-salesforce-warp-drive]] /
[[lan-2021-warpdrive]], [[gh-emerge-lab-gpudrive]] / [[kazemkhani-2024-gpudrive]], [[gh-mlech26l-gigastep]] /
[[lechner-2023-gigastep]], [[gh-bold-lab-ai-jaxmarl]], [[gh-pufferai-pufferlib]]) keep all worlds on one
device. [[hu-2025-toward]] and [[gorsane-2022-towards]] are the reviews.

**ABM frameworks and swarm robotics.** General ABM: [[gh-mesa-mesa]] with [[gh-mesa-mesa-llm]] and
[[gh-mesa-mesa-frames]], [[gh-netlogo-netlogo]], [[gh-juliadynamics-agents-jl]] ([[datseris-2022-agents]]),
[[gh-eclab-mason]], [[gh-krabmaga-krabmaga]], [[gh-flamegpu-flamegpu2]] ([[richmond-2023-flame]]),
[[gh-repast-repast4py]], [[gh-i-m-iron-man-abmax]] ([[chaturvedi-2025-abmax]]), [[gh-jofmi-agentpy]],
[[gh-abm4all-melodie]], [[gh-gama-platform-gama]]. Robotics and drones: [[gh-ilpincy-argos3]],
[[gh-jic-csb-kilombo]], [[gh-learnsyslab-gym-pybullet-drones]] ([[panerati-2021-learning]]),
[[gh-learnsyslab-crazyflow]], [[gh-lis-epfl-swarmlab]], [[gh-nekonaute-roborobo4]], and
[[gh-chroma-citi-dancers]], which co-simulates robots with ns-3 radio links. Model description standard:
[[grimm-2020-odd]].

**Network, protocol and market substrates.** Deterministic simulation of real binaries:
[[gh-shadow-shadow]] ([[jansen-2022-co-opting]]), [[gh-ethereum-ethshadow]], [[gh-shadow-tornettools]]
([[jansen-2021-once]]). Packet-level models: [[gh-nsnam-ns-3-dev-git]]. Container emulation with attacker
roles: [[gh-testground-testground]], [[gh-libp2p-gossipsub-hardening]], [[gh-crytic-attacknet]],
[[gh-ethpandaops-ethereum-package]]. Cheap DHT and chain models: [[gh-datahop-kademlia-simulator]],
[[gh-dsg-titech-simblock]] ([[aoki-2019-simblock]]), [[gh-maher243-blocksim]] ([[alharby-2020-blocksim]]).
Token and market models: [[gh-cadcad-org-cadcad]], [[gh-cadlabs-radcad]], [[gh-tokenspice-tokenspice]],
[[gh-jpmorganchase-abides-jpmc-public]] ([[byrd-2019-abides]], [[amrouni-2021-abides]]),
[[gh-m1kuw1ll-mmasim]] ([[wu-2023-strategic]]). Consistency oracles: [[gh-jepsen-io-maelstrom]].

**Harnesses.** [[gh-ukgovernmentbeis-inspect-ai]] and [[gh-meridianlabs-ai-inspect-petri]] (auditor, target
and judge roles with fabricated tool results), plus the security sandboxes already catalogued for
fork-merge ([[gh-ukgovernmentbeis-control-arena]], [[debenedetti-2024-agentdojo]]). The live canary
[[gh-palisaderesearch-llm-honeypot]] ([[reworr-2024-llm]]) is the in-the-wild counterpart.

## What is known

Measured on our machine (M1 Max CPU, 2026-10-03, single process unless noted; Run notes in each entry):

| environment | workload | throughput |
|---|---|---|
| [[gh-krabmaga-krabmaga]] | boids, 200 to 10k agents | 3.45M to 3.68M agent-steps/s (1.69M at 100k) |
| [[gh-cognitive-ai-systems-pogema]] | pathfinding grid, 64 to 1,024 agents | 168k to 196k agent-steps/s |
| [[gh-jpmorganchase-abides-jpmc-public]] | RMSC04 market, 1,117 agents | about 67.5k messages/s |
| [[gh-semitable-lb-foraging]] | 2-agent foraging | 29.2k agent-steps/s |
| [[gh-jofmi-agentpy]] | boids | 14.6k to 19.6k agent-steps/s |
| [[gh-mesa-mesa]] | boids | 10.8k agent-steps/s |
| [[gh-neuralmmo-environment]] | 128 to 512 agents, random actions | 6.1k to 6.4k agent-steps/s |
| [[gh-learnsyslab-gym-pybullet-drones]] | Crazyflie physics | about 4.9k drone-steps/s (50 drones at 2x real time) |
| [[gh-proroklab-vectorizedmultiagentsimulator]] | flocking, 64 envs x 8 agents | 1,615 agent-steps/s |
| [[gh-textarena-textarena]] | 4-player public goods, local llama3.1 8B | 48 turns in 274 s |
| [[gh-floriangroetschla-agentsnet]] | 4-node colouring, 4 rounds, local 8B | 8.5 min, score 0.833 |

The spread between rule-based engines is about 340x (krABMaga vs Mesa), consistent with the framework
comparison in [[datseris-2022-agents]] (Mesa 25 to 126x slower than Agents.jl) and its CI successor
[[gh-juliadynamics-abmframeworkscomparison]] (Mesa 59.5x on large flocking). Any LLM-in-the-loop sim is
three to six orders of magnitude slower than any of them, so the engine is never the bottleneck once an LLM
acts every step. The TextArena run is one seed with one model: a scripted free-rider that promised to
contribute and gave nothing won 116.2 to about 66, and the llama agents never called it out. That is a smoke
test, not a finding.

Established in the literature about building these environments:

- **Validity of LLM societies is mostly unvalidated.** Of 35 generative-ABM papers, 15 validate only
  subjectively, most use one run, and none does sensitivity analysis [[larooij-2025-do]]. Small changes to
  persona format or instructions move cooperation by up to 76 points (abstract only) [[ye-2026-stop]].
  [[zhou-2025-pimmur]] proposes validity principles for LLM societies.
- **An omniscient orchestrator leaks private state.** When one LLM plays all sides, bargaining reaches a deal
  94% of the time against 30% with separate agents [[zhou-2024-is]]. Any game-master design
  ([[gh-google-deepmind-concordia]]) has to keep agent contexts separate.
- **LLM agents are homogeneous.** They drift to the accurate consensus unless biased by prompt
  [[chuang-2023-simulating]]; demographic personas reach 74% normalised accuracy against 86% for
  interview-grounded ones [[park-2024-llm]]. Archetype broadcasting reaches 8.4M agents by giving up
  per-agent variation [[chopra-2024-limits]].
- **The simulated population can manufacture the signal.** In BotSim, replayed humans never reply to bots,
  and a graph detector reaches 89.9% by exploiting the missing edges while text detectors sit near chance
  [[qiao-2025-botsim]]. This is the main hazard for using a simulator to train swarm detectors.
- **Update order changes outcomes.** Synchronous vs asynchronous updating flips the spatial Prisoner's Dilemma
  from persistent cooperation to all-defect [[huberman-1993-evolutionary]]; activation regime reverses results
  in Epstein's and Axtell's models [[radax-2010-timing]]. Vectorised engines are synchronous by construction,
  so the same model can disagree across frameworks for this reason alone (inferred, noted in
  [[gh-mesa-mesa-frames]]).
- **One sampled network is a sample of one.** Differences between independently sampled Tor networks
  exceeded seed-to-seed variation; at 1% scale the point estimate pointed the wrong way [[jansen-2021-once]].
- **Benchmarks can be solved without looking.** On several SMAC maps a timestep-only policy matches an
  observing one; the fix was per-episode randomisation of teams and starts [[ellis-2022-smacv2]]. MARL papers
  mostly evaluate on one environment with few seeds [[gorsane-2022-towards]].
- **Broad objectives produce dominant strategies.** Neural MMO's survival objective collapsed specialisation
  [[suarez-2023-neural]].
- **Throughput comes from keeping state on one device and batching worlds** ([[lan-2021-warpdrive]],
  [[shacklett-2023-extensible]]), headline numbers need checking (Gigastep's "1B steps/s" against about 1M in
  its own figure, [[lechner-2023-gigastep]]), and per-agent throughput, not per-env, is the comparable unit
  [[kazemkhani-2024-gpudrive]].
- **The protocol is a treatment.** Changing only the market rules moved efficiency between 56% and 89% with
  the same LLM traders [[chupilkin-2026-artificial]]; changing only the backbone model flipped a persistent
  10-agent world from stable governance to collapse, one run per condition [[akkil-2026-emergence-platform]].
- **Generated simulator code runs but does not reproduce.** Of 17 LLMs turning an ODD description into code,
  only one produced statistically valid code in 6 of 6 trials (skim) [[fachada-2026-can]].
- **Lockstep ticks waste LLM throughput.** Scheduling by real dependencies gave 1.3 to 4.15x over lockstep
  (abstract) [[xie-2024-ai]].
- **Survivorship and attribution need designing in.** Snapshot every agent, dead ones included
  [[ng-2026-microverse]]; measure one agent's effect by swapping it for a reference policy under the same
  seed [[yan-2026-ceo]].
- **Real-platform data has holes that look like findings.** In the Moltbook scrape an empty comment list does
  not mean no replies for about a third of posts [[data-moltbook-dataset-2026]].
- **ODD has no slot for LLM agents.** Prompt, model id, decoding settings and seed need adding to any model
  description [[grimm-2020-odd]].
- **Population scale hurts coordination.** Success falls from 61% at N=2 to 18% at N=100 even when the
  information has been delivered [[zhang-2026-silo]]; LLM market agents show a first-proposal bias worth
  10 to 30x quality [[bansal-2025-magentic]].

## Open problems and disagreements

- Whether LLM societies are models of anything. [[larooij-2025-do]] says validation is absent; the platform
  papers ([[yang-2024-oasis]], [[piao-2025-agentsociety]]) report replication of known social effects. No
  platform reports a sensitivity analysis over prompts and models.
- Scale claims are unverified. YuLan-OneSim's 100k, AgentTorch's millions and OASIS's million agents were not
  reproduced here; AgentTorch reaches its count by sharing one LLM decision per archetype, which is a
  different object from a million independent agents.
- Determinism with LLMs in the loop. Shadow-style deterministic simulation and LLM API calls do not mix:
  network calls break simulated time (inferred in [[gh-shadow-shadow]]). Local models with fixed seeds are
  the only reproducible option, and even those are not bit-stable across hardware (not checked here).
- Maintenance. A large share of the field is archived or rotting: Hanabi, Google Research Football,
  WarpDrive, AI Economist, ChatArena, Werewolf Arena, MineLand, Nocturne are archived or deprecated; ABIDES
  needed a dependency shim; EconAgent's model is retired; AgentsNet breaks on current langchain.

## Code, data and tools

What to start from, by research line. "Bootstrap" means fork it and add to it; it already runs.

| if the question is about | start from | why | missing piece you add |
|---|---|---|---|
| LLM agents in a shared feed, herding, bot detection | [[gh-camel-ai-oasis]] or [[gh-ysocialtwin-ysocial]] | recommender + feed + scale; Y Social lets humans join | a Sybil/operator layer; ground-truth labels |
| small-N LLM games with deception, free-riding, commons | [[gh-textarena-textarena]], [[gh-giorgiopiatti-govsim]] | ran here on a local model; any seat is a callable; GovSim has greedy-newcomer injection | identity layer, many seeds |
| distributed coordination on graphs (consensus, colouring) | [[gh-floriangroetschla-agentsnet]], [[zhang-2026-silo]] | ran here; per-node coroutine is a ready Byzantine slot | Byzantine and Sybil nodes |
| swarm dynamics with LLM agents in space | [[gh-mesa-mesa-llm]] on [[gh-mesa-mesa]], [[gh-ruc-gsai-yulan-swarmintell]] | LLM agents with vision radius and tools; SwarmBench has flocking, sync, foraging tasks | a classical baseline run side by side |
| rule-based null models at scale | [[gh-krabmaga-krabmaga]], [[gh-pmocz-activematter-python]], [[gh-mesa-mesa-frames]] | 3.5M agent-steps/s on CPU; Vicsek transition reproduced | nothing |
| RL populations, open worlds, trade | [[gh-neuralmmo-environment]], [[gh-cognitive-ai-systems-pogema]], [[gh-google-deepmind-meltingpot]] | ran here; PLAYER_N knob; Melting Pot's held-out focal/background split | join/leave mid-episode |
| Sybil attacks on P2P overlays | [[gh-libp2p-gossipsub-hardening]], [[gh-datahop-kademlia-simulator]] | ship Sybil and eclipse attackers and peer scoring | LLM-driven attackers |
| Sybil economics, mechanism parameters | [[gh-cadlabs-radcad]] | ran here with a Sybil policy (`src/sim-envs/radcad_sybil.py`) | nothing for analytic sweeps |
| MEV, builder auctions | [[gh-m1kuw1ll-mmasim]], [[gh-ethpandaops-ethereum-package]] | ran here; real PBS stack in Docker | identity and collusion among builders |
| fork-and-merge of LLM sub-agents | [[gh-ukgovernmentbeis-inspect-ai]] + [[gh-meridianlabs-ai-inspect-petri]] | ran a canary task with a mock model (`src/sim-envs/forkmerge_task.py`); Petri fabricates tool results | the merge step itself and a real model |
| LLM society with agents joining and leaving | [[gh-zju-llms-agent-kernel]] | runtime add/remove of LLM agents; 10k-agent demo (claimed) | adversaries, labels |
| auditable, replayable LLM economy runs | [[gh-apromisedland-trustworthy-agent-simulation]] | seeded batches, resume, replay without model calls, Mesa underneath | scale beyond tens |
| cross-owner agents and identity/consent attacks | [[gh-kingofspace0wzz-weclawarena]] | 620 task variants with built-in attack conditions | scale |
| real agent-society data to calibrate against | [[gh-kelkalot-moltbook-observatory]], [[data-moltbook-dataset-2026]] | 2.6M posts from 176k agents; 421k posts and 3.7M comments | a sim to compare with |
| market microstructure | [[gh-jpmorganchase-abides-jpmc-public]] | ran here at 1,117 agents | dependency pins |
| real binaries on a simulated network | [[gh-shadow-shadow]], [[gh-ethereum-ethshadow]] | deterministic, used at full Tor scale | Linux host |

Not worth starting from: [[gh-farama-foundation-chatarena]] (deprecated), [[gh-openbmb-agentverse]] (stale),
[[gh-jofmi-agentpy]] (unmaintained per README), [[gh-salesforce-warp-drive]] and [[gh-salesforce-ai-economist]]
(archived), [[gh-testground-testground]] (unmaintained since 2023, though its attacker-group pattern is worth
copying).

Data that changes what a simulator is for: the hackathon offers AI Village transcripts (170k+ messages, 2M+
computer-use turns) as the testbed [[x-aidigest-2100638869603713244]], and Moltbook has been studied as a live
agent society [[de-marzo-2026-collective]], with a temporal graph dataset for coordinated-agent detection
announced in [[x-kunmukh-2054965024863461739]]. A simulator's best use at this event is as a ground-truth
generator next to those corpora: we know which agents are one operator, which messages were injected and
which sub-agent was compromised, which the real transcripts cannot tell us.

## Gaps

- **Open populations exist, but without adversaries.** [[hu-2025-toward]]'s table gives every MARL benchmark a
  fixed or ranged population, and MetaDrive's respawn ([[gh-metadriverse-metadrive]]) is RL-only. On the LLM
  side, [[gh-zju-llms-agent-kernel]] ([[mao-2025-agent-kernel]]) adds and removes LLM agents at runtime and
  reports a 10,000-agent campus run (not reproduced here). It has no adversarial hooks.
- **Identity attacks exist only at small N, and operator ownership exists nowhere.**
  [[gh-kingofspace0wzz-weclawarena]] ([[wang-2026-weclawarena]]) models agents with different human owners
  and ships invalid-identity, consent and mandate attack variants, at a handful of owners per task. Emergence
  World injected prompt injection, misinformation and memory leaks into running 10-agent worlds
  ([[akkil-2026-emergence]]), but its engine is not released ([[gh-emergenceai-emergence-world]]). Sybils
  at scale exist only in the P2P testbeds ([[gh-libp2p-gossipsub-hardening]],
  [[gh-datahop-kademlia-simulator]]) as scripted Go or Java nodes. No catalogued environment provides
  operator-controlled clusters of LLM agents with ground-truth operator labels. The closest template for
  "inject labelled adversarial typologies, emit a labelled log" is from finance: [[gh-ibm-amlsim]].
- **No fork-and-merge primitive.** No environment lets an agent spawn sub-agents that act independently and
  then merge state back, with the merge as the attack surface. Roborobo's robot-to-robot genome spread
  ([[gh-nekonaute-roborobo4]]) is the closest analogue and is evolutionary, not LLM.
- **No detector-validity controls.** Given [[qiao-2025-botsim]], a swarm-detection sim needs humans or
  background agents that do interact with the injected agents; none of the bot sandboxes provide that.
- **No LLM extension of a model-description standard.** ODD ([[grimm-2020-odd]]) has no slot for prompts,
  models or decoding, and none of the platforms emits a run manifest that would let another team rerun it.

The practical reading: do not build a new world engine, a new feed simulator, a new game suite or a new
P2P testbed. Each exists and several ran here in under ten minutes. What does not exist is a thin layer
(identity and operator ownership, fork and merge, injected adversaries, ground-truth labels and a run
manifest) that could sit on top of one of them. That layer is the build.

## Saturation

Not reached for papers; arguably reached for maintained code.

- The final saturation pass added 86 entries (28 papers, 57 repos, 1 dataset), so the search was still
  productive late in the day. Forward-citation rounds on Melting Pot, OASIS, Concordia, Generative Agents and
  ODD ran 0.55 to 1.0 new per relevant hit; the Semantic Scholar keyword round ran 0.8. LLM-society papers in
  2026 are appearing faster than one day of search can close.
- The last two logged rounds show 0 new of 19 and 0 new of 2, which passes the mechanical gate. Those rounds
  were GitHub searches restricted to repos with at least 500 and 1,000 stars. They show that well-known,
  maintained environments are covered; they do not show saturation of small repos or papers.
- OpenAlex (daily budget exhausted) and Semantic Scholar keyword search (rate-limited) were mostly
  unavailable, so scholarly-index coverage leans on arXiv and forward citations.

The survey is therefore left at `status: in-progress` even though the gate's floors are met. What it would
take to close: a Semantic Scholar keyword sweep with an API key over "LLM social simulation", "generative
agent-based model" and "multi-agent environment" for 2025 to 2026, plus forward citations of
[[yang-2024-oasis]] and [[piao-2025-agentsociety]] beyond the top 25. The conclusion in Gaps is the part most
exposed to a missed source: a 2026 paper with operator-labelled LLM Sybil clusters would change it.
