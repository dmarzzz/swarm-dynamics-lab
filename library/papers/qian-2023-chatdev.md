---
id: qian-2023-chatdev
type: paper
title: 'ChatDev: Communicative Agents for Software Development'
authors:
- Chen Qian
- Wei Liu
- Hongzhang Liu
- Nuo Chen
- Yufan Dang
- Jiahao Li
- Cheng Yang
- Weize Chen
- Yusheng Su
- Xin Cong
- Juyuan Xu
- Dahai Li
- Zhiyuan Liu
- Maosong Sun
year: 2023
venue: 'Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024), Volume 1: Long Papers'
url: https://arxiv.org/abs/2307.07924
doi: 10.18653/v1/2024.acl-long.810
arxiv: '2307.07924'
cite: 'Qian, C., Liu, W., Liu, H., Chen, N., Dang, Y., Li, J., Yang, C., Chen, W., Su, Y., Cong, X., et al. (2024). ChatDev: Communicative agents for software development. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 15174-15186. https://doi.org/10.18653/v1/2024.acl-long.810'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1260 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

ChatDev is a virtual software company of LLM agents (CEO, CTO, programmer, reviewer, tester) that move through design, coding and testing phases via a "chat chain" that specifies what to communicate, and "communicative dehallucination" that specifies how (agents ask for clarification before answering). The authors find natural language helps system design and code-language communication helps debugging.

## Contribution

Influential demonstration of role-structured LLM teams for end-to-end software generation; its codebase later hosted the 1000-agent MacNet experiments ([[qian-2024-scaling]]).

## Key results

- End-to-end generation of small software projects with improved completeness and executability over single-agent baselines (abstract-level; numbers not read).

## Methods and models

Waterfall-like chat chain of two-agent dialogues; role prompts; dehallucination by reverse questioning. Code: https://github.com/OpenBMB/ChatDev

## Limitations and open questions

Fixed roles and sequential phases; [[cemri-2025-why]] reports frequent role-disobedience and verification failures and a +9.4% gain from tightening role specification.

## Relevance to us

Background for role-based MAS design; not swarm-like.
