---
id: liang-2025-dont
type: paper
title: "Don't Trust Your Upstream: Exploiting LLM Multi-Agent System via Topology-Guided Adversarial Propagation"
authors: [Ruichao Liang, Le Yin, Jing Chen, Yebo Feng, Cong Wu, Xiaoyu Zhang, Huangpeng Gu, Zijian Zhang, Yang Liu]
year: 2025
venue: Network and Distributed System Security (NDSS) Symposium 2026 (per the paper header; arXiv v1 December 2025)
url: https://arxiv.org/abs/2512.04129
doi: null
arxiv: '2512.04129'
cite: "Liang, R., Yin, L., Chen, J., Feng, Y., Wu, C., Zhang, X., Gu, H., Zhang, Z., & Liu, Y. (2025). Don't Trust Your Upstream: Exploiting LLM Multi-Agent System via Topology-Guided Adversarial Propagation. In Network and Distributed System Security (NDSS) Symposium 2026. arXiv:2512.04129."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-contagion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null  # Semantic Scholar and OpenAlex were rate-limited on 2026-10-03
code: []
---

## Summary

Studies how adversarial content that reaches an externally exposed "edge" agent (one that reads web pages, files or images) can travel through a multi-agent system's internal topology to a privileged agent that never touches outside content. The attacker is black-box: no access to weights, memory or inter-agent channels, only the public interface and the environment the edge agent reads. The paper models contamination spread on the agent graph, evaluates on three frameworks (Magentic-One, LangManus, OWL), five topologies and three models, and proposes a topology-trust defence (T-Guard).

## Contribution

Shows that the multi-agent topology is both a barrier and a channel: single-agent attacks that succeed 37-77% on single agents scored 0% end to end on the multi-agent systems (Table I), while topology-aware multi-hop propagation succeeded 40-78%. Names three structural weaknesses: topology leakage, uncalibrated inter-agent trust, and exposure of internal agents through multi-hop dependencies.

## Key results

- Black-box topology inference from ordinary queries recovered agent roles and edges with average F1 0.94 (measured); hiding the topology gave weak protection.
- End-to-end success 40-78% across 180 configurations; star and tree topologies (hubs) were most vulnerable, chain and mesh least, with the underlying model the largest factor (measured).
- 17 of 20 scenarios succeeded on two real applications (GPT-Researcher, TradingAgents). Two failures were cases where contaminated content was only written to persistent output files and never re-entered live execution (measured).
- A topology-unaware flooding baseline did markedly worse; path choice mattered most in mesh and star graphs (ablation).
- T-Guard (cross-modal check at edge agents, per-agent trust map, trust-gated permissions) blocked 94.8% of attacks, with detection about 94% at about 3.5% false positives and 31 ms added latency (measured, prototype on one framework).

## Methods and models

Agents built on GPT-4o, Claude 3.7 Sonnet and DeepSeek-R1; edge agents with browser and file-system MCP tools; a privileged execution agent reachable only through other agents. Contamination model: per-node taint updated from upstream neighbours with attenuation per hop; validated against measured semantic similarity of propagated content.

## Limitations and open questions

Attack payload details are withheld by the authors for ethical reasons. T-Guard is a prototype evaluated on one framework and one model. Static topologies only; no adaptive defender.

## Relevance to us

Directly the fork-merge geometry: the exploring sub-agent is the edge agent, and the parent is the high-privilege core that never reads the hostile domain itself. Q3: the measured result is that compromising the exposed part is enough to reach the core in 40-85% of cases, without impersonation or memory access. Q1: the topology-recovery F1 of 0.94 is negative evidence for "hide the structure" defences that rely on opacity alone; hiding which branch returns would need to survive the same probing. Q2: the failure analysis (content that only lands in a stored file does not propagate until something re-reads it) suggests a merge that quarantines returned memory as inert data breaks the chain; T-Guard's trust-gated permissions are a per-branch version of this. Compare [[wang-2025-g-safeguard]], [[yu-2024-netsafe]], [[he-2025-red]].
