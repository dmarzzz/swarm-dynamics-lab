---
id: he-2025-red
type: paper
title: Red-Teaming LLM Multi-Agent Systems via Communication Attacks
authors:
- Pengfei He
- Yupin Lin
- Shen Dong
- Han Xu
- Yue Xing
- Hui Liu
year: 2025
venue: ACL 2025 (per the arXiv comment field; track not stated)
url: https://arxiv.org/abs/2502.14847
doi: null
arxiv: '2502.14847'
cite: He, P., Lin, Y., Dong, S., Xu, H., Xing, Y., & Liu, H. (2025). Red-Teaming LLM Multi-Agent Systems via Communication Attacks. ACL 2025 (per the arXiv comment field; track not stated). arXiv:2502.14847.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Proposes Agent-in-the-Middle (AiTM): an external LLM-based adversarial agent intercepts the messages sent to one victim agent in a multi-agent system and replaces them with instructions tailored to the victim's role, refined turn by turn with a reflection step. The attacker does not modify any agent, prompt or tool and does not know the system's internal structure. Evaluated on AutoGen and Camel with four communication structures (chain, tree, complete, random) on MMLU biology and physics, HumanEval and MBPP, and on MetaGPT and ChatDev. Main text read in full; appendices not read.

## Contribution

First study of the inter-agent channel, rather than an agent, as the compromised component. It shows that controlling what one agent hears is enough to steer the whole system's output.

## Key results

- Attack success above 40% in every cell of Table 1 (32 cells) and above 70% in most, all agents on GPT-4o (measured).
- Chain is most vulnerable (code injection 95-98.5%); complete graphs resisted targeted answer changes on MMLU better (about 40-50%) because other agents challenged visible manipulations; denial-of-service exceeded 80% in 23 of 32 cells (measured).
- Position matters: in a tree, intercepting a parent rather than a child raised targeted ASR from 40.7% to 67.4% (AutoGen, MMLU-bio); intercepting later speakers in a complete graph raised it from 43.9% to 95.3% (measured, Table 2).
- More persuasive adversarial prompts raised targeted ASR from 19.5% to 40.7% (AutoGen tree), and a stronger attacker model than the victim system increased success (measured).
- MetaGPT (a chain with no monitoring): 75.7-100% across roles. ChatDev: 0% when intercepting CPO or CEO, 45-70% at CTO or Programmer, attributed to phase-level output constraints (measured, Table 4).

## Methods and models

Three to six agents per structure; final answer by last agent or an LLM judge. Success for targeted attacks is defined as the output containing a prescribed transformation (MMLU label shifted by four letters) or an injected file-scanning function in generated code; DoS is a refusal-like response. GPT-3.5-turbo, GPT-4o-mini and GPT-4o compared as attacker and victim models.

## Limitations and open questions

No defence evaluated and no baseline attack. Interception is assumed possible (eavesdropping in decentralised deployments) rather than demonstrated. Black-box GPT models only. Code release was promised at writing.

## Relevance to us

Q3: the merge channel between a returning child and the parent is exactly a message the parent receives; AiTM measures what happens when an adversary controls one such channel. The position result is directly relevant: corrupting the link into a higher-level aggregator (the parent) roughly doubled success in the tree setting, which is the fork-merge topology. Q2: the complete-graph and tree results are the only evidence here that peer cross-checking reduces success, and only for manipulations other agents can notice (answer flips), not for subtle code additions or refusals. Q1: the attacker needed no knowledge of the structure, so hiding the structure alone would not stop a channel-level adversary. Related: [[triedman-2025-multi]], [[liang-2025-dont]], [[yu-2024-netsafe]].


## Notes from shadow/sol-g74

Issue #74 rerun, 2026-10-03. Source opened: https://arxiv.org/abs/2502.14847 . Read depth in this session: skim.

Re-read abstract and Tables 1, 2 and 4 in the HTML. Table 1 has 64 cells across two attack objectives, not 32 total: 32 targeted and 32 denial-of-service cells. Its minimum targeted ASR is 40.7%. The parent-position comparison in Table 2 is 40.7% versus 67.4% for AutoGen/MMLU-bio/tree; the later-speaker comparison is 43.9% versus 95.3% for AutoGen/MMLU-bio/complete. These are targeted ASRs, not real-world interception probabilities. Table 4 confirms 0% for ChatDev CPO/CEO in the tested roles and 45.4-69.3% for CTO/Programmer across its tasks. A controlled incoming communication channel is assumed; the study does not prove that hidden real systems can be intercepted.
