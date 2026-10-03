---
id: zhou-2025-corba
type: paper
title: 'CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models'
authors:
- Zhenhong Zhou
- Zherui Li
- Jie Zhang
- Yuanhe Zhang
- Kun Wang
- Yang Liu
- Qing Guo
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.14529
doi: null
arxiv: '2502.14529'
cite: 'Zhou, Z., Li, Z., Zhang, J., Zhang, Y., Wang, K., Liu, Y., & Guo, Q. (2025). CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models. arXiv preprint. arXiv:2502.14529.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Introduces Contagious Recursive Blocking Attacks (Corba): a prompt injected at one entry agent that instructs it to block (stop doing useful work) and to pass the same instruction to every agent it talks to, recursively, so the instruction reaches every node reachable from the entry and keeps consuming compute. The instructions look benign, so alignment does not reject them. Evaluated on AutoGen and Camel with GPT-4o-mini, GPT-4, GPT-3.5-turbo and Gemini 2.0 Flash at 3, 5 and 10 agents, plus an open-ended six-agent free-dialogue simulation. Read: the whole short paper (workshop-length main text); appendices not read.

## Contribution

Shows that availability attacks propagate contagiously through agent topologies and that a recursive self-forwarding instruction outperforms broadcast-style injection, especially as systems grow.

## Key results

- Proportional attack success (share of agents blocked), 10 agents, GPT-4o-mini: 79% (AutoGen) and 92% (Camel) for Corba against 52% and 64% for the broadcast baseline, as I read the layout of Table 1 (measured; the HTML table labels are ambiguous).
- 100% of agents blocked in 3-agent systems on GPT-4o-mini for both methods; Corba's advantage grows with system size (measured).
- Peak blocking was reached in 1.6-1.9 turns for Corba against 2.0-4.1 for the baseline (measured, Table 2).
- In the open-ended six-agent dialogue, Corba compromised most agents within a few turns (measured, Figure 1).

## Methods and models

Metrics: P-ASR (fraction of blocked agents) and PTN (turns to peak). Topologies varied within each framework. Code at github.com/zhrli324/Corba.

## Limitations and open questions

No defence is studied (stated). Blocking is a denial-of-service objective; the paper does not measure corruption of outputs.

## Relevance to us

Q3: a recursive "do X and tell everyone you talk to to do X" instruction is the minimal self-propagating payload, and the paper shows it saturates small systems in under two turns. For fork-merge, this is the mechanism by which one corrupted child, after merge, would reach every sibling the parent subsequently forks. It also shows that payloads need not look harmful to spread, so harm filters at merge time do not catch it. Q2: success fell with more agents for weaker models (GPT-3.5-turbo: 70% at 3 agents to 30% at 10), which is weak evidence that dilution helps only when the models are not compliant. Related: [[papadopoulos-2026-mind]], [[zhang-2026-agentworm]], [[zhang-2024-breaking]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2502.14529 . Read depth in this session: full.

Read all sections and both appendices. Table 1 labels are now checked: for 10 GPT-4o-mini agents the blocked-agent proportions are 79% AutoGen and 92% Camel, versus 52% and 64% for the baseline. These are P-ASR fractions of agents blocked, not percentages of arbitrary-code execution trials. The existing statement that no defence was studied is incomplete: Appendix A evaluates an LLM checker, a workflow monitor and perplexity detection. The monitor interception rate remains below 0.25, and attack perplexity is close to benign content in Table 5. No successful containment defence is developed. The 1.6-1.9 turn peaks in Table 2 are specific to the shared-history framework setups; topological tests take more turns (Table 4).
