---
id: yang-2024-watch
type: paper
title: "Watch Out for Your Agents! Investigating Backdoor Threats to LLM-Based Agents"
authors: [Wenkai Yang, Xiaohan Bi, Yankai Lin, Sishuo Chen, Jie Zhou, Xu Sun]
year: 2024
venue: Advances in Neural Information Processing Systems 37 (NeurIPS 2024)
url: https://arxiv.org/abs/2402.11208
doi: null
arxiv: '2402.11208'
cite: "Yang, W., Bi, X., Lin, Y., Chen, S., Zhou, J., & Sun, X. (2024). Watch Out for Your Agents! Investigating Backdoor Threats to LLM-Based Agents. Advances in Neural Information Processing Systems 37 (NeurIPS 2024). arXiv:2402.11208."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []  # github.com/lancopku/agent-backdoor-attacks, not opened
---

## Summary

A framework and experiments for backdoors in LLM agents, classified by outcome and by trigger location. Query-Attack hides the trigger in the user query; Observation-Attack hides it in an environment observation returned mid-task; Thought-Attack leaves the final output correct but changes intermediate reasoning, for example always calling a particular tool. Experiments fine-tune agents on AgentInstruct (web shopping) and ToolBench (tool use) with small numbers of poisoned traces, and test textual backdoor defences.

## Contribution

Identified the agent-specific backdoor forms that leave final answers correct while controlling intermediate actions, which output-only checks cannot see.

## Key results

- Measured: Query-Attack and Observation-Attack reach high attack success on WebShop sneaker queries with poisoned-trace budgets swept from 5 to 50 traces (target: always search for one brand), while performance on held-in tasks stays close to clean models.
- Measured: Observation-Attack keeps normal-task performance higher than Query-Attack, but responding to triggers in observations is harder to learn.
- Measured: Thought-Attack raises the rate at which the agent calls the attacker's target tool for translation queries, with normal-task performance similar to clean agents.
- Measured: existing textual backdoor defences do not easily mitigate these attacks.

## Methods and models

LLaMA2-7B-Chat (AgentInstruct) and LLaMA2-7B (ToolBench) fine-tuned on mixtures of clean and poisoned traces at several absolute and relative poisoning ratios; metrics are success rate, performance rate and attack success rate per task.

## Limitations and open questions

Requires training-data access; triggers and targets are simple; only two task families.

## Relevance to us

Q3. Two properties matter for merge. Observation-Attack means the trigger can be planted in the environment, so a backdoored part can be activated after merge by content the attacker places where the parent will look. Thought-Attack means a corrupted part can return correct final reports while its process (which tools, which sources) is steered; a merge protocol that compares only outputs across parts (a Q2 vote) will not detect it. Related: [[wang-2024-badagent]], [[hubinger-2024-sleeper]], [[zhang-2024-agent]].
