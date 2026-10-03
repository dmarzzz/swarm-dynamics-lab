---
id: song-2026-hll
type: paper
title: "HLL: Can Agents Cross Humanity's Last Line of Verification?"
authors: ["Xinhao Song", "Su Su", "Sirui Song", "Hongliang Wu", "Wen Shen", "Zhihua Wei", "Gongshen Liu", "Linfeng Zhang", "Dongrui Liu"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.02449
doi: "10.48550/arXiv.2606.02449"
arxiv: "2606.02449"
cite: "Song, X., Su, S., Song, S., Wu, H., Shen, W., Wei, Z., Liu, G., Zhang, L., & Liu, D. (2026). HLL: Can Agents Cross Humanity's Last Line of Verification?. arXiv preprint arXiv:2606.02449."
topics: ["swarm-detection", "sybil-resistance", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "1 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Song, Su, Song, Wu, Shen, Wei, Liu, Zhang and Liu build HLL (Humanity's Last Line of Verification), a controlled benchmark that tests whether multimodal agents can pass interactive CAPTCHAs through grounded, human-like interaction in a closed-loop GUI, with stressors such as cluttered pages, harder variants and validation of the action trace. Eight frontier agents remain brittle: performance varies sharply by verification type, falls under realistic interfaces, and drops further when the solution must be backed by a valid action trace.

## Contribution

Adds trace-conditioned validation: checking how the answer was produced, not just whether it is right.

## Key results

- Measured (abstract): eight frontier multimodal agents brittle across verification types; numbers not in abstract.
- Measured (abstract): requiring valid action traces lowers success further.

## Methods and models

Closed-loop GUI environment, diverse CAPTCHA interactions, realism stressors, trace validation. Code: github.com/XinhaoS0101/HLL. Abstract only.

## Limitations and open questions

Abstract only.

## Relevance to us

Trace validation is the CAPTCHA-world version of behavioural fingerprinting ([[wang-2026-fp-agent]]): the process leaks the agent even when the answer is right.
