# Poietic Agents prior art boundary

Screening update on 2026-10-04 UTC. This is a focused design check, not a complete survey or a novelty certificate. Existing background is in the [HX collection](../heterogeneous-swarms/README.md) and [frontier review](../heterogeneous-swarms/frontiers/LITERATURE.md). Those earlier rankings did not include all the close methods found below.

## Close work found in this design pass

| Source and actual reading | Already covered | Consequence for this design |
| --- | --- | --- |
| [[chen-2026-agentslimming]] — abstract, introduction, selected methods and appendix E; skim | Graph-node pruning, cheaper-model replacement and optimization break-even accounting | Neither model downgrading nor charging discovery cost is new; include a prune/replace comparator |
| [[huang-2026-manta]] — abstract and official project page; no full methods audit | Runtime topology repair, changing roles/links, and retained structural experience | Dynamic topology and cross-run adaptation cannot be our novelty claim; compare a central optimizer |
| [[sampath-2026-adaptive]] — abstract only | Dynamic specialist hiring, eviction and history pruning | A changing specialist roster is already a published proposal/result claim; inspect its evaluation before claiming a gap |
| [[zhang-2026-safesieve]] — publisher abstract only | Progressive communication pruning using experience | Fewer communication edges alone are insufficient |

Primary pages actually opened: [AgentSlimming](https://arxiv.org/html/2605.08813v1), [MANTA paper](https://arxiv.org/abs/2607.28527), [MANTA project](https://mao-code.github.io/MANTA/), [Adaptive Orchestration](https://arxiv.org/abs/2601.09742), and [SafeSieve](https://ojs.aaai.org/index.php/AAAI/article/view/40236). The MANTA repository README was also inspected, but neither implementation was installed or run. Reported performance is not independently replicated here.

Existing closest controls remain [[ong-2024-routellm]], [[yue-2025-masrouter]], [[kim-2026-multi]] and [[gh-denis-pplx-autojev]]. The biological motivation [[morris-2014-coexistence]] suggests testing dependency and rescue; it does not establish software efficacy.

## The remaining candidate question

Can initially equivalent agents discover useful shared **data services**, actually surrender direct capabilities, and restore a good allocation after changes, using only permitted operational history? Does agent-proposed differentiation beat a coherent cache, a static architecture and a central adaptive controller once maintenance, freshness, capacity and total cost are enforced?

That conjunction is a candidate distinction, not proof of an unanswered question. Uniform starting prompts alone would be a weak novelty claim. Recovery alone would also be insufficient. The design earns a contribution only if the prior methods do not already answer the same operational comparison and the results survive the strongest applicable baseline.

## Search record and next research gate

The three discovery queries were:

- `LLM agents adaptive specialization tool pruning heterogeneous multi agent systems self organization cost redundancy`
- `"multi-agent" "capability" "pruning" tools topology`
- `"agent" "workflow" "hardening" distillation small models`

This was one web-search screening pass with follow-up primary opens, not eight structured rounds or demonstrated saturation. AgentEvo, AgentPrune, adaptive graph pruning and automated workflow search appeared as further leads; their titles/snippets are leads, not methods findings. Four new close papers are enough to reject a claim that the earlier search was saturated.

The existing [methods task](../../../../tasks/heterogeneous-methods-review.md) now prioritizes Poietic Agents. It must inspect complete methods/appendices and code, follow backward and forward citations, search distributed systems/service caching, adaptive task allocation and biological division of labor, and satisfy the repository's full source and saturation requirements. Then obtain cross-researcher survey and hypothesis reviews. This pass adds no full-read credit and closes none of those gates.

## Design kill or reframe decisions

If a prior implementation already covers the proposed mechanism and comparison, frame the work as a replication or a deployment benchmark. If cache coherence and a static provider service explain the benefit, ship that simpler architecture. If only a central optimizer works, describe centralized architecture adaptation. Use biological language only if measured capability loss creates dependency and a controlled withdrawal/rescue demonstrates it.
