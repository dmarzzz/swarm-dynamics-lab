---
id: perrier-2025-position
type: paper
title: "Position: Stop Acting Like Language Model Agents Are Normal Agents"
authors: [Elija Perrier, Michael Timothy Bennett]
year: 2025
venue: arXiv
url: https://arxiv.org/abs/2502.10420
doi: null
arxiv: "2502.10420"
cite: "Perrier, E., & Bennett, M. T. (2025). Position: Stop acting like language model agents are normal agents. arXiv preprint arXiv:2502.10420."
topics: [fork-merge-security, llm-agent-swarms, meta]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: 6  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

A position paper (read from the arXiv abstract) arguing that language model agents (LMAs) should not be treated as "normal agents" with coherent goals, adaptation across contexts and intentionality. They inherit the structural problems of LLMs (hallucination, jailbreaking, misalignment, unpredictability) and, despite external memory and tools, remain "ontologically stateless, stochastic, semantically sensitive, and linguistically intermediated". These pathologies destabilise identifiability, continuity, persistence and consistency. The authors call for measuring these ontological properties before, during and after deployment.

## Contribution

Lists the properties (identifiability, continuity, persistence, consistency) whose instability undermines treating an LM agent as a single persisting agent, and proposes measuring them.

## Key results

- Conceptual; no measurements in the abstract.

## Methods and models

Position argument.

## Limitations and open questions

Abstract only; the measurement programme is proposed, not carried out.

## Relevance to us

Background for Q3 and for any merge test. If continuity and consistency are properties to be measured rather than assumed, a parent deciding whether to merge a returning child should measure the child's continuity with the parent's frozen state (does it still hold the same commitments and memories?) instead of relying on its identity, which is the Parfit-style "what matters is connectedness" test in [[olson-2023-personal]]. Companion argument on reputation: [[hu-2026-dissociative]].
