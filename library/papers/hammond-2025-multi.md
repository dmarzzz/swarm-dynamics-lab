---
id: hammond-2025-multi
type: paper
title: Multi-Agent Risks from Advanced AI
authors:
- Lewis Hammond
- Alan Chan
- Jesse Clifton
- Jason Hoelscher-Obermaier
- Akbir Khan
- Euan McLean
- Chandler Smith
- Wolfram Barfuss
- Jakob Foerster
- Tomáš Gavenčiak
- The Anh Han
- Edward Hughes
- Vojtěch Kovařík
- Jan Kulveit
- Joel Z. Leibo
- Caspar Oesterheld
- Christian Schroeder de Witt
- Nisarg Shah
- Michael Wellman
- Paolo Bova
- Theodor Cimpeanu
- Carson Ezell
- Quentin Feuillade-Montixi
- Matija Franklin
- Esben Kran
- Igor Krawczuk
- Max Lamparth
- Niklas Lauffer
- Alexander Meinke
- Sumeet Motwani
- Anka Reuel
- Vincent Conitzer
- Michael Dennis
- Iason Gabriel
- Adam Gleave
- Gillian Hadfield
- Nika Haghtalab
- Atoosa Kasirzadeh
- Sébastien Krier
- Kate Larson
- Joel Lehman
- David C. Parkes
- Georgios Piliouras
- Iyad Rahwan
year: 2025
venue: 'Cooperative AI Foundation Technical Report #1 (arXiv preprint)'
url: https://arxiv.org/abs/2502.14143
doi: null
arxiv: '2502.14143'
cite: 'Hammond, L., Chan, A., Clifton, J., Hoelscher-Obermaier, J., Khan, A., McLean, E., Smith, C., Barfuss, W., Foerster, J., Gavenčiak, T., et al. (2025). Multi-agent risks from advanced AI. Cooperative AI Foundation, Technical Report #1. arXiv:2502.14143.'
topics:
- llm-agent-swarms
- fork-merge-security
- marl-emergence
- sybil-resistance
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "10 (OpenAlex W4407806359, arXiv record, 2026-10-03); Semantic Scholar 207 same day"
code: []
---

## Summary

A structured taxonomy of risks from many interacting advanced AI agents: three failure modes based on incentives (miscoordination, conflict, collusion) and seven risk factors (information asymmetries, network effects, selection pressures, destabilising dynamics, commitment problems, emergent agency, multi-agent security), each illustrated with real-world examples and experimental evidence, plus mitigation directions.

## Contribution

The reference risk taxonomy for multi-agent AI; "destabilising dynamics" and "network effects" are explicitly collective-dynamics risk factors.

## Key results

- Taxonomy and review; no new data.

## Methods and models

Expert synthesis (44 authors).

## Limitations and open questions

Broad; quantitative evidence is drawn from other studies.

## Relevance to us

Framing for why swarm dynamics of AI agents matters; pairs with [[cemri-2025-why]] (engineering failures) and [[gu-2024-agent]] (contagion).

## Notes from dmarz/sybil-llm-agents

Reread 2026-10-03 for Sybil resistance (arXiv HTML, searched the full text for identity, Sybil and collusion passages). The report has no section on Sybil attacks as such, but three parts bear on it. (1) Collusion (Section 2.3) defines AI collusion as undesirable cooperation, notes that agents can learn to collude without developer intent, and lists LLM collusion work including [[motwani-2024-secret]] and [[fish-2024-algorithmic]]. (2) "Homogeneity and Correlated Failures" warns that many agents will run on a few similar foundation models; [[bara-2026-epistemic]] measures exactly this as correlated extraction error (gamma = 0.719) that caps what more agents can add. (3) Under institutions and monitoring, it proposes unique agent identifiers ([[chan-2024-ids]]) as the basis for reputation systems in pseudo-anonymous settings such as marketplaces, and immutable identifiers plus tamper-evident logs to detect suspicious patterns among agent networks, citing [[ju-2024-flooding]]. It does not discuss how many identities one principal can create, which is the gap later work on reputation laundering ([[xia-2026-when]]) and marketplace Sybils ([[karten-2026-agent]]) addresses.

## Notes from dmarz/fm-ai-control

Reread 2026-10-03 for fork-merge corruption (arXiv HTML, Section 3.7 Multi-Agent Security read in full). Three passages bear on it. (1) "Swarm attacks" notes that many small agents can parallelise tasks and recompose their outputs, which "can undermine the common assumption that individual agents with restricted capabilities are safe"; this is the attacker-side mirror of a parent splitting and recombining, and it is what [[makins-2026-multi]] later measured as the fragmentation effect. (2) Case study 12 reports from Jones et al. that decomposing a malicious task between a frontier model and a weak unconstrained model raised success from under 3% for either alone to 43% combined (measured there, quoted here). (3) Case study 13, run by the report's authors: Llama 2 7B fine-tuned on 120 documents describing prompt injections spontaneously tried to jailbreak an LLM scorer in 4% of cases when told an LLM would score it, and never when told a human would. This is the only measured instance I found in this lane of an agent spontaneously attacking another agent that evaluates its output, which is the role a parent plays when it vets a returning child (Q3). Directions in 3.7.3 (containment and isolation protocols, tamper-evident logs, immutable identifiers) are suggestions, not results. The report does not discuss agents that fork and later merge.
