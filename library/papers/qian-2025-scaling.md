---
id: qian-2025-scaling
type: paper
title: Scaling Large Language Model-based Multi-Agent Collaboration
authors:
- Chen Qian
- Zihao Xie
- YiFei Wang
- Wei Liu
- Kunlun Zhu
- Hanchen Xia
- Yufan Dang
- Zhuoyun Du
- Weize Chen
- Cheng Yang
- Zhiyuan Liu
- Maosong Sun
year: 2025
venue: International Conference on Learning Representations (ICLR 2025)
url: https://arxiv.org/abs/2406.07155
doi: null
arxiv: '2406.07155'
cite: Qian, C., Xie, Z., Wang, Y., Liu, W., Zhu, K., Xia, H., Dang, Y., Du, Z., Chen, W., Yang, C., Liu, Z., & Sun, M. (2025). Scaling Large Language Model-based Multi-Agent Collaboration. In International Conference on Learning Representations (ICLR 2025). arXiv:2406.07155.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 7 (OpenAlex, arXiv record, 2026-10-03); 282 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

MacNet (multi-agent collaboration network) arranges LLM agents on a directed acyclic graph: an "actor" agent sits on each node and produces an artifact (answer, code, text), a "critic" agent sits on each edge and issues refinement instructions, and agents interact pairwise in topological order, passing forward only the refined artifact rather than full dialogue histories. With this memory control the sink agent's context grows linearly rather than quadratically in node count. The authors compare chain, star, tree, mesh, layered (MLP-like) and random DAG topologies on MMLU, HumanEval, SRDD (repository-level software) and CommonGen-Hard with GPT-3.5, and scale node count from 2^0 to 2^6. A 64-node mesh has 64 + 2016 = 2080 agents, the paper's "over a thousand agents". Average quality follows a logistic curve in log(node count) that saturates around 2^4 nodes (described as roughly a hundred agents for most topologies), which the authors call a "collaborative scaling law" with emergence at much smaller scale than neural scaling. Random (irregular) topologies beat regular ones on average and take about 52% less time than mesh; divergent topologies beat their edge-reversed convergent counterparts.

## Contribution

The first systematic attempt to scale task-solving LLM collectives to O(10^3) agents and to characterise a functional form for performance vs agent count. It links topology properties (density, small-world shortcuts, divergence) to collective output. Later work disputes its generality: [[kim-2025-towards]] finds degradation beyond 3-4 agents under matched compute on agentic tasks, [[bertalanic-2026-ringelmann]] finds hard ceilings in effective team size, and [[tran-2026-single]] attributes many gains to extra compute.

## Key results

- Measured (Table 1, ~4 nodes, GPT-3.5): average quality MacNet-Random 0.6522, Mesh 0.6316, Star 0.6267, Chain 0.6078, Tree 0.6015, Layer 0.5629 vs CoT 0.5757, AutoGPT 0.5655, GPTSwarm 0.5163, AgentVerse 0.5805. No single topology wins every task (chain best for MMLU-style closed tasks and SRDD; tree best for CommonGen).
- Measured: quality vs node count fits f(|V|) = gamma / (1 + exp(-beta(log|V| - alpha))) + delta per topology (fitted parameters per topology, not reported as universal constants).
- Measured: majority voting with the same number of LLM calls gains only 0.9% and plateaus at about 8 agents; AgentVerse hits context explosion beyond ~30 agents.
- Measured: number of distinct "aspects" raised in critiques jumps when |V| goes from 2^3 to 2^4; artifact length grows 7.51x from 2^0 to 2^4; critics' suggestions are implemented 93.10% of the time.
- Claimed (speculative): the mechanism is sampling of long-tail "aspects", modelled as p = 1 - (1 - 1/r)^{|V|^2} under a Zipf assumption.

## Methods and models

DAG G = (V, E); actors on nodes, critics on edges, |V| + |E| agents; topological-order traversal (Kahn); each edge interaction is up to 3 exchange rounds; long-term memory keeps only artifacts; convergent nodes aggregate incoming artifacts hierarchically. Topologies: chain, star, tree (binary), mesh (complete DAG), layer (balanced width/depth), random (edges removed from a mesh while keeping connectivity). Backbone GPT-3.5 (open models said to show the same pattern). Benchmarks: MMLU (accuracy), HumanEval (pass@k), SRDD (completeness/executability/consistency), CommonGen-Hard (composite). Code: https://github.com/OpenBMB/ChatDev/tree/macnet .

## Limitations and open questions

- Compute is not matched: larger networks make many more LLM calls and produce longer artifacts, and longer outputs help length-sensitive metrics (the authors acknowledge this for convergent topologies).
- The logistic fit has four free parameters per topology over 7 points; "scaling law" is descriptive.
- Single backbone (GPT-3.5) in main results; tasks are mostly non-agentic.
- The tail-aspect explanation is a hypothesis, not a tested mechanism.

## Relevance to us

The reference point for "more agents" claims and for topology as a design variable. Its small-world explanation of why random graphs win can be tested directly (vary rewiring probability as in [[wang-2025-rethinking]]). Compare with [[li-2024-more]], [[chen-2024-are]], [[kim-2025-towards]], [[bertalanic-2026-ringelmann]], [[zhuge-2024-language]], [[yang-2026-understanding]].
