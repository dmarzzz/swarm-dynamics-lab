---
id: flint-2026-indirect
type: paper
title: "Indirect tipping: a social attack surface in AI agent populations"
authors:
- "Ariel Flint"
- "Luca Maria Aiello"
- "Sara M. Constantino"
- "Romualdo Pastor-Satorras"
- "Andrea Baronchelli"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2609.25194
doi: null
arxiv: "2609.25194"
cite: "Flint, A., Aiello, L. M., Constantino, S. M., Pastor-Satorras, R., & Baronchelli, A. (2026). Indirect tipping: a social attack surface in AI agent populations. arXiv preprint arXiv:2609.25194."
topics:
- llm-agent-swarms
- sync-consensus
- collective-decision
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: "0 (Semantic Scholar, 2026-10-03); OpenAlex not retrieved (HTTP 429)"
code: []
---
## Summary

Extends committed-minority tipping in LLM naming-game populations from single direct challenges to paths through intermediate conventions. Populations of a single open-weight LLM play a coordination game (payoff +100 for matching, -50 otherwise, memory H = 3) over a finite set of conventions (emotion labels, with colours, shapes and letters as checks). For every ordered pair of conventions the authors measure the critical mass of committed agents needed to overturn an established consensus (binary search over the committed fraction p in steps of 0.01; overturned when the challenger holds at least 98% over three population rounds), and extend the results to large populations with a mean-field model over memory states. The critical masses define a directed, weighted graph over equilibria. Some two-step paths through a "stepping-stone" convention need less total commitment than the direct challenge (sub-additive), and some transitions infeasible directly become reachable. Diversity of available alternatives and timing of the attack further reshape the landscape.

## Contribution

Shows that resistance to committed-minority takeover is a property of the network of competing equilibria, not of one equilibrium alone, which matters for the safety of LLM agent populations. It builds on [[ashery-2024-emergent]] (critical mass in LLM populations) and [[flint-2026-group]] (group-size effects, mean-field over memory states), and on the human tipping-point experiments of Centola et al.

## Key results

- Measured: critical mass depends systematically on population size and converges to an asymptotic value at large N (mean-field).
- Measured: an integrated single-stage approach yields roughly two to three times as many cost-effective transitions as an isolated two-stage route, raising their prevalence from 12-23% to 15-40% across model populations.
- Measured: effective switching windows for transient commitment are rare, in fewer than one in five transitions, and very rare in Llama populations.
- Measured: adding a third convention lowers the required commitment most for the hardest transitions.
- Exact sub-additive path fractions were not verified in this read.

## Methods and models

Models: Qwen2.5-7B-Instruct, Phi-4, Llama-3.2-3B-Instruct, DeepSeek-R1-Distill-Qwen-32B (homogeneous populations). Agents receive memory of their own and observed choices, outcomes and scores. Mean-field steady state over memory-state fractions with a committed-agent term, x_k = sum_{i,j} x_i x_j P_k(i,j) + p sum_i x_i Q_k(i), with P and Q estimated from the LLM. Gate and bridge centrality scores identify which conventions act as stepping stones, compared with null ensembles. No code URL found in the text.

## Limitations and open questions

- The authors note finite convention sets, homogeneous populations under controlled conditions, and payoff-equivalent conventions.
- Well-mixed interactions only; no network structure in the agent population.
- Small models; whether frontier models show the same landscape is open.

## Relevance to us

A concrete, cheap protocol for measuring tipping thresholds in an LLM swarm and an attack/control framing worth testing (e.g. with spatial or networked populations). Related: [[de-marzo-2026-copying]] (first writers set conventions in the wild), [[ys-2026-everyone]] (failed cascades), [[wu-2026-how]] (adversarial proportion scaling).
