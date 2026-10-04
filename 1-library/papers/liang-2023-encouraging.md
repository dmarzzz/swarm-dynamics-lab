---
id: liang-2023-encouraging
type: paper
title: Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate
authors:
- Tian Liang
- Zhiwei He
- Wenxiang Jiao
- Xing Wang
- Yan Wang
- Rui Wang
- Yujiu Yang
- Shuming Shi
- Zhaopeng Tu
year: 2023
venue: Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024)
url: https://arxiv.org/abs/2305.19118
doi: null
arxiv: '2305.19118'
cite: Liang, T., He, Z., Jiao, W., Wang, X., Wang, Y., Wang, R., Yang, Y., Shi, S., & Tu, Z. (2024). Encouraging divergent thinking in large language models through multi-agent debate. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024). arXiv:2305.19118.
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "29 (OpenAlex W4378945542, arXiv record, 2026-10-03); Semantic Scholar 1433 same day"
code: []
---

## Summary

Identifies "Degeneration-of-Thought": once an LLM is confident in a solution, self-reflection cannot generate new ideas even when the solution is wrong. The proposed Multi-Agent Debate (MAD) has agents argue in a "tit for tat" manner while a judge manages the debate and picks the final answer. On commonsense machine translation and counter-intuitive arithmetic, MAD improves over reflection baselines; an adaptive stopping rule and a modest level of disagreement work best, and an LLM judge may be unfair when debaters use different LLMs.

## Contribution

Introduced deliberate disagreement (negative coupling) as a tool against premature convergence, the counterpart to the consensus-seeking debate of [[du-2023-improving]].

## Key results

- MAD outperforms self-reflection on two challenging datasets (abstract claim; numbers not read).
- Too much adversarial pressure hurts; moderate tit-for-tat is best (abstract claim).

## Methods and models

Affirmative and negative debaters plus a judge; adaptive break of debate. Code: https://github.com/Skytliang/Multi-Agents-Debate

## Limitations and open questions

Two datasets; judge bias; gains later questioned by majority-voting baselines ([[choi-2025-debate]]).

## Relevance to us

Mechanistically it is a signed-coupling intervention; [[el-2026-physics]] models such "discordant" edges explicitly (J_ij = -1) and finds them weaker than concordant ties.
