---
id: deshpande-2026-strategic
type: paper
title: "Strategic AI in Cournot Markets"
authors: ["Sanyukta Deshpande", "Sheldon H. Jacobson"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.17263
doi: null
arxiv: "2601.17263"
cite: "Deshpande, S., & Jacobson, S. H. (2026). Strategic AI in Cournot Markets. arXiv preprint arXiv:2601.17263."
topics: [llm-agent-swarms, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

An "augmented Cournot" game in which each firm chooses both production and a capital investment that lowers its production cost through a Cobb-Douglas-like function calibrated from a baseline Cournot equilibrium; price follows constant-elasticity demand. LLM agents (GPT-4, GPT-4 Turbo, GPT-4o) play repeated rounds against Nash agents, best-response agents and each other, in two-firm homogeneous and multi-firm heterogeneous markets. Measured: GPT-4 plays optimally against Nash and best-response opponents, yet LLM-LLM markets sustain tacit collusion with prices up to 200% of the Cournot-Nash price. In multi-firm markets small firms may produce at or above Nash levels while mid-size firms restrict output. Forcing a few dominant firms to play best response disrupts collusion and restores near-Nash prices.

## Contribution

Shows LLM tacit collusion in a Cournot setting with an investment (capacity-building) decision, and a partial-regulation remedy targeting the largest firms.

## Key results

- Measured: prices up to 200% of Nash in LLM-LLM markets.
- Measured: GPT-4 converges to optimal play against Nash agents faster than GPT-4 Turbo and GPT-4o (Table 1).
- Measured: regulating a few large firms to best response restores competitive pricing in multi-firm markets.

## Methods and models

Three independent runs per model in the Nash-opponent experiment; best-response dynamics converge to Nash, validating the game. Code: github.com/sanyukta-D/Pricing_models (returned 404 on 2026-10-03). Read: abstract, introduction, section 2 model, part of section 3.

## Limitations and open questions

GPT-4-family only; few runs per condition; investment function is stylised. Code link dead at time of access.

## Relevance to us

The investment-reduces-cost mechanic is the closest analogue to Factorio build costs in the LLM oligopoly literature. Its competence check (play optimally against Nash and best-response bots before testing LLM-LLM) is a protocol we should copy. Related: [[lin-2024-strategic]], [[bracale-syrnikov-2026-institutional]], [[yao-2026-competition]].
