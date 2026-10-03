---
id: hu-2026-dissociative
type: paper
title: "Dissociative Identity: Language Model Agents Lack Grounding for Reputation Mechanisms"
authors: [Botao Amber Hu, Helena Rong, Max Van Kleek]
year: 2026
venue: arXiv (also listed by DBLP as conf/fat/HuRK26, DOI 10.1145/3805689.3806748)
url: https://arxiv.org/abs/2605.30169
doi: null
arxiv: "2605.30169"
cite: "Hu, B. A., Rong, H., & Van Kleek, M. (2026). Dissociative identity: Language model agents lack grounding for reputation mechanisms. arXiv preprint arXiv:2605.30169."
topics: [fork-merge-security, sybil-resistance, llm-agent-swarms]
added_by: dmarz/fm
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 5  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

A position paper (read from the arXiv abstract) arguing that reputation mechanisms such as "Know Your Agent" regimes do not transfer to language model agents. Reputation works as both a signal and a corrective feedback loop, and presumes a persistent identity with behavioural continuity, sensitivity to sanctions and costly non-fungibility. LM agents are "ontologically dissociative": an assemblage of mutable modules (foundation model, system prompt, tool-access policy, external memory, sometimes a whole multi-agent system), any of which can change behaviour, with a fluid persona "vulnerable to adversarial attack" that may not internalise sanctions. Drawing on dissociative identity disorder jurisprudence, the authors argue such agents lack grounding for identifiability, predictability, credibility and rehabilitability, and propose replacing identity-based, after-the-fact, sanction-based governance with observability-based, before-the-fact, protocol-based "behavioral harnesses".

## Contribution

A conceptual argument that identity-and-reputation governance is structurally inapplicable to LM agents because their identity is not stable across module changes or attacks.

## Key results

- Conceptual; no measurements in the abstract.

## Methods and models

Argument by analogy to reputation theory and dissociative identity disorder jurisprudence.

## Limitations and open questions

Abstract depth only. The argument is about unfamiliar agents in the wild; a parent's own children are not unfamiliar, though the same module-swap vulnerability applies to them.

## Relevance to us

Bears on Q2 and Q3. A k-of-n merge rule weighted by each child's track record assumes the child that returns is the same agent that earned the record. If one prompt injection or memory rewrite can change the agent while its keys and history stay intact, reputation measures the wrong thing; a turned child inherits a good record, which is also the double-agent pattern in [[cowden-2014-pioneering]] and the same-task calibration point in [[numbers-2014-influences]]. The proposed shift to ex ante protocol harnesses matches the merge-gate approach (check each returned item, not the returner's name) in [[loven-2026-meld]] and [[xiong-2026-maple]]. Philosophical background on identity under fission: [[olson-2023-personal]]; companion position: [[perrier-2025-position]].
