---
id: garra-2026-mitigating
type: paper
title: "Mitigating Emergent Collusion in LLM Pricing Agents"
authors: ["Abdullah Garra"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.13037
doi: null
arxiv: "2609.13037"
cite: "Garra, A. (2026). Mitigating Emergent Collusion in LLM Pricing Agents. arXiv preprint arXiv:2609.13037."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Reproduces the prompt-sensitivity effect of [[fish-2024-algorithmic]] with DeepSeek-V3.1: prompt P1 yields significantly higher prices and profits than P2, though less monopoly-like than the original GPT-4 results. Three interventions are tested. A prompt-only warning reduces but does not eliminate above-Nash pricing; a Harrington-inspired expected-damages payoff regulator brings P1 near the duopoly Nash benchmark and removes the P1-P2 gap; an active random entrant has the strongest effect, pushing prices below the random-entrant Nash benchmark.

## Contribution

A partial replication of Fish et al. on an open model plus a comparison of incentive-changing versus prompt-only remedies.

## Key results

- Measured (abstract): P1 > P2 replicates on DeepSeek-V3.1, weaker than GPT-4.
- Measured (abstract): entrant > damages regulator > prompt warning in reducing supracompetitive pricing.

## Methods and models

Repeated duopoly pricing; abstract read only.

## Limitations and open questions

Single model; abstract only.

## Relevance to us

Replication evidence for the Fish et al. anchor and support for incentive-side remedies, matching [[bracale-syrnikov-2026-institutional]]. An entrant firm is a cheap intervention to include in swarm factory conditions.
