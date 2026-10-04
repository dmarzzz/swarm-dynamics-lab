---
id: tessera-2026-benchmarking
type: paper
title: "Benchmarking Open-Ended Multi-Agent Coordination in Language Agents"
authors: ["Kale-ab Abebe Tessera", "Andras Szecsenyi", "Cameron Barker", "Alexander Rutherford", "Davide Paglieri", "Aidan Scannell", "Henry Gouk", "Elliot J. Crowley", "Tim Rocktäschel", "Amos Storkey"]
year: 2026
venue: "arXiv preprint (NeurIPS 2026 Evaluations and Datasets per repo)"
url: https://arxiv.org/abs/2606.08340
doi: null
arxiv: '2606.08340'
cite: "Tessera, K. A., Szecsenyi, A., Barker, C., Rutherford, A., Paglieri, D., Scannell, A., Gouk, H., Crowley, E. J., Rocktäschel, T., & Storkey, A. (2026). Benchmarking open-ended multi-agent coordination in language agents. arXiv:2606.08340."
topics: [llm-agent-swarms, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "2 (Semantic Scholar, 2026-10-03)"
code: [gh-alem-world-alem-env]
---

## Summary

Introduces alem, a pure-JAX benchmark built on Craftax-Coop that adds procedurally generated coordination tasks (synchronous actions, handovers, joint construction), soft role specialisation, a broadcast communication channel and three difficulty tiers inside a long-horizon survival world (episodes up to 10,000 steps). It exposes both an RL interface (symbolic observations) and a text interface, so the same world evaluates MARL agents and zero-shot LLM teams. Thirteen LLMs average only about 6% normalised return.

## Contribution

One environment that scores LLM teams and trained MARL teams on the same coordination tasks, separating base-task competence from coordination reward.

## Key results

- Zero-shot Gemini-3.1-Pro-High on the hardest coordination setting approaches MARL agents trained for one billion steps; GPT-5.4-High gets strong base reward but much lower coordination reward.
- Ablations: removing communication gives the largest coordination drop; scratchpad memory helps only for models that use it as a forward planner; reducing reasoning lowers both base and coordination scores.
- Heterogeneous teams score near the average of their homogeneous counterparts, neither collapsing to the weakest nor rising to the strongest member.
- 20 seeds per difficulty for open-weight models, 10 for closed models, rliable bootstrap CIs.

## Methods and models

Dec-POMDP on Craftax-Coop dynamics; LLM harness rebuilds a prompt each step (rules, last eight observation/action pairs, scratchpad up to a character cap, broadcast message); open models served by vLLM; MARL baselines (IPPO) trained end-to-end in JAX.

## Limitations and open questions

Fully cooperative teams of a few agents (1-8 in throughput tests), so no defection or adversaries. Text harness resets context each step by design, which removes context-management confounds but also removes long-context strategies.

## Relevance to us

Bootstrap candidate for a small-team coordination testbed where LLM and RL agents share one env; complements [[al-omari-2025-multi]] and [[gh-baselomari-ma-craftax]], which it extends. Lesson: mixing stronger models into a team does not lift it to the strongest member.
