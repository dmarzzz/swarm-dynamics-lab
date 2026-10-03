---
id: du-2023-improving
type: paper
title: Improving Factuality and Reasoning in Language Models through Multiagent Debate
authors:
- Yilun Du
- Shuang Li
- Antonio Torralba
- Joshua B. Tenenbaum
- Igor Mordatch
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2305.14325
doi: null
arxiv: '2305.14325'
cite: Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). Improving factuality and reasoning in language models through multiagent debate. arXiv preprint arXiv:2305.14325.
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 2371 (Semantic Scholar, 2026-10-03; OpenAlex unavailable that day)
code: []
---

## Summary

Several instances of a language model each propose an answer, then over multiple rounds read the others' answers and reasoning and revise their own, converging on a common final answer. The same prompts and procedure are used across tasks. The authors report that this "society of minds" debate improves mathematical and strategic reasoning and reduces factual errors and hallucinations relative to a single model, and that it works with black-box models.

## Contribution

The seminal multi-agent debate (MAD) paper: it framed iterated peer exchange among LLM copies as a consensus process that improves accuracy, launching a large literature on debate, voting and discussion protocols.

## Key results

- Debate improves arithmetic, GSM8K-style math, chess-move and factuality benchmarks over single-agent baselines (abstract-level claim; per-task numbers not read here).
- Gains depend on number of agents and rounds (stated in the paper's analysis; not checked in this session).

## Methods and models

N agents (copies of one LLM) answer independently; in each round each agent receives the other agents' latest responses and is asked to update; final answer by agreement or majority. Project page with code is linked from the arXiv record (not opened).

## Limitations and open questions

Later work questions where the gains come from: [[choi-2025-debate]] shows majority voting alone accounts for most of the improvement and models debate as a martingale; [[wang-2024-mixture]] and [[li-2024-more]] show that sampling-and-aggregating is a strong baseline. Debate also induces conformity ([[weng-2025-do]], [[cho-2025-herd]]).

## Relevance to us

Debate is the simplest LLM consensus dynamics on a complete graph, and the natural baseline when we study how network topology and coupling change collective accuracy ([[el-2026-physics]], [[zheng-2026-absorbing]]).
