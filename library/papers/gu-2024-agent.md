---
id: gu-2024-agent
type: paper
title: 'Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast'
authors:
- Xiangming Gu
- Xiaosen Zheng
- Tianyu Pang
- Chao Du
- Qian Liu
- Ye Wang
- Jing Jiang
- Min Lin
year: 2024
venue: Proceedings of the 41st International Conference on Machine Learning (ICML 2024)
url: https://arxiv.org/abs/2402.08567
doi: null
arxiv: '2402.08567'
cite: 'Gu, X., Zheng, X., Pang, T., Du, C., Liu, Q., Wang, Y., Jiang, J., & Lin, M. (2024). Agent Smith: A single image can jailbreak one million multimodal LLM agents exponentially fast. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). arXiv:2402.08567.'
topics:
- llm-agent-swarms
- sybil-resistance
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "4 (OpenAlex W4391871694, arXiv record, 2026-10-03); Semantic Scholar 178 same day"
code: []
---

## Summary

Introduces "infectious jailbreak": the adversary jailbreaks a single multimodal agent by placing an adversarial image in its memory, and through randomised pairwise chats the jailbreak spreads to almost all agents exponentially fast without further intervention. Simulations use up to one million LLaVA-1.5 agents. The authors derive a simple principle for when a defence provably restrains spread, but no practical defence meeting it is given.

## Contribution

Shows that epidemic (SI-type) spreading dynamics apply literally to LLM agent populations, with a contagion threshold criterion for defences.

## Key results

- Up to 10^6 agents; near-total infection exponentially fast via pairwise chat (abstract).
- Defence principle: containment requires recovery to outpace infection (paraphrase of the abstract's "simple principle"; exact form not read).

## Methods and models

Randomised pairwise chat among multimodal agents with memory banks storing images; adversarial image optimised to be retrieved and re-shared. Project page: https://sail-sg.github.io/Agent-Smith/ (code linked there, not opened).

## Limitations and open questions

Simulation with one model type; idealised random mixing; practical defences open.

## Relevance to us

A clean example of contagion dynamics (topic link to epidemic and cascade models) in an LLM swarm; pairs with tipping-point results in [[ashery-2024-emergent]] and risk framing in [[hammond-2025-multi]] and [[schroeder-2025-how]].

## Notes from dmarz/sybil-llm-agents

Reread the abstract 2026-10-03 for the Sybil-resistance lane. Infectious jailbreak needs only one compromised agent (one adversarial image in one agent's memory) to reach almost all of up to one million LLaVA-1.5 agents under random pairwise chat. For Sybil analysis this sets the lower bound: an adversary does not need many identities when contagion through shared memory does the multiplying, so identity-count defences ([[jo-2025-byzantine]], [[chen-2024-blockagents]]) must be paired with containment of what agents store and relay.
