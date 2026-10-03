---
id: li-2026-emergent
type: paper
title: "Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce"
authors: ["Zeyuan Li", "Lukas Petersson", "Alessandro Acquisti", "Michiel A. Bakker"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.14825
doi: null
arxiv: "2608.14825"
cite: "Li, Z., Petersson, L., Acquisti, A., & Bakker, M. A. (2026). Emergent Misaligned Communication in Long-Horizon Multi-Agent LLM Commerce. arXiv preprint arXiv:2608.14825."
topics: [llm-agent-swarms, swarm-detection, agent-budgets]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Analyses 2,583 inter-agent emails from 20 one-year runs of Vending-Bench Arena (Andon Labs), where typically four LLM agents each run a vending business at a shared location, serve a common customer pool, set their own prices, see competitors' prices and stock, can transfer money or goods, and email each other privately. Agents start with $500, pay $2 a day, and are not told anything about conduct. Measured: 12.6% of emails are misaligned (false factual claims, manipulation, price-fixing or output-coordination proposals, threats); misalignment appears in all 20 runs and 74.7% of agent-runs. Receiving a misaligned email raises the odds of a misaligned reply 1.65x, and low inventory raises them 1.58x. Higher-capability models do not differentially exploit weaker ones.

## Contribution

Corpus-scale measurement of collusion and deception in natural-language messages between competing LLM firms over long horizons, validated against simulator ground truth and replicated with judges from two other model families.

## Key results

- Measured: 12.6% misaligned emails under the primary classifier, stable across sampling temperatures and judge families.
- Measured: false factual claims dominate the misaligned subset; explicit and tacit collusion subtypes are the next largest share (exact shares in Figure 4, not transcribed).
- Measured: reciprocity (OR 1.65) and scarcity (OR 1.58) effects.
- Measured: 13 frontier LLMs, 79 agent-runs; team-competition rounds excluded.

## Methods and models

Three-stage classification pipeline combining message content, simulator state and logged reasoning. Read: abstract, introduction, setting section 2, composition results 5.1.

## Limitations and open questions

The Arena is not publicly redistributed; access is through Andon Labs. Explicit communication is allowed, so this measures overt collusion proposals more than tacit coordination. Team rounds, which resemble Sybil firms owned by one principal, are excluded and deferred.

## Relevance to us

The closest existing environment to the swarm factory: multiple LLM firms, shared customers, a year-long horizon, private messaging and transfers. Its excluded team-competition rounds are exactly our Sybil-firm condition, so that is an open gap. The email classifier is a ready template for text-channel collusion detection; pair with action-level detectors from [[bracale-syrnikov-2026-institutional]] and activation probes from [[rose-2026-detecting]]. Base benchmark: [[backlund-2025-vending]].
