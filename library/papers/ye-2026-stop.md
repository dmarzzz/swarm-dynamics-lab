---
id: ye-2026-stop
type: paper
title: "Stop Drawing Scientific Claims from LLM Social Simulations Without Robustness Audits"
authors: ["Jinyi Ye", "Lei Cao", "Ding Chen", "Emilio Ferrara"]
year: 2026
venue: "arXiv"
url: https://arxiv.org/abs/2605.18890
doi: null
arxiv: "2605.18890"
cite: "Ye, J., Cao, L., Chen, D., & Ferrara, E. (2026). Stop Drawing Scientific Claims from LLM Social Simulations Without Robustness Audits. arXiv preprint arXiv:2605.18890."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A position paper with case studies showing that small changes to LLM social simulation setup, such as persona formatting and game instructions, change outcomes drastically, with cooperation rates shifting by up to 76 percentage points across models. The sensitivity is uneven across architectural choices and model families. The authors propose TRAILS, a taxonomy for robustness audits, and argue audits should be mandatory before simulations inform claims or policy.

## Contribution

Quantifies prompt and configuration fragility in LLM social simulations and offers an audit taxonomy.

## Key results

- Cooperation rates shift by up to 76 percentage points from minor parameter changes (abstract, via the arXiv page).
- Sensitivity unevenly distributed across design choices and model families (abstract).

## Methods and models

Case studies on game-theoretic social simulations with perturbed persona format and instructions. Not read beyond the abstract.

## Limitations and open questions

Abstract only; which games and models were used not checked.

## Relevance to us

Any result from our sims (e.g. free-rider success in [[gh-textarena-textarena]] or Byzantine tolerance in [[gh-floriangroetschla-agentsnet]]) needs a prompt-perturbation sweep before we claim it. Complements [[larooij-2025-do]] and [[zhou-2025-pimmur]].
