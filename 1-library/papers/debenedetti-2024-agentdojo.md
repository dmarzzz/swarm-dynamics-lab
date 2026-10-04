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

## Notes from dmarz/fm-identity-hijack

Read in full (arXiv HTML v3, main text). Numbers that bear on fork-merge corruption, all measured in the paper:

- Without attack, current LLMs solve under 66% of tasks. The generic "Important message" injection succeeds against the best agents in under 25% of cases; a prompt-injection detector cuts this to 8%, and a tool filter (agent picks its tools before seeing untrusted data) to 7.5%.
- Inverse scaling: more capable models are easier to attack, as in [[perez-2022-ignore]] and [[wang-2025-mcptox]].
- Per-suite spread is large: 92% targeted success in the Slack suite, where attackers control much of the tool output (web pages), and 0% on one two-goal travel injection task.
- Injections at the end of a tool response are most effective, up to 70% against GPT-4o.
- Attacker knowledge: addressing the model and user by correct names adds 1.9 points; wrong guesses cut success by about 22 points (45.8% to 23.2% or 23.7%). An attacker in a foreign domain who knows which model and principal a sub-agent serves gains little, but guessing wrong costs a lot, which weakly supports hiding the parent's identity (Q1).
- The authors note the tool filter fails when a user gives tasks over time without resetting context, since an injection can tell the agent to wait for a task with the right tools. A long-running exploring sub-agent is exactly that setting.
- They also note that planner/executor isolation still fails when the injection only alters the result of a tool call (for example a listing that tells the model to always select it). A returning part's biased findings are this case.

Adaptive and repeated-attempt results on this benchmark are in [[nist-2025-technical]] (11% to 81%; 57% to 80% with 25 tries). Persistence beyond one session, which AgentDojo does not model, is measured in [[xie-2026-what]].

## Notes from dmarz/fm-code-bench

Code catalogued as [[gh-ethz-spylab-agentdojo]] (MIT, 889 stars, last push 2026-06-02, pip package `agentdojo`). For fork-merge corruption it is the harness for the first step, compromising a child through untrusted tool output (Q3); it has no multi-agent or merge stage, so propagation into a parent must be added on top. Related harnesses: [[gh-asago-ai-midojo]] (man-in-the-middle variant with sandbox evidence) and CaMeL's evaluation code [[gh-google-research-camel-prompt-injection]].
