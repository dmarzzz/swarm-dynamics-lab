---
id: muennighoff-2025-s1
type: paper
title: "s1: Simple test-time scaling"
authors:
- Niklas Muennighoff
- Zitong Yang
- Weijia Shi
- Xiang Lisa Li
- Li Fei-Fei
- Hannaneh Hajishirzi
- Luke Zettlemoyer
- Percy Liang
- Emmanuel Candès
- Tatsunori Hashimoto
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2501.19393
doi: null
arxiv: '2501.19393'
cite: "Muennighoff, N., Yang, Z., Shi, W., Li, X. L., Fei-Fei, L., Hajishirzi, H., Zettlemoyer, L., Liang, P., Candès, E., & Hashimoto, T. (2025). s1: Simple test-time scaling. arXiv preprint arXiv:2501.19393."
topics:
- agent-budgets
added_by: dmarz/budget-a
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1501 (Semantic Scholar, 2026-10-03)
code: []
---
## Summary

Looks for the simplest recipe for test-time scaling. The authors fine-tune Qwen2.5-32B-Instruct on s1K, 1,000 questions with reasoning traces chosen for difficulty, diversity and quality, and add "budget forcing": at decode time they either cut the thinking off at a token limit or, when the model tries to stop, append "Wait" to make it keep thinking. Reported in the abstract: s1-32B beats o1-preview on competition math by up to 27% (MATH and AIME24), and budget forcing lifts AIME24 from 50% to 57%.

## Contribution

Introduces budget forcing, a decode-time intervention that sets thinking length from outside the model with no budget signal shown to it. It is the standard "hidden, externally enforced" budget mechanism that later visible-budget methods compare against.

## Key results

- Measured (abstract): s1-32B exceeds o1-preview by up to 27% on MATH and AIME24.
- Measured (abstract): extending thinking with budget forcing raises AIME24 from 50% to 57%.
- Claimed (abstract): appending "Wait" often leads the model to re-check and fix wrong steps.

## Methods and models

SFT of Qwen2.5-32B-Instruct on the 1,000-example s1K set; budget forcing by forced termination or "Wait" insertion. Model, data and code are released (not catalogued here).

## Limitations and open questions

Abstract-level read. Math benchmarks only; no tools or agents. Budget forcing controls length but does not let the model plan against a known budget. Semantic Scholar lists an EMNLP venue; the citation here is the arXiv preprint.

## Relevance to us

The contrast case for budget-aware agents: here the budget is imposed by truncation and padding, while [[han-2024-token]], [[wen-2025-budgetthinker]] and [[liu-2025-budget]] show the budget to the model. Surveyed in [[alomrani-2025-reasoning]].
