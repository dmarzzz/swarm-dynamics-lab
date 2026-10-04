---
id: brockers-2025-disentangling
type: paper
title: Disentangling Interaction and Bias Effects in Opinion Dynamics of Large Language Models
authors:
- Vincent C. Brockers
- David A. Ehrlich
- Viola Priesemann
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2509.06858
doi: null
arxiv: '2509.06858'
cite: Brockers, V. C., Ehrlich, D. A., & Priesemann, V. (2025). Disentangling interaction and bias effects in opinion dynamics of large language models. arXiv preprint arXiv:2509.06858.
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03); OpenAlex has no matching record for this arXiv DOI"
code: []
---

## Summary

A Bayesian framework that separates genuine interaction from three systematic biases in LLM opinion dynamics: topic bias toward the model's default stance, agreement bias toward the prompted statement, and anchoring bias toward the initiating agent. Applied to multi-step dialogues on 12 questions (climate change, social justice, music preferences), opinion trajectories quickly converge to a shared attractor, with both interaction and bias effects decaying over time and differing between LLMs. Fine-tuning on strongly opinionated statements (including misinformation) shifts the attractor accordingly.

## Contribution

A statistical decomposition of "interaction vs bias" from the Priesemann group (known for dynamical-systems and criticality work in neuroscience), parallel to the physics fits in [[de-nobili-2026-collective]] and [[el-2026-physics]].

## Key results

- Convergence to a model-specific attractor; biases differ across LLMs (abstract).
- Fine-tuning moves the attractor (abstract).

## Methods and models

Bayesian model of opinion updates in dyadic multi-turn dialogues; fine-tuning experiments. Code not checked.

## Limitations and open questions

Dyads rather than populations; abstract-level read.

## Relevance to us

Needed as a control in any consensus experiment: without it, attractors set by model priors can be mistaken for collective dynamics. See also [[chuang-2023-simulating]].
