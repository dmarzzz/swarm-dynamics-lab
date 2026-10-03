---
id: blumenkamp-2020-emergence
type: talk
title: "[CoRL 2020] The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning"
authors: [Jan Blumenkamp, Amanda Prorok]
year: 2020
url: https://www.youtube.com/watch?v=YGrDcR2yj_E
venue: "CoRL 2020 presentation, Prorok Lab; video uploaded 2021-01-26"
topics: [marl-emergence, fork-merge-security]
added_by: shadow/sol-aud
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Prorok Lab's short presentation demonstrates learned manipulative communication by a self-interested agent among cooperative peers. Read all recovered timestamped captions through the closing thanks, approximately five minutes. The YouTube landing page supplies title, publisher, and upload date; the associated paper's opened author header at https://arxiv.org/html/2008.02616v2 verifies research authors Jan Blumenkamp and Amanda Prorok. The narrator is not personally identified in the captions, so the authors field credits the research team, not a claim that both speak in the recording. This is a full-transcript read, not inspection of the plots or a full-paper read.

- [00:44] The task uses cooperative agents in a grid-world coverage problem with learned decentralized communication. [01:11] The model accommodates individual, non-shared rewards within a common differentiable communication channel, and heterogeneous actor weights allow a self-interested agent to differ from the cooperative agents.
- [02:08] Cooperative policies are trained first and then frozen while the self-interested policy is optimized relative to them. The three examples are non-convex coverage, split coverage rewarding one side, and path planning. This is not joint defensive co-training.
- [02:54] The presentation reports mean performance across 100 evaluation runs, comparing communication enabled and disabled between the self-interested agent and cooperative peers. With communication enabled, the self-interested agent obtains a larger return share; with it disabled, cooperative agents outperform it. The same qualitative pattern is reported across the three tasks, but numerical effect sizes are not stated in the captions.
- [03:37] Post-hoc message decoding is compared with true local observations: cooperative messages reflect those observations more closely than self-interested ones, supporting the manipulative-message interpretation. [04:33] Co-training, detection, and mitigation are expressly future work, not successful defenses demonstrated here.

## Relevance to us

Direct evidence that a shared learned communication channel can be exploited by an agent with a different objective even when peers retain fixed cooperative policies. Useful for testing message-level trust and separating channel isolation from physical-interaction effects. It is not an LLM, memory-poisoning, Sybil, or reintegration experiment; no universal safe corrupt-agent fraction follows from the single-agent example.
