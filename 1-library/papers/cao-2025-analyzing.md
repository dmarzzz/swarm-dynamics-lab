---
id: cao-2025-analyzing
type: paper
title: "Analyzing Memory Effects in Large Language Models through the lens of Cognitive Psychology"
authors: [Zhaoyang Cao, Lael Schooler, Reza Zafarani]
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2509.17138
doi: null
arxiv: "2509.17138"
cite: "Cao, Z., Schooler, L., & Zafarani, R. (2025). Analyzing memory effects in large language models through the lens of cognitive psychology. arXiv preprint arXiv:2509.17138."
topics: [fork-merge-security]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Read from the arXiv abstract. The authors test seven human memory phenomena, framed by Schacter's memory "sins", on state-of-the-art LLMs using paradigms from psychology. Like humans, LLMs remember less under information overload (list-length effect), remember better with repetition (list-strength effect), confuse overlapping facts (fan effect), falsely "remember" words related to studied words that were never shown (false memories), and generalise across domains. Unlike humans, they are less affected by presentation order (positional bias) and more robust to nonsense material.

## Contribution

A side-by-side test of whether classic human memory distortions appear in LLMs, giving a basis for transferring human memory-security findings to models.

## Key results

- False memory for related, unpresented items appears in LLMs as in humans (abstract claim; magnitudes not read).
- Overload reduces recall and repetition increases it, in both (abstract claim).
- LLMs show weaker positional bias and less nonsense-material impairment than humans.

## Methods and models

Psychology paradigms adapted to prompts; models and sample sizes not checked at abstract depth.

## Limitations and open questions

Abstract only. In-context list memory is not the same as an agent's persistent memory store. The paper does not test misinformation (post-event suggestion), source monitoring or social contagion, which are the paradigms closest to the fork-merge attack.

## Relevance to us

A small bridge for Q3. It gives some measured support for treating the human results in [[loftus-2005-planting]] and [[roediger-2001-social]] as hypotheses worth testing on LLM agents: the same reconstruction-based false memory and repetition effects appear. The repetition (list-strength) result predicts that a corrupted child that restates a plant several times during merge will make it stick, as [[meade-2002-explorations]] found in humans. The gap it leaves, no test of post-event misinformation or source attribution in LLM agents, is a concrete experiment this lane could run.
