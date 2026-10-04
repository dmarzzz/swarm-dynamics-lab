---
id: han-2024-static
type: paper
title: "Static network structure cannot stabilize cooperation among large language model agents"
authors:
- "Jin Han"
- "Balaraju Battu"
- "Ivan Romić"
- "Talal Rahwan"
- "Petter Holme"
year: 2024
venue: "PLOS ONE"
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0320094
doi: 10.1371/journal.pone.0320094
arxiv: "2411.10294"
cite: "Han, J., Battu, B., Romić, I., Rahwan, T., & Holme, P. (2025). Static network structure cannot stabilize cooperation among large language model agents. PLOS ONE, 20(5), e0320094. https://doi.org/10.1371/journal.pone.0320094"
topics:
- llm-agent-swarms
- marl-emergence
- collective-decision
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: "2 (OpenAlex W4410616606, published version, 2026-10-03); 0 (OpenAlex W4404569754, arXiv record)"
code: []
---

## Summary

Repeats the classic network-reciprocity experiment (Nowak's rule that cooperation is stabilised on a graph when b/c > k) with LLM agents instead of humans. Agents play an iterated Prisoner's Dilemma either in well-mixed populations or on fixed ring lattices of degree k = 2, 4, 6 with benefit-to-cost ratios b/c = 2, 4, 6, 8. Humans in the matching experiments (Rand et al. 2014) cooperate more on fixed networks when b/c > k; LLMs show the opposite: GPT-4 cooperates most in well-mixed populations and loses cooperation as networks get denser, and GPT-3.5 sits near 50% regardless of parameters.

## Contribution

A direct test of whether a canonical result of evolutionary game theory on networks transfers to LLM populations, and a negative one: network structure does not stabilise LLM cooperation the way theory and human data predict. It complements [[piatti-2024-cooperate]] and [[vallinder-2024-cultural]] with a population-structure manipulation.

## Key results

- GPT-3.5: about 50% cooperation across all b/c and k, insensitive to parameters, with period-two oscillations on structured networks. Measured.
- GPT-4: about 80-90% cooperation in well-mixed populations, sharp decline as network degree rises; some sensitivity to sparse networks (k = 2) with b/c > k. Measured.
- Controlled-neighbourhood test: with 4 cooperating neighbours Claude and GPT-4 cooperate about 80-90%; with 3 defectors and 1 cooperator, about 10-20%. GPT-3.5 and Mixtral stay near 50%. Measured.
- Model identity matters more than network structure. Measured.

## Methods and models

Iterated PD where cooperation costs c and gives b to each neighbour; populations of 8 players (more rounds) and 25 players (15 rounds); models GPT-3.5, GPT-4, Claude, Mixtral. Code and outputs: https://github.com/jin-awoo/Static-network-structure-cannot-stabilize-cooperation-among-Large-Language-Model-agents-llm-outputs . Read via the PLOS full text (results and methods skimmed).

## Limitations and open questions

Small populations, only ring lattices, few rounds; LLM behaviour depends on prompt framing of the game. It is unclear whether agents get enough history to condition on neighbours as humans do. Open: whether memory, reputation or dynamic rewiring (rather than static structure) restores network reciprocity.

## Relevance to us

A warning that textbook spatial-game results may not carry over to LLM collectives, and a ready protocol (b/c vs k sweep) to test on newer models. Pairs with [[papachristou-2025-network]] (network formation among LLMs) and [[ashery-2024-emergent]] (conventions in well-mixed populations).
