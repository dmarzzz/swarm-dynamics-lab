---
id: huang-2024-resilience
type: paper
title: On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents
authors:
- Jen-tse Huang
- Jiaxu Zhou
- Tailin Jin
- Xuhui Zhou
- Zixi Chen
- Wenxuan Wang
- Youliang Yuan
- Michael R. Lyu
- Maarten Sap
year: 2024
venue: Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267
url: https://arxiv.org/abs/2408.00989
doi: null
arxiv: '2408.00989'
cite: 'Huang, J.-t., Zhou, J., Jin, T., Zhou, X., Chen, Z., Wang, W., Yuan, Y., Lyu, M. R., & Sap, M. (2025). On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents. In Proceedings of the 42nd International Conference on Machine Learning (ICML 2025), PMLR 267, 26202-26226. arXiv:2408.00989.'
topics:
- llm-agent-swarms
- sybil-resistance
- fork-merge-security
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (OpenAlex, 2026-10-03); 122 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Asks how resilient different multi-agent structures are when some agents are clumsy or malicious, and how to defend them. Faulty agents are simulated with AutoTransform and AutoInject, which introduce errors into agents' responses. Across four downstream tasks and six systems, the hierarchical structure A -> (B <-> C) is most resilient, with a 5.5% performance drop versus 10.5% and 23.7% for the other two structures tested (the abstract names A -> B -> C and A <-> B <-> C as examples but does not map the two figures to them). Two defences, a Challenger mechanism letting each agent challenge others' outputs and an Inspector agent that reviews and corrects messages, recover up to 96.4% of errors.

## Contribution

An early controlled robustness study of LLM-MAS topology, anticipating the "centralised verification contains errors" finding of [[kim-2025-towards]].

## Key results

- Measured: performance drop 5.5% (hierarchical) vs 10.5% and 23.7% (the other two structures).
- Measured: Challenger/Inspector recover up to 96.4% of injected errors.

## Methods and models

Six multi-agent systems grouped into structures; four downstream tasks (not detailed here); AutoTransform and AutoInject error injection. Code and data: https://github.com/CUHK-ARISE/MAS-Resilience .

## Limitations and open questions

Abstract-level read; small teams (3-5 agents).

## Relevance to us

Topology-resilience trade-off is a classic swarm question; test whether these results hold in larger sparse swarms. Related: [[wu-2026-how]], [[zhang-2025-which]].

## Notes from dmarz/llm-agent-swarms-recent-audit

Audit 2026-10-03: venue confirmed on the PMLR proceedings page (https://proceedings.mlr.press/v267/huang25ay.html, pages 26202-26226); venue and cite updated from "not verified" to ICML 2025. The year field and id keep 2024, the arXiv v1 date. Key numbers (5.5% vs 10.5% and 23.7% drop) match the abstract.

## Notes from dmarz/sybil-llm-agents

Reread the abstract 2026-10-03 for the Sybil-resistance lane. The faulty-agent model (AutoTransform, AutoInject) corrupts one agent's outputs; it does not let an adversary hold several seats, so the 5.5% vs 10.5% vs 23.7% topology result is a single-fault resilience result, not a Sybil result. The Inspector defence is a centralised checker; [[jo-2025-byzantine]] and [[lee-2026-robust]] are the decentralised counterparts with explicit Byzantine bounds, and [[el-mir-2026-byzantine]] shows that detecting a bad agent does not imply the group recovers.

## Notes from dmarz/fm-bft-aggregation

Opened the arXiv abstract page this session (2026-10-03). Bearing on fork-merge corruption, Q2: the abstract reports that a hierarchical structure, A->(B<->C), is the most resilient of the tested multi-agent structures under injected faulty agents (AutoTransform, AutoInject). For a parent that reintegrates sub-agents, the analogue is a merge path where returning parts are cross-checked by peers before reaching the parent, rather than written straight into its state. The faults here are benign-style errors, not targeted takeovers, so this bounds resilience from above for Q3-style attacks. Compare [[lee-2026-robust]] and [[liu-2026-consensus]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2408.00989 . Read depth in this session: abstract.

The task seed called this Huang et al. (2024), malicious-agent resilience. The current arXiv record is titled On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents, with nine authors and a 2024 initial submission. This resolves the changed-title seed, rather than creating a duplicate. The abstract confirms hierarchical resilience and up to 96.4% error recovery. Those are injected-fault benchmark results, not a general guarantee against optimized self-propagating attackers.
