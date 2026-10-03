---
id: han-2026-conformity
type: paper
title: "Conformity Dynamics in LLM Multi-Agent Systems: The Roles of Topology and Self-Social Weighting"
authors:
- "Chen Han"
- "Jin Tan"
- "Bohan Yu"
- "Wenzhen Zheng"
- "Xijin Tang"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.05606
doi: null
arxiv: "2601.05606"
cite: "Han, C., Tan, J., Yu, B., Zheng, W., & Tang, X. (2026). Conformity dynamics in LLM multi-agent systems: The roles of topology and self-social weighting. arXiv preprint arXiv:2601.05606."
topics:
- llm-agent-swarms
- sync-consensus
- collective-decision
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: "0 (OpenAlex W7123320592, arXiv record, 2026-10-03); Semantic Scholar 10 same day"
code: []
---

## Summary

Studies how network topology and a self-versus-social weight shape conformity in groups of 7 LLM agents doing binary misinformation detection. Each round, an agent outputs a judgment and a self-reported confidence; a support score is updated by confidence-normalised pooling, s_i(t+1) = [alpha p_i y_i + (1 - alpha) sum_j p_j y_j] / [alpha p_i + (1 - alpha) sum_j p_j], a DeGroot-style rule with a tunable self-weight alpha. Centralised aggregation (star or hierarchical trees) is compared with distributed consensus (ring, complete graph).

## Contribution

Combines a classical weighted-consensus update with LLM judgments to separate topology effects from self-reliance, and identifies "wrong-but-sure" cascades in dense graphs. A small-N, controlled counterpart to [[el-2026-physics]] and [[chen-2023-multi]].

## Key results

- Centralised structures decide immediately but accuracy is capped by the hub's competence; hubs favour peers whose reasoning resembles their own (same-model alignment bias). Measured.
- Distributed structures give more robust consensus; higher connectivity speeds convergence and raises average accuracy but increases the risk of high-confidence wrong cascades. Measured.
- Larger alpha (more self-reliance) generally improves accuracy. Measured.
- Mixed GPT-3.5/GPT-4o groups on complete graphs (ratios 0:7 to 7:0, 50 claims x 10 runs, alpha = 0.75) converge more slowly than homogeneous ones; final accuracy follows the majority model class. Measured.

## Methods and models

N = 7 agents, three LLMs (including GPT-3.5 and GPT-4o), fact-checking claims, fixed per-round update template. Skimmed method, results and limitations.

## Limitations and open questions

Fixed N = 7, three models, self-reported confidence that may not be calibrated, and a structured template rather than free deliberation (stated by the authors).

## Relevance to us

Gives a tunable self-weight parameter and topology sweep that map directly onto consensus theory, a template for small-N controlled experiments. Related: [[cho-2025-herd]], [[weng-2025-do]], [[bellina-2026-conformity]], [[zheng-2026-absorbing]].
