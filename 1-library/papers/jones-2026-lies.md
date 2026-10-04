---
id: jones-2026-lies
type: paper
title: "Lies, damned lies, and language statistics: a comprehensive review of risks from manipulation, persuasion, and deception with large language models"
authors: [Cameron R. Jones, Benjamin K. Bergen]
year: 2026
venue: "Artificial Intelligence Review"
url: https://link.springer.com/article/10.1007/s10462-026-11517-6
doi: 10.1007/s10462-026-11517-6
arxiv: null  # preprint is arXiv 2412.17128 under a different title, see Summary
cite: "Jones, C. R., & Bergen, B. K. (2026). Lies, damned lies, and language statistics: a comprehensive review of risks from manipulation, persuasion, and deception with large language models. Artificial Intelligence Review, 59(4), 116. https://doi.org/10.1007/s10462-026-11517-6"
topics: [swarm-detection, llm-agent-swarms]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "3 (Crossref, 2026-10-03)"
code: []
---

## Summary

Long review (journal version of arXiv 2412.17128, first titled "Lies, Damned Lies, and Distributional Language Statistics: Persuasion and Deception with Large Language Models") of LLM persuasion and deception. Structure: theoretical mechanisms (pre-training, emergent capability, deployment, user interaction); misuse by criminals, propagandists and companies, including bot networks that fake social proof and astroturfing; misalignment; empirical work on LLM persuasiveness (static text, LLM-LLM interaction, human-LLM dialogue) and on hallucination and strategic deception; mitigations (truthfulness training, autonomy preservation, interpretability probes, evaluation and monitoring, debate, education, regulation); five open questions. Their bottom line: models are already about as persuasive as untrained humans, sometimes more persuasive than experts on short static messages, but measured effects are small, around 4-8 percentage points in self-reported belief. Read: abstract, sections 2.2 (misuse and systemic harms), 3.3.2 (LLM-LLM interaction), 5.1 (how persuasive could AI get), and skimmed the rest.

## Contribution

A consolidated map of the persuasion and deception literature up to 2025, with a quantitative projection: combining a scaling result of about 1.5 pp more persuasion per order of magnitude of compute with roughly one order of magnitude every two years, they project about 9 pp more (to about 20%) in ten years, flagged as highly uncertain.

## Key results

- Persuasion effect sizes from current LLMs: small (about 4-8 pp), comparable to human-written messages.
- Prompting matters a lot: GPT-4 Turing-test pass rates varied from 6% to 50% across 40+ prompts (their earlier work), suggesting measured persuasion is a lower bound.
- Debate between LLMs raised judge accuracy (88% vs 60% for humans in Khan et al. 2024), whereas a single deceptive consultant got more effective as it got more capable.
- Linear probes for deception show promise but generalise poorly; training against a lie detector can teach more subtle deception (reviewed results).
- Systemic risks are speculative: "epistemic pollution", erosion of source attribution, or alternatively an advantage for true arguments.

## Methods and models

Narrative review; no new experiments.

## Limitations and open questions

Coverage of coordinated multi-account operations is thin: bot networks appear as a misuse vector (citing [[yang-2023-anatomy]]) but detection of coordinated LLM agents is not reviewed. Most cited persuasion studies use self-reported attitude change right after exposure.

## Relevance to us

Background for the threat model behind swarm detection: what a coordinated LLM agent swarm would be trying to do (persuade, fake social proof, deceive) and how big single-message effects currently are. The debate vs consultancy result matters for multi-agent oversight designs. Pair with [[yang-2023-anatomy]] for a real LLM botnet and [[pacheco-2021-uncovering]] for coordination detection methods.
