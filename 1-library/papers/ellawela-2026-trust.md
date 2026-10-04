---
id: ellawela-2026-trust
type: paper
title: 'Trust, Lies, and Long Memories: Emergent Social Dynamics and Reputation in Multi-Round Avalon with LLM Agents'
authors: [Suveen Ellawela]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2604.20582
doi: null
arxiv: '2604.20582'
cite: 'Ellawela, S. (2026). Trust, Lies, and Long Memories: Emergent Social Dynamics and Reputation in Multi-Round Avalon with LLM Agents. arXiv preprint arXiv:2604.20582.'
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

LLM agents play 188 games of The Resistance: Avalon while keeping memory of earlier games, including who played which role and how they behaved. Reputation emerges from that memory: agents cite past games ("I am wary of repeating last game's mistake of over-trusting early success"), reputations are role-conditional, and high-reputation players get 46% more team inclusions. Higher reasoning effort yields more strategic deception: evil players pass early missions to build trust before sabotaging in 75% of high-effort games vs 36% of low-effort ones.

## Contribution

Evidence that LLM agents carry lessons about having been deceived across episodes through memory, and that deceivers exploit the trust-then-betray pattern more with more reasoning.

## Key results

- 188 multi-round games with cross-game memory (measured).
- High-reputation players included in teams 46% more often (measured).
- Trust-then-sabotage by evil players: 75% (high effort) vs 36% (low effort) (measured).

## Methods and models

Hidden-role deception game with persistent memory between games. Abstract only.

## Limitations and open questions

From the abstract alone, no separation of whether "wariness" improves detection of evil players or just lowers inclusion of everyone; no signal-detection analysis reported.

## Relevance to us

V1: qualitative evidence that a remembered betrayal changes later behaviour ("wary of repeating last game's mistake"). The quantitative version of this is [[chen-2026-trust]]. The trust-then-betray tactic is also the adversary a honeypot-aware swarm would face.
