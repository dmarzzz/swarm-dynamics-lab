---
id: zhou-2024-is
type: paper
title: "Is this the real life? Is this just fantasy? The Misleading Success of Simulating Social Interactions With LLMs"
authors: ["Xuhui Zhou", "Zhe Su", "Tiwalayo Eisape", "Hyunwoo Kim", "Maarten Sap"]
year: 2024
venue: "arXiv (Semantic Scholar lists EMNLP 2024)"
url: https://arxiv.org/abs/2403.05020
doi: null
arxiv: "2403.05020"
cite: "Zhou, X., Su, Z., Eisape, T., Kim, H., & Sap, M. (2024). Is this the real life? Is this just fantasy? The Misleading Success of Simulating Social Interactions With LLMs. arXiv preprint arXiv:2403.05020."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "78 (Semantic Scholar, 2026-10-03)"
code: [gh-sotopia-lab-sotopia]
---

## Summary

Using Sotopia scenarios, the authors compare Script mode (one omniscient LLM writes the whole dialogue), Agents mode (one LLM per character with private goals) and Mindreaders mode (agents see each other's goals). Omniscient simulations reach goals far more often and read as more natural; for example Script-mode bargaining ends in a deal 94% of the time versus 30% in Agents mode. Fine-tuning on Script data transfers its agreeable, leak-exploiting style rather than real social skill. I read the main text, not the appendices.

## Contribution

Shows that information asymmetry, not dialogue fluency, is what LLM social simulations get wrong, and that the common single-LLM 'omniscient' setup silently leaks private state, inflating apparent social competence. Proposes a 'simulation card' to report the mode.

## Key results

- 450 simulations per model per mode (GPT-3.5, Mixtral-8x7B), 90 scenarios, 5 character pairs each.
- Script and Mindreaders modes score significantly higher goal completion than Agents mode.
- Craigslist bargaining: deal reached in 94% (Script), 30% (Agents), 93% after fine-tuning on Script data.
- MutualFriends: mean first-mention position of the shared friend 0.13 in Script vs. 0.39 in Agents, i.e. the omniscient writer 'guesses' immediately.
- Human raters judge Script dialogues more natural; Agents dialogues are more verbose, and prompting for brevity did not fix it.
- The original Generative Agents codebase used Script mode for conversations, which the paper had not reported.

## Methods and models

Built on the Sotopia library: 40 characters with public and secret attributes, scenario context shared, social goals private. GPT-4 judges goal completion (0 to 10). GPT-3.5 fine-tuned on 1,252 Script episodes from 269 new scenarios, evaluated back in Agents mode. Human naturalness preference with 30 annotations per comparison.

## Limitations and open questions

Dyadic only; goal completion is LLM-judged; 2023-era models. Does not test whether stronger models close the gap. Turn-taking, multi-party and asynchronous settings are left out.

## Relevance to us

Directly applies to our sim design: a game master or single orchestrator LLM that sees every agent's private state will leak it into outcomes, so any experiment on deception, sybil coordination or swarm detection must run one model context per agent with enforced information boundaries, and must report this. Relevant to [[gh-google-deepmind-concordia]] (GM sees everything), [[gh-joonspk-research-generative-agents]], and to fork-and-merge experiments where merged contexts are by construction omniscient.
