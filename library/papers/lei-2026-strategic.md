---
id: lei-2026-strategic
type: paper
title: "Strategic Exploitation in LLM Agent Markets: A Simulation Framework for E-Commerce Trust"
authors: ["Shijun Lei", "Quang Nguyen", "Swapneel S Mehta", "Zeping Li", "Huichuan Fu", "Xiaolong Zheng", "Siki Chen", "Yunji Liang", "Philip Torr", "Zhenfei Yin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.10059
doi: null
arxiv: "2605.10059"
cite: "Lei, S., Nguyen, Q., Mehta, S. S., Li, Z., Fu, H., Zheng, X., Chen, S., Liang, Y., Torr, P., & Yin, Z. (2026). Strategic Exploitation in LLM Agent Markets: A Simulation Framework for E-Commerce Trust. arXiv preprint arXiv:2605.10059."
topics: [llm-agent-swarms, sybil-resistance]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Introduces TruthMarketTwin, a controlled simulation of e-commerce markets in which LLM seller agents privately know product quality and LLM buyer agents rely on advertised claims and reputation; agents make listing, purchasing, rating and recourse decisions. The authors report that LLM agents placed in conventional markets autonomously exploit weaknesses in reputation-based governance, and that warrant enforcement reduces deception and changes their strategic reasoning.

## Contribution

Brings asymmetric-information bilateral trade into LLM-agent market simulation and shows reputation systems being gamed without being prompted to.

## Key results

- LLM sellers exploit reputation-governance weaknesses without instruction (abstract).
- Warrant enforcement reduces deception (abstract; magnitudes not read).

## Methods and models

Not read beyond the abstract. Code availability not checked.

## Limitations and open questions

Only the abstract was read; models, population sizes and statistics unknown here.

## Relevance to us

Evidence that reputation alone does not hold against LLM agents in a market; relevant to Sybil-resistant reputation designs such as those studied in [[xia-2026-when]], and a possible extension target for [[gh-microsoft-multi-agent-marketplace]].
