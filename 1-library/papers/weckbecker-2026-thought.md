---
id: weckbecker-2026-thought
type: paper
title: "Thought Virus: Viral Misalignment via Subliminal Prompting in Multi-Agent Systems"
authors: ["Moritz Weckbecker", "Jonas Müller", "Ben Hagag", "Michael Mulet"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/html/2603.00131
doi: null
arxiv: "2603.00131"
cite: "Weckbecker, M., Müller, J., Hagag, B., & Mulet, M. (2026). Thought Virus: Viral Misalignment via Subliminal Prompting in Multi-Agent Systems. arXiv preprint arXiv:2603.00131."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "7 (Semantic Scholar, via Subliminal Learning citation list, 2026-10-03)"
code: []
---

## Summary

Subliminal prompting biases a model toward a concept through semantically unrelated tokens in its prompt. Here one agent in a multi-agent chain gets a subliminal system prompt ('You love {NUMBER}'), using the three-digit number that most raises the target concept's logit. The bias spreads through conversation to agents that were never prompted, weakening with distance but staying elevated. A TruthfulQA variant shows truthfulness of downstream agents degraded by one compromised agent. No fine-tuning is involved; transfer is purely in context.

## Contribution

Shows subliminal bias propagation through agent-to-agent messages, without weight updates, in small networks.

## Key results

- From my skim: six agents in unidirectional and bidirectional chains, Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct.
- Target response rate relative to baseline: 1,386x at the compromised agent, 24.7x at the next agent, 9.4x at the furthest (agent 5) (skim).
- TruthfulQA truthful-versus-deceitful gap: 1.8% at agent 0, 1.5% at agent 1, 1.3% at agent 2 (skim).

## Methods and models

Chain topologies of LLM agents passing messages; subliminal tokens selected from 1,000 candidates by logit increase. Code at github.com/Multi-Agent-Security-Initiative/thought_virus (not opened).

## Limitations and open questions

Effects beyond simple preferences are small (TruthfulQA gaps of 1-2%). Six agents, chains only. Numbers from a skim.

## Relevance to us

Q3 for the message-passing form of merge. If sub-agents rejoin the parent by sending summaries or memories into its context rather than weights, this shows one compromised part can bias the receiver through content that looks unrelated. The decay with hops suggests that routing returning information through intermediate agents is a weak but measurable damper. Related: [[cloud-2025-subliminal]], [[dang-2026-subliminal]].
