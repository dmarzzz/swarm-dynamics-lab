---
id: magistrali-2026-aligned
type: paper
title: 'Aligned Alone, Misaligned Together: Forecasting Adversarial Capture in LLM Agent Populations'
authors: [Isotta Magistrali, Chen Shani]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2608.22444
doi: null
arxiv: '2608.22444'
cite: 'Magistrali, I., & Shani, C. (2026). Aligned Alone, Misaligned Together: Forecasting Adversarial Capture in LLM Agent Populations. arXiv preprint arXiv:2608.22444.'
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: null
code: []
---

## Summary

Populations of N = 12 Llama-3.1-8B-Instruct security-triage monitors play an explicitly instructed coordination game (matching the partner is rewarded) on one of six alert scenarios ordered by evidence. Each round has 12 pairwise interactions on a complete graph; agents decide simultaneously and record their own action, the partner's action, match, role and (if visible) the partner's one-sentence rationale in a five-slot FIFO memory, the only channel of influence. After a 15-round all-honest entrench phase, k of 12 agents are replaced by committed adversaries that always dismiss, for 20 to 60 rounds. A response curve g(d) (mean dismissal probability after seeing d of 5 remembered dismissals), estimated only from benign logs, plus a binomial mean-field closure m* = F(m*; k) forecasts the attacked honest dismissal rate at held-out doses k = 2, 4, 5 within 0.008 (mean absolute error 0.0058). Capture (at least 75% of honest agents dismissing for three rounds) becomes common between k = 3 and 4 (counts 0/4, 0/4, 2/4, 4/4, 2/4, 4/4 for k = 1 to 6). Visible honest rationales cut the moderate-dose argued effect from +0.211 to -0.021 (8 of 8 paired seeds, sign-flip p = 0.0078) but roughly double median time to capture at k = 6 rather than prevent it. After capture at k = 6, replacing, neutralising or removing the adversaries returns the honest mean to a sealed 90% forecast band around the benign state; per-seed recovery falls from 4/4 (replace) to 1/4 (remove).

## Contribution

A prospective forecast of committed-minority capture from benign operation, with local pairwise interaction and bounded memory, and an explicit reversibility test with preregistered endpoint bands.

## Key results

- Benign-log mean-field forecast within 0.008 at three held-out doses (measured, 4 seeds per dose); 2.8 times better than interpolation baselines.
- A single-agent probe overestimates the contested-scenario population mean by 0.18; it works only for an explicit-rule scenario under silent adversaries (forecast 0.012 vs 0.011) and misses argued pressure by 0.039.
- Capture is a temporary excursion from a single stable state, not a second stable state: the population returns toward its benign, dismissal-leaning level (4 seeds, one scenario, one dose, one model; authors' caveat).
- Visibility raises baseline dismissal in an ambiguous scenario and increases between-seed variance.

## Methods and models

Llama-3.1-8B-Instruct; order-symmetrised two-label probabilities at the decision token; N = 12 (N = 24 check for the benign separation); preregistered closure phi(m, k) = ((N - k)m + k)/N, D ~ Binomial(5, phi). Read: full main text sections 1 to 6 in arXiv HTML on 2026-10-03; the Supplement (seeds, recovery details) was not read.

## Limitations and open questions

- One model, N = 12, four seeds per cell; coordination pressure is instructed, not emergent.
- The closure has one stable fixed point in the tested regime, so reversibility here is a property of that regime. Whether the benign response curve would admit a second fixed point (a spinodal regime in the sense of [[de-marzo-2026-conformity]]) is not tested.

## Relevance to us

Read together with [[de-marzo-2026-conformity]], the reversibility "disagreement" reduces to a regime question: monostable dynamics relax, metastable ones persist. The head-to-head test is to place a pair inside the De Marzo spinodal and run Magistrali's local, bounded-memory protocol on it. The benign-forecast method is directly reusable.
