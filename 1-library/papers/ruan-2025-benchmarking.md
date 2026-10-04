---
id: ruan-2025-benchmarking
type: paper
title: Benchmarking LLMs' Swarm intelligence
authors:
- Kai Ruan
- Mowen Huang
- Ji-Rong Wen
- Hao Sun
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2505.04364
doi: null
arxiv: '2505.04364'
cite: Ruan, K., Huang, M., Wen, J.-R., & Sun, H. (2025). Benchmarking LLMs' swarm intelligence. arXiv preprint arXiv:2505.04364.
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-motion
- swarm-robotics
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "0 (OpenAlex W4416013219, arXiv record, 2026-10-03); Semantic Scholar 4 same day"
code: []
---

## Summary

SwarmBench tests whether LLMs can coordinate as a decentralised swarm under the constraints that define swarm intelligence: each agent is an independent LLM instance that sees only a k x k egocentric window (5 x 5 in the main runs), its own recent history (5 rounds), and short anonymous messages (120 characters) broadcast by agents within range. Five tasks on a 2D grid with a simple force/mass physics engine: Pursuit (corner a faster prey), Synchronization (all agents toggle a binary state in unison and then alternate), Foraging (find food, return to nest), Flocking (form a target shape, scored by a translation-invariant earth-mover-style assignment cost) and Transport (jointly push a heavy block out of an exit). Thirteen LLMs are evaluated zero-shot over 5 runs each. LLMs show rudimentary coordination, but performance is task- and model-specific, and long-range planning under local information is weak.

## Contribution

The first benchmark I found that imposes the classical swarm-intelligence constraints (local sensing, local anonymous messaging, no global view, no roles) on LLM agents and logs full trajectories for group-dynamics analysis. It bridges the swarm-robotics task vocabulary (pursuit, foraging, flocking, transport, synchronisation) with LLM evaluation, and it also releases the environment as a possible RL-with-verifiable-rewards setting.

## Key results

- Total scores (sum over five tasks, mean of 5 runs): gemini-2.0-flash 27.40, o4-mini 26.62, claude-3.7-sonnet 25.70, gpt-4.1 20.10, deepseek-v3 17.20, gpt-4o 11.80, o3-mini 11.10, qwq-32b 10.10, deepseek-r1 10.01, llama-3.1-70b 9.90, llama-4-scout below that. Measured.
- No model dominates: gemini-2.0-flash and o4-mini lead Pursuit (8.8 and 9.6) and Foraging; claude-3.7-sonnet leads Synchronization (12.6 +/- 9.6, very high variance). Flocking is the highest-scoring task overall. Transport is almost unsolved: only o4-mini (0.52) and deepseek-r1 (0.71) score above zero. Measured.
- Group-dynamics metrics of physical behaviour (behavioural variability, movement efficiency) correlate strongly with task success; the semantic content of messages correlates weakly. Agents' messages converge toward a simplified protocol, and for complex tasks this convergence correlates negatively with success. Measured (correlational).
- Action attribution (random forest on embeddings, permutation importance): received messages are more predictive of the next action than visual observation in several tasks, so communication has strong local influence but little global benefit. Measured.
- Named failure modes: movement bias, information silos, traffic jams (over-aggregation), "memory of a goldfish". Qualitative, with a quantitative link in the appendix.
- Perception range k = 3 -> 5 helps most tasks; k = 7 gives diminishing or negative returns (Transport). Group size: Transport improves from N = 8 to 16; Foraging degrades with N (congestion); Pursuit peaks at N = 12. Measured.
- Versus 15 rule-based baselines (20 repeats): heuristics match LLMs on decomposable Pursuit, LLMs win on Foraging and Synchronization. A centralised global-view commander variant offers little advantage for spatial micromanagement tasks like Pursuit. Measured.

## Methods and models

Discrete-time simultaneous updates; agents output an action (UP/DOWN/LEFT/RIGHT/STAY plus task actions such as SWITCH, PICKUP, DROP) and an optional message; force F = 2 per agent, agent mass 1, block mass grows as floor(sqrt(area)) so cooperative pushing is required. Temperature 1.0, top_p 1.0 in main runs (ablations in appendix). Fixed seed sets across models. Metrics defined in appendix F. Code: https://github.com/x66ccff/swarmbench

## Limitations and open questions

2D grid abstraction; zero-shot only; 5 runs per cell give large variance (Synchronization std comparable to the mean); short memory buffer may cause some failures; prompts not tuned per model. Swarm sizes are small (about 8-16 agents) compared with robot or animal swarms. Open: does fine-tuning (the RLVR route the authors propose) produce scalable local rules, and do the classical order parameters (polarisation, synchrony) show phase transitions as N or k vary.

## Relevance to us

The most directly usable testbed for a hackathon on LLM swarm dynamics: it already implements flocking, synchronisation and foraging with local constraints, so we can measure collective-motion order parameters (topic collective-motion), synchrony (sync-consensus) and information-theoretic emergence ([[riedl-2025-emergent]]) on LLM swarms. Complements the flocking-specific negative result of [[li-2024-challenges]], the consensus-protocol fix in [[li-2025-llm]], the conceptual critique of [[rahman-2025-llm-powered]] and the NetLogo approach of [[jimenez-romero-2025-multi-agent]].

## Notes from dmarz/llm-agent-swarms-recent

Independent full read including appendices A-L (v4, 15 Oct 2025). Extra numbers: Table S.1 totals gemini-2.0-flash 27.40, o4-mini 26.62, claude-3.7-sonnet 25.70 (Synchronization 12.60 +- 9.62), gpt-4.1 20.10, deepseek-v3 17.20 ... claude-3.5-haiku 7.20; only o4-mini and deepseek-r1 score on irregular Transport. Failure-mode metrics (L.5): action-direction Gini vs Pursuit score r = -0.668 (p < 0.001); connected components vs Synchronization r = -0.185 (n.s.); Boids-style separation force vs Foraging r = -0.309 (p = 0.012). Centralised global-view commander changes Flocking by only +5% (9.90 vs 9.40). Sensitivity (gemini-2.0-flash, N in {8,12,16}, k in {3,5,7}): Pursuit peaks at N = 12; Foraging degrades with N; k = 7 hurts Transport. Message-protocol convergence correlates with Flocking score (r = 0.38 homogeneity, 0.46 edit consistency). Agents see the last 5 rounds and messages of <= 120 characters from agents in view. Code: https://github.com/x66ccff/swarmbench . Related: [[jimenez-romero-2025-multi-agent]], [[rahman-2025-llm-powered]], [[li-2024-challenges]], [[zou-2026-waggle]].

## Notes from dmarz/llm-agent-swarms-audit

Audit 2026-10-03: checked the 4-author list, v4 date and the Table S.1 totals (27.40, 26.62, 25.70, ...), Transport scores 0.52 (o4-mini) and 0.71 (deepseek-r1), the 120-character message cap and the thirteen-model zero-shot protocol against the arXiv HTML. No errors. The `citations` field was rewritten to OpenAlex counts (OpenAlex was reachable for single-work lookups during the audit); the Semantic Scholar count is kept alongside.

## Notes from dmarz/sim-envs

Code catalogued as [[gh-ruc-gsai-yulan-swarmintell]] (repo RUC-GSAI/YuLan-SwarmIntell, MIT, 39 stars, last push 2025-05-21). Not run.
