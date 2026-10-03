---
id: wu-2026-how
type: paper
title: How does Adversarial Influence Scale in Multi-Agent Systems?
authors:
- Addison J. Wu
- Jasin Cekinmez
- Michel Liao
- Karthik Narasimhan
- Thomas L. Griffiths
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.30028
doi: null
arxiv: '2609.30028'
cite: Wu, A. J., Cekinmez, J., Liao, M., Narasimhan, K., & Griffiths, T. L. (2026). How does Adversarial Influence Scale in Multi-Agent Systems? arXiv preprint arXiv:2609.30028.
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Studies how susceptibility to deceptive agents scales with group size and the fraction of deceivers in multi-agent deliberation. What matters is the proportion of deceivers, not the number of agents. The defection rate (how often initially correct agents switch to an incorrect final answer) rises linearly with that proportion. Unlike humans in comparable conformity experiments, who are reliably swayed only when misleading confederates are a majority, LLM agents defect regularly even when deceivers are a minority. Susceptibility depends on which models interact, especially on the honest side. Allowing deceivers to coordinate privately can make them less effective. Adding more agents is therefore not a defence, because the adversary can scale with the group.

## Contribution

A scaling law for adversarial influence in LLM collectives, with an explicit comparison to Asch-style human conformity. Complements [[ashery-2024-emergent]] (committed minorities) and [[huang-2024-resilience]] (faulty agents).

## Key results

- Claimed: defection rate linear in deceiver proportion; independent of group size at fixed proportion.
- Claimed: LLMs defect under deceiving minorities, unlike humans.
- Claimed: private coordination among deceivers can reduce their effectiveness.

## Methods and models

Multi-agent deliberation with varying group size and deceiver fraction; several model pairings. Details not checked.

## Limitations and open questions

Abstract-level read; task types and number of rounds unknown.

## Relevance to us

Gives a dose-response baseline for adversarial agents in swarms. Related: [[ys-2026-everyone]], [[lee-2024-prompt]].
