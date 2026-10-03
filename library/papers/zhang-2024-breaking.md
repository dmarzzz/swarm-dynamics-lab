---
id: zhang-2024-breaking
type: paper
title: 'Breaking Agents: Compromising Autonomous LLM Agents Through Malfunction Amplification'
authors:
- Boyang Zhang
- Yicong Tan
- Yun Shen
- Ahmed Salem
- Michael Backes
- Savvas Zannettou
- Yang Zhang
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2407.20859
doi: null
arxiv: '2407.20859'
cite: 'Zhang, B., Tan, Y., Shen, Y., Salem, A., Backes, M., Zannettou, S., & Zhang, Y. (2024). Breaking Agents: Compromising Autonomous LLM Agents Through Malfunction Amplification. arXiv preprint. arXiv:2407.20859.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies attacks that make LLM agents malfunction rather than do something overtly harmful: trapping them in infinite loops of repeated actions, or making them execute an irrelevant but benign function. Tests prompt injection, adversarial perturbations (GCG, VIPER, SCPN) and adversarial demonstrations at three entry points (user input, intermediate tool output, memory) on an agent emulator (many toolkits) and two implemented LangChain agents (Gmail and CSV), then in multi-agent chains where one compromised agent passes the malfunction on. Evaluates an LLM self-examination detector. Read: abstract, introduction, threat model, attack types, results tables and limitations.

## Contribution

Shows that "benign-looking" malfunction attacks are effective and, unlike overtly harmful injections, evade LLM-based self-examination, and that they propagate across agents.

## Key results

- Emulator, GPT-3.5-Turbo: failure rate 15.3% baseline, 59.4% with infinite-loop prompt injection, 26.4% with incorrect-function injection; GPT-4 32.1%, Claude-2 88.1% for the loop injection (measured, Tables 1-2). Adversarial perturbations (GCG, VIPER, SCPN) stayed near baseline.
- Implemented agents: injection through user input 75-90% success; through intermediate external output 0-60%; through the memory component 0% in all cases tested (measured, Table 4).
- Multi-agent propagation: infinite loop 30% and incorrect function 50% among same-type Gmail agents; 80% and 75% across different agent types (measured, Table 5; small case counts).
- Self-examination detection caught overtly harmful injections (direct harm 84-90%, data stealing 100% with one detector) but 0% of the infinite-loop and incorrect-function injections in most settings (measured).

## Methods and models

ToolEmu-style emulator with LLM-simulated tools; ReAct agents; failure judged by the agent's own end-of-chain self-reflection with human spot checks. GPT-3.5-Turbo, GPT-4, Claude-2.

## Limitations and open questions

Two implemented agents only; three 2023-2024 models; failure labelled by agent self-reflection (stated). Memory injection was ineffective in this setup, which conflicts with later memory-poisoning results and may reflect how memory was implemented.

## Relevance to us

Q3: a returning child does not need to carry anything that looks malicious to damage the parent; instructions to repeat or to run a harmless but wrong action pass harm-focused review. Detection at merge time that looks for harmful intent will miss this class, as the self-examination results show. The finding that memory injection failed here is a useful counterpoint to later work showing it succeeding (see [[papadopoulos-2026-mind]], [[zhang-2026-agentworm]]): the outcome depends on whether memory is loaded as instructions or as data. Related: [[zhou-2025-corba]], [[triedman-2025-multi]].
