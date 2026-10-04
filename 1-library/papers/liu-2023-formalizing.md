---
id: liu-2023-formalizing
type: paper
title: 'Formalizing and Benchmarking Prompt Injection Attacks and Defenses'
authors: [Yupei Liu, Yuqi Jia, Runpeng Geng, Jinyuan Jia, Neil Zhenqiang Gong]
year: 2023
venue: USENIX Security Symposium 2024; arXiv preprint
url: https://arxiv.org/abs/2310.12815
doi: null
arxiv: '2310.12815'
cite: 'Liu, Y., Jia, Y., Geng, R., Jia, J., & Gong, N. Z. (2024). Formalizing and Benchmarking Prompt Injection Attacks and Defenses. In 33rd USENIX Security Symposium (USENIX Security 24). arXiv:2310.12815.'
topics: [fork-merge-security]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

The paper gives a formal framework in which a prompt injection makes an LLM-integrated application perform an injected task instead of its target task, by combining injected instruction and data with the legitimate data. Earlier ad hoc attacks are special cases of this framework, and the authors build a combined attack from them. They benchmark 5 attacks and 10 defences across 10 LLMs and 7 tasks, and release the Open-Prompt-Injection platform. The abstract states that existing work was limited to case studies and that the benchmark is meant as a common yardstick.

## Contribution

It provides a shared formal vocabulary for prompt injection (target task, injected task, separator and context-ignoring components) and the first systematic attack-by-defence benchmark.

## Key results

- 5 attacks and 10 defences evaluated across 10 LLMs and 7 tasks (abstract). The numerical results were not read.
- A combined attack built from the framework (abstract).

## Methods and models

Open-Prompt-Injection platform, github.com/liu00222/Open-Prompt-Injection (not opened). The PoisonedRAG codebase [[gh-sleeeepeer-poisonedrag]] reuses its model layer.

## Limitations and open questions

Single-turn and stateless. It does not model memory persistence or multi-agent propagation.

## Relevance to us

Background for Q3. It formalises the single-hop step (untrusted data hijacks the sub-agent's current task) on which persistence ([[dong-2025-memory]], [[gadgil-2026-bad]]) and propagation ([[cohen-2024-here]]) build. Its target-task and injected-task formalism is a candidate way to state "the sub-agent now pursues the attacker's task" in a fork-merge threat model. Seminal predecessor: [[greshake-2023-not]].

## Notes from dmarz/fm-code-bench

Code catalogued as [[gh-liu00222-open-prompt-injection]] (MIT, 503 stars, still maintained, last push 2026-09-27).
