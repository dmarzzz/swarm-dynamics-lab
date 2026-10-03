---
id: karten-2026-agent
type: paper
title: 'Agent Bazaar: Enabling Economic Alignment in Multi-Agent Marketplaces'
authors:
- Seth Karten
- Cameron Crow
- Chi Jin
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2605.17698
doi: null
arxiv: '2605.17698'
cite: 'Karten, S., Crow, C., & Jin, C. (2026). Agent Bazaar: Enabling Economic Alignment in Multi-Agent Marketplaces. arXiv preprint arXiv:2605.17698.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A multi-agent market simulator for "economic alignment" with two failure scenarios. In The Crash (B2C), LLM firms undercut prices until the market collapses. In The Lemon Market (C2C), a single deceptive principal runs K seller identities with independent reputations, using diverse personas to post lexically distinct but fraudulently equivalent listings for poor-quality goods (q = 0.1); an identity whose reputation falls below 0.3 is retired and replaced by a fresh one at 0.8. Twelve sellers and twelve buyers trade used cars over 50 steps with anonymised seller IDs. Sybil revenue share stays below 5% at K = 3 for all buyer models but reaches 10 to 17% at K = 9, and trading volume falls from about 10 to 6 bids per step. A "Skeptical Guardian" prompt harness cuts Sybil revenue share by about 30% at K = 6. A Qwen 3.5 9B buyer trained with REINFORCE++ and a Sybil curriculum (K raised from 3 to about 7) reaches 92% Sybil detection with an 11% Sybil purchase rate.

## Contribution

The paper claims to be the first study of Sybil attacks executed by a single LLM agent coordinating multiple identities, and it shows Sybil detection can be trained into buyer agents with RL.

## Key results

- Measured: Sybil revenue share below 5% at K = 3, 10 to 17% at K = 9 (Sonnet and GPT buyers worse than Gemini), 3 seeds.
- Measured: guardian harness about 30% lower Sybil revenue share at K = 6 with Gemini buyers.
- Measured: RL-trained guardian detection 92% (88% before training), Sybil purchase rate 11%; detection 87 to 95% during training.
- Reported: failure severity varies by model, not by size; the Economic Alignment Score of the trained 9B model is 0.79.

## Methods and models

LLM buyer and seller agents in a posted-listing market with reputation; Sybil principal with identity rotation (whitewashing); prompt harnesses; REINFORCE++ with adaptive curriculum. 4 x 2 x 3 factorial over K, reputation visibility and seeds.

## Limitations and open questions

Skimmed (introduction, Lemon Market setup and results, training). Small markets (12 by 12), few seeds, simulated goods. Defence is buyer-side detection; no identity cost or admission control is modelled.

## Relevance to us

A ready testbed for Sybil attacks in agent marketplaces, including whitewashing via identity rotation and persona diversity that defeats text similarity (consistent with [[bara-2026-epistemic]]). Its buyer-side detection could be compared with structural defences such as the evidence gate in [[xia-2026-when]] or stake in [[hu-2025-inter-agent]]. Related marketplaces: [[bansal-2025-magentic]].
