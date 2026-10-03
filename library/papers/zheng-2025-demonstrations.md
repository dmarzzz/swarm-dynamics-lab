---
id: zheng-2025-demonstrations
type: paper
title: Demonstrations of Integrity Attacks in Multi-Agent Systems
authors:
- Can Zheng
- Yuhan Cao
- Xiaoning Dong
- Tianxing He
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2506.04572
doi: null
arxiv: '2506.04572'
cite: Zheng, C., Cao, Y., Dong, X., & He, T. (2025). Demonstrations of Integrity Attacks in Multi-Agent Systems. arXiv preprint. arXiv:2506.04572.
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

Studies integrity attacks in LLM multi-agent systems: a malicious agent leaves the end task working but biases the system for its own gain. Four archetypes are implemented with crafted prompts or replaced outputs in CAMEL, AutoGen and MetaGPT on HumanEval, CIAR and MMLU-College: Self-Dealer (steers other agents to a particular tool, here Bing over Google), Free-Rider (hands its work to the next agent while emitting a fixed template), Scapegoater (inserts fake "system notification" blaming another agent) and Boaster (fake notification praising itself). An LLM monitor scores each agent's contribution. Read: abstract, introduction, attack definitions, all results sections including the defence test, conclusion and limitations.

## Contribution

Moves the threat model from performance degradation to manipulation of credit, reputation and tool choice, which leaves end-task metrics unchanged and so is invisible to outcome-based checks.

## Key results

- Scapegoater lowered the target agent's monitor scores by 18-67% (personal) and 25-71% (collective) while end-task performance moved by at most about 6% (measured, Table 1).
- Boaster raised the attacker's own scores by 1.5-19.7% and lowered other agents' collective scores by up to 34.6% (measured, Table 2).
- Self-Dealer shifted search-engine choice from mostly Google to Bing in all frameworks and tasks (measured, Figure 2).
- Free-Rider: target agents produced many more tokens doing the attacker's work; the attacker spent zero tokens and overall performance barely changed in CAMEL (measured, Figure 3, Table 4).
- A monitor told explicitly about the four attacks still failed to detect them; an o3-mini monitor in a small Scapegoater test behaved similarly (measured, Table 3 and appendix).

## Methods and models

GPT-family agents (GPT-4o-mini monitor by default); fake system-notification strings appended to normal outputs; percentage change versus baseline in personal and collective evaluation scores.

## Limitations and open questions

Academic frameworks only; preliminary defence; hand-written templates (an automation is sketched in the appendix) (stated).

## Relevance to us

Q3: for fork-merge, a corrupted child does not need to change the parent's answers to win; it can change the parent's model of which children to trust. Scapegoating siblings and boasting about itself are precisely the moves that would let one child "cut the others out" before or during merge, and LLM monitors did not catch them even when warned. Q2: any merge rule that weights children by a reputation or contribution score (as in [[ebrahimi-2025-adversary]] or [[wu-2025-securing]]) is itself an attack surface if the score comes from an LLM reading the children's own reports. Related: [[triedman-2025-multi]] (fake error messages), [[he-2025-red]].
