---
id: orlando-2026-emergent
type: paper
title: "Emergent Coordinated Behaviors in Networked LLM Agents: Modeling the Strategic Dynamics of Information Operations"
authors: ["Gian Marco Orlando", "Jinyi Ye", "Valerio La Gatta", "Mahdi Saeedi", "Vincenzo Moscato", "Emilio Ferrara", "Luca Luceri"]
year: 2026
venue: "Proceedings of the ACM Web Conference 2026 (WWW)"
url: https://arxiv.org/html/2510.25003
doi: "10.1145/3774904.3792580"
arxiv: "2510.25003"
cite: "Orlando, G. M., Ye, J., La Gatta, V., Saeedi, M., Moscato, V., Ferrara, E., & Luceri, L. (2026). Emergent Coordinated Behaviors in Networked LLM Agents: Modeling the Strategic Dynamics of Information Operations. In Proceedings of the ACM Web Conference 2026 (pp. 4805–4816). ACM."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "13 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A generative agent-based simulation of an X-like platform with 50 LLM agents: 10 information-operation (IO) agents told to promote a candidate and a campaign hashtag, and 40 organic agents initialised from real 2020-election Twitter users. Three regimes vary what IO agents know: Common Goal (objective only), Teammate Awareness (they are told who their teammates are), and Collective Decision-Making (every 5 steps they deliberate and an orchestrator agent consolidates a strategy). Each run lasts 50 iterations, three repetitions per regime. They measure the coordination signals used to detect real IOs.

## Contribution

The first systematic measurement of whether LLM agents left alone reproduce the trace signatures detectors look for. They do, and telling agents who their teammates are produces almost as much coordination as explicit deliberation.

## Key results

- Share of IO re-shares targeting IO peers: 0.82 (Common Goal), 0.96 (Teammate Awareness), 0.94 (Collective Decision-Making).
- IO intra-group density 0.74 to 0.89 to 0.89; clustering 0.86 to 0.96 to 0.97; reciprocity 0.56 to 0.68 to 0.65.
- Co-retweet similarity (the [[pacheco-2021-uncovering]] metric) 0.28 to 0.31 to 0.35 for IO agents, against 0.11 for organic agents in every regime.
- Pairwise post embedding similarity 0.89 to 0.91 for IO agents against about 0.62 for organic agents; intra-IO comment sentiment 0.68 to 0.83.
- Campaign hashtag in original posts 0.42 to 0.47 to 0.54; cascade size 3.84 to 4.26 to 4.56.
- Qualitatively, deliberating agents converge on amplifying high-performing posts, unified messaging, cross-promotion and shared key phrases, the tactics of real IOs.

## Methods and models

Simulator of Ferraro et al. (2024): agents with persona, memory and action policy (post, comment, re-share, follow) and a recommender. All agents run on a single LLM; the HTML full text I read does not name it. Mann-Whitney tests across agent pairs; statistics over 3 runs per regime. Code at an anonymised 4open.science link and a dashboard at llmxio-dashboard.vercel.app.

## Limitations and open questions

Small scale (50 agents) saturates intra-group ties; one LLM; three repetitions; one hashtag. The paper does not run a detector or measure detection accuracy; it shows the signals exist in simulation. Whether operators would let agents coordinate this visibly in the wild, or deliberately add noise, is not tested.

## Relevance to us

Direct evidence that LLM swarms emit the classical co-retweet and synchrony signatures, so the detectors in [[pacheco-2021-uncovering]] and [[luceri-2024-unmasking]] should transfer, at least to naive swarms. Its strongest result (mere teammate awareness suffices) suggests a hackathon experiment: what does a detector see when agents are told to coordinate but also to avoid co-retweet overlap? Pairs with [[qiao-2025-botsim]] and [[mukherjee-2026-moltgraph]].
