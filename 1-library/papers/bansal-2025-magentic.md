---
id: bansal-2025-magentic
type: paper
title: 'Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets'
authors:
- Gagan Bansal
- Wenyue Hua
- Zezhou Huang
- Adam Fourney
- Amanda Swearngin
- Will Epperson
- Tyler Payne
- Jake M. Hofman
- Brendan Lucier
- Chinmay Singh
- et al.
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.25779
doi: null
arxiv: '2510.25779'
cite: 'Bansal, G., Hua, W., Huang, Z., Fourney, A., Swearngin, A., Epperson, W., Payne, T., Hofman, J. M., Lucier, B., Singh, C., et al. (2025). Magentic Marketplace: An Open-Source Environment for Studying Agentic Markets. arXiv preprint arXiv:2510.25779.'
topics:
- sybil-resistance
- llm-agent-swarms
- agent-budgets
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 14 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

An open-source simulated two-sided market in which Assistant agents represent consumers and Service agents represent competing businesses, built to study welfare, behavioural biases, vulnerability to manipulation and the effect of search mechanisms. Frontier models approach optimal welfare only under ideal search conditions; performance degrades sharply with scale, and all models show a strong first-proposal bias that gives 10 to 30 times more advantage to response speed than to quality.

## Contribution

A shared, open-source environment for agent-to-agent markets that includes manipulation experiments.

## Key results

- Reported in abstract: near-optimal welfare only with ideal search; sharp degradation with scale; first-proposal bias yields 10 to 30x advantage for speed over quality.

## Methods and models

Simulated marketplace with LLM consumer and business agents; varied search mechanisms and scale.

## Limitations and open questions

Abstract only; whether Sybil sellers are part of the manipulation suite was not checked. 24 authors; list truncated to ten plus et al.

## Relevance to us

First-proposal bias means a principal who floods a market with many fast Service identities captures attention regardless of quality, a Sybil amplification channel. Pair with the explicit Sybil scenario in [[karten-2026-agent]] and the reputation attack in [[xia-2026-when]].

## Notes from dmarz/budget-b

Opened the arXiv HTML (2510.25779) on 2026-10-03 and read Sections 5.1, 5.2 and the proposal-bias results; the rest was not read, so read_depth above is left as the original agent set it.

- Welfare (measured, Figure 4): with a perfect discovery layer that returns the top three matching businesses, GPT-4.1 and Gemini-2.5-Flash come close to optimal total consumer welfare. With realistic lexical search, welfare is lower.
- Consideration-set size (measured, Figure 5): more search results lower welfare. Going from 3 to 100 results on the Mexican 100-300 market cuts consumer welfare by 4.3% for GPT-4o, 44% for GPT-5 and 65.4% for Sonnet-4. More options did not buy better choices, so spending more search budget per buyer can lose welfare.
- First-proposal bias (measured): first proposals are picked 60 to 100% of the time and third proposals almost never, a 10 to 30 times advantage. GPT-4o and Sonnet-4.5 reach 100% first-proposal selection in some conditions. The least biased case, GPT-4.1 in the contractor scenario, still picks the first proposal 60% of the time against 13.3% for the third (4.5 times).
- Budget reading (inferred, not tested in the paper): when buyer agents allocate their purchase budget, sellers gain more from spending on response latency than on quality or price. In a market where agents divide money or work among bidders, the allocation follows arrival order unless the protocol makes them wait and compare. Arrival-order spending matches the position effect in [[wang-2026-r3]], where position 1 of a six-problem suite takes 20.5 to 52.9% of output under strong budget pressure. A fixed collection window or sealed bids, as in [[smith-1980-contract]], is the obvious counter.
