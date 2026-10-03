---
id: bracale-syrnikov-2026-institutional
type: paper
title: "Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs"
authors: ["Marcantonio Bracale Syrnikov", "Federico Pierucci", "Marcello Galisai", "Matteo Prandi", "Piercosma Bisconti", "Francesco Giarrusso", "Olga Sorokoletova", "Vincenzo Suriani", "Daniele Nardi"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.11369
doi: null
arxiv: "2601.11369"
cite: "Bracale Syrnikov, M., Pierucci, F., Galisai, M., Prandi, M., Bisconti, P., Giarrusso, F., Sorokoletova, O., Suriani, V., & Nardi, D. (2026). Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs. arXiv preprint arXiv:2601.11369."
topics: [llm-agent-swarms, agent-budgets, swarm-detection]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

A replication-aligned extension of [[lin-2024-strategic]]: two LLM firms in a repeated two-commodity Cournot game with capacity constraints, linear inverse demand and PLANS/INSIGHTS memory. Six model configurations (homogeneous GPT-5 Mini, Grok-4 Fast, Gemini 2.5 Flash duopolies and three cross-provider pairs), 90 runs per condition, three regimes: Ungoverned, Constitutional (a fixed anti-collusion text in the prompt) and Institutional (a public governance graph with an Oracle that detects coordination from quantities and a Controller that warns, fines and suspends firms, with credit-based restoration). Measured: mean collusion tier falls from 3.10 (Ungoverned) and 3.02 (Constitutional) to 1.82 (Institutional), Cohen's d 1.28; severe Tier-4 collusion falls from 50% to 5.6% of runs. The prompt-only constitution gives no reliable improvement.

## Contribution

A direct replication target of LLM market division plus a programmatic, LLM-free collusion detector over market-structure signals, with auditable enforcement.

## Key results

- Measured: Ungoverned Tier 1/2/3/4 shares 11.1/17.8/21.1/50.0%; Institutional 47.8/27.8/18.9/5.6%.
- Measured: HHI excess falls 0.305 and max firm-level specialisation (CV) excess falls 1.100 versus Ungoverned.
- Measured: direction holds in all six model configurations.
- Measured: constitutional prompt alone does not reduce collusion.

## Methods and models

Collusion tiers are defined from run-level HHI excess and within-firm coefficient-of-variation excess over the Cournot-Nash benchmark (computed by iterated best response with SLSQP). Oracle signals: one-step synchrony of quantity moves, windowed cross-firm dispersion collapse, high HHI and specialisation. Read: abstract, introduction, sections 5 to 7 and 9.

## Limitations and open questions

The authors list two-firm narrowness (no contracts, entry or exit) and Goodharting of fixed thresholds. Fines condition on market structure, so efficient specialisation could be penalised as collusion. No code link found in the text.

## Relevance to us

Must-cite. Its Oracle signals (HHI, specialisation CV, synchrony, dispersion collapse) are a ready baseline detector for the swarm factory, and its tier scale gives a comparable outcome metric. Testing whether Sybil firms owned by one principal look the same as tacitly colluding independents under these signals is an open extension. Related: [[deshpande-2026-strategic]], [[eschenbaum-2026-auditing]], [[nakamura-2026-colosseum]].
