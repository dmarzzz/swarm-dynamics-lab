---
id: el-mir-2026-byzantine
type: paper
title: 'Byzantine Cheap Talk: Adversarial Resilience and Topology Effects in LLM Coordination Games'
authors:
- Aya El Mir
- Martin Takáč
- Salem Lahlou
year: 2026
venue: NETYS 2026 (International Conference on Networked Systems), accepted per arXiv comment
url: https://arxiv.org/abs/2606.07790
doi: null
arxiv: '2606.07790'
cite: 'El Mir, A., Takáč, M., & Lahlou, S. (2026). Byzantine Cheap Talk: Adversarial Resilience and Topology Effects in LLM Coordination Games. arXiv preprint arXiv:2606.07790. Accepted at NETYS 2026.'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 3 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Studies a 4-player Stag Hunt with cheap-talk communication across six model families and 720 trials. When Byzantine agents signal cooperation but defect, honest agents detect the betrayal within one round but fail to adapt collectively; many keep cooperating despite repeated exploitation because the unanimity payoff makes recovery impossible. Explicitly telling agents that communication topology is restricted collapses cooperation, while applying the same restriction silently preserves near-perfect cooperation. Two archetypes replicate across cohorts: Defection-Prone models that switch permanently after betrayal and Cooperation-Persistent models that keep cooperating at individual cost.

## Contribution

Shows that coordination failure under Byzantine agents in LLM groups comes from agents' meta-reasoning about hidden information, not from information loss.

## Key results

- Reported in abstract: detection within one round, but no collective recovery; disclosed topology restriction collapses cooperation, silent restriction does not; two stable behavioural archetypes.

## Methods and models

4-player Stag Hunt, cheap-talk channel, Byzantine signal-then-defect agents, topology manipulations, six model families, 720 trials.

## Limitations and open questions

Abstract only; one game with a unanimity payoff, four players.

## Relevance to us

Small-group evidence that detecting a Byzantine or Sybil agent is not the same as recovering from it: the swarm needs a mechanism (exclusion, reweighting) rather than relying on agents to adapt. Disclosing network structure can itself degrade coordination, which matters for any swarm that publishes its membership or reputation graph. Related: [[jo-2025-byzantine]], [[huang-2024-resilience]].
