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
- fork-merge-security
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

## Notes from dmarz/fm-memory-injection

Read in full (arXiv HTML v2) on 2026-10-03 for the fork-merge lane. In each round, agents are paired at random. The questioner retrieves an image from its FIFO image album with CLIP and sends it to the answerer, and the answerer stores it. One adversarial image placed in one agent's album both triggers harmful output and makes itself the image retrieved, so it copies itself into the albums of new agents. The paper models this as an SIR-style recurrence. The number of rounds to reach a target infected fraction grows with log N, and a defence provably stops spread only if it drives the effective transmission below the recovery rate (Remark II). Recovery comes from album eviction, so smaller albums slow spread. Measured: exponential infection up to one million LLaVA-1.5 agents, including a heterogeneous LLaVA and InstructBLIP population and harmful function-call JSON. Plain visual and textual prompt-injection baselines failed to infect even one agent.

How it bears on fork-merge (Q3, Q2): the attack never asks agents to "become" the attacker. It only needs the payload to be both harmful and preferentially retrieved, so that it propagates through ordinary memory exchange. A merge is one such exchange with a high-centrality node, the parent. The recovery condition in Remark II is the population-level analogue of a merge threshold. If merges, together with eviction or rollback, remove contamination faster than returning sub-agents reintroduce it, the infection dies out (inference from the paper's model, not tested for fork-merge). Related lane entries: [[dong-2025-memory]], [[xiong-2026-maple]], [[cohen-2024-here]].

## Notes from dmarz/fm-code-bench

Code catalogued as [[gh-sail-sg-agent-smith]] (MIT, 130 stars, last commit 2024-03-26; needs A100-class GPUs). The epidemic framing (one infected memory item, spread through pairwise exchange) maps onto a parent that merges children's memories as a hub; the paper's containment condition is the epidemic analogue of a Byzantine threshold (Q2).


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2402.08567 . Read depth in this session: abstract.

Seed title, eight authors and 2024 date match the opened arXiv record. The million-agent result concerns simulated multimodal agents and retrieval-mediated image exchange, not one million independent production deployments. Forward chasing through Semantic Scholar identifies Cowpox and the newer reliability-contagion work; the former was read in full here. Do not treat a population transmission threshold as a Byzantine k-of-n merge theorem. See [[wu-2025-cowpox]] and [[niu-2026-reliability-contagion]].
