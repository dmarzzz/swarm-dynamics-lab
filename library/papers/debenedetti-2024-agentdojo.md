---
id: debenedetti-2024-agentdojo
type: paper
title: 'AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents'
authors: [Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr]
year: 2024
venue: Advances in Neural Information Processing Systems (NeurIPS 2024) Datasets and Benchmarks; arXiv preprint
url: https://arxiv.org/abs/2406.13352
doi: null
arxiv: '2406.13352'
cite: 'Debenedetti, E., Zhang, J., Balunović, M., Beurer-Kellner, L., Fischer, M., & Tramèr, F. (2024). AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. arXiv:2406.13352.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 150 (Semantic Scholar, 2026-10-03)
code: []  # github.com/ethz-spylab/agentdojo, not opened
---

## Summary

An extensible evaluation environment for agents that call tools over untrusted data, rather than a fixed test suite. Populated with 97 realistic user tasks (email client, e-banking, travel booking, Slack-like workspace) and 629 security test cases pairing user tasks with injection tasks, plus attack and defence paradigms from the literature. Measured (abstract): state-of-the-art LLMs fail many tasks even without attack, and existing injection attacks break some security properties but not all.

## Contribution

The shared yardstick: CaMeL [[debenedetti-2025-defeating]], Fides [[costa-2025-securing]] and the MAS-hijacking baselines in [[triedman-2025-multi]] all report against it.

## Key results

- 97 tasks, 629 security cases (abstract).
- Neither attacks nor defences saturate the benchmark (abstract).

## Methods and models

Four simulated environments; utility and attack-success scoring functions per task; pluggable attacks and defences. Venue taken from Semantic Scholar (NeurIPS); not checked on the proceedings page.

## Limitations and open questions

Single-agent tool loop; no multi-agent or memory-merge scenarios, which is the gap for our topic.

## Relevance to us

- Q3 (attack): the benchmark of record for injection through tool outputs, the entry point by which a sub-agent in a hostile domain gets corrupted. It does not model what happens when that corrupted agent's state is merged into another agent; building that scenario on AgentDojo is a concrete experiment idea (inferred).
Related: [[wallace-2024-instruction]], [[beurer-kellner-2025-design]].
